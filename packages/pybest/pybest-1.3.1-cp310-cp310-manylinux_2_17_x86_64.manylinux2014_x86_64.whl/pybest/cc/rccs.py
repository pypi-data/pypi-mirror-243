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
"""Restricted Coupled Cluster Singles Class

   Variables used in this module:
    :nocc:       total number of occupied orbitals
    :nvirt:      total number of virtual orbitals
    :ncore:      number of frozen core orbitals in the principle configuration
    :nacto:      number of active occupied orbitals
    :nactv:      number of active virtual orbitals
    :energy:     the CCS energy, dictionary containing different contributions
    :amplitudes: the CCS amplitudes (dict), contains t_1
    :t_1:        the single-excitation amplitudes

    Indexing convention:
    :o:        matrix block corresponding to occupied orbitals of principle
               configuration
    :v:        matrix block corresponding to virtual orbitals of principle
               configuration

    EXAMPLE APPLICATION

    cc_solver = RCCS(linalg_factory, occupation_model)
    cc_result = cc_solver(
        AO_one_body_ham, AO_two_body_ham, hf_io_data_container
    )
"""
import gc
from functools import partial
from math import sqrt

from pybest.auxmat import get_fock_matrix
from pybest.exceptions import ArgumentError
from pybest.io.iodata import IOData
from pybest.linalg import CholeskyFourIndex, DenseOneIndex, DenseTwoIndex
from pybest.log import log, timer
from pybest.pt.perturbation_utils import get_epsilon
from pybest.utils import unmask

from .rcc import RCC


class RCCS(RCC):
    """Restricted Coupled Cluster Singles for arbitrary single-determinant
    reference function.
    """

    acronym = "RCCS"
    long_name = "Restricted Coupled Cluster Singles"
    reference = "any single-reference wavefunction"
    cluster_operator = "T1"
    singles = True
    pairs = False
    doubles = False

    @property
    def t_1(self):
        """Single excitation cluster amplitudes."""
        return self._t_1

    @t_1.setter
    def t_1(self, t_1):
        if isinstance(t_1, DenseTwoIndex):
            self._t_1 = t_1
        else:
            raise TypeError("t_1 must be DenseTwoIndex instance.")

    @property
    def l_1(self):
        """Single de-excitation lambda amplitudes."""
        return self._l_1

    @l_1.setter
    def l_1(self, l_1):
        if isinstance(l_1, DenseTwoIndex):
            self._l_1 = l_1
        else:
            raise TypeError("l_1 must be DenseTwoIndex instance.")

    @property
    def amplitudes(self):
        """Dictionary of amplitudes."""
        return {"t_1": self.t_1}

    @amplitudes.setter
    def amplitudes(self, amplitudes):
        if isinstance(amplitudes, dict):
            iterable = amplitudes.values()
        else:
            iterable = amplitudes
        for value in iterable:
            if isinstance(value, DenseTwoIndex):
                self.t_1 = value

    def get_max_amplitudes(self, threshold=0.01, limit=None):
        """Returns a dictionary with list of amplitudes and their indices."""
        # Single-excitation amplitudes
        t_1 = self.t_1.get_max_values(absolute=True)
        t_1.sort(key=lambda x: abs(x[1]), reverse=True)
        if limit is None or limit > self.nacto * self.nactv:
            limit_1 = sum(abs(t[1]) > abs(threshold) for t in t_1)
        max_t1 = []
        for index, value in t_1[:limit_1]:
            i, a = index
            i += self.ncore + 1
            a += self.nocc + 1
            max_t1.append(((i, a), value))
        return {"t_1": max_t1}

    @property
    def l_amplitudes(self):
        """Dictionary of amplitudes."""
        return {"l_1": self.l_1}

    @l_amplitudes.setter
    def l_amplitudes(self, amplitudes):
        if isinstance(amplitudes, dict):
            iterable = amplitudes.values()
        else:
            iterable = amplitudes
        for value in iterable:
            if isinstance(value, DenseTwoIndex):
                self.l_1 = value

    @property
    def freeze(self):
        """The freezed coupled cluster amplitudes"""
        return self._freeze

    @freeze.setter
    def freeze(self, args):
        self._freeze = args

    def read_input(self, *args, **kwargs):
        """Looks for Hamiltonian terms, orbitals, and overlap."""
        one_mo, two_mo, orb = RCC.read_input(self, *args, **kwargs)
        #
        # Overwrite defaults
        #
        self.initguess = kwargs.get("initguess", "mp2")
        self.freeze = kwargs.get("freeze", [])
        # Choose optimal internal contraction schemes (select=None)
        self.tco = kwargs.get("tco", None)
        self.e_core = unmask("e_core", *args, **kwargs)

        return one_mo, two_mo, orb

    def set_hamiltonian(self, ham_1_ao, ham_2_ao, mos):
        """Saves Hamiltonian terms in cache.

        Arguments:

        ham_1_ao : TwoIndex
            Sum of one-body elements of the electronic Hamiltonian in AO
            basis, e.g. kinetic energy, nuclei--electron attraction energy

        ham_2_ao : FourIndex
            Sum of two-body elements of the electronic Hamiltonian in AO
            basis, e.g. electron repulsion integrals.

        mos : Orbital
            Molecular orbitals, e.g. RHF orbitals or pCCD orbitals.
        """
        #
        # Transform integrals
        #
        mo1, mo2 = self.transform_integrals(ham_1_ao, ham_2_ao, mos)
        ham_2_ao.dump_array(ham_2_ao.label)
        #
        # Clear cache
        #
        self.clear_cache()
        #
        # Update aux matrices
        #
        self.update_hamiltonian(mo1, mo2)
        #
        # Clean up (should get deleted anyways)
        #
        mo2.__del__()

    def set_dm(self, *args):
        """Determine all supported RDMs and put them into the cache."""
        raise NotImplementedError

    @timer.with_section("Hamiltonian CCS")
    def update_hamiltonian(self, mo1, mo2):
        """Derive all auxiliary matrices.

        **Arguments:**

        mo1, mo2
             one- and two-electron integrals to be sorted.

        cia
             The geminal coefficients. A TwoIndex instance
        """
        if log.do_medium:
            log("Computing auxiliary matrices and effective Hamiltonian.")
        #
        # Get ranges for contract
        #
        occ = self.nacto
        act = self.nact
        #
        # Inactive Fock matrix
        #
        fock = self.init_cache("fock", act, act)
        get_fock_matrix(fock, mo1, mo2, occ)

        #
        # 4-Index slices of ERI
        #
        def alloc(arr, block):
            "Determines alloc keyword argument for init_cache method."
            # We keep one whole CholeskyFourIndex to rule them all.
            # Non-redundant blocks are accessed as views.
            if isinstance(arr, CholeskyFourIndex):
                return (partial(arr.view, **self.get_range(block)),)
            # But we store only non-redundant blocks of DenseFourIndex
            return (partial(arr.copy, **self.get_range(block)),)

        #
        # Get blocks
        #
        slices = ["ovvo", "ovov", "oooo", "vooo", "ovvv"]
        for slice_ in slices:
            self.init_cache(f"g{slice_}", alloc=alloc(mo2, slice_))

    @staticmethod
    def compute_t1_diagnostic(t_1, nocc):
        """Computes T1 diagnostic = |t_1| / sqrt(2 * nocc)."""
        return sqrt(t_1.contract("ab,ab", t_1)) / sqrt(2 * nocc)

    def generate_random_single_amplitudes(self):
        """Generate random guess for t_1 ov matrix."""
        t_1 = DenseTwoIndex(self.nacto, self.nactv)
        t_1.randomize()
        t_1.iscale(-1.0 / self._nov)
        return t_1

    def generate_random_guess(self):
        """Generate random guess for t_1 ov matrix."""
        t_1 = self.generate_random_single_amplitudes()
        return {"t_1": t_1}

    def generate_constant_guess(self, constant):
        """Generate constant guess for t_1 ov matrix."""
        t_1 = DenseTwoIndex(self.nacto, self.nactv)
        t_1.assign(constant)
        return {"t_1": t_1}

    def read_guess_from_file(self):
        """Reads guess from file self.initguess."""
        data = IOData.from_file(self.initguess)
        return self.get_amplitudes_from_iodata(data)

    def get_amplitudes_from_dict(self, dictionary):
        """Reads available amplitudes from dict instance. Generates random
        amplitudes for missing terms.
        Amplitudes in dict are recognized by key:
         * 't_1' or 'c_2' for single excitation amplitudes (DenseTwoIndex).
        """
        t_1 = None
        if "t_1" in dictionary:
            t_1 = dictionary["t_1"]
        elif "c_1" in dictionary:
            t_1 = dictionary["c_1"]
        if t_1 is None:
            raise ArgumentError("Initial amplitudes not found.")
        return {"t_1": t_1}

    def get_amplitudes_from_iodata(self, iodata):
        """Reads available amplitudes from IOData instance. Generates random
        amplitudes for missing terms.
        Amplitudes in iodata are recognized by attribute name:
         * 't_2' or 'c_2' for double excitatation amplitudes (DenseFourIndex),
         * 't_1' or 'c_2' for single excitation amplitudes (DenseTwoIndex).
        """
        t_1 = None
        if hasattr(iodata, "amplitudes"):
            return self.get_amplitudes_from_dict(iodata.amplitudes)
        if hasattr(iodata, "t_1"):
            t_1 = iodata.t_1
        elif hasattr(iodata, "c_1"):
            t_1 = iodata.c_1
        if t_1 is None:
            raise ArgumentError("Initial amplitudes not found.")
        return {"t_1": t_1}

    @timer.with_section("RCCS: MP2 guess")
    def generate_mp2_guess(self):
        """Generate the MP2 initial guess for CC amplitudes"""
        if log.do_medium:
            log("Performing an MP2 calculations for an initial guess.")
        no = self.occ_model.nacto[0]
        # Get Fock matrix
        t_1 = self.from_cache("fock").copy(end0=no, begin1=no)
        # get slices
        fi = self.from_cache("fock").copy_diagonal(end=no)
        fa = self.from_cache("fock").copy_diagonal(begin=no)
        # get eps[ia] (fa - fi)
        eps_1 = get_epsilon(
            self.denself, [fi, fa], singles=True, doubles=False
        )
        # determine amplitudes
        t_1.idivide(eps_1, factor=-1.0)
        if log.do_medium:
            log("Resuming CC calculation.")
            log.hline("~")
        return {"t_1": t_1}

    def calculate_energy(self, e_ref, e_core=0.0, **amplitudes):
        """Returns a dictionary of energies:
        e_tot: total energy,
        e_corr: correlation energy,
        e_ref: energy of reference function,
        e_corr_s: part of correlation energy,
        """
        energy = {
            "e_ref": e_ref,
            "e_tot": 0.0,
            "e_corr": 0.0,
            "e_corr_s": 0.0,
            "e_corr_d": 0.0,
        }
        #
        # Get amplitudes and integrals
        #
        fock = self.from_cache("fock")
        govvo = self.from_cache("govvo")
        try:
            t_1 = amplitudes.get("t_1", self.t_1)
        except AttributeError:
            t_1 = amplitudes.get("t_1")
        #
        # E_singles
        # 2 F_md t_md
        ov2 = self.get_range("ov", offset=2)
        e_1 = 2.0 * t_1.contract("ab,ab", fock, **ov2)
        # tia tjb L_ijab
        tmp_ov = self.lf.create_two_index(self.nacto, self.nactv)
        govvo.contract("abcd,ac->db", t_1, tmp_ov, factor=2.0)
        govvo.contract("abcd,ab->dc", t_1, tmp_ov, factor=-1.0)
        e_11 = tmp_ov.contract("ab,ab", t_1)
        #
        energy["e_corr_s"] = e_1 + e_11
        energy["e_corr"] = energy["e_corr_s"]

        energy["e_tot"] = e_ref + e_core + energy["e_corr"]
        return energy

    def print_energy_details(self):
        """Prints energy contributions."""
        log(f"{'Singles':21} {self.energy['e_corr_s']:16.8f} a.u.")

    def print_amplitudes(self, threshold=1e-4, limit=None):
        """Prints highest amplitudes."""
        occ = self.nacto
        amplitudes = self.get_max_amplitudes(threshold=threshold, limit=limit)
        max_single = amplitudes["t_1"]

        if max_single:
            log("\nLeading single excitation amplitudes\n")
            log(f"{'amplitude':>13}{'i':>4}  ->{'a':>4}\n")
            for index, value in max_single:
                i, a = index
                log(f"{value:13.6f}{i:>4}  ->{a:4}")
            log.hline("-")
        t1_diagnostic = self.compute_t1_diagnostic(self.t_1, occ)
        log(f"T1 diagnostic: {t1_diagnostic:4.6f}")

    def ravel(self, amplitudes):
        """Return a one-dimensional numpy.ndarray or a DenseOneIndex containing
        flatten data from input operands. Note that operand arrays stored in
        the `amplitudes` argument are deleted.

        Arguments:
            amplitudes : dict
                contains:
                - t_1 : DenseTwoIndex

         Returns:
            vector/vector._array : DenseOneIndex/numpy.ndarray
                - t_1 [:]

        """
        t_1 = None
        for value in amplitudes.values():
            if isinstance(value, DenseTwoIndex):
                t_1 = value
        if t_1 is None:
            raise ArgumentError("DenseTwoIndex object not found!")
        vector = DenseOneIndex(self._nov)
        vector.assign(t_1.array.ravel())
        if self.solver in ["pbqn"]:
            return vector
        return vector.array

    def unravel(self, vector):
        """Returns DenseTwoIndex and DenseFourIndex instances filled out with
        data from input flat_ndarray.

        Arguments:
            vector : DenseOneIndex or numpy.array. If DenseOneIndex is passed,
                     its elements get deleted after the operation is done
        """
        occ = self.nacto
        vir = self.nactv
        t_1 = DenseTwoIndex(occ, vir)
        t_1.assign(vector)
        # clear memory
        if isinstance(vector, DenseOneIndex):
            vector.__del__()
        gc.collect()
        return {"t_1": t_1}

    @timer.with_section("VecFct RCCS")
    def vfunction(self, vector):
        """1D vector function of CC residual vector (numpy.ndarray)."""
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
        * t_1 - current solution for CC amplitudes
        * out_s - vector function
        """
        t_1 = amplitudes["t_1"]
        #
        # Get ranges
        #
        oo2 = self.get_range("oo", offset=2)
        vv2 = self.get_range("vv", offset=2)
        ov2 = self.get_range("ov", offset=2)
        vo2 = self.get_range("vo", offset=2)
        occ = self.nacto
        vir = self.nactv
        #
        # Get auxiliary matrices
        #
        fock = self.from_cache("fock")
        govvo = self.from_cache("govvo")
        govov = self.from_cache("govov")
        gvooo = self.from_cache("gvooo")
        govvv = self.from_cache("govvv")
        #
        # temporary storage
        #
        tmp_vv = self.lf.create_two_index(vir, vir)
        tmp_oo = self.lf.create_two_index(occ, occ)
        tmp_ov = self.lf.create_two_index(occ, vir)
        to_oo = {"out": tmp_oo, "select": self.tco}
        to_ov = {"out": tmp_ov, "select": self.tco}
        to_vv = {"out": tmp_vv, "select": self.tco}
        #
        # singles
        #
        out_s = t_1.new()
        to_s = {"out": out_s, "clear": False, "select": self.tco}
        #
        # t_kc L<ic|ak> (s4)
        #
        govvo.contract("abcd,db->ac", t_1, **to_s, factor=2.0)
        govov.contract("abcd,cb->ad", t_1, **to_s, factor=-1.0)
        #
        # Fac tic; Fki tka (s2,3)
        #
        t_1.contract("ab,bc->ac", fock, **to_s, **vv2)
        t_1.contract("ab,ac->cb", fock, **to_s, factor=-1.0, **oo2)
        #
        # F_ia (s1)
        #
        out_s.iadd(fock, 1.0, **ov2)
        #
        # quadratic terms
        #
        # tic Fck tka = fik tka
        t_1.contract("ab,bc->ac", fock, **to_oo, clear=True, **vo2)
        tmp_oo.contract("ab,bc->ac", t_1, **to_s, factor=-1.0)
        #
        # <ci||lk> tlc tka = gik tka
        #
        gvooo.contract("abcd,ca->bd", t_1, **to_oo, factor=2.0, clear=True)
        gvooo.contract("abcd,da->bc", t_1, **to_oo, factor=-1.0)
        tmp_oo.contract("ab,bc->ac", t_1, **to_s, factor=-1.0)
        #
        # <ka||cd> tkc tid = tid gad
        #
        govvv.contract("abcd,ac->bd", t_1, **to_vv, factor=2.0, clear=True)
        govvv.contract("abcd,ad->bc", t_1, **to_vv, factor=-1.0)
        t_1.contract("ab,cb->ac", tmp_vv, **to_s)
        #
        # cubic terms
        #
        # <kl||cd> tld tic tka = tic Lkc tka = tLik tka
        govvo.contract("abcd,db->ac", t_1, **to_ov, factor=2.0, clear=True)
        govvo.contract("abcd,dc->ab", t_1, **to_ov, factor=-1.0)
        t_1.contract("ab,cb->ac", tmp_ov, **to_oo, clear=True)
        tmp_oo.contract("ab,bc->ac", t_1, **to_s, factor=-1.0)
        #
        # Freeze some amplitudes if required
        #
        for row in self.freeze:
            out_s.set_element(row[0], row[1], 0.0, symmetry=1)

        return {"out_s": out_s}

    @timer.with_section("Jacobian CCS")
    def jacobian(self, amplitudes, *args):
        """Jacobian approximation to find coupled cluster singles amplitudes.

        **Arguments:**

        amplitudes
             Cluster amplitudes.

        args
             All function arguments needed to calculate the vector function
        """
        if log.do_medium:
            log("Computing Jacobian approximation for Quasi-Newton solver.")
        fock = self.from_cache("fock")
        occ = self.nacto
        nov = self._nov
        fi = fock.copy_diagonal(end=occ)
        fa = fock.copy_diagonal(begin=occ)
        #
        # Output
        #
        out = self.lf.create_one_index(nov)
        # The function returns fi-fa and fi-fa+fj-fb
        fia, _ = get_epsilon(
            self.denself,
            [fi, fa],
            singles=self.singles,
            shift=[1e-12, 1e-12],
        )
        fia.iscale(-1.0)
        eps1 = fia.array.reshape(nov)
        out.assign(eps1, end0=nov)
        return out

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


class RpCCDCCS(RCCS):
    """Restricted pair Coupled Cluster Doubles with Coupled Cluster Singles"""

    acronym = "RpCCDCCS"
    long_name = (
        "Restricted pair Coupled Cluster Doubles Coupled Cluster Singles"
    )
    cluster_operator = "T1"

    @property
    def t_p(self):
        """Pair amplitudes - DenseTwoIndex instance"""
        return self._t_p

    @t_p.setter
    def t_p(self, t_p):
        if isinstance(t_p, DenseTwoIndex):
            self._t_p = t_p
        else:
            raise TypeError("t_p must be a DenseTwoIndex instance.")

    @property
    def iodata(self):
        """Container for output data"""
        iodata = super().iodata
        iodata.update({"t_p": self.t_p})
        return iodata

    def read_input(self, *args, **kwargs):
        """Looks for Hamiltonian terms, orbitals, and overlap."""
        #
        # Call parent class method
        #
        one_mo, two_mo, orb = RCCS.read_input(self, *args, **kwargs)
        #
        # Read electron pair amplitudes
        #
        self.t_p = unmask("t_p", *args, **kwargs)
        #
        # Overwrite reference energy
        #
        self.e_ref = unmask("e_tot", *args, **kwargs)

        return one_mo, two_mo, orb

    def print_energy(self):
        """Prints energy terms."""
        if log.do_medium:
            log.hline("-")
            log(f"{self.acronym} energy")
            log(f"{'Total energy':24} {self.energy['e_tot']:14.8f} a.u.")
            log(
                f"{'Reference wavefunction':24} {self.energy['e_ref']:14.8f} a.u."
            )
            log(
                f"{'Total correlation energy':24} {self.energy['e_corr']:14.8f} a.u."
            )
            log.hline("~")
            self.print_energy_details()
            log.hline("-")
            log(" ")

    def print_energy_details(self):
        """Prints energy contributions."""
        log(f"{'Singles':24} {self.energy['e_corr_s']:14.8f} a.u.")

    def set_hamiltonian(self, ham_1_ao, ham_2_ao, mos):
        """Compute auxiliary matrices

        **Arguments:**

        ham_1_ao, ham_2_ao
             One- and two-electron integrals (some Hamiltonian matrix
             elements) in the AO basis.

        mos
             The molecular orbitals.
        """
        #
        # Transform integrals
        #
        mo1, mo2 = self.transform_integrals(ham_1_ao, ham_2_ao, mos)
        ham_2_ao.dump_array(ham_2_ao.label)
        #
        # Clear cache
        #
        self.clear_cache()
        #
        # Update aux matrices
        #
        # Child class
        self.update_hamiltonian(mo1, mo2)
        # Base class
        RCCS.update_hamiltonian(self, mo1, mo2)
        #
        # Clean up (should get deleted anyways)
        #
        mo2.__del__()

    @timer.with_section("Ham RpCCD-CCS")
    def update_hamiltonian(self, mo1, mo2):
        #
        # Get ranges and variables
        #
        oov = self.get_range("oov")
        ovo = self.get_range("ovo")
        ovv = self.get_range("ovv")
        vvo = self.get_range("vvo")
        occ = self.nacto
        vir = self.nactv
        act = self.nact
        t_p = self.t_p
        #
        # pCCD reference function:
        #
        # use 3-index intermediate (will be used several times)
        # This also works with Cholesky
        # <pq|rr>
        gpqrr = self.lf.create_three_index(act)
        mo2.contract("abcc->abc", out=gpqrr)
        #
        # vc_ij = sum_d <ij|dd> c_j^d
        #
        vcij = self.init_cache("vcij", occ, occ)
        gpqrr.contract("abc,bc->ab", t_p, vcij, **oov)
        #
        # oc_ab = sum_m <ab|mm> c_m^a
        #
        ocab = self.init_cache("ocab", vir, vir)
        gpqrr.contract("abc,ca->ab", t_p, ocab, **vvo)
        #
        # oc_jb = sum_m <jb|mm> c_m^b
        #
        ocjb = self.init_cache("ocjb", occ, vir)
        gpqrr.contract("abc,cb->ab", t_p, ocjb, **ovo)
        #
        # vc_jb = sum_d <jb|dd> c_j^d
        #
        vcjb = self.init_cache("vcjb", occ, vir)
        gpqrr.contract("abc,ac->ab", t_p, vcjb, **ovv)

    @timer.with_section("VecFct RpCCD-CCS")
    def vfunction(self, vector):
        """Shorter version of residual vector to accelerate solving."""
        amplitudes = self.unravel(vector)
        #
        # RLCCD part
        #
        residual = RCCS.cc_residual_vector(self, amplitudes)
        #
        # Coupling to pCCD reference
        #
        residual = self.cc_residual_vector(amplitudes, residual)
        return self.ravel(residual)

    def cc_residual_vector(self, amplitudes, output=None):
        """Residual vector of Coupled Cluster equations. Needs to be zero.

        Arguments:

            amplitudes : numpy.ndarray
                vector containing double cluster amplitudes.

        Abbreviations:

        * o - number of active occupied orbitals
        * v - number of active virtual orbitals
        * t_1  - current solution for CC amplitudes
        * out_s - vector function
        """
        t_1 = amplitudes["t_1"]
        t_p = self.t_p
        tco = self.tco
        #
        # Get ranges
        #
        ov2 = self.get_range("ov", offset=2)
        occ = self.nacto
        vir = self.nactv
        #
        # Get auxiliary matrices
        #
        fock = self.from_cache("fock")
        ocjb = self.from_cache("ocjb")
        vcjb = self.from_cache("vcjb")
        vcij = self.from_cache("vcij")
        ocab = self.from_cache("ocab")
        govvo = self.from_cache("govvo")
        #
        # singles
        #
        out_s = output["out_s"]
        to_s = {"out": out_s, "clear": False, "select": self.tco}
        #
        # temporary storage
        #
        tmp_ov = self.lf.create_two_index(occ, vir)
        #
        # pCCD reference function
        #
        # L<ik|ac> c_ia t_kc (s12) (icak, iack)
        #
        govvo.contract("abcd,db->ac", t_1, tmp_ov, factor=2.0, select=tco)
        govvo.contract("abcd,dc->ab", t_1, tmp_ov, factor=-1.0, select=tco)
        tmp_ov.imul(t_p, 1.0)
        out_s.iadd(tmp_ov)
        #
        # tic (a,c) (s14)
        #
        t_1.contract("ab,cb->ac", ocab, **to_s, factor=-1.0)
        #
        # tka (k,i) (s13)
        #
        t_1.contract("ab,ac->cb", vcij, **to_s, factor=-1.0)
        #
        # Fia cia (s9-3)
        #
        out_s.iadd_mult(t_p, fock, 1.0, **ov2)
        #
        # (i,a) (s11-2)
        # <ia|kk> cka = ocia
        #
        out_s.iadd(ocjb, -1.0)
        #
        # (i,a) (s10-2)
        # <ia|cc> cic = vcia
        #
        out_s.iadd(vcjb, 1.0)
        #
        # Set all diagonal amplitudes zero
        #
        for row in self.freeze:
            out_s.set_element(row[0], row[1], 0.0, symmetry=1)

        return {"out_s": out_s}

    @timer.with_section("Jacobian pCCD-CCS")
    def jacobian(self, amplitudes, *args):
        """Jacobian approximation to find coupled cluster doubles amplitudes.

        **Arguments:**

        amplitudes
             Cluster amplitudes.

        args
             All function arguments needed to calculated the vector
        """
        #
        # RCCS part
        #
        jacobian = self.unravel(super().jacobian(amplitudes, *args).array)
        jacobian_1 = jacobian["t_1"]
        #
        # Get auxiliary matrices and other intermediates
        #
        t_p = self.t_p
        govvo = self.from_cache("govvo")
        giaai = govvo.contract("abba->ab")
        occ = self.nacto
        vir = self.nactv
        nov = self._nov
        #
        # Output
        #
        out = self.lf.create_one_index(nov)

        if self.jacobian_approximation == 2:
            #
            # T_1
            #
            tmp = self.lf.create_one_index(occ)
            giaai.contract("ab,ab->a", t_p, tmp)
            jacobian_1.iadd_expand_one_to_two("a->ab", tmp, -1.0)
            tmp = self.lf.create_one_index(vir)
            giaai.contract("ab,ab->b", t_p, tmp)
            jacobian_1.iadd_expand_one_to_two("b->ab", tmp, -1.0)

        eps1 = jacobian_1.array.reshape(nov)
        out.assign(eps1, end0=nov)

        return out
