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
"""Optimization methods

   Davidson diagonalization
"""

import numpy as np
import scipy

from pybest import filemanager
from pybest.exceptions import ArgumentError, UnknownOption
from pybest.log import log, timer

__all__ = [
    "Davidson",
]


class Davidson:
    def __init__(
        self,
        lf,
        nroots,
        nguess=None,
        maxiter=200,
        tolerance=1e-6,
        tolerancev=1e-4,
        maxvectors=None,
        skipgs=True,
        todisk=True,
    ):
        """
        Davidson Diagonalizer.
        Diagonalizes a (non)symmetric matrix and returns the (right)
        eigenvectors.
        Matrix of search space is constructed on-the-fly and must be defined in
        ``build_subspace_hamiltonian`` as a class method.

        ** Arguments **

        maxiter
            Maximum number of iterations (int)

        tolerance
            Convergence tolerance for energy (float)

        tolerancev
            Convergence tolerance for vectors (float)

        ** Returns **

          :eigval:   eigenvalues
          :eigvec:   eigenvectors

        """
        #
        # Set private attributes (fixed during execution)
        #
        self._lf = lf
        if maxiter < 0:
            raise UnknownOption("Number of iterations has to be positive.")
        self._maxiter = maxiter
        self._tol = tolerance
        self._tolv = tolerancev
        if nroots < 0:
            raise UnknownOption("Number of roots has to be positive.")
        self._nroots = nroots
        self._skipgs = skipgs
        self._todisk = todisk
        #
        # Set number of guess vectors if not defined by user
        #
        if nguess is None:
            nguess = int((nroots - 1) * 4 + 1)
        if maxvectors is None:
            maxvectors = int(nroots - 1) * 10
        self._nguess = nguess
        self._maxvectors = maxvectors
        self.nbvector = 0
        self.nsigmav = 0

    @property
    def lf(self):
        """The linalg factory"""
        return self._lf

    @property
    def maxiter(self):
        """The maximum number of Davidson steps"""
        return self._maxiter

    @property
    def tol(self):
        """The convergence threshold for the energy"""
        return self._tol

    @property
    def tolv(self):
        """The convergence threshold for the wave function"""
        return self._tolv

    @property
    def nroots(self):
        """The total number of roots to target"""
        return self._nroots

    @property
    def skipgs(self):
        """
        Skip printing information of ground state wave function/lowest root
        (boolean)
        """
        return self._skipgs

    @property
    def todisk(self):
        """Write sigma and b vectors to disk (boolean)"""
        return self._todisk

    @property
    def nguess(self):
        """The total number of guess vectors"""
        return self._nguess

    @property
    def maxvectors(self):
        """The maximum number of Davidson vectors before subspace collapse"""
        return self._maxvectors

    @property
    def nbvector(self):
        """The number of b vectors used to construct the subspace Hamiltonian"""
        return self._nbvector

    @nbvector.setter
    def nbvector(self, new):
        self._nbvector = new

    @property
    def nsigmav(self):
        """The number of sigma vectors used to construct the subspace Hamiltonian"""
        return self._nsigmav

    @nsigmav.setter
    def nsigmav(self, new):
        self._nsigmav = new

    def read_from_disk(self, inp, select, ind):
        """Reads input vectors from disk if inp is None, otherwise it returns
        element inp[ind] from list
        """
        if inp is None:
            from pybest.io.iodata import IOData

            fname = f"{select}_{ind}.h5"
            filename = filemanager.temp_path(fname)
            bv = IOData.from_file(filename)
            return bv.vector
        elif isinstance(inp, list):
            return inp[ind]
        elif isinstance(inp, np.ndarray):
            return inp[:, ind]
        else:
            raise ArgumentError("Do not know how to handle input")

    def push_vector(self, inp, new, select, ind):
        """Appends new vector to list of previous vectors inp. If inp is None,
        vector is pushed to disk.
        """
        if inp is None:
            from pybest.io.iodata import IOData

            fname = f"{select}_{ind}.h5"
            filename = filemanager.temp_path(fname)
            v = IOData(vector=new)
            v.to_file(filename)
            v = None
            return None
        elif isinstance(inp, np.ndarray):
            inp[:, ind] = new[:]
        elif isinstance(inp, list):
            inp.append(new)
        else:
            raise ArgumentError("Do not know how to handle input")
        return inp

    def reset_vector(self, inp):
        """Resets input vectors to empty list. If vectors are dump to disk,
        returns None.
        """
        if inp is None:
            return None
        elif isinstance(inp, np.ndarray):
            inp[:] = 0.0
        elif isinstance(inp, list):
            inp = []
        else:
            raise ArgumentError("Do not know how to handle input")
        return inp

    def normalize_correction_vector(self, inp, dim):
        """Normalizes vectors using QR. If vectors are stored to disk, reads
        them in first and stores solution vectors to disk.
        """
        if inp is None:
            #
            # Use GS instead of np.qr to save memory
            #
            for j in range(self.nroots):
                bj = self.lf.create_one_index(dim)
                evecj = self.read_from_disk(None, "residual", j)
                bj.assign(evecj)
                if j != 0:
                    bjortho = self.gramschmidt(
                        None, bj, j, "residualortho", threshold=0.0
                    )
                    if bjortho is not None:
                        self.push_vector(None, bjortho, "residualortho", j)
                    bjortho = None
                else:
                    normbj = bj.norm()
                    if normbj > 0.0:
                        bj.iscale(1.0 / normbj)
                    else:
                        bj.clear()
                        bj.set_element(0, 1.0)
                    self.push_vector(None, bj, "residualortho", j)
            bj = None
            evecj = None
            return None
        elif isinstance(inp, np.ndarray):
            deltak, R = np.linalg.qr(inp.real)
        else:
            raise ArgumentError("Don't know how to handle input vectors")
        return deltak

    #   def check_real(self, eigval, eigvec):
    def sort_eig(self, eigval, eigvec):
        """Sort eigenvalues and eigenvectors."""
        idx = eigval.argsort()
        esort = eigval[idx]
        vsort = eigvec[:, idx]
        #
        # Right now, simply push them up in the spectrum to improve convergence
        #
        (imag_,) = np.where(esort.imag)
        if not np.isreal(eigval).all():
            if np.amin(imag_) < self.nroots:
                for i in range(self.nroots):
                    if abs(esort[i].imag) > 1e-4:
                        log(
                            f"Imaginary eigenvalues found for root {i}. "
                            f"Taking only real part."
                        )
            if log.do_high:
                log(f"Imaginary eigenvalues found for roots {imag_}.")
                log("Eigenvalue spectrum:")
                log(f"{*esort,}")
        for i in imag_:
            esort[i] = esort[i].real

        #
        # Get all (almost) degenerate states and orthogonalize them
        #
        ue, uind, uinv, ucount = np.unique(
            esort.round(decimals=6), True, True, True
        )
        for i in range(len(esort)):
            if i not in uind:
                deg = uind[uinv[i]]
                log(
                    f"Orthogonalization of (almost) degenerate vectors {i} {deg}"
                )
                v1 = vsort[:, deg]
                #
                # Degenerate eigenvalues should show up as complex conjugate pairs
                #
                if np.allclose(vsort[:, deg], vsort[:, i].conjugate()):
                    if log.do_high and deg < self.nroots:
                        log(
                            f"norm of real part, norm of imaginary part: "
                            f"{np.linalg.norm(vsort[:, deg].real, ord=2)}, "
                            f"{np.linalg.norm(vsort[:, deg].imag, ord=2)}"
                        )
                    v1 = vsort[:, deg].real
                    v2 = vsort[:, deg].imag
                else:
                    v2 = vsort[:, i]
                proj = np.dot(v1.conjugate(), v2) / np.dot(v1, v1.conjugate())
                v2 = v2[:] - v1[:] * proj
                vsort[:, deg] = v1 / np.linalg.norm(v1, ord=2)
                vsort[:, i] = v2 / np.linalg.norm(v2, ord=2)
                if log.do_high:
                    if not np.isreal(vsort[:, deg]).all():
                        log(
                            f"Imaginary part of eigenvector non-zero {vsort[:, deg]}"
                        )
                    if not np.isreal(vsort[:, i]).all():
                        log(
                            f"Imaginary part of eigenvector non-zero {vsort[:, i]}"
                        )
                    if deg < self.nroots:
                        log(
                            f"root {deg} (after normalization) {*vsort[:, deg],}"
                        )
                        log(f"root {i} (after normalization) {*vsort[:, i],}")
                v1 = None
                v2 = None

        return esort.real, vsort.real

    def build_guess_vectors(self, obj, *args):
        """
        Build (orthonormal) set of guess vectors for each root.

        Calls method-dependent function defined in class obj to construct
        optimal guess vector of the search space.

        If self.todisk is True, subroutine has to store vectors to
        {filemanager.temp_dir}/bvector_#int.h5

        ** Returns **

            List of OneIndex instances (guess vectors)
        """
        bvector, nvec = obj.build_guess_vectors(
            self.nguess, self.todisk, *args
        )
        self.nbvector = nvec
        return bvector

    def compute_h_diag(self, obj, *args):
        """
        Calculate the diagonal elements of the matrix to be diagonalized.
        Function is defined in obj class and can take function arguments args.

        ** Returns **

            OneIndex instance
        """
        return obj.compute_h_diag(*args)

    def build_subspace_hamiltonian(
        self, obj, bvector, hdiag, sigma, hamsub, *args
    ):
        """
        Build subspace Hamiltonian of search space defined in obj class used to
        calculate the diagonal elements of the matrix.
        Can take function arguments args.

        ** Returns **

            OneIndex instance
        """
        bind = 0
        if sigma is False:
            # first iteration
            # sigma = []
            self.nsigmav = 0
            if self.todisk:
                sigma = None
            else:
                sigma = []
        else:
            # Append
            bind = self.nsigmav
        # Loop over all bvectors to calculate sigma vectors
        for b in range(bind, self.nbvector):
            bv = self.read_from_disk(bvector, "bvector", b)
            sigma_ = obj.build_subspace_hamiltonian(bv, hdiag, *args)
            sigma = self.push_vector(sigma, sigma_, "sigmav", self.nsigmav)
            self.nsigmav += 1
        ham = self.calculate_subspace_hamiltonian(bvector, sigma, hamsub, bind)
        return ham, sigma

    def calculate_subspace_hamiltonian(self, bvector, sigmav, hamsub, bind):
        """Calculate subspace Hamiltonian (bvector.sigma)_ij"""
        subham = self.lf.create_two_index(self.nbvector, self.nbvector)
        if hamsub is not False:
            subham.assign(hamsub, end0=hamsub.nbasis, end1=hamsub.nbasis1)
            del hamsub
            for b in range(0, self.nbvector):
                for s in range(bind, self.nbvector):
                    bv = self.read_from_disk(bvector, "bvector", b)
                    sv = self.read_from_disk(sigmav, "sigmav", s)
                    prod1 = bv.dot(sv)
                    subham.set_element(b, s, prod1, symmetry=1)
                    if b < s:
                        bv = self.read_from_disk(bvector, "bvector", s)
                        sv = self.read_from_disk(sigmav, "sigmav", b)
                        prod2 = bv.dot(sv)
                        subham.set_element(s, b, prod2, symmetry=1)
        else:
            row = 0
            for b in range(0, self.nbvector):
                bv = self.read_from_disk(bvector, "bvector", b)
                col = 0
                for s in range(0, self.nbvector):
                    sv = self.read_from_disk(sigmav, "sigmav", s)
                    prod = bv.dot(sv)
                    subham.set_element(row, col, prod, symmetry=1)
                    col += 1
                row += 1
        return subham

    def gramschmidt(
        self, old, new, nvector, select, norm=True, threshold=1e-4
    ):
        """
        Orthonormalize a vector (new) on a set of other (already orthonormal)
        vectors (old) using the Gram-Schmidt orthonormalization procedure.
        """
        for i in range(0, nvector):
            oldi = self.read_from_disk(old, select, i)
            proj = oldi.copy()
            norm2 = oldi.dot(oldi)
            newdotold = new.dot(oldi, 1.0)
            proj.iscale(newdotold / norm2)
            new.iadd(proj, -1.0)
            oldi = None
            proj = None
        if norm:
            newnormo = new.norm()
            if log.do_high:
                log(f"Norm {newnormo}")
            if newnormo <= threshold:
                return None
            else:
                new.iscale(1 / newnormo)
                return new
        return new

    @timer.with_section("Davidson")
    def __call__(self, obj, *args):
        """The Davidson diagonalization."""
        #
        # compute diagonal of Hamiltonian
        #
        hdiag = self.compute_h_diag(obj, *args)
        #
        # compute guess vectors
        #
        bvector = self.build_guess_vectors(obj, hdiag, *args)

        if log.do_medium:
            log.hline("=")
            log("Davidson diagonalization")
            log.hline("~")
            log(f"{'maxiter':>20s}: {self.maxiter}")
            log(f"{'nroots':>20s}: {self.nroots}")
            log(f"{'nguess':>20s}: {self.nguess}")
            log(f"{'to disk':>20s}: {self.todisk}")
            log(f"{'Energy tolerance':>20s}: {self.tol}")
            log(f"{'Vector tolerance':>20s}: {self.tolv}")
            log.hline("~")

        theta_old = np.zeros(self.nroots)
        iter_ = 0
        restart = False
        dim = obj.dimension
        rknorm = np.zeros(self.nroots)
        if self.todisk:
            evec = None
            rk = None
        else:
            evec = np.zeros((dim, self.nroots))
            rk = np.zeros((dim, self.nroots))
        converged = []
        while True:
            #
            # First iteration or after subspace collapse: construct full Hamiltonian
            #
            if iter_ == 0 or restart:
                hamsub, sigma = self.build_subspace_hamiltonian(
                    obj, bvector, hdiag, False, False, *args
                )
                restart = False
            #
            # subsequent iterations: construct new subspace Hamiltonian elements
            #
            else:
                hamsub, sigma = self.build_subspace_hamiltonian(
                    obj, bvector, hdiag, sigma, hamsub, *args
                )
            #
            # diagonalization of submatrix (eigenvalues not sorted)
            #
            theta, s = scipy.linalg.eig(
                hamsub._array,
                b=None,
                left=False,
                right=True,
                overwrite_a=False,
                overwrite_b=False,
                check_finite=True,
            )
            #
            # sort eigenvalues and eigenvectors
            #
            theta, s = self.sort_eig(theta, s)
            #
            # loop over all roots
            #
            evec = self.reset_vector(evec)
            rk = self.reset_vector(rk)
            for j in range(0, self.nroots):
                tmpevj = np.zeros(dim)
                tmprkj = np.zeros(dim)
                for i in range(self.nsigmav):
                    bv = self.read_from_disk(bvector, "bvector", i)
                    sv = self.read_from_disk(sigma, "sigmav", i)
                    tmpevj[:] += bv._array * s[i, j].real
                    tmprkj[:] = (
                        tmprkj[:]
                        + sv._array * s[i, j]
                        - theta[j] * bv._array * s[i, j]
                    )
                #
                # Calculate norm for convergence
                #
                rknorm[j] = np.linalg.norm(tmprkj[:], ord=2)
                #
                # Append to list or store to disk
                #
                evec = self.push_vector(evec, tmpevj.real, "evecs", j)
                #
                # get rid of nans or division by almost small numbers:
                #
                ind = np.where(abs(theta[j] - hdiag._array) < 1e-4)
                # Preconditioning
                # Do not divide by zero
                if rknorm[j] >= 1e-4:
                    tmprkj = (
                        np.divide(
                            tmprkj[:],
                            (theta[j] - hdiag._array),
                            where=(abs(theta[j] - hdiag._array) != 0.0),
                        )
                    ).real
                # If denominator small, set to zero
                tmprkj[ind] = 0.0
                # Push back residual
                rk = self.push_vector(rk, tmprkj, "residual", j)
                tmpevj = None
                tmprkj = None
            # free memory
            s = None
            #
            # normalize correction vectors
            #
            deltak = self.normalize_correction_vector(rk, dim)
            #
            # perform subspace collapse if required
            #
            if self.nbvector > self.maxvectors:
                if log.do_medium:
                    log(
                        "Maximum number of Davidson vectors reached. "
                        "Performing subspace collapse."
                    )
                self.nbvector = 0
                bvector = self.reset_vector(bvector)
                restart = True
                for j in range(self.nroots):
                    bj = self.lf.create_one_index(dim)
                    evecj = self.read_from_disk(evec, "evecs", j)
                    bj.assign(evecj)
                    if j != 0:
                        bjortho = self.gramschmidt(
                            bvector, bj, self.nbvector, "bvector"
                        )
                        if bjortho is not None:
                            bvector = self.push_vector(
                                bvector, bjortho, "bvector", self.nbvector
                            )
                            self.nbvector += 1
                    else:
                        bvector = self.push_vector(
                            bvector, bj, "bvector", self.nbvector
                        )
                        self.nbvector += 1
                    bj = None
                    evecj = None
            #
            # expand search space with correction vectors
            #
            for j in range(0, self.nroots):
                newv = self.lf.create_one_index(dim)
                drk = self.read_from_disk(deltak, "residualortho", j)
                newv.assign(drk)
                #
                # orthogonalize correction vectors against bvectors
                #
                deltakortho = self.gramschmidt(
                    bvector, newv, self.nbvector, "bvector"
                )
                if log.do_high:
                    try:
                        log(
                            f"New b vector for root {j} with norm: {deltakortho.norm()}"
                        )
                    except Exception:
                        log(f"b vector neglected for root {j}.")
                if deltakortho is not None:
                    # append new vector
                    bvector = self.push_vector(
                        bvector, deltakortho, "bvector", self.nbvector
                    )
                    self.nbvector += 1
                deltakortho = None
                drk = None
            # free memory
            newv = None
            #
            # calculate convergence thresholds
            #
            de = abs(theta[: self.nroots].real - theta_old.real)
            if log.do_medium:
                log(
                    f"{'iter':>6s} {'vector':>7s} {'|HR-ER|':>10s} "
                    f"{'E(new)-E(old)':>19s} {'E_excitation':>14s}"
                )
                for i in range(self.nroots):
                    if i == 0 and self.skipgs:
                        continue
                    if i in converged:
                        if abs(de[i]) > self.tol or rknorm[i] > self.tolv:
                            log(
                                f"{iter_:>5d} {i:>6d}   {rknorm[i]:> .6e}    "
                                f"{theta[i] - theta_old[i]:> .6e}  {theta[i]:> .6e}  "
                            )
                            converged.remove(i)
                        continue
                    if abs(de[i]) < self.tol and rknorm[i] < self.tolv:
                        log(
                            f"{iter_:>5d} {i:>6d}   {rknorm[i]:> .6e}    "
                            f"{theta[i] - theta_old[i]:> .6e}  {theta[i]:> .6e}  "
                            f"converged"
                        )
                        if i not in converged:
                            converged.append(i)
                    elif i not in converged:
                        log(
                            f"{iter_:>5d} {i:>6d}   {rknorm[i]:> .6e}    "
                            f"{theta[i] - theta_old[i]:> .6e}  {theta[i]:> .6e}  "
                        )
                log(" ")
            theta_old = theta[: self.nroots].real
            #
            # check for convergence
            #
            if (de < self.tol).all() and (rknorm < self.tolv).all():
                if log.do_medium:
                    log.hline("~")
                    log("   Davidson converged")
                    log.hline("=")
                return theta.real, evec
            iter_ += 1
            if iter_ >= self.maxiter:
                if log.do_medium:
                    log.hline("~")
                    log("   Davidson NOT converged")
                    log.hline("=")
                return theta.real, evec
