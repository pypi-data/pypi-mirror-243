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
# An original version of this implementation can also be found in 'Horton 2.0.0'.
# # However, this file has been updated and debugged. Compatibility with Horton is NOT
# guaranteed.
#
# 10.2022:
# This module has been rewritten by Emil Sujkowski
# New methods:
# - created __init__ defining self._geminal_matrix and self._lagrange_matrix
# - created _get_alloc_size
#
# - changed initial_guess from list to dictionary
# - added timer to solve_model
# - ncore, npairs, nocc, nvirt, nbasis variables has been removed and replaced by
#   the use of occ_model
#
# Detailed changes:
# See CHANGELOG

"""Correlated wavefunction implementations

   This module contains restricted pCCD

   Variables used in this module:
    :nacto:     number of electron pairs
                (abbreviated as no)
    :nactv:     number of (active) virtual orbitals in the principal configuration
                (abbreviated as nv)
    :ncore:     number of core orbitals
                (abbreviated as nc)
    :nact:      total number of basis functions
                (abbreviated as na)

    Indexing convention:
     :i,j,k,..: occupied orbitals of principal configuration
     :a,b,c,..: virtual orbitals of principal configuration
     :p,q,r,..: general indices (occupied, virtual)

    Abbreviations used (if not mentioned in doc-strings):
     :L_pqrs: 2<pq|rs>-<pq|sr>
     :g_pqrs: <pq|rs>

    For more information see doc-strings.
"""
import numpy as np
from scipy import optimize

from pybest import filemanager
from pybest.auxmat import get_diag_fock_matrix
from pybest.exceptions import ArgumentError, NoConvergence, UnknownOption
from pybest.geminals.geminals_base import GeminalsBase
from pybest.geminals.utils import print_solution
from pybest.helperclass import PropertyHelper
from pybest.linalg.base import Orbital, TwoIndex
from pybest.linalg.cholesky import CholeskyFourIndex, CholeskyLinalgFactory
from pybest.log import log, timer
from pybest.orbital_utils import project_orbitals
from pybest.pt.perturbation_utils import get_epsilon
from pybest.utils import check_options, check_type, unmask


class RpCCDBase(GeminalsBase):
    """Restricted pCCD base class"""

    acronym = ""
    long_name = ""
    reference = ""
    cluster_operator = ""
    comment = ""

    def __init__(
        self,
        lf,
        occ_model,
        freezerot=None,
    ):
        GeminalsBase.__init__(
            self,
            lf,
            occ_model,
            freezerot=None,
        )

        self.geminal_matrix = None
        self.lagrange_matrix = None

    @GeminalsBase.geminal_matrix.setter
    def geminal_matrix(self, new):
        if new is None:
            no = self.occ_model.nacto[0]
            nv = self.occ_model.nactv[0]

            self._geminal_matrix = self.lf.create_two_index(
                no, nv, label="t_p"
            )

        else:
            self._geminal_matrix.assign(new)

    @GeminalsBase.lagrange_matrix.setter
    def lagrange_matrix(self, new):
        if new is None:
            no = self.occ_model.nacto[0]
            nv = self.occ_model.nactv[0]

            self._lagrange_matrix = self.lf.create_two_index(
                no, nv, label="l_p"
            )

        else:
            self._lagrange_matrix.assign(new)

    def _get_alloc_size(self, select):
        na = self.occ_model.nact[0]

        check_options(
            "ndm",
            select,
            "one_dm_ps2",
            "one_dm_response",
            "two_dm_ppqq",
            "two_dm_pqpq",
            "two_dm_rppqq",
            "two_dm_rpqpq",
        )

        alloc = {
            "one_dm_ps2": (self.lf.create_one_index, na),
            "one_dm_response": (self.lf.create_one_index, na),
            "two_dm_ppqq": (self.lf.create_two_index, na),
            "two_dm_pqpq": (self.lf.create_two_index, na),
            "two_dm_rppqq": (self.lf.create_two_index, na),
            "two_dm_rpqpq": (self.lf.create_two_index, na),
        }

        return alloc[select]

    def get_ndm(self, select):
        """Get a density matrix (n-RDM). If not available, it will be created
        (if possible)

        **Arguments:**

        select
             'ps2', or 'response'.
        """
        if select not in self.cache:
            self.update_ndm(select)

        return self.cache.load(select)

    one_dm_ps2 = PropertyHelper(get_ndm, "one_dm_ps2", "Alpha 1-RDM")
    one_dm_response = PropertyHelper(get_ndm, "one_dm_response", "Alpha 1-RDM")
    two_dm_ppqq = PropertyHelper(
        get_ndm, "two_dm_ppqq", "Alpha-beta PS2 (ppqq) 2-RDM"
    )
    two_dm_pqpq = PropertyHelper(
        get_ndm, "two_dm_pqpq", "Alpha-beta PS2 (pqpq) 2-RDM"
    )
    two_dm_rppqq = PropertyHelper(
        get_ndm, "two_dm_rppqq", "Alpha-beta (ppqq) 2-RDM"
    )
    two_dm_rpqpq = PropertyHelper(
        get_ndm, "two_dm_rpqpq", "Alpha-beta (pqpq) 2-RDM"
    )

    #
    # Density matrices:
    #
    @timer.with_section("nDM-pCCD")
    def update_ndm(self, select, ndm=None):
        cached_ndm, method = self.init_ndm(select)
        if ndm is None:
            if select in ["one_dm_response", "two_dm_rppqq", "two_dm_rpqpq"]:
                method(
                    cached_ndm,
                    self.geminal_matrix,
                    self.lagrange_matrix,
                    select,
                    1.0,
                )
            elif select in ["one_dm_ps2", "two_dm_ppqq", "two_dm_pqpq"]:
                method(
                    cached_ndm,
                    self.geminal_matrix,
                    self.geminal_matrix,
                    select,
                    1.0,
                )
            else:
                raise UnknownOption(
                    f"Do not know what to do with option {select}"
                )
        else:
            cached_ndm.assign(ndm)

    def generate_guess(self, guess, dim=None, mo1=None, mo2=None):
        no = self.occ_model.nacto[0]
        na = self.occ_model.nact[0]

        if log.do_medium:
            log.hline("~")
            log(f"Generating initial {guess['type']} guess")
        check_options("guess.type", guess["type"], "random", "const", "mp2")
        check_type("guess.factor", guess["factor"], int, float)
        if guess["factor"] == 0:
            raise ValueError("Scaling factor must be different from 0.")
        if dim is None:
            dim = self.dimension
        if guess["type"] == "random":
            return np.random.random(dim) * guess["factor"]
        if guess["type"] == "const":
            return np.ones(dim) * guess["factor"]
        # Do MP2 guess
        self.clear_cache()
        self.update_hamiltonian("guess", mo2, mo1)
        iiaa = self.from_cache("gppqq")
        fock = self.from_cache("fock")
        fi = fock.copy(0, no)
        fa = fock.copy(no, na)
        eps = get_epsilon(self.denself, [fi, fa], singles=True, doubles=False)
        guess = iiaa.divide(eps, end0=no, begin1=no)

        return guess.array.ravel()

    def get_guess(self, one, two, olp, orb, **kwargs):
        guess = kwargs.get("guess", None)
        restart = kwargs.get("restart", False)
        indextrans = kwargs.get("indextrans", None)

        if restart:
            from pybest.io.iodata import IOData

            data = IOData.from_file(restart)
            if hasattr(data, "t_p"):
                guess["geminal"] = data.t_p.array.ravel()
            if hasattr(data, "l_p"):
                guess["lagrange"] = data.l_p.array.ravel()
            if hasattr(data, "olp") and hasattr(data, "orb_a"):
                if isinstance(olp, TwoIndex) and isinstance(orb, Orbital):
                    project_orbitals(data.olp, olp, data.orb_a, orb)
                else:
                    olp = data.olp
                    orb = data.orb_a
            if hasattr(data, "e_core"):
                self.e_core = unmask("e_core", data, **kwargs)
            if self.e_core is None:
                raise ArgumentError("Cannot find core energy in arguments.")
        initial_guess = {}

        if guess["geminal"] is None:
            if guess["type"] == "mp2":
                #
                # Transform integrals into MO basis
                #
                one_mo, two_mo = self.transform_integrals(
                    one, two, orb, indextrans
                )
                initial_guess["t_p"] = self.generate_guess(
                    guess, mo1=one_mo, mo2=two_mo
                )
                #
                # Delete integrals explicitly
                #
                one_mo.__del__()
                two_mo.__del__()
            else:
                initial_guess["t_p"] = self.generate_guess(guess)
        else:
            check_type("guess.geminal", guess["geminal"], np.ndarray)
            if not guess["geminal"].shape[0] == self.dimension:
                raise ValueError(
                    "Size of geminal guess array does not match number of unknowns."
                )
            initial_guess["t_p"] = guess["geminal"]
        if "lagrange" in guess:
            if guess["lagrange"] is None:
                if guess["type"] == "mp2":
                    initial_guess["l_p"] = initial_guess["t_p"]

                else:
                    initial_guess["l_p"] = self.generate_guess(guess)
            else:
                check_type("guess.lagrange", guess["lagrange"], np.ndarray)
                if not guess["lagrange"].shape[0] == self.dimension:
                    raise ValueError(
                        "Size of Lagrange guess array does not match number of unknowns."
                    )
                initial_guess["l_p"] = guess["lagrange"]
        # We need to return olp and orb in case they are None type as arguments
        return olp, orb, initial_guess

    @timer.with_section("1DM-pCCD")
    def compute_1dm(self, dmout, mat1, mat2, select, factor=1.0):
        no = self.occ_model.nacto[0]
        nv = self.occ_model.nactv[0]
        na = self.occ_model.nact[0]

        summand = 1.0
        if select in ["one_dm_ps2"]:
            summand = 1 + mat1.contract("ab,ab", mat2, select="einsum")

        #
        # Calculate occupied block
        #
        tmpocc = self.lf.create_one_index(no)
        tmpocc.assign(summand)
        mat1.contract("ab,ab->a", mat2, tmpocc, factor=-1.0, select="einsum")

        #
        # Calculate virtual block
        #
        tmpvir = self.lf.create_one_index(nv)
        mat1.contract("ab,ab->b", mat2, tmpvir, select="einsum")

        #
        # Combine both blocks and scale
        #
        dmout.assign(tmpocc, 0, no)
        dmout.assign(tmpvir, no, na)
        dmout.iscale(factor)

    @timer.with_section("2DM-pCCD")
    def compute_2dm(self, dmout, mat1, mat2, select, factor=1.0):
        no = self.occ_model.nacto[0]
        nv = self.occ_model.nactv[0]
        na = self.occ_model.nact[0]

        lc = mat1.contract("ab,ab", mat2, select="einsum")
        factor1 = 1.0

        if select in ["two_dm_rppqq", "two_dm_rpqpq"]:
            factor1 = factor1 - lc
            dm1 = self.one_dm_response
        else:
            dm1 = self.one_dm_ps2

        if "ppqq" in select:
            #
            # temporary storage
            #
            tmpvv = self.lf.create_two_index(nv, nv)
            tmpoo = self.lf.create_two_index(no, no)
            tmpvv2 = self.lf.create_two_index(nv, nv)
            tmpov = self.lf.create_two_index(no, nv)
            tmpo = self.lf.create_one_index(no)
            tmpv = self.lf.create_one_index(nv)

            #
            # o-o block
            #
            mat2.contract("ab,cb->ca", mat1, tmpoo, select="einsum")
            tmpoo.assign_diagonal(0.0)
            dmout.iadd(tmpoo, 1.0, 0, no, 0, no)
            #
            # v-v block
            #
            mat2.contract("ab,ac->bc", mat1, tmpvv, select="td")
            dmout.iadd(tmpvv, 1.0, no, na, no, na)
            #
            # v-o block
            #
            dmout.iadd_t(mat2, 1.0, no, na, 0, no)
            #
            # o-v block
            #
            tmpvv2.iadd_tdot(mat2, mat1)
            tmpov.iadd_dot(mat1, tmpvv2)
            mat2.contract("ab,ab->a", mat1, tmpo, select="einsum")
            mat1.contract("ab,a->ab", tmpo, tmpov, factor=-2.0)
            mat2.contract("ab,ab->b", mat1, tmpv, select="einsum")
            mat1.contract("ab,b->ab", tmpv, tmpov, factor=-2.0)
            mat2_ = mat2.copy()
            mat2_.imul(mat1)
            mat2_.imul(mat1)
            tmpov.iadd(mat2_, 2.0)

            dmout.iadd(mat1, (factor1 + lc), 0, no, no, na)
            dmout.iadd(tmpov, 1.0, 0, no, no, na)
        elif "pqpq" in select:
            #
            # temporary storage
            #
            tmpo = self.lf.create_one_index(no)
            mat2.contract("ab,ab->a", mat1, tmpo, select="einsum")
            dm1v = dm1.copy(no, na)
            mat2_ = mat2.copy()
            mat2_.imul(mat1)
            for i in range(no):
                for j in range(i + 1, no):
                    value = (
                        factor1
                        + lc
                        - tmpo.get_element(i)
                        - tmpo.get_element(j)
                    )
                    dmout.set_element(i, j, value, symmetry=2)
                value = factor1 + lc - tmpo.get_element(i)
                dmout.set_element(i, i, value)
            dmout.iadd_t(dm1v, 1.0, 0, no, no, na)
            dmout.iadd(mat2_, -1.0, 0, no, no, na)
            dmout.iadd(dm1v, 1.0, no, na, 0, no)
            dmout.iadd_t(mat2_, -1.0, no, na, 0, no)
        # scale
        dmout.iscale(factor)

    @timer.with_section("Solve Model RpCCD")
    def solve_model(self, one, two, orb, **kwargs):
        """Solve for pCCD model.

        **Arguments:**

        one, two
             One- and two-body integrals (some Hamiltonian matrix elements).
             A TwoIndex and FourIndex/Cholesky instance

        orb
             An expansion instance which contains the MO coefficients.

        **Keywords:**
             guess: initial guess for wfn (1-dim np.array)
             guesslm: initial guess Lagrange multipliers (1-dim np.array)
             solver: wfn/Lagrange solver (dictionary)
             indextrans: 4-index Transformation (str).
             maxiter: maximum number of iterations (dictionary)
             thresh: thresholds (dictionary)
             orbitaloptimizer: orbital optimization method (str)

             For more details, see :py:meth:`OOGeminals.solve`
        """

        nc = self.occ_model.ncore[0]
        guess = kwargs.get("guess", None)
        guesslm = kwargs.get("guesslm", None)
        solver = kwargs.get("solver", None)
        indextrans = kwargs.get("indextrans", None)
        maxiter = kwargs.get("maxiter", None)
        thresh = kwargs.get("thresh", None)
        orbitaloptimizer = kwargs.get("orbitaloptimizer", "variational")
        #
        # Clear Hamiltonian as it stores the ERI
        #
        self.clear_cache()
        #
        # Read two-electron integrals from disk if required
        #
        if not hasattr(two, "_array"):
            two.load_array("eri")
        #
        # Transform integrals into MO basis
        #
        e_core = self.e_core
        one_mo, two_mo = self.transform_integrals(one, two, orb, indextrans)
        self.e_core = e_core
        #
        # Dump AOs to file
        #
        self.dump_eri(two)
        #
        # Generate effective Hamiltonian elements needed for optimization
        #
        if log.do_high:
            log("Creating auxiliary quantities")
        self.update_hamiltonian("scf", two_mo, one_mo)
        #
        # Delete integrals explicitly
        #
        one_mo.__del__()
        two_mo.__del__()
        del one_mo, two_mo
        #
        # Optimize pCCD wavefunction amplitudes:
        #
        if log.do_high:
            log("Optimizing pCCD cluster amplitudes")
        coeff = self.solve_geminal(
            guess, solver, thresh["wfn"], maxiter["wfniter"]
        )
        self.geminal_matrix = coeff
        #
        # Update IOData container
        #
        self.checkpoint.update("t_p", self.geminal_matrix)
        #
        # Optimize pCCD Lagrange multipliers (lambda equations):
        #
        if orbitaloptimizer == "variational":
            if log.do_high:
                log("Optimizing pCCD lambda amplitudes")
            lcoeff = self.solve_lagrange(
                guesslm, solver, thresh["wfn"], maxiter["wfniter"]
            )
            self.lagrange_matrix = lcoeff
            #
            # Update IOData container
            #
            self.checkpoint.update("l_p", self.lagrange_matrix)

            #
            # Update occupation numbers (response 1-RDM)
            #
            self.clear_dm()
            self.update_ndm("one_dm_response")
            self.update_ndm("two_dm_rpqpq")
            self.update_ndm("two_dm_rppqq")
            orb.assign_occupations(self.one_dm_response, nc)
            orb.clear_energies()
            #
            # Update IOData container
            # Copy final orbitals
            self.checkpoint.update("orb_a", orb.copy())
            self.checkpoint.update("dm_1", self.one_dm_response)
            self.checkpoint.update(
                "dm_2", {"pqpq": self.two_dm_rpqpq, "ppqq": self.two_dm_rppqq}
            )

        elif orbitaloptimizer == "ps2":
            self.clear_dm()
            self.update_ndm("one_dm_ps2")
            self.update_ndm("two_dm_pqpq")
            self.update_ndm("two_dm_ppqq")
            #
            # Update IOData container
            #
            self.checkpoint.update("orb_a", orb.copy())
            self.checkpoint.update("dm_1", self.one_dm_ps2)
            self.checkpoint.update(
                "dm_2", {"pqpq": self.two_dm_pqpq, "ppqq": self.two_dm_ppqq}
            )

    @timer.with_section("PSEqRpCCD")
    def solve_geminal(self, guess, solver, wfnthreshold, wfnmaxiter):
        """Solves for geminal matrix

        **Arguments:**

        guess
             The initial guess. A 1-dim np array.

        solver
             The solver used. A dictionary with element 'wfn'.

        wfnthreshold
             The optimization threshold. A float.

        wfnmaxiter
             The maximum number of iterations. An integer.
        """
        iiaa = self.from_cache("gppqq")
        iaia = self.from_cache("lpqpq")
        one = self.from_cache("t")
        fock = self.from_cache("fock")
        sol = optimize.root(
            self.vector_function_geminal,
            guess,
            args=(iiaa, iaia, one, fock),
            method=solver["wfn"],
            options={"xtol": wfnthreshold, "maxiter": wfnmaxiter},
            callback=None,
        )
        if not sol.success:
            raise NoConvergence(
                f"Program terminated. Error in solving pCCD equations: "
                f"{sol.message}"
            )
        if log.do_high:
            log(
                f"Optimization of geminal coefficients converged in {sol.nit} iterations."
            )
        #
        # Update IOData container
        #
        self.checkpoint.update("niter_t_p", sol.nit)
        return sol.x

    @timer.with_section("LagrangeRpCCD")
    def solve_lagrange(self, guess, solver, wfnthreshold, wfnmaxiter):
        """Solves for Lagrange multipliers

        **Arguments:**

        guess
             The initial guess. A 1-dim np array.

        solver
             The solver used. A dictionary with element 'lagrange'.

        wfnthreshold
             The optimization threshold. A float.

        wfnmaxiter
             The maximum number of iterations. An integer.
        """
        iiaa = self.from_cache("gppqq")
        iaia = self.from_cache("lpqpq")
        one = self.from_cache("t")
        fock = self.from_cache("fock")
        sol = optimize.root(
            self.vector_function_lagrange,
            guess,
            args=(self.geminal_matrix, iiaa, iaia, one, fock),
            method=solver["lagrange"],
            callback=None,
            options={"xtol": wfnthreshold, "maxiter": wfnmaxiter},
        )
        if not sol.success:
            raise NoConvergence(
                f"Program terminated. Error in solving Lagrange multipliers: "
                f"{sol.message}"
            )
        if log.do_high:
            log(
                f"Optimization of Lagrange multipliers converged in {sol.nit} iterations."
            )
        #
        # Update IOData container
        #
        self.checkpoint.update("niter_l_p", sol.nit)
        return sol.x

    #
    # effective Hamiltonian elements
    #

    @timer.with_section("pCCD: Heff")
    def update_hamiltonian(self, select, two_mo, one_mo=None):
        na = self.occ_model.nact[0]

        try:
            one_mo = one_mo[0]
            two_mo = two_mo[0]
        except Exception:
            pass
        check_options(
            select,
            select,
            "scf",
            "nonscf",
            "guess",
        )
        na = self.occ_model.nact[0]
        #
        # 1-el MOs
        #
        matrix = self.init_cache("t", na, na)
        matrix.assign(one_mo)
        #
        # <pp|qq>
        #
        gppqq = self.init_cache("gppqq", na, na)
        two_mo.contract("aabb->ab", gppqq)
        #
        # inactive diagonal Fock = h_pp + sum_i (<pi||pi>+<pi|pi>)
        #
        fock = self.init_cache("fock", na)
        get_diag_fock_matrix(fock, one_mo, two_mo, self.occ_model.nacto[0])

        if select in ["scf", "nonscf"]:
            #
            # <pq|pq>
            #
            gpqpq = self.init_cache("gpqpq", na, na)
            two_mo.contract("abab->ab", gpqpq)
            #
            # <pq||pq>+<pq|pq>
            #
            lpqpq = self.init_cache("lpqpq", na, na)
            lpqpq.iadd(gpqpq, factor=2.0)
            lpqpq.iadd(gppqq, factor=-1.0)
        if select == "scf":
            #
            # <pq|rq> (faster this way)
            #
            opt = "einsum"
            if isinstance(two_mo, CholeskyFourIndex):
                opt = "td"
            gpqrq = self.init_cache("gpqrq", na, na, na)
            two_mo.contract("abcb->abc", gpqrq, select=opt)
            #
            # store 2-el MOs
            # This doubles the current memory as we create a copy
            # Note: the peak memory is caused in the solver
            #
            if isinstance(self.lf, CholeskyLinalgFactory):
                mo2 = self.init_cache("mo2", na, na, na, na, nvec=two_mo.nvec)
            else:
                mo2 = self.init_cache("mo2", na, na, na, na)
            mo2.assign(two_mo)

    #
    # Functions for energy evaluation:
    #
    def compute_correlation_energy(self, arg=None):
        """Get correlation energy of restricted pCCD

        **Optional arguments:**

        arg
             The pCCD coefficient matrix (np.array or TwoIndex instance).
             If not provided, the correlation energy is calculated
             from self.geminal_matrix (default None)
        """

        no = self.occ_model.nacto[0]
        nv = self.occ_model.nactv[0]

        ov = self.get_range("ov", 2)
        if arg is None:
            coeff = self.geminal_matrix
        else:
            coeff = self.lf.create_two_index(no, nv)
            coeff.assign(arg)
        kmat = self.from_cache("gppqq")
        #
        # Ecorr = sum_ia c_ia <ii|aa>
        #
        return coeff.contract("ab,ab", kmat, **ov, select="einsum")

    def compute_reference_energy(self):
        """Get energy of reference determinant for restricted pCCD including core energy"""

        no = self.occ_model.nacto[0]

        one = self.from_cache("t")
        fock = self.from_cache("fock")
        #
        # Eref = sum_i (t_ii + F_ii)
        #
        energy = one.trace(0, no, 0, no)
        energy += fock.trace(0, no)
        return energy + self.e_core

    def compute_total_energy(self, coeff=None):
        """Get total energy (reference + correlation) including nuclear-repulsion/
        core energy for restricted pCCD.

        **Optional arguments:**

        coeff
             The pCCD coefficient matrix (np.array or TwoIndex instance).
             If not provided, the correlation energy is calculated
             from self.geminal_matrix (default None)
        """
        return (
            self.compute_correlation_energy(coeff)
            + self.compute_reference_energy()
        )

    #
    # Vector function for pCCD:
    #
    @timer.with_section("VecFctGeminal")
    def vector_function_geminal(self, coeff, miiaa, miaia, one, diagfock):
        """Construct vector function for optimization of pCCD coefficients.

        **Arguments:**

        coeff
             The pCCD coefficients (np.array)

        miiaa, miaia
             effective Hamiltonian elements (TwoIndex instances)

        one
             1-electron integrals (TwoIndex instance)

        diagfock
             Diagonal inactive Fock matrix (OneIndex instances)
        """

        no = self.occ_model.nacto[0]
        nv = self.occ_model.nactv[0]

        # get ranges
        o2 = self.get_range("o", 2)
        v2 = self.get_range("v", 2)
        oo = self.get_range("oo")
        vo2 = self.get_range("vo", 2)
        ov2 = self.get_range("ov", 2)
        vv2 = self.get_range("vv", 2)
        cia = self.lf.create_two_index(no, nv)
        cia.assign(coeff)

        #
        # correlation energy for current iteration step
        #
        e_corr = self.compute_correlation_energy(cia)

        #
        # vectorFunction_ia
        #
        result = self.lf.create_two_index(no, nv)

        #
        # Add contributions to vectorFunction_ia:
        #
        # c_ia*e_corr
        #
        result.iadd(cia, -e_corr)

        #
        # c_0*miiaa
        #
        result.iadd(miiaa, 1.0, **ov2)

        #
        # -2c_ia*f_ii
        #
        cia.contract("ab,a->ab", diagfock, result, factor=-2.0, **o2)

        #
        # 2c_ia*f_aa
        #
        cia.contract("ab,b->ab", diagfock, result, factor=2.0, **v2)

        #
        # -2c_ia*(<ia||ia>+<ia|ia>)
        #
        result.iadd_mult(cia, miaia, -2.0, **ov2)

        #
        # c_ja*(<ii|jj>)
        #
        result.iadd_dot(miiaa, cia, 1.0, **oo)

        #
        # c_ib*(<bb|aa>)
        #
        result.iadd_dot(cia, miiaa, 1.0, **vv2)

        #
        # c_ia*(c_jb*<jj|bb>)
        #
        factor = cia.contract("ab,ab", miiaa, **ov2, select="einsum")
        result.iadd(cia, factor)

        #
        # c_ib*<bb|jj>*c_ja
        #
        tmp = self.lf.create_two_index(no, no)
        tmp.iadd_dot(cia, miiaa, 1.0, **vo2)
        result.iadd_dot(tmp, cia, 1.0)

        #
        # -2c_ja*c_ia*<jj|aa>
        #
        tmpv = self.lf.create_one_index(nv)
        cia.contract("ab,ab->b", miiaa, tmpv, **ov2, select="einsum")
        cia.contract("ab,b->ab", tmpv, result, factor=-2.0, select="einsum")

        #
        # -2c_ib*c_ia*<ii|bb>
        #
        tmpo = self.lf.create_one_index(no)
        cia.contract("ab,ab->a", miiaa, tmpo, **ov2, select="einsum")
        cia.contract("ab,a->ab", tmpo, result, factor=-2.0, select="einsum")

        #
        # +2c_ia*c_ia*<ii|aa>
        #
        tmp = cia.copy()
        tmp.imul(cia)
        result.iadd_mult(tmp, miiaa, 2.0, **ov2)

        return result.array.ravel(order="C")

    #
    # Jacobian for pCCD:
    #
    def jacobian_pccd(self, coeff, miiaa, miaia, one, fock):
        """Construct Jacobian for optimization of geminal coefficients."""
        raise NotImplementedError

    #
    # Vector function for Lagrange multipliers:
    #
    @timer.with_section("VecFctLagrange")
    def vector_function_lagrange(
        self, lagrange, cia, miiaa, miaia, one, diagfock
    ):
        """Construct vector function for optimization of Lagrange multipliers.

        **Arguments:**

        lagrange
             The lagrange multipliers (np array)

        cia
             The geminal coefficients (TwoIndex instance)

        miiaa, miaia
             effective Hamiltonian elements (TwoIndex instances)

        one
             1-electron integrals (TwoIndex instance)

        diagfock
             Diagonal inactive Fock matrix (OneIndex instance)
        """

        no = self.occ_model.nacto[0]
        nv = self.occ_model.nactv[0]
        ov = self.get_range("ov")
        o2 = self.get_range("o", 2)
        v2 = self.get_range("v", 2)
        oo = self.get_range("oo")
        ov2 = self.get_range("ov", 2)
        vv2 = self.get_range("vv", 2)
        lmat = self.lf.create_two_index(no, nv)
        lmat.assign(lagrange)

        #
        # intermediate variables:
        # cgi = sum_b c_ib <ii|bb>
        # cga = sum_j c_ja <jj|aa>
        # lci = sum_b c_ib l_ib
        # lca = sum_j c_ja l_ja
        #
        cgi = self.lf.create_one_index(no)
        cga = self.lf.create_one_index(nv)
        lci = self.lf.create_one_index(no)
        lca = self.lf.create_one_index(nv)
        cia.contract("ab,ab->a", miiaa, cgi, **ov2, select="einsum")
        cia.contract("ab,ab->b", miiaa, cga, **ov2, select="einsum")
        lmat.contract("ab,ab->a", cia, lci, select="einsum")
        lmat.contract("ab,ab->b", cia, lca, select="einsum")

        #
        # vectorFunction_ia
        #
        result = self.lf.create_two_index(no, nv)

        #
        # miiaa
        #
        result.iadd(miiaa, 1.0, **ov2)

        #
        # -2l_ia*cgi
        #
        lmat.contract("ab,a->ab", cgi, result, factor=-2.0)

        #
        # -2l_ia*cga
        #
        lmat.contract("ab,b->ab", cga, result, factor=-2.0)

        #
        # -2miiaa*lci
        #
        miiaa.contract("ab,a->ab", lci, result, factor=-2.0, **ov)

        #
        # -2miiaa*lca
        #
        miiaa.contract("ab,b->ab", lca, result, factor=-2.0, **ov)

        #
        # -2l_ia*f_ii
        #
        lmat.contract("ab,a->ab", diagfock, result, factor=-2.0, **o2)

        #
        # 2l_ia*f_aa
        #
        lmat.contract("ab,b->ab", diagfock, result, factor=2.0, **v2)

        #
        # -2l_ia*(<ia||ia>+<ia|ia>)
        #
        result.iadd_mult(lmat, miaia, -2.0, **ov2)

        #
        # l_ja*(<ii|jj>)
        #
        result.iadd_dot(miiaa, lmat, 1.0, **oo)

        #
        # l_ib*(<bb|aa>)
        #
        result.iadd_dot(lmat, miiaa, 1.0, **vv2)

        #
        # 4l_ia*c_ia*<ii|aa>
        #
        tmp = lmat.copy()
        tmp.imul(cia)
        result.iadd_mult(tmp, miiaa, 4.0, **ov2)

        #
        # <ii|bb>*c_jb*l_ja
        #
        tmp = self.lf.create_two_index(nv, nv)
        tmp.iadd_tdot(cia, lmat)
        result.iadd_dot(miiaa, tmp, 1.0, **ov)

        #
        # l_ib*c_jb*<jj|aa>
        #
        tmp = self.lf.create_two_index(no, no)
        tmp.iadd_dott(lmat, cia)
        result.iadd_dot(tmp, miiaa, 1.0, **ov2)

        return result.array.ravel(order="C")

    #
    # Jacobian for Lagrange multipliers of OpCCD:
    #
    def jacobian_lambda(self, lagrange, cia, miiaa, miaia, one, diagfock):
        """Construct Jacobian for optimization of Lagrange multipliers for
        restricted pCCD.
        """
        raise NotImplementedError

    def print_final(self, status="Final"):
        """Print energies

        **Optional arguments:**

        status
             A string.
        """
        log.hline("-")
        log(
            f"{status+' reference Energy:':<30} {self.compute_reference_energy():> 16.12f}"
        )
        log(
            f"{status+' correlation Energy:':<30} {self.compute_correlation_energy():> 16.12f}"
        )
        log.hline("=")
        log(
            f"{status+' total Energy:':<30} {self.compute_total_energy():> 16.12f}"
        )
        log.hline("=")

    def dump_final(
        self,
        orb,
        printoptions,
        dumpci,
        checkpoint,
        checkpoint_fn="checkpoint_pccd.h5",
    ):
        """Dump final solution (orbitals, wavefunction amplitudes, geminal
        coefficients)

        **Arguments:**

        orb
             An expansion instance. AO/MO coefficients stored on disk

        printoptions, dumpci
             A dictionary. See :py:meth:`OOGeminals.solve`

        checkpoint:
             An integer. See :py:meth:`OOGeminals.solve`

        checkpoint_fn
             The filename of the checkpoint file.
        """
        if checkpoint > 0:
            if log.do_medium:
                log(
                    f"Writing pCCD output to file {filemanager.result_dir}/"
                    f"{checkpoint_fn}"
                )
            self.checkpoint.to_file(checkpoint_fn)
            if log.do_medium:
                log.hline("-")
                log(
                    f"Final solution for coefficients: (only printed if |c_i| > "
                    f"{printoptions['threshold']})"
                )
        if printoptions["geminal_coefficients"]:
            self.print_amplitudes(printoptions["threshold"])
        else:
            print_solution(
                self,
                printoptions["threshold"],
                printoptions["excitationlevel"],
                amplitudestofile=dumpci["amplitudestofile"],
                fname=dumpci["amplitudesfilename"],
            )
        if printoptions["geminal"]:
            log.hline("-")
            log("Geminal matrix: (rows=occupied, columns=virtual)")
            self.print_geminal_coefficients()
        if log.do_medium:
            log.hline("-")
            log("Natural occupation numbers (for spatial orbitals):")
            self.print_occupations(orb)
            log.hline("=")

    def print_geminal_coefficients(self):
        """Print geminal coefficients"""

        no = self.occ_model.nacto[0]
        nv = self.occ_model.nactv[0]

        log.hline("")
        s = "".join(f"{(i + 1 + no):11}" for i in range(nv))
        log(f"  {s}")
        log.hline("")
        for line in range(no):
            s = f"{(line + 1):>4}:"
            for row in range(nv):
                s += f"{self.geminal_matrix.get_element(line, row):> 11.6f}"
            log(s)

    def get_max_amplitudes(self, threshold=0.01, limit=None):
        """Returns a dictionary with a list of amplitudes and their indices.

        **Arguments:**

        threshold
            (float) amplitudes smaller than threshold won't be printed

        limit
            (int) restrict the number of printed amplitudes to at most `limit`
            in number. If `limit` is set, all remaining amplitudes will be
            ignored even if they are above `threshold` in absolute value
        """
        t_p = self.geminal_matrix.get_max_values(absolute=True)
        t_p.sort(key=lambda x: abs(x[1]), reverse=True)
        if limit is None:
            limit = sum(abs(t[1]) > abs(threshold) for t in t_p)
        max_t_p = []
        nc = self.occ_model.ncore[0]
        no = self.occ_model.nacto[0]
        for index, value in t_p[:limit]:
            i, a = index
            i += nc + 1
            a += nc + no + 1
            max_t_p.append(((i, a), value))
        return {"t_p": max_t_p}

    def print_amplitudes(self, threshold=1e-2, limit=None):
        """Prints amplitudes in descending order in absolute value.

        **Arguments:**

        threshold
            (float) amplitudes smaller than threshold won't be printed

        limit
            (int) restrict the number of printed amplitudes to at most `limit`
            in number. If `limit` is set, all remaining amplitudes will be
            ignored even if they are above `threshold` in absolute value
        """
        amplitudes = self.get_max_amplitudes(threshold=threshold, limit=limit)
        max_amplitudes = amplitudes["t_p"]

        if max_amplitudes:
            log.hline("-")
            log(
                "Leading electron-pair excitation amplitudes "
                "(i,a = alpha spin; I, A = beta spin)"
            )
            log(" ")
            log(f"{'amplitude':>13}{'i':>5}{'I':>5}  ->{'a':>5}{'A':>5}")
            log(" ")

            for index, value in max_amplitudes:
                i, a = index
                log(f"{value:13.6f}{i:>5}{i:>5}  ->{a:>5}{a:>5}")

    def print_occupations(self, orb):
        """Print occupation numbers"""
        # Print occupation numbers for the complete orbital basis
        # frozen core + nacto + nactv
        na = self.occ_model.nbasis[0]

        # Print at most 6 in one line
        s = ""
        for i, el in zip(range(na), orb.occupations):
            if i % 5 == 0 and i != 0:
                log(s)
                s = ""
            s += f"{(i + 1):>6}: {(el * 2.0): 7.6f}"
        log(s)

    #
    # compute approximate overlap:
    #
    def compute_overlap(self):
        """Compute approximate overlap of pCCD"""
        return 1 + self.geminal_matrix.contract(
            "ab,ab", self.geminal_matrix, select="einsum"
        )
