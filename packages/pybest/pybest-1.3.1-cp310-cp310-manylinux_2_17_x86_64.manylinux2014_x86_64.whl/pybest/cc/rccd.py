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
"""Restricted Coupled Cluster Doubles Class

   Variables used in this module:
    :nocc:       total number of occupied orbitals
    :nvirt:      total number of virtual orbitals
    :ncore:      number of frozen core orbitals in the principle configuration
    :nacto:      number of active occupied orbitals
    :nactv:      number of active virtual orbitals
    :energy:     the CCD energy, dictionary containing different contributions
    :amplitudes: the CCD amplitudes (dict), contains only t_2
    :t_2:        the double-excitation amplitudes

    Indexing convention:
    :o:        matrix block corresponding to occupied orbitals of principle
               configuration
    :v:        matrix block corresponding to virtual orbitals of principle
               configuration

    EXAMPLE APPLICATION (see pybest/data/examples/rccsd for complete code)

    #  1) Orbitals and reference energy are given explicitly
    solver = RCCD(linalg_factory, occupation_model)
    result = solver(AO_one_body_ham, AO_two_body_ham, orbitals, eref=hf_energy)

    #  2) Orbitals and reference energy come from the RHF solver
    rhf_solver = RHF(linalg_factory, occupation_model)
    rhf_data = hf(AO_one_body_ham, AO_two_body_ham, initial_orbitals)
    solver = RCCD(linalg_factory, occupation_model)
    result = solver(AO_one_body_ham, AO_two_body_ham, rhf_data)
"""

import gc
from functools import partial

import numpy as np

from pybest.auxmat import get_fock_matrix
from pybest.exceptions import ArgumentError
from pybest.io.iodata import IOData
from pybest.linalg import CholeskyFourIndex, DenseFourIndex, DenseOneIndex
from pybest.log import log, timer
from pybest.pt.perturbation_utils import get_epsilon

from .rcc import RCC


class RCCD(RCC):
    """Restricted Coupled Cluster Doubles
    for arbitrary single-determinant reference function.
    """

    acronym = "RCCD"
    long_name = "Restricted Coupled Cluster Doubles"
    reference = "any single-reference wavefunction"
    cluster_operator = "T2"

    @property
    def t_2(self):
        """Doubles amplitudes - DenseTwoIndex instance"""
        return self._t_2

    @t_2.setter
    def t_2(self, t_2):
        if isinstance(t_2, DenseFourIndex):
            self._t_2 = t_2
        else:
            raise TypeError("t_2 must be DenseFourIndex instance.")

    @property
    def l_2(self):
        """Doubles Lambda amplitudes - DenseTwoIndex instance"""
        return self._l_2

    @l_2.setter
    def l_2(self, l_2):
        if isinstance(l_2, DenseFourIndex):
            self._l_2 = l_2
        else:
            raise TypeError("l_2 must be DenseFourIndex instance.")

    @property
    def amplitudes(self):
        """Dictionary of amplitudes."""
        return {"t_2": self.t_2}

    @amplitudes.setter
    def amplitudes(self, amplitudes):
        if isinstance(amplitudes, dict):
            iterable = amplitudes.values()
        elif isinstance(amplitudes, (list, tuple)):
            iterable = amplitudes
        for value in iterable:
            if isinstance(value, DenseFourIndex):
                t_2 = value
        self.t_2 = t_2

    def get_max_amplitudes(self, threshold=0.01, limit=None):
        """Returns a dictionary with list of amplitudes and their indices."""
        t_2 = self.t_2.get_max_values(absolute=True)
        t_2.sort(key=lambda x: abs(x[1]), reverse=True)
        if limit is None:
            limit = sum(abs(t[1]) > abs(threshold) for t in t_2)
        max_t2 = []
        for index, value in t_2[:limit]:
            i, a, j, b = index
            i += self.ncore + 1
            j += self.ncore + 1
            a += self.nocc + 1
            b += self.nocc + 1
            max_t2.append(((i, a, j, b), value))
        return {"t_2": max_t2}

    @property
    def l_amplitudes(self):
        """Dictionary of amplitudes."""
        return {"l_2": self.l_2}

    @l_amplitudes.setter
    def l_amplitudes(self, amplitudes):
        if isinstance(amplitudes, dict):
            iterable = amplitudes.values()
        elif isinstance(amplitudes, (list, tuple)):
            iterable = amplitudes
        for value in iterable:
            if isinstance(value, DenseFourIndex):
                l_2 = value
            else:
                raise TypeError("Value must be a DenseFourIndex instance.")
        self.l_2 = l_2

    def set_hamiltonian(self, ham_1_ao, ham_2_ao, mos):
        """Saves Hamiltonian terms in cache.

        Arguments:

        one_body_ham : DenseTwoIndex
            Sum of one-body elements of the electronic Hamiltonian in AO
            basis, e.g. kinetic energy, nuclei--electron attraction energy

        two_body_ham : DenseFourIndex
            Sum of two-body elements of the electronic Hamiltonian in AO
            basis, e.g. electron repulsion integrals.

        mos : DenseOrbital
            Molecular orbitals, e.g. RHF orbitals or pCCD orbitals.
        """
        # Transform integrals
        ham_1, ham_2 = self.transform_integrals(ham_1_ao, ham_2_ao, mos)
        ham_2_ao.dump_array(ham_2_ao.label)
        fock = self.lf.create_two_index(self.nacto + self.nactv)
        fock = get_fock_matrix(fock, ham_1, ham_2, self.nacto)

        self.clear_cache()

        def alloc(string, arr):
            "Determines alloc argument for cache.load method."
            # We keep one whole CholeskyFourIndex to rule them all.
            # Non-redundant blocks are accessed as views.
            if isinstance(arr, CholeskyFourIndex):
                return (partial(arr.view, **self.get_range(string)),)
            # But we store only non-redundant blocks of DenseFourIndex
            return (partial(arr.copy, **self.get_range(string)),)

        # Blocks of Fock matrix
        for block in ["oo", "vv"]:
            self.init_cache(f"fock_{block}", alloc=alloc(block, fock))
        # Blocks of two-body Hamiltonian
        for block in ["oooo", "ovov", "oovv", "vvvv"]:
            self.init_cache(f"eri_{block}", alloc=alloc(block, ham_2))

        # Exchange terms from CC equations
        def alloc_exc(string):
            "Determines alloc argument for cache.load method."
            kwargs = self.get_range(string)
            return (partial(ham_2.contract, "abcd->abcd", **kwargs),)

        # exchange_oovv = <ijka> - 2 <ikja>
        mat = self.init_cache("exchange_oovv", alloc=alloc_exc("oovv"))
        mat.iadd_transpose((0, 1, 3, 2), factor=-2)
        if self.dump_cache:
            self.cache.dump("exchange_oovv")

        ham_2.__del__()
        gc.collect()

    def set_dm(self, *args):
        """Determine all supported RDMs and put them into the cache."""
        raise NotImplementedError

    def generate_random_guess(self):
        """Generate random guess for t_1 ov matrix and t_2 ovov matrix."""
        t_2 = DenseFourIndex(self.nacto, self.nactv, self.nacto, self.nactv)
        t_2.randomize()
        t_2.iscale(-1.0 / (self.nocc * self.nvirt))
        t_2.iadd_transpose((2, 3, 0, 1))
        return {"t_2": t_2}

    def generate_constant_guess(self, constant):
        """Generate constant guess for t_1 ov matrix and t_2 ovov matrix."""
        t_2 = DenseFourIndex(self.nacto, self.nactv, self.nacto, self.nactv)
        t_2.assign(constant)
        return {"t_2": t_2}

    def read_guess_from_file(self):
        """Reads guess from file self.initguess."""
        data = IOData.from_file(self.initguess)
        return self.get_amplitudes_from_iodata(data)

    def get_amplitudes_from_dict(self, dictionary):
        """Gets amplitudes from dictionary. Amplitudes are recognized by key:
        't_2' or 'c_2'."""
        if "t_2" in dictionary:
            return {"t_2": dictionary["t_2"]}
        if "c_2" in dictionary:
            return {"t_2": dictionary["c_2"]}
        raise ArgumentError("Initial amplitudes not found.")

    def get_amplitudes_from_iodata(self, iodata):
        """Gets amplitudes from IOData. Amplitudes are recognized by attribute
        name: 't_2' or 'c_2'."""
        if hasattr(iodata, "amplitudes"):
            return self.get_amplitudes_from_dict(iodata.amplitudes)
        if hasattr(iodata, "t_2"):
            return {"t_2": iodata.t_2}
        if hasattr(iodata, "c_2"):
            return {"t_2": iodata.c_2}
        raise ArgumentError("Initial amplitudes not found.")

    @timer.with_section("RCCD: MP2 guess")
    def generate_mp2_guess(self):
        """Generates amplitudes from MP2 calculations."""
        if log.do_medium:
            log("Performing an MP2 calculations for an initial guess.")
        no = self.occ_model.nacto[0]
        nv = self.occ_model.nactv[0]
        # Get effective Hamiltonian
        try:
            eri_oovv = self.from_cache("eri_oovv")
            fi = self.from_cache("fock_oo").copy_diagonal()
            fa = self.from_cache("fock_vv").copy_diagonal()
        except KeyError:
            eri_oovv = self.from_cache("goovv")
            fi = self.from_cache("fock").copy_diagonal(end=no)
            fa = self.from_cache("fock").copy_diagonal(begin=no)
        # Get eps[ia,jb] (fa + fb - fi - fj)
        # Requires us to store dense ovov object
        # NOTE: this part of the code can be moved to C++
        eps = get_epsilon(self.denself, [fi, fa], singles=False, doubles=True)
        # Determine amplitudes
        t_2 = eri_oovv.contract("abcd->acbd")
        t_2.array[:] /= eps.array.reshape(no, nv, no, nv)
        # free memory
        eps.__del__()
        gc.collect()
        if log.do_medium:
            log("Resuming CC calculation.")
            log.hline("~")
        return {"t_2": t_2}

    def calculate_energy(self, e_ref, e_core=0.0, **amplitudes):
        """Returns a dictionary of energies:
        e_tot: total energy,
        e_corr: correlation energy,
        e_ref: energy of reference determinant,
        e_corr_s: part of correlation energy,
        e_corr_d: part of correlation energy.
        """
        energy = {
            "e_ref": e_ref,
            "e_tot": 0.0,
            "e_corr": 0.0,
            "e_corr_s": 0.0,
            "e_corr_d": 0.0,
        }

        try:
            t_2 = amplitudes.get("t_2", self.t_2)
        except AttributeError:
            t_2 = amplitudes.get("t_2")
        exchange_oovv = self.from_cache("exchange_oovv")
        energy["e_corr_d"] = -exchange_oovv.contract("abcd,adbc", t_2)
        if self.dump_cache:
            self.cache.dump("exchange_oovv")
        energy["e_corr"] = energy["e_corr_d"]
        energy["e_tot"] = e_ref + e_core + energy["e_corr"]
        return energy

    def print_energy_details(self):
        """Prints energy contributions."""
        log(f"{'Doubles':21} {self.energy['e_corr_d']:16.8f} a.u.")

    def print_amplitudes(self, threshold=1e-2, limit=None):
        """Prints highest amplitudes."""
        amplitudes = self.get_max_amplitudes(threshold=threshold, limit=limit)
        max_double = amplitudes["t_2"]

        if max_double:
            log("Leading double excitation amplitudes")
            log(" ")
            log(f"{'amplitude':>13}{'i':>4}{'j':>4}  ->{'a':>4}{'b':>4}")
            log(" ")

            for index, value in max_double:
                i, a, j, b = index
                log(f"{value:13.6f}{i:4}{j:4}  ->{a:4}{b:4}")
            log.hline("-")

    def ravel(self, amplitudes):
        """Return a one-dimensional numpy.ndarray or a DenseOneIndex containing
        flatten data from input operands. Note that operand arrays stored in
        the `amplitudes` argument are deleted.

        Arguments:
            t_2 : DenseFourIndex

        Returns:
            vector/vector._array : DenseOneIndex/numpy.ndarray
                - t_2 [:]
        """
        t_2 = None
        for value in amplitudes.values():
            if isinstance(value, DenseFourIndex):
                t_2 = value
        if t_2 is None:
            raise ArgumentError("T_2 amplitudes not found!")
        t_2_triu = t_2.get_triu()
        vector = DenseOneIndex(len(t_2_triu))
        vector.assign(t_2_triu)
        # delete arrays
        t_2.__del__()
        if self.solver in ["pbqn"]:
            return vector
        return vector.array

    def unravel(self, vector):
        """Returns DenseFourIndex instance filled out with data from input
        flat_ndarray.

        Arguments:
            vector : DenseOneIndex or numpy.array. If DenseOneIndex is passed,
                     its elements get deleted after the operation is done
        """
        occ = self.nacto
        vir = self.nactv
        t_2 = DenseFourIndex(occ, vir, occ, vir)
        t_2.assign_triu(vector)
        t_p = t_2.contract("abab->ab")
        t_2.iadd_transpose((2, 3, 0, 1))
        ind1, ind2 = np.indices((occ, vir))
        t_2.assign(t_p, [ind1, ind2, ind1, ind2])
        # clear memory
        if isinstance(vector, DenseOneIndex):
            vector.__del__()
        gc.collect()
        return {"t_2": t_2}

    @timer.with_section("VecFct RCCD")
    def vfunction(self, vector):
        """Shorter version of residual vector to accelerate solving."""
        amplitudes = self.unravel(vector)
        return self.ravel(self.cc_residual_vector(amplitudes))

    def cc_residual_vector(self, amplitudes):
        """Residual vector of Coupled Cluster equations. Needs to be zero.

        Arguments:

            amplitudes : numpy.ndarray
                vector containing double cluster amplitudes.

        Abbreviations:

        * o - number of active occupied orbitals
        * v - number of active virtual orbitals
        * t_2 - current solution for CC amplitudes
        * out_d - vector function
        * mat_ov - auxiliary DenseTwoIndex (ov is occupied x virtual)
        * e_oovv - four index integrals with exchange part
        """
        t_2 = amplitudes["t_2"]
        occ = self.nacto
        vir = self.nactv

        # Fock matrix, ERI, exchange terms
        fock_oo = self.from_cache("fock_oo")
        fock_vv = self.from_cache("fock_vv")
        eri_oooo = self.from_cache("eri_oooo")
        eri_oovv = self.from_cache("eri_oovv")
        eri_ovov = self.from_cache("eri_ovov")
        eri_vvvv = self.from_cache("eri_vvvv")

        ## DOUBLEs ##

        # Create vector function
        out_d = DenseFourIndex(occ, vir, occ, vir)
        out_d.clear()
        to_d = {"out": out_d, "clear": False}
        # 3 intermediate matrix X_il = -f_il + (<kl|cd> - 2 <kl|dc>) t_ik^cd
        mat_oo = fock_oo.copy()
        mat_oo.iscale(-1)
        to_o = {"out": mat_oo, "clear": False}
        exchange_oovv = self.from_cache("exchange_oovv")
        exchange_oovv.contract("abcd,ecad->eb", t_2, **to_o)
        # 12.0 X_il t_jl^ba
        t_2.contract("abcd,ec->edab", mat_oo, **to_d)
        mat_oo.__del__()
        # 4 intermediate matrix Y_ac = f_ac + (<kl|cd> - 2 <kl|dc>) t_lk^ad
        mat_vv = fock_vv.copy()
        to_v = {"out": mat_vv, "clear": False}
        exchange_oovv.contract("abcd,bead->ec", t_2, **to_v)
        # 12.1 Y_ac t_ji^bc
        t_2.contract("abcd,ed->ceab", mat_vv, **to_d)
        mat_vv.__del__()
        #
        u_ovov = DenseFourIndex(occ, vir, occ, vir)
        to_u = {"out": u_ovov, "clear": False}
        # 11.3 U_iakc += (<kl|dc> -2<kl|cd>) (T_li^ad - t_il^ad)
        exchange_oovv.contract("abcd,ecbf->efad", t_2, **to_u)
        exchange_oovv.contract("abcd,efbc->efad", t_2, **to_u, factor=-1.0)
        if self.dump_cache:
            self.cache.dump("exchange_oovv")
        # 11.0 U_iakc -= <ia|kc>
        eri_ovov.contract("abcd->abcd", u_ovov, factor=-1)
        # 11.1 U_iakc += 2 <ik|ac>
        eri_oovv.contract("abcd->acbd", out=u_ovov, factor=2)
        # 12.3  U_iakc t_jk^bc
        u_ovov.contract("abcd,efcd->abef", t_2, **to_d)
        u_ovov.__del__()
        # 13.1 -<ik|ac> T_kj^bc
        eri_oovv.contract("abcd,befd->acfe", t_2, out_d, factor=-1)
        # 13.2 -<ib|kc> T_kj^ac
        eri_ovov.contract("abcd,cefd->aefb", t_2, out_d, factor=-1)
        # Permutation
        out_d.iadd_transpose((2, 3, 0, 1))
        # 14.0 <kl|cd> t_kj^bc t_li^ad
        intmat = DenseFourIndex(occ, vir, occ, vir)
        eri_oovv.contract("abcd,befd->feac", t_2, out=intmat, clear=True)
        intmat.contract("abcd,cefd->abfe", t_2, **to_d)
        # 14.1 <kl|cd> t_lj^ac t_ki^bd
        eri_oovv.contract("abcd,edaf->efbc", t_2, out=intmat, clear=True)
        intmat.contract("abcd,cefd->aefb", t_2, **to_d)
        intmat.__del__()
        # 14.2 and 14.5 (<kl|cd> T_ij^cd + <ij|kl>) T_kl^ab
        intmat = DenseFourIndex(occ, occ, occ, occ)
        eri_oovv.contract("abcd,ecfd->efab", t_2, out=intmat)
        eri_oooo.contract("abcd->abcd", out=intmat)
        intmat.contract("abcd,cedf->aebf", t_2, **to_d)
        intmat.__del__()
        # 14.3  <ij|ab>
        eri_oovv.contract("abcd->acbd", out=out_d)
        # 14.4 bottleneck contraction  <ab|cd> T_ij^cd
        eri_vvvv.contract("abcd,ecfd->eafb", t_2, out=out_d)

        return {"out_d": out_d}

    def vfunction_l(self, vector):
        """Shorter version of residual vector to accelerate solving."""
        raise NotImplementedError

    def l_residual_vector(self, amplitudes):
        """Residual vector of Lambda equations. Needs to be zero.

        Arguments:

            amplitudes : numpy.ndarray
                vector containing double Lambda amplitudes.

        """
        raise NotImplementedError

    @timer.with_section("Jacobian RCCD")
    def jacobian(self, amplitudes, *args):
        """Jacobian approximation to find coupled cluster doubles amplitudes.

        **Arguments:**

        amplitudes
             Cluster amplitudes.

        args
             All function arguments needed to calculate the vector
        """
        if log.do_medium:
            log("Computing Jacobian approximation for Quasi-Newton solver.")
        # We do not support more advanced (amplitude-free) Jacobians, yet
        # 1: only Fock matrix elements (f_i - f_a)
        # 2: additional ERI terms
        if self.jacobian_approximation >= 2:
            raise NotImplementedError
        #
        # Get auxiliary matrices and other intermediates
        #
        nov = self._nov
        fi = self.from_cache("fock_oo").copy_diagonal()
        fa = self.from_cache("fock_vv").copy_diagonal()
        unknowns = nov * (nov + 1) // 2
        #
        # Output
        #
        out = self.lf.create_one_index(unknowns)
        #
        # Approximate Jacobian
        #
        # The function returns fi-fa and fi-fa+fj-fb
        fiajb = get_epsilon(
            self.denself, [fi, fa], singles=False, shift=[1e-12, 1e-12]
        )
        fiajb.iscale(-1.0)
        # Assign Jacobian for doubles (only unique elements)
        out.assign(fiajb.get_triu())

        return out
