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
"""Equation of Motion Coupled Cluster implementations of a common base class
   for EOM-LCCD-type methods, like EOM-LCCD and EOM-pCCD-LCCD.

   Child class of REOMCC.
"""

import gc

import numpy as np

from pybest.auxmat import get_fock_matrix
from pybest.exceptions import ArgumentError
from pybest.linalg import CholeskyLinalgFactory
from pybest.log import log
from pybest.utils import unmask

from .eom_base import REOMCC


class REOMLCCDBase(REOMCC):
    """Base class for various EOM-LCCD methods"""

    long_name = "Equation of Motion Linearized Coupled Cluster Doubles"
    acronym = "EOM-LCCD"
    reference = "any LCCD wave function"
    singles_ref = False
    pairs_ref = ""
    doubles_ref = True
    singles_ci = False
    pairs_ci = ""
    doubles_ci = True

    @property
    def dimension(self):
        """The number of unknowns (total number of excited states incl. ground
        state) for each EOM-CC flavor. Variable used by the Davidson module."""
        return self.nacto * self.nactv * (self.nacto * self.nactv + 1) // 2 + 1

    def build_full_hamiltonian(self, *args):
        """Construct full Hamiltonian matrix used in exact diagonalization.
        Not supported here.
        """
        raise NotImplementedError

    def unmask_args(self, *args, **kwargs):
        #
        # t_p
        #
        if self.pairs_ref:
            t_p = unmask("t_p", *args, **kwargs)
            if t_p is None:
                raise ArgumentError("Cannot find Tp amplitudes.")
            self.checkpoint.update("t_p", t_p)
        #
        # t_2
        #
        t_2 = unmask("t_2", *args, **kwargs)
        if t_2 is None:
            raise ArgumentError("Cannot find T2 amplitudes.")
        self.checkpoint.update("t_2", t_2)
        #
        # Call base class method
        #
        return REOMCC.unmask_args(self, *args, **kwargs)

    def print_ci_vectors(self, index, ci_vector):
        """Print information on CI vector (excitation and its coefficient).

        **Arguments:**

        index:
            (int) the composite index that corresponds to a specific excitation

        ci_vector:
            (np.array) the CI coefficient vector that contains all coefficients
            for one specific state
        """
        #
        # Remove reference state index
        #
        index_ = index - 1
        #
        # Print contribution of double excitation
        #
        i, a, j, b = self.get_index_d(index_)
        # Account for frozen core, occupied orbitals, and numpy index convention
        i, a, j, b = (
            i + self.ncore + 1,
            a + self.ncore + self.nacto + 1,
            j + self.ncore + 1,
            b + self.ncore + self.nacto + 1,
        )
        log(
            f"          t_iajb:  ({i:3d},{a:3d},{j:3d},{b:3d})   {ci_vector[index]: 1.5f}"
        )

    def print_weights(self, ci_vector):
        """Print weights of excitations.

        **Arguments:**

        ci_vector:
            (np.array) the CI coefficient vector that contains all coefficients
            for one specific state
        """
        log(
            f"          weight(d): {np.dot(ci_vector[1:], ci_vector[1:]): 1.5f}"
        )

    def compute_h_diag(self, *args):

        """Used by Davidson module for pre-conditioning.

        **Arguments:**

        args:
            required for Davidson module (not used here)
        """
        t_iajb = self.checkpoint["t_2"]
        occ = self.nacto
        vir = self.nactv
        act = self.nact
        #
        # Output objects
        #
        h_diag_d = self.dense_lf.create_four_index(occ, vir, occ, vir)
        #
        # Get ranges
        #
        oovv = self.get_range("oovv")
        #
        # Get auxiliary matrices
        #
        gpqpq = self.from_cache("gpqpq")
        m22ki = self.from_cache("m22ki")
        m22ac = self.from_cache("m22ac")
        m22ijkl = self.from_cache("m22ijkl")
        if isinstance(self.lf, CholeskyLinalgFactory):
            eri = self.from_cache("mo2")
        mkcl = self.lf.create_three_index(occ, vir, occ)
        loovv = self.from_cache("loovv")
        t_iajb.contract("abcd,acbd->abc", loovv, mkcl)
        mkcd = self.lf.create_three_index(occ, vir, vir)
        t_iajb.contract("abcd,acbd->abd", loovv, mkcd)
        if self.dump_cache:
            self.cache.dump("loovv")
        #
        # Doubles:
        #
        # -mkcl-mkcl(ldk)
        h_diag_d.iadd_expand_three_to_four("3", mkcl, -1.0)
        tmp = mkcl.copy()
        tmp.itranspose(2, 0, 1)
        h_diag_d.iadd_expand_three_to_four("1", tmp, -1.0)
        # -mkcd-mkcd(ldc)
        h_diag_d.iadd_expand_three_to_four("2", mkcd, -1.0)
        tmp = mkcd.copy()
        tmp.itranspose(2, 0, 1)
        h_diag_d.iadd_expand_three_to_four("0", tmp, -1.0)
        # m22ki (k,l,c,d)
        tmpo = m22ki.copy_diagonal()
        tmpv = m22ac.copy_diagonal()
        h_diag_d.iadd_expand_one_to_four("0", tmpo)
        h_diag_d.iadd_expand_one_to_four("2", tmpo)
        h_diag_d.iadd_expand_one_to_four("1", tmpv)
        h_diag_d.iadd_expand_one_to_four("3", tmpv)
        # m22jbkc (kckc,ldld)
        m22jbkc = self.from_cache("m22jbkc")
        tmp = m22jbkc.contract("abab->ab", clear=True, select="einsum")
        if self.dump_cache:
            self.cache.dump("m22jbkc")
        h_diag_d.iadd_expand_two_to_four("ab->abcd", tmp)
        h_diag_d.iadd_expand_two_to_four("cd->abcd", tmp)
        # m22kbid (kdkd,lclc)
        m22kbid = self.from_cache("m22kbid")
        tmp = m22kbid.contract("abab->ab", clear=True, select="einsum")
        if self.dump_cache:
            self.cache.dump("m22kbid")
        h_diag_d.iadd_expand_two_to_four("ad->abcd", tmp)
        h_diag_d.iadd_expand_two_to_four("cb->abcd", tmp)
        # m22ijkl (klkl,lklk)
        tmp = m22ijkl.contract("abab->ab", clear=True, select="einsum")
        h_diag_d.iadd_expand_two_to_four("ac->abcd", tmp)
        h_diag_d.iadd_expand_two_to_four("ca->abcd", tmp)
        # m22abcd (cdcd,dcdc)
        if isinstance(self.lf, CholeskyLinalgFactory):
            tmp = gpqpq.copy(occ, act, occ, act)
            tmp.iscale(0.5)
            tmpoovv = eri.contract(
                "abcd->abcd", out=None, factor=1.0, **oovv, select="einsum"
            )
            t_iajb.contract("abcd,acbd->bd", tmpoovv, tmp)
            tmpoovv = None
        else:
            m22abcd = self.from_cache("m22abcd")
            tmp = m22abcd.contract("abab->ab", clear=True, select="einsum")
            if self.dump_cache:
                self.cache.dump("m22abcd")
        h_diag_d.iadd_expand_two_to_four("bd->abcd", tmp)
        h_diag_d.iadd_expand_two_to_four("db->abcd", tmp)

        return h_diag_d

    def build_subspace_hamiltonian(self, bvector, hdiag, *args):

        """
        Used by Davidson module to construct subspace Hamiltonian. Includes all
        terms that are similar for all EOM-LCC flavours. The doubles contributions
        do not include any permutations due to non-equivalent lines.

        **Arguments:**

        bvector:
            (OneIndex object) contains current approximation to CI coefficients

        hdiag:
            Diagonal Hamiltonian elements required in Davidson module (not used
            here)

        args:
            Set of arguments passed by the Davidson module (not used here)
        """
        t_iajb = self.checkpoint["t_2"]
        tco = {"select": self.tco}
        occ = self.nacto
        vir = self.nactv
        #
        # Get auxiliary matrices and effective Hamiltonian terms
        #
        m22ki = self.from_cache("m22ki")
        m22ac = self.from_cache("m22ac")
        m22ijkl = self.from_cache("m22ijkl")
        #
        # Calculate sigma vector (H.bvector)_kc
        #
        sigma_d = self.dense_lf.create_four_index(occ, vir, occ, vir)
        bv_d = self.dense_lf.create_four_index(occ, vir, occ, vir)
        to_d = {"out": sigma_d, "select": self.tco, "clear": False}
        #
        # reshape bvector
        #
        bv_d.assign_triu(bvector, begin4=1)
        bv_p = bv_d.contract("abab->ab", clear=True, select="einsum")
        bv_d.iadd_transpose((2, 3, 0, 1))
        self.set_seniority_0(bv_d, bv_p)
        #
        # Reference vector R_0
        #
        # X0,kc rkc
        loovv = self.from_cache("loovv")
        sum0_ = bv_d.contract("abcd,acbd", loovv)
        if self.dump_cache:
            self.cache.dump("loovv")
        #
        # Double excitations
        #
        # P Xki rkajb
        bv_d.contract("abcd,ae->ebcd", m22ki, **to_d)
        # P Xac ricjb
        bv_d.contract("abcd,eb->aecd", m22ac, **to_d)
        # P Xabcd ricjd
        self.get_effective_hamiltonian_term_abcd(bv_d, sigma_d)
        # P Xijkl rkalb
        m22ijkl.contract("abcd,cedf->aebf", bv_d, **to_d)
        # P Xkajc rkbic
        m22kbid = self.from_cache("m22kbid")
        bv_d.contract("abcd,aefd->cefb", m22kbid, **to_d)
        if self.dump_cache:
            self.cache.dump("m22kbid")
        # P Xkaci rkbjc
        m22kadi = self.from_cache("m22kadi")
        m22kadi.contract("abcd,aefc->dbfe", bv_d, **to_d)
        if self.dump_cache:
            self.cache.dump("m22kadi")
        # P Xjbkc riakc
        m22jbkc = self.from_cache("m22jbkc")
        bv_d.contract("abcd,efcd->abef", m22jbkc, **to_d)
        if self.dump_cache:
            self.cache.dump("m22jbkc")
        # (19) P Xjabkcd ridkc
        # Llkdc rkcjd; lj t_ialb
        tmp = self.lf.create_two_index(occ)
        loovv = self.from_cache("loovv")
        loovv.contract("abcd,bdec->ae", bv_d, tmp, **tco)
        t_iajb.contract("abcd,ce->abed", tmp, **to_d, factor=-1.0)
        # (18) P Xknclmd rldmf
        # Lklcd rkbld; cb t_iajc
        tmp = self.lf.create_two_index(self.nactv)
        loovv.contract("abcd,aebd->ce", bv_d, tmp, **tco)
        t_iajb.contract("abcd,de->abce", tmp, **to_d, factor=-1.0)
        tmp = None
        if self.dump_cache:
            self.cache.dump("loovv")

        return sum0_, sigma_d, bv_d

    def update_hamiltonian(self, mo1, mo2):
        """Derive all auxiliary matrices. Derive all matrices that are common
        for all EOM-LCCD flavors.

        **Arguments:**

        mo1, mo2
             one- and two-electron integrals to be sorted.
        """
        t_iajb = self.checkpoint["t_2"]
        tco = {"select": self.tco}
        occ = self.nacto
        vir = self.nactv
        act = self.nact
        #
        # Get ranges
        #
        oo2 = self.get_range("oo", offset=2)
        vv2 = self.get_range("vv", offset=2)
        oooo = self.get_range("oooo")
        oovv = self.get_range("oovv")
        oovv4 = self.get_range("oovv", offset=4)
        ovvo = self.get_range("ovvo")
        ovov = self.get_range("ovov")
        vvvv = self.get_range("vvvv")
        #
        # Get auxiliary matrices
        #
        #
        # 2<pq|pq>-<pq|pq>
        #
        gpqpq = self.init_cache("gpqpq", act, act)
        mo2.contract("abab->ab", gpqpq, factor=1.0, select="einsum")
        lpqpq = gpqpq.copy()
        lpqpq.iscale(2.0)
        mo2.contract("abba->ab", out=lpqpq, factor=-1.0, select="einsum")
        #
        # <pq|rq> and <pq||rq>+<pq|rq>
        #
        gpqrq = self.init_cache("gpqrq", act, act, act)
        mo2.contract("abcb->abc", gpqrq, factor=1.0, select="einsum")
        lpqrq = self.init_cache("lpqrq", act, act, act)
        lpqrq.assign(gpqrq)
        lpqrq.iscale(2.0)
        #
        # <pq|rr>
        #
        gpqrr = self.lf.create_three_index(act)
        mo2.contract("abcc->abc", out=gpqrr, clear=True, select="einsum")
        #
        # add exchange part to lpqrq using gpqrr
        #
        tmp3 = self.lf.create_three_index(act)
        tmp3.assign(gpqrr.array.transpose(0, 2, 1))
        lpqrq.iadd(tmp3, factor=-1.0)
        del tmp3, gpqrr
        #
        # Inactive Fock matrix
        #
        fock = self.init_cache("fock", act, act)
        get_fock_matrix(fock, mo1, mo2, occ)
        #
        # <pp|qq>
        #
        gppqq = self.init_cache("gppqq", act, act)
        mo2.contract("aabb->ab", gppqq, select="einsum")
        #
        # <oo||vv>+<oo|vv>
        #
        loovv = self.init_cache("loovv", occ, occ, vir, vir)
        mo2.contract("abcd->abcd", loovv, factor=2.0, **oovv, select="einsum")
        mo2.contract("abcd->abdc", loovv, factor=-1.0, **oovv, select="einsum")
        if self.dump_cache:
            self.cache.dump("loovv")
        # temporary matrix needed for some contractions
        goovv = self.init_cache("goovv", occ, occ, vir, vir)
        mo2.contract("abcd->abcd", goovv, **oovv, select="einsum")
        if self.dump_cache:
            self.cache.dump("goovv")
        #
        # Most expensive operation. Do first to have largest amount of memory available
        # Aux matrix for M22iajb,ijcb (abcd)
        # Only calculated for DenseLinalgFactory
        # X_abcd
        if not isinstance(self.lf, CholeskyLinalgFactory):
            m22abcd = self.init_cache("m22abcd", vir, vir, vir, vir)
            # <ab|cd>
            mo2.contract(
                "abcd->abcd", m22abcd, factor=0.5, **vvvv, select="einsum"
            )
            # tkalb <kl|cd>
            t_iajb.contract(
                "abcd,acef->bdef", mo2, m22abcd, factor=0.5, **tco, **oovv4
            )
            if self.dump_cache:
                self.cache.dump("m22abcd")
        #
        # Aux matrix for M22iajb,kjcb (akic) and Mp2iaia,kica (akic)
        # Aux matrix for M22iajb,kjcb (jbkc) and Mp2iaia,kica (jbkc)
        # (13) X_jbkc
        m22jbkc = self.init_cache("m22jbkc", occ, vir, occ, vir)
        # Lkbcj / jcbk - jbkc
        mo2.contract(
            "abcd->acdb", m22jbkc, factor=2.0, **ovvo, select="einsum"
        )
        mo2.contract(
            "abcd->abcd", m22jbkc, factor=-1.0, **ovov, select="einsum"
        )
        # Llkdc theta_jbld/jdlb
        loovv = self.from_cache("loovv")
        loovv.contract("abcd,efac->efbd", t_iajb, m22jbkc, factor=2.0, **tco)
        loovv.contract("abcd,ecaf->efbd", t_iajb, m22jbkc, factor=-1.0, **tco)
        if self.dump_cache:
            self.cache.dump("m22jbkc")
            self.cache.dump("loovv")
        #
        # Aux matrix for M22iajb,kjbd (kadi) and M2piaia,kiad
        # (14) X_jbkc
        m22kadi = self.init_cache("m22kadi", occ, vir, vir, occ)
        # <ka|di>
        mo2.contract(
            "abcd->abcd", m22kadi, factor=-1.0, **ovvo, select="einsum"
        )
        # tlaic <lk|cd>
        goovv = self.from_cache("goovv")
        t_iajb.contract("abcd,aedf->ebfc", goovv, m22kadi, **tco)
        if self.dump_cache:
            self.cache.dump("goovv")
        # t_iame Lmked
        loovv = self.from_cache("loovv")
        t_iajb.contract("abcd,cedf->ebfa", loovv, m22kadi, factor=-1.0, **tco)
        if self.dump_cache:
            self.cache.dump("m22kadi")
            self.cache.dump("goovv")
        #
        # Aux matrix for M22iajb,kjad (kbid)
        # (15) X_ajkc
        m22kbid = self.init_cache("m22kbid", occ, vir, occ, vir)
        # <kb|id>
        mo2.contract(
            "abcd->abcd", m22kbid, factor=-1.0, **ovov, select="einsum"
        )
        # tmbie <km|ed>
        goovv = self.from_cache("goovv")
        t_iajb.contract("abcd,eadf->ebcf", goovv, m22kbid, **tco)
        if self.dump_cache:
            self.cache.dump("m22kbid")
            self.cache.dump("goovv")
        #
        # Aux matrix for M22iajb,klab (ijkl) and Mp2iaia,klaa (ikl)
        # (17) X_ijkl
        m22ijkl = self.init_cache("m22ijkl", occ, occ, occ, occ)
        # <ij|kl>
        mo2.contract(
            "abcd->abcd", m22ijkl, factor=0.5, **oooo, select="einsum"
        )
        # tiejf <kl|ef>
        goovv = self.from_cache("goovv")
        t_iajb.contract("abcd,efbd->acef", goovv, m22ijkl, factor=0.5)
        if self.dump_cache:
            self.cache.dump("goovv")
        #
        # Aux matrix for M22iajb,kjab (ki) and Mp2iaia,kiaa (ki)
        # (11) X_jk
        m22ki = self.init_cache("m22ki", occ, occ)
        # fki
        m22ki.iadd(fock, -1.0, **oo2)
        # Lmkef tmeif
        loovv = self.from_cache("loovv")
        loovv.contract("abcd,aced->be", t_iajb, m22ki, factor=-1.0, **tco)
        #
        # Aux matrix for M22iajb,ijcb (ac) and Mp2iaia,iica (ac)
        # (12) X_bc
        m22ac = self.init_cache("m22ac", vir, vir)
        # fac
        m22ac.iadd(fock, 1.0, **vv2)
        # Lmnec tmena
        loovv.contract("abcd,acbe->ed", t_iajb, m22ac, factor=-1.0, **tco)
        if self.dump_cache:
            self.cache.dump("loovv")

        gc.collect()

    #
    # Expensive effective Hamiltonian terms
    #

    def get_effective_hamiltonian_term_abcd(self, bv_d, sigma):
        """Compute effective Hamiltonian term involving an ovvv block

        **Arguments:**

        :bv_d: (DenseFourIndex) the current approximation to the CI doubles
               coefficient

        :sigma: (DenseFourIndex) the output sigma vector
        """
        to_d = {"out": sigma, "clear": False, "select": self.tco}
        if isinstance(self.lf, CholeskyLinalgFactory):
            t_iajb = self.checkpoint["t_2"]
            eri = self.from_cache("mo2")
            oovv = self.get_range("oovv")
            vvvv = self.get_range("vvvv")
            occ = self.nacto
            tco = {"select": self.tco}
            # (16) Xabcd ricjd
            # <abcd>
            eri.contract("abcd,ecfd->eafb", bv_d, **to_d, factor=0.5, **vvvv)
            # <klcd> tkalb ricjd
            tmp = self.dense_lf.create_four_index(occ, occ, occ, occ)
            eri.contract("abcd,ecfd->efab", bv_d, tmp, **oovv, **tco)
            tmp.contract("abcd,cedf->aebf", t_iajb, **to_d, factor=0.5)
        else:
            m22abcd = self.from_cache("m22abcd")
            bv_d.contract("abcd,efbd->aecf", m22abcd, **to_d)
            if self.dump_cache:
                self.cache.dump("m22abcd")
