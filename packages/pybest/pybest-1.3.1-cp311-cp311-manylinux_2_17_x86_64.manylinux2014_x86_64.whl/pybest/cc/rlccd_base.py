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
"""Restricted Linearized Coupled Cluster Doubles base Class. Not intended to be
   used on its own.

   Variables used in this module:
    :nocc:      number of occupied orbitals in the principle configuration
    :nvirt:     number of virtual orbitals in the principle configuration
    :ncore:     number of frozen core orbitals in the principle configuration
    :nbasis:    total number of basis functions
    :energy:    the LCC energy, dictionary that contains different
                contributions
    :t_2:       the optimized amplitudes

    Indexing convention:
    :o:        matrix block corresponding to occupied orbitals of principle
               configuration
    :v:        matrix block corresponding to virtual orbitals of principle
               configuration

"""
from functools import partial

from pybest.auxmat import get_fock_matrix
from pybest.cc.rcc import RCC
from pybest.exceptions import ArgumentError
from pybest.helperclass import PropertyHelper as PH
from pybest.linalg import CholeskyFourIndex, DenseFourIndex
from pybest.log import log, timer
from pybest.pt.perturbation_utils import get_epsilon
from pybest.utils import unmask

from .rdm_lcc import (
    compute_1dm_lccd,
    compute_2dm_lccd,
    compute_3dm_lccd,
    compute_4dm_lccd,
)


class RLCCDBase(RCC):
    """Class containing methods characteristic for linearized CCD."""

    reference = ""
    singles = False
    doubles = True

    def get_ndm(self, select):
        """Get some RDM from the Cache. Needs to be defined here as it is used
        by the PropertyHelper class."""
        if select not in self.cache:
            raise ArgumentError(f"Density matrix {select} not found.")
        return self.cache.load(select)

    dm_1_pp = PH(get_ndm, "dm_1_pp", "Diagonal 1-RDM for alpha/beta spin")
    dm_1_pq = PH(get_ndm, "dm_1_pq", "1-RDM for alpha/beta spin")
    dm_2_pPPp = PH(get_ndm, "dm_2_pPPp", "2-RDM for alpha/beta spin")
    dm_2_pqqp = PH(get_ndm, "dm_2_pqqp", "2-RDM for alpha/beta spin")
    dm_2_pQQp = PH(get_ndm, "dm_2_pQQp", "2-RDM for alpha/beta spin")
    dm_2_qQQp = PH(get_ndm, "dm_2_qQQp", "2-RDM for alpha/beta spin")
    dm_2_pQPp = PH(get_ndm, "dm_2_pQPp", "2-RDM for alpha/beta spin")
    dm_2_qQPq = PH(get_ndm, "dm_2_qQPq", "2-RDM for alpha/beta spin")
    dm_2_qQPp = PH(get_ndm, "dm_2_qQPp", "2-RDM for alpha/beta spin")
    dm_2_pQPq = PH(get_ndm, "dm_2_pQPq", "2-RDM for alpha/beta spin")
    dm_2_qPPp = PH(get_ndm, "dm_2_qPPp", "2-RDM for alpha/beta spin")
    dm_3_qPQQPp = PH(get_ndm, "dm_3_qPQQPp", "3-RDM for alpha/beta spin")
    dm_3_qpPPpq = PH(get_ndm, "dm_3_qpPPpq", "3-RDM for alpha/beta spin")
    dm_4_pPqQQqPp = PH(get_ndm, "dm_4_pPqQQqPp", "4-RDM for alpha/beta spin")

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
    def iodata(self):
        """Container for output data"""
        iodata = super().iodata
        if self._converged_l:
            iodata["dm_1"] = {
                "pp": self.dm_1_pp,
                "pq": self.dm_1_pq,
            }
            iodata["dm_2"] = {
                "pPPp": self.dm_2_pPPp,
                "pqqp": self.dm_2_pqqp,
                "pQQp": self.dm_2_pQQp,
                "qQQp": self.dm_2_qQQp,
                "pQPp": self.dm_2_pQPp,
                "qQPq": self.dm_2_qQPq,
                "qQPp": self.dm_2_qQPp,
                "pQPq": self.dm_2_pQPq,
                "qPPp": self.dm_2_qPPp,
            }
            iodata["dm_3"] = {
                "qPQQPp": self.dm_3_qPQQPp,
                "qpPPpq": self.dm_3_qpPPpq,
            }
            iodata["dm_4"] = {"pPqQQqPp": self.dm_4_pPqQQqPp}
        return iodata

    @property
    def freeze(self):
        """The freezed linearized coupled cluster doubles amplitudes"""
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
        self.freeze = kwargs.get("freeze", [])
        # Choose optimal internal contraction schemes (select=None)
        self.tco = kwargs.get("tco", None)
        self.e_core = unmask("e_core", *args, **kwargs)

        return one_mo, two_mo, orb

    def calculate_energy(self, e_ref, e_core=0, **amplitudes):
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
            "e_core": self.e_core,
            "e_corr": 0.0,
            "e_corr_s": 0.0,
            "e_corr_d": 0.0,
            "e_corr_s2": 0.0,
            "e_corr_s4": 0.0,
        }
        #
        # Get amplitudes and integrals
        #
        govvo = self.from_cache("govvo")
        try:
            t_2 = amplitudes.get("t_2", self.t_2)
        except AttributeError:
            t_2 = amplitudes.get("t_2")
        #
        # E_doubles = sum_mkde L_mkde t_mdke
        #
        energy["e_corr_d"] = t_2.contract("abcd,adbc", govvo) * 2.0
        energy["e_corr_d"] -= t_2.contract("abcd,abdc", govvo)
        energy["e_corr"] = energy["e_corr_d"]
        energy["e_tot"] = e_ref + energy["e_corr"]
        #
        # Seniority-2 sector
        #
        energy["e_corr_s2"] = t_2.contract("abac,acba", govvo)
        energy["e_corr_s2"] += t_2.contract("abcb,abbc", govvo)
        #
        # Seniority-4 sector
        #
        energy["e_corr_s4"] = energy["e_corr_d"] - energy["e_corr_s2"]

        return energy

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
        self.update_hamiltonian(mo1, mo2)
        #
        # Clean up (should get deleted anyways)
        #
        mo2.__del__()

    def set_dm(self, *args):
        """Determine all supported RDMs and put them into the cache."""
        #
        # Clear cache
        #
        self.clear_cache(tags="d")
        #
        # Update RDMs
        #
        self.update_ndm("dm_1_pp", "pp", self.nact)
        self.update_ndm("dm_1_pq", "pq", self.nact, self.nact)
        self.update_ndm("dm_2_pPPp", "pPPp", self.nact)
        self.update_ndm("dm_2_pqqp", "pqqp", self.nact, self.nact)
        self.update_ndm("dm_2_pQQp", "pQQp", self.nact, self.nact)
        self.update_ndm("dm_2_qQQp", "qQQp", self.nact, self.nact)
        self.update_ndm("dm_2_pQPp", "pQPp", self.nact, self.nact)
        self.update_ndm("dm_2_qQPq", "qQPq", self.nact, self.nact)
        self.update_ndm("dm_2_qQPp", "qQPp", self.nact, self.nact)
        self.update_ndm("dm_2_pQPq", "pQPq", self.nact, self.nact)
        self.update_ndm("dm_2_qPPp", "qPPp", self.nact, self.nact)
        self.update_ndm("dm_3_qPQQPp", "qPQQPp", self.nact, self.nact)
        self.update_ndm("dm_3_qpPPpq", "qpPPpq", self.nact, self.nact)
        self.update_ndm("dm_4_pPqQQqPp", "pPqQQqPp", self.nact, self.nact)

    def update_ndm(self, select, option, *args, **kwargs):
        """Wrapper function that is used to update all supported N-particle
        RDMs.

        **Arguments:**

        select:
            (str) name of DM stored in the cache

        option:
            (str) specific block of DM to be calculated

        args:
            tuple of (int) indicating the dimensions of the DM to be calculated.
            Used for initializing the cache instance.

        **Keyword arguments:**
            passed to the utility functions. Currenlty not used here.

        """
        options = {"tags": "d"}
        cached_ndm = self.init_cache(select, *args, **options)
        method = {
            "dm_1": compute_1dm_lccd,
            "dm_2": compute_2dm_lccd,
            "dm_3": compute_3dm_lccd,
            "dm_4": compute_4dm_lccd,
        }
        for key in method:
            if key in select:
                method_ = method[key]
        method_(
            option,
            cached_ndm,
            self.l_amplitudes,
            self.amplitudes,
            1.0,
            *args,
            **kwargs,
        )

    @timer.with_section("UpdatingAuxMat")
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
        # Get ranges
        #
        act = self.nact
        no = self.occ_model.nacto[0]
        nv = self.occ_model.nactv[0]
        #
        # Inactive Fock matrix
        #
        fock = self.init_cache("fock", act, act)
        get_fock_matrix(fock, mo1, mo2, self.nacto)
        #
        # <pq|pq>
        #
        gpqpq = self.init_cache("gpqpq", act, act)
        mo2.contract("abab->ab", out=gpqpq, clear=True)
        #
        # <ov|vo> intermediate
        #
        govvo = self.init_cache("govvo", no, nv, nv, no)
        mo2.contract("abcd->abcd", out=govvo, **self.get_range("ovvo"))
        if self.dump_cache:
            self.cache.dump("govvo")

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
        slices = ["ovov", "oooo", "vvvv", "oovv"]
        for slice_ in slices:
            self.init_cache(f"g{slice_}", alloc=alloc(mo2, slice_))

    @timer.with_section("VecFctRLCC")
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
        """
        t_2 = amplitudes["t_2"]
        #
        # Get ranges
        #
        oo4 = self.get_range("oo", offset=4)
        vv4 = self.get_range("vv", offset=4)
        #
        # Get auxiliary matrices
        #
        fock = self.from_cache("fock")
        goovv = self.from_cache("goovv")
        govov = self.from_cache("govov")
        goooo = self.from_cache("goooo")
        gvvvv = self.from_cache("gvvvv")
        #
        # doubles
        #
        out_d = t_2.new()
        to_d = {"out": out_d, "clear": False}
        #
        # <ab|ij> (d-d1)
        #
        goovv.contract("abcd->acbd", out=out_d, factor=0.5)
        # (d-d3-1)
        # sum_k t_iakb*F_kj
        #
        t_2.contract("abcd,ce->abed", fock, factor=-1.0, **oo4, **to_d)
        # (d-d2-1)
        # sum_c t_iajc*F_bc
        #
        t_2.contract("abcd,ed->abce", fock, **vv4, **to_d)
        # (d-d6-1)
        # sum_kc t_iakc*L_kbcj
        # (jkbc,iakc)
        goovv.contract("abcd,efbd->efac", t_2, factor=2.0, **to_d)
        # (jbkc,iakc)
        # NOTE: slow contraction
        govov.contract("abcd,efcd->abef", t_2, factor=-1.0, **to_d)
        # (d-d6-3)
        # sum_kc (t_kajc*g_ibkc)
        # NOTE: slow contraction
        govov.contract("abcd,cfed->afeb", t_2, factor=-1.0, **to_d)
        # (d-d6-2)
        # sum_kc (t_kaic*g_kbcj)
        # jkbc,icka
        goovv.contract("abcd,edbf->efac", t_2, factor=-1.0, **to_d)
        # (d-d4-1)
        # sum_kl t_kalb*g_ijkl
        #
        goooo.contract("abcd,cedf->aebf", t_2, factor=0.5, **to_d)
        #
        # (d-d5-1)
        # sum_cd t_icjd*g_abcd
        # NOTE: bottleneck operation
        gvvvv.contract("abcd,ecfd->eafb", t_2, factor=0.5, **to_d)
        #
        # Add permutation
        #
        out_d.iadd_transpose((2, 3, 0, 1))
        #
        # Freeze some amplitudes if required
        #
        for row in self.freeze:
            t_2.set_element(row[0], row[1], row[2], row[3], 0.0, symmetry=1)
            t_2.set_element(row[2], row[3], row[0], row[1], 0.0, symmetry=1)

        return {"out_d": out_d}

    @timer.with_section("Jacobian LCCD")
    def jacobian(self, amplitudes, *args):
        """Jacobian approximation to find coupled cluster doubles amplitudes.

        **Arguments:**

        amplitudes
             Cluster amplitudes.

        args
             All function arguments needed to calculated the vector
        """
        if log.do_medium:
            log("Computing Jacobian approximation for Quasi-Newton solver.")
        #
        # Get auxiliary matrices and other intermediates
        #
        fock = self.from_cache("fock")
        fi = fock.copy_diagonal(end=self.nacto)
        fa = fock.copy_diagonal(begin=self.nacto)
        occ = self.nacto
        vir = self.nactv
        unknowns = occ * vir * (occ * vir + 1) // 2
        #
        # Output
        #
        out = self.lf.create_one_index(unknowns)
        #
        # Approximate Jacobian
        #
        fiajb = get_epsilon(
            self.denself,
            [fi, fa],
            singles=self.singles,
            shift=[1e-12, 1e-12],
        )
        fiajb.iscale(-1.0)
        # Assign to output
        out.assign(fiajb.get_triu())
        fiajb.__del__()
        # Add other terms:
        if self.jacobian_approximation == 2:
            govov = self.from_cache("govov")
            gpqpq = self.from_cache("gpqpq")
            # temporary copy
            eps2 = self.denself.create_four_index(occ, vir, occ, vir)
            # Libaj
            govvo = self.from_cache("govvo")
            govvo.contract("abcd->acdb", out=eps2, factor=2.0)
            if self.dump_cache:
                self.cache.dump("govvo")
            govov.contract("abcd->adcb", out=eps2, factor=-1.0)
            govov.contract("abcd->abcd", eps2, factor=-1.0)
            # <ab|ab>
            eps2.iadd_expand_two_to_four(
                "bd->abcd", gpqpq, 0.5, begin0=occ, begin1=occ
            )
            # <ij|ij>
            eps2.iadd_expand_two_to_four(
                "ac->abcd", gpqpq, 0.5, end0=occ, end1=occ
            )
            # Permutation
            eps2.iadd_transpose((2, 3, 0, 1))
            out.iadd(eps2.get_triu())
            eps2.__del__()

        return out

    @timer.with_section("VecFct Lambda RLCCD")
    def vfunction_l(self, vector):
        """Shorter version of residual vector to accelerate solving."""
        amplitudes = self.unravel(vector)
        return self.ravel(self.l_residual_vector(amplitudes))

    def l_residual_vector(self, amplitudes):
        """Residual vector of Lambda equations. Needs to be zero.

        Arguments:

            amplitudes : numpy.ndarray
                vector containing double Lambda amplitudes.

        Abbreviations:

        * o - number of active occupied orbitals
        * v - number of active virtual orbitals
        * t_2 - current solution for Lambda amplitudes
        * out_d - vector function
        """
        l_2 = amplitudes["t_2"]
        #
        # Get ranges
        #
        oo4 = self.get_range("oo", offset=4)
        vv4 = self.get_range("vv", offset=4)
        #
        # Get auxiliary matrices
        #
        fock = self.from_cache("fock")
        govov = self.from_cache("govov")
        goooo = self.from_cache("goooo")
        gvvvv = self.from_cache("gvvvv")
        #
        # Lambda_iajb
        #
        out_d = l_2.new()
        to_d = {"out": out_d, "clear": False, "select": self.tco}
        #
        #
        # 1
        govvo = self.from_cache("govvo")
        govvo.contract("abcd->acdb", out=out_d, factor=2.0, clear=True)
        govvo.contract("abcd->abdc", out=out_d, factor=-1.0)
        # 9-1
        govvo.contract("abcd,efdb->acef", l_2, **to_d, factor=2.0)
        # 10
        govvo.contract("abcd,efdb->afec", l_2, **to_d, factor=-1.0)
        if self.dump_cache:
            self.cache.dump("govvo")
        # 9-2
        govov.contract("abcd,efcb->adef", l_2, **to_d, factor=-1.0)
        # 5
        l_2.contract("abcd,ed->abce", fock, **to_d, factor=1.0, **vv4)
        # 6
        l_2.contract("abcd,ec->abed", fock, **to_d, factor=-1.0, **oo4)
        # 7
        gvvvv.contract("abcd,ecfd->eafb", l_2, **to_d, factor=0.5)
        # 8
        goooo.contract("abcd,cedf->aebf", l_2, **to_d, factor=0.5)
        # 11
        govov.contract("abcd,ebcf->edaf", l_2, **to_d, factor=-1.0)
        #
        # Add permutation
        #
        out_d.iadd_transpose((2, 3, 0, 1))
        #
        # Freeze some amplitudes if required
        #
        for row in self.freeze:
            out_d.set_element(row[0], row[1], row[2], row[3], 0.0, symmetry=1)
            out_d.set_element(row[2], row[3], row[0], row[1], 0.0, symmetry=1)

        return {"out_d": out_d}
