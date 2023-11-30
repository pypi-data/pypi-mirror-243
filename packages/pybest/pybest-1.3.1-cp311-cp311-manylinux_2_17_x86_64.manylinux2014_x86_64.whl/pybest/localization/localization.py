# -*- coding: utf-8 -*-
# PyBEST: Pythonic Black-box Electronic Structure Tool
# Copyright (C) 2016-- The PyBEST Development Team
#
# This file is part of PyBEST.
#
# PyBEST is free software; you can redistribute it and/or
# modify it under the terms of the GNU General Public License
# as published by the Free Software Foundation; either version 3
# of the License, or (at your option) any later version.
#
# PyBEST is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, see <http://www.gnu.org/licenses/>
# --

# Detailed changelog:
# This module has been originally written and updated by Katharina Boguslawski (see CHANGELOG)
# Its current version contains updates from the PyBEST developer team.
#
# This implementation can also be found in `Horton 2.0.0`.
# However, this file has been updated and debugged. Compatibility with Horton is NOT
# guaranteed.
#
# Detailed changes:
# See CHANGELOG
# 12/2020: frozen core support, new variable convention, abc, properties

"""Orbital localization procedures

   Currently supported localization flavours:
    * Pipek-Mezey

"""

from abc import ABC, abstractmethod

import numpy as np

from pybest.cache import Cache
from pybest.exceptions import UnknownOption
from pybest.linalg.base import Orbital
from pybest.log import log, timer
from pybest.orbital_utils import compute_unitary_matrix
from pybest.steplength.stepsearch import RStepSearch
from pybest.utils import check_options, unmask_orb

__all__ = [
    "PipekMezey",
]


class Localization(ABC):
    """Base class for all localization methods"""

    def __init__(self, lf, occ_model, projector):
        """Localize canonical HF orbitals.

        **Arguments:**

        lf
             A LinalgFactory instance.

        occ_model
             Occupation model.

        Projector
             Projectors for atomic basis function. A list of TwoIndex
             instances.

        """
        self._lf = lf
        self._proj = projector
        self._occ_model = occ_model
        self._nocc = occ_model.nocc[0]
        self._nbasis = lf.default_nbasis
        self._nvirt = lf.default_nbasis - occ_model.nocc[0]
        #
        # number of active orbitals
        #
        self._nacto = occ_model.nocc[0] - occ_model.ncore[0]
        self._ncore = occ_model.ncore[0]
        if self._nacto <= 0 or self._nacto > occ_model.nocc[0]:
            raise ValueError(
                f"Impossible number of frozen core orbitals! You have chosen {occ_model.ncore[0]} "
                f"frozen core orbitals out of {occ_model.nocc[0]} occupied orbitals."
            )
        # total number of active orbitals (only frozen core supported)
        self._nact = lf.default_nbasis - self._ncore
        # total number of active virtuals
        self._nactv = self._nact - self._nacto
        if (
            self._nvirt <= 0
            or self._nvirt > lf.default_nbasis - occ_model.nocc[0]
        ):
            raise ValueError(
                f"Impossible number of virtual orbitals: {self._nvirt}!"
            )
        if (
            self._nactv <= 0
            or self._nactv > lf.default_nbasis - occ_model.nocc[0]
        ):
            raise ValueError(
                f"Impossible number of active virtual orbitals: {self._nactv}!"
            )
        self._cache = Cache()
        self._block_type = None
        self._pop_matrix = None

    @timer.with_section("Localization")
    def __call__(self, data, select, **kwargs):
        """Localizes the orbitals using a unitary transformation to rotate the
        AO/MO coefficient matrix. The orbitals are optimized by minimizing
        an objective function.

        This works only for restricted orbitals.

        **Arguments:**

        data
             An IOData container containing an Orbital instance. This
             instance will be overwritten.

        select
             The orbital block to be localised (str). Any of ``occ`` (occupied
             orbitals), ``virt`` (virtual orbitals)

        **Keywords:**

        :maxiter: (int) maximum number of iterations for localization
                  (default 2000)
        :threshold: (float) localization threshold for objective function
                    (default 1e-6)
        :levelshift: level shift of Hessian (float) (default 1e-8)
        :stepsearch: step search options (dictionary) containing:

                     * method: step search method used (str). One of
                       ``trust-region`` (default), ``None``, ``backtracking``
                     * alpha: scaling factor for Newton step (float), used in
                       ``backtracking`` and ``None`` method (default 0.75)
                     * c1: parameter used in ``backtracking`` (float)
                       (default 1e-4)
                     * minalpha: minimum step length used in ``backracking``
                       (float) (default 1e-6)
                     * maxiterouter: maximum number of search steps (int)
                       (default 10)
                     * maxiterinner: maximum number of optimization
                       steps in each search step (int) (used only in ``pcg``,
                       default 500)
                     * maxeta: upper bound for estimated vs actual change in
                       ``trust-region`` (float) (default 0.75)
                     * mineta: lower bound for estimated vs actual change in
                       ``trust-region`` (float) (default 0.25)
                     * upscale: scaling factor to increase trustradius in
                       ``trust-region`` (float) (default 2.0)
                     * downscale: scaling factor to decrease trustradius in
                       ``trust-region`` (float) and scaling factor in
                       ``backtracking`` (default 0.25)
                     * trustradius: initial trustradius (float) (default
                       0.75)
                     * maxtrustradius: maximum trustradius (float) (default
                       0.75)
                     * threshold: trust-region optimization threshold, only
                       used in ``pcg`` (float) (default 1e-8)
                     * optimizer: optimizes step to boundary of trustradius
                       (str). One of ``pcg``, ``dogleg``, ``ddl`` (default
                       ddl)
        """
        if log.do_medium:
            log(f"Performing localization of {select} block")
        log.cite("the Pipek-Mezey localization scheme", "pipek1989")
        #
        # Assign default keyword arguements
        #
        names = []

        def _helper(x, y):
            names.append(x)
            return kwargs.get(x, y)

        maxiter = _helper("maxiter", 2000)
        thresh = _helper("threshold", 1e-6)
        lshift = _helper("levelshift", 1e-8)
        stepsearch = _helper("stepsearch", dict({}))
        stepsearch.setdefault("method", "trust-region")
        stepsearch.setdefault("minalpha", 1e-6)
        stepsearch.setdefault("alpha", 1.0)
        stepsearch.setdefault("c1", 0.0001)
        stepsearch.setdefault("maxiterouter", 10)
        stepsearch.setdefault("maxiterinner", 500)
        stepsearch.setdefault("maxeta", 0.75)
        stepsearch.setdefault("mineta", 0.25)
        stepsearch.setdefault("upscale", 2.0)
        stepsearch.setdefault("downscale", 0.25)
        stepsearch.setdefault("trustradius", 0.75)
        stepsearch.setdefault("maxtrustradius", 0.75)
        stepsearch.setdefault("threshold", 1e-8)
        stepsearch.setdefault("optimizer", "ddl")

        for name, value in kwargs.items():
            if name not in names:
                raise UnknownOption(f"Unknown keyword argument {name}")
            if value < 0:
                raise UnknownOption(f"Illegal value for {name}: {value}")

        #
        # Get orbitals from IOData container.
        # Note: orbitals will be overwritten in original container!
        #
        (orb,) = unmask_orb(data, **kwargs)
        #
        # Update information about localization block
        #
        self.block_type = select

        if log.do_medium:
            log(f"{'Iter':3}  {'D(ObjectiveFunction)':12}  {'Steplength':10}")
        #
        # Initialize step search
        #
        stepsearch_ = RStepSearch(self.lf, **stepsearch)
        #
        # Calculate initial objective function
        #
        self.solve_model(orb)
        objfct_ref = self.compute_objective_function()

        maxThresh = True
        maxIter = True
        it = 0
        while maxThresh and maxIter:
            #
            # Update population matrix for new orbitals
            #
            self.compute_population_matrix(orb)
            #
            # Calculate orbital gradient and diagonal approximation to the Hessian
            #
            kappa, gradient, hessian = self.orbital_rotation_step(lshift)
            #
            # Apply steps search to orbital rotation step 'kappa' and perform
            # orbital rotation
            #
            stepsearch_(
                self,
                None,
                None,
                orb,
                **{"kappa": kappa, "gradient": gradient, "hessian": hessian},
            )
            #
            # update objective function
            #
            objfct = self.compute_objective_function()
            it += 1
            #
            # Print localization progress
            #
            if log.do_medium:
                log(f"{it:4} {abs(objfct - objfct_ref):14.8f}")
            #
            # Check convergence
            #
            maxThresh = abs(objfct - objfct_ref) > thresh
            maxIter = it < maxiter
            #
            # Prepare for new iteration
            #
            objfct_ref = objfct
        if maxThresh and not maxIter:
            if log.do_medium:
                log(" ")
                log.warn(
                    f"Orbital localization not converged in {it - 1} iteration"
                )
                log(" ")
        else:
            if log.do_medium:
                log(" ")
                log(f"Orbital localization converged in {it - 1} iteration")
                log(" ")

    @property
    def occ_model(self):
        """The occupation model"""
        return self._occ_model

    @property
    def nbasis(self):
        """The number of basis functions"""
        return self._nbasis

    @property
    def nocc(self):
        """The number of occupied orbitals"""
        return self._nocc

    @property
    def nvirt(self):
        """The number of virtual orbitals"""
        return self._nvirt

    @property
    def nact(self):
        """The number of active orbitals"""
        return self._nact

    @property
    def nacto(self):
        """The number of active occupied orbitals"""
        return self._nacto

    @property
    def nactv(self):
        """The number of active virtual orbitals"""
        return self._nactv

    @property
    def ncore(self):
        """The number of frozen core orbitals"""
        return self._ncore

    @property
    def lf(self):
        """The LinalgFactory"""
        return self._lf

    @property
    def proj(self):
        """The Projectors. A list of TwoIndex instances"""
        return self._proj

    @property
    def block_type(self):
        """The orbital block to be localized"""
        return self._block_type

    @block_type.setter
    def block_type(self, new):
        """Update localization block"""
        check_options("block", new, "occ", "virt")
        self._block_type = new

    @property
    def pop_matrix(self):
        """The population matrix. A list of TwoIndex instances"""
        return self._pop_matrix

    @pop_matrix.setter
    def pop_matrix(self, new):
        """Update pop_matrix"""
        self._pop_matrix = new

    @property
    @abstractmethod
    def block(self):
        """The orbital block used during localization (OneIndex object)"""
        raise NotImplementedError

    @abstractmethod
    def grad(self):
        """Gradient of objective function"""
        raise NotImplementedError

    @abstractmethod
    def hessian(self):
        """Diagonal Hessian of objective function"""
        raise NotImplementedError

    @abstractmethod
    def compute_objective_function(self):
        """Objective function of a chosen localization flavor to be maximized"""
        raise NotImplementedError

    def __clear__(self):
        self.clear()

    def clear(self):
        """Clear all wavefunction information"""
        self._cache.clear()

    #
    # Don't change function name or implementation will break. The function
    # ``solve_model`` is used in the StepSearch module.
    #
    def solve_model(self, *args, **kwargs):
        """Update population matrix used to calculate objective function.
        args and kwargs are used in StepSearch module. Here, only args
        are used:

        **Arguments:**

        args
             an orbital instance.
        """
        for arg in args:
            if isinstance(arg, Orbital):
                self.compute_population_matrix(arg)

    def orbital_rotation_step(self, lshift):
        """Calculate gradient, hessian, and orbital rotation step

        **Arguments:**

        lshift
             Shift elements of Hessian
        """
        grad = self.grad()
        hess = self.hessian(lshift)

        kappa = grad.divide(hess, -1.0)

        return kappa, grad, hess

    def compute_rotation_matrix(self, coeff):
        """Determine orbital rotation matrix

        **Arguments:**

        coeff
             The non-reduntant orbital rotations, we need only values for
             p<q
        """
        indl = np.tril_indices(self.nbasis, -1)
        kappa = self.lf.create_two_index(self.nbasis, self.nbasis)
        #
        # frozen core orbitals are accounted for in block property
        #
        kappa.assign(coeff, indl)
        #
        # k_pq = -k_qp
        #
        kappa.iadd_t(kappa, -1.0)

        out = compute_unitary_matrix(kappa)
        return out

    def compute_population_matrix(self, orb):
        """Determine population matrix

        **Arguments:**

        orb
             The current AO/MO coefficients. An Orbital instance
        """
        #
        # Calculate population matrices for orbital block
        #
        pop_mat = list()
        for op in self.proj:
            pop = self.lf.create_two_index(self.nbasis, self.nbasis)
            orbblock = orb.copy()
            orbblock.imul(self.block)
            orbblock.itranspose()
            pop.assign_dot(orbblock, op)
            orbblock.itranspose()
            pop.idot(orbblock)

            pop_mat.append(pop)
        self.pop_matrix = pop_mat


class PipekMezey(Localization):
    """Perform Pipek-Mezey localization of occupied or virtual Hartree-Fock
    orbitals.
    """

    @property
    def block(self):
        """The orbital block used during localization (OneIndex object)"""
        block = self.lf.create_one_index(self.nbasis)
        if self.block_type == "occ":
            #
            # account for frozen core orbitals
            #
            block.assign(1.0, begin0=self.ncore, end0=self.nocc)
        elif self.block_type == "virt":
            block.assign(1.0, begin0=self.nocc)
        return block

    def grad(self):
        """Gradient of objective function"""
        grad = self.lf.create_two_index(self.nbasis, self.nbasis)
        for pop in self.pop_matrix:
            #
            # 4 [ pop_kk - pop_ll ] * pop_kl
            #
            diag = pop.copy_diagonal()
            pop.contract("ab,a->ab", diag, grad, factor=4.0)
            pop.contract("ab,b->ab", diag, grad, factor=-4.0)
        grad.iscale(-1)

        ind = np.tril_indices(self.nbasis, -1)
        return grad.ravel(ind=ind)

    # TODO: use exact Hessian
    def hessian(self, lshift=1e-8):
        """Diagonal Hessian of objective function

        **Optinal arguments:**

        lshift
             Shift elements of Hessian (float)
        """
        hessian = self.lf.create_two_index(self.nbasis, self.nbasis)
        for pop in self.pop_matrix:
            #
            # pop_ll*pop_ll
            #
            diag2 = self.lf.create_one_index(self.nbasis)
            diag = pop.copy_diagonal()
            diag.mult(diag, diag2)
            #
            # H_kl += -4 pop_ll*pop_ll - 4 pop_kk*pop_kk
            #
            hessian.iadd_t(diag2, 4.0)
            hessian.iadd(diag2, 4.0)
            #
            # H_kl += 8 pop_ll*pop_kk
            #
            hessian.iadd_one_mult(diag, diag, -8.0, transpose0=True)
            #
            # H_kl += 8 pop_kl*pop_kl
            #
            hessian.iadd_mult(pop, pop, 8.0)
        hessian.iadd_shift(lshift)

        ind = np.tril_indices(self.nbasis, -1)
        return hessian.ravel(ind=ind)

    def compute_objective_function(self):
        """Objective function of PM localization to be maximized. The current
        implementation minimizes -(objective_function).
        """
        result = 0.0
        #
        # sum_iA pop(A)_ii^2
        #
        for pop in self.pop_matrix:
            diag2 = self.lf.create_one_index(self.nbasis)
            diag = pop.copy_diagonal()
            diag.mult(diag, diag2)

            result += diag2.trace()
        return -result
