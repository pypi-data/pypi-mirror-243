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
   for EOM-LCCSD-type methods, like EOM-LCCSD and EOM-pCCD-LCCSD

   Child class of REOMCC class.
"""

import gc

import numpy as np

from pybest.auxmat import get_fock_matrix
from pybest.exceptions import ArgumentError
from pybest.linalg import CholeskyLinalgFactory
from pybest.log import log
from pybest.utils import unmask

from .eom_base import REOMCC


class REOMLCCSDBase(REOMCC):
    """Base class for various EOM-LCCSD methods"""

    long_name = "Equation of Motion Linearized Coupled Cluster Singles Doubles"
    acronym = ""
    reference = "any LCCSD wave function"
    singles_ref = True
    pairs_ref = ""
    doubles_ref = True
    singles_ci = True
    pairs_ci = ""
    doubles_ci = True

    @property
    def dimension(self):
        """The number of unknowns (total number of excited states incl. ground
        state) for each EOM-CC flavor. Variable used by the Davidson module."""
        return (
            self.nacto * self.nactv * (self.nacto * self.nactv + 1) // 2
            + self.nacto * self.nactv
            + 1
        )

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
        # t_1
        #
        t_1 = unmask("t_1", *args, **kwargs)
        if t_1 is None:
            raise ArgumentError("Cannot find T1 amplitudes.")
        self.checkpoint.update("t_1", t_1)
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
        # Either single or double excitation
        #
        doubles = index_ - self.nacto * self.nactv >= 0
        #
        # Print contribution
        #
        if doubles:
            #
            # Shift by single excitations
            #
            index_ -= self.nacto * self.nactv
            #
            # Get double excitation
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
        else:
            #
            # Get single excitation
            #
            i, a = self.get_index_s(index_)
            # Account for frozen core, occupied orbitals, and numpy index convention
            i, a = i + self.ncore + 1, a + self.ncore + self.nacto + 1
            log(
                f"            t_ia:          ({i:3d},{a:3d})   {ci_vector[index]: 1.5f}"
            )

    def print_weights(self, ci_vector):
        """Print weights of excitations.

        **Arguments:**

        ci_vector:
            (np.array) the CI coefficient vector that contains all coefficients
            for one specific state
        """
        nov = self.nacto * self.nactv + 1
        log(
            f"          weight(s): {np.dot(ci_vector[1:nov], ci_vector[1:nov]): 1.5f}"
        )
        log(
            f"          weight(d): {np.dot(ci_vector[nov:], ci_vector[nov:]): 1.5f}"
        )

    def compute_h_diag(self, *args):

        """Used by Davidson module for pre-conditioning.

        **Arguments:**

        args:
            required for Davidson module (not used here)
        """
        t_ia = self.checkpoint["t_1"]
        t_iajb = self.checkpoint["t_2"]
        occ = self.nacto
        vir = self.nactv
        act = self.nact
        #
        # Output objects
        #
        h_diag_s = self.lf.create_two_index(occ, vir)
        h_diag_d = self.dense_lf.create_four_index(occ, vir, occ, vir)
        #
        # Get ranges
        #
        ovv = self.get_range("ovv")
        oovv = self.get_range("oovv")
        #
        # Get auxiliary matrices
        #
        gpqpq = self.from_cache("gpqpq")
        gpqrq = self.from_cache("gpqrq")
        miaka = self.from_cache("miaka")
        miaic = self.from_cache("miaic")
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
        # Singles
        #
        miakc = self.from_cache("miakc")
        miakc.contract("abab->ab", out=h_diag_s, clear=True, select="einsum")
        if self.dump_cache:
            self.cache.dump("miakc")
        tmp = miaka.copy_diagonal()
        h_diag_s.iadd_expand_one_to_two("a->ab", tmp, 1.0)
        tmp = miaic.copy_diagonal()
        h_diag_s.iadd_expand_one_to_two("b->ab", tmp, 1.0)
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
        h_diag_d.iadd_expand_one_to_four("0", tmpo, 1.0)
        h_diag_d.iadd_expand_one_to_four("2", tmpo, 1.0)
        h_diag_d.iadd_expand_one_to_four("1", tmpv, 1.0)
        h_diag_d.iadd_expand_one_to_four("3", tmpv, 1.0)
        # m22jbkc (kckc,ldld)
        m22jbkc = self.from_cache("m22jbkc")
        tmp = m22jbkc.contract("abab->ab", clear=True, select="einsum")
        if self.dump_cache:
            self.cache.dump("m22jbkc")
        h_diag_d.iadd_expand_two_to_four("ab->abcd", tmp, 1.0)
        h_diag_d.iadd_expand_two_to_four("cd->abcd", tmp, 1.0)
        # m22kbid (kdkd,lclc)
        m22kbid = self.from_cache("m22kbid")
        tmp = m22kbid.contract("abab->ab", clear=True, select="einsum")
        if self.dump_cache:
            self.cache.dump("m22kbid")
        h_diag_d.iadd_expand_two_to_four("ad->abcd", tmp, 1.0)
        h_diag_d.iadd_expand_two_to_four("cb->abcd", tmp, 1.0)
        # m22ijkl (klkl,lklk)
        tmp = m22ijkl.contract("abab->ab", clear=True, select="einsum")
        h_diag_d.iadd_expand_two_to_four("ac->abcd", tmp, 1.0)
        h_diag_d.iadd_expand_two_to_four("ca->abcd", tmp, 1.0)
        # m22abcd (cdcd,dcdc)
        if isinstance(self.lf, CholeskyLinalgFactory):
            tmp = gpqpq.copy(occ, act, occ, act)
            tmp.iscale(0.5)
            gpqrq.contract("abc,ac->cb", t_ia, tmp, factor=-1.0, **ovv)
            tmpoovv = eri.contract("abcd->abcd", **oovv, select="einsum")
            t_iajb.contract("abcd,acbd->bd", tmpoovv, tmp)
            tmpoovv = None
        else:
            m22abcd = self.from_cache("m22abcd")
            tmp = m22abcd.contract("abab->ab", clear=True, select="einsum")
            if self.dump_cache:
                self.cache.dump("m22abcd")
        h_diag_d.iadd_expand_two_to_four("bd->abcd", tmp, 1.0)
        h_diag_d.iadd_expand_two_to_four("db->abcd", tmp, 1.0)

        return h_diag_s, h_diag_d

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
        t_ia = self.checkpoint["t_1"]
        t_iajb = self.checkpoint["t_2"]
        tco = {"select": self.tco}
        occ = self.nacto
        vir = self.nactv
        #
        # Get ranges
        #
        ov2 = self.get_range("ov", offset=2)
        #
        # Get auxiliary matrices and effective Hamiltonian terms
        #
        fock = self.from_cache("fock")
        looov = self.from_cache("looov")
        miaka = self.from_cache("miaka")
        miaic = self.from_cache("miaic")
        m1kald = self.from_cache("m1kald")
        m1iald = self.from_cache("m1iald")
        m21ijak = self.from_cache("m21ijak")
        m22ki = self.from_cache("m22ki")
        m22ac = self.from_cache("m22ac")
        m22ijkl = self.from_cache("m22ijkl")
        #
        # Calculate sigma vector (H.bvector)_kc
        #
        end_s = occ * vir + 1
        # singles
        sigma_s = self.lf.create_two_index(occ, vir)
        to_s = {"out": sigma_s, "clear": False, "select": self.tco}
        bv_s = self.dense_lf.create_two_index(occ, vir)
        # doubles
        sigma_d = self.dense_lf.create_four_index(occ, vir, occ, vir)
        to_d = {"out": sigma_d, "clear": False, "select": self.tco}
        bv_d = self.dense_lf.create_four_index(occ, vir, occ, vir)
        #
        # reshape bvector
        #
        bv_s.assign(bvector, begin2=1, end2=end_s)
        bv_d.assign_triu(bvector, begin4=end_s)
        bv_p = bv_d.contract("abab->ab", clear=True, select="einsum")
        bv_d.iadd_transpose((2, 3, 0, 1))
        self.set_seniority_0(bv_d, bv_p)
        #
        # Reference vector R_0
        #
        # X0,kc rkc
        sum0_ = bv_s.contract("ab,ab", fock, **ov2) * 2.0
        tmp = self.lf.create_two_index(occ, vir)
        loovv = self.from_cache("loovv")
        loovv.contract("abcd,bd->ac", t_ia, tmp)
        sum0_ += bv_s.contract("ab,ab", tmp) * 2.0
        sum0_ += bv_d.contract("abcd,acbd", loovv)
        if self.dump_cache:
            self.cache.dump("loovv")
        #
        # Single excitations
        #
        # Xkcld rld
        sigma_s.clear()
        miakc = self.from_cache("miakc")
        miakc.contract("abcd,cd->ab", bv_s, **to_s)  # iakc,kc->ia
        if self.dump_cache:
            self.cache.dump("miakc")
        # Xkclc rlc
        miaka.contract("ab,bc->ac", bv_s, **to_s)
        # Xkckd rkd
        bv_s.contract("ab,cb->ac", miaic, **to_s)  # ic,ac->ia
        # Xlkic rlakc
        m1kald.contract("abcd,aebd->ce", bv_d, **to_s)  # klid,kald->ia
        # Xkacd rkcid
        self.get_effective_hamiltonian_term_kcda(bv_d, sigma_s)
        # Xld Rkcld
        bv_d.contract("abcd,cd->ab", m1iald, **to_s, factor=2.0)
        bv_d.contract("abcd,ad->cb", m1iald, **to_s, factor=-1.0)
        #
        # All remaining double excitations
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
        if self.dump_cache:
            self.cache.dump("loovv")
        t_iajb.contract("abcd,ce->abed", tmp, **to_d, factor=-1.0)
        # (18) P Xknclmd rldmf
        # Lklcd rkbld; cb t_iajc
        tmp = self.lf.create_two_index(vir)
        loovv = self.from_cache("loovv")
        loovv.contract("abcd,aebd->ce", bv_d, tmp, **tco)
        if self.dump_cache:
            self.cache.dump("loovv")
        t_iajb.contract("abcd,de->abce", tmp, **to_d, factor=-1.0)
        tmp = None
        #
        # Coupling to singles
        # P Xijak rkb
        m21ijak.contract(
            "abcd,de->acbe", bv_s, sigma_d, **tco
        )  # ijak,kb->iajb
        # P Xabcj ric
        self.get_effective_hamiltonian_term_abcj(bv_s, sigma_d)
        # P Xijabkc rkc
        self.get_effective_hamiltonian_term_ijabkc(bv_s, sigma_d)
        tmp = self.lf.create_two_index(occ)
        looov.contract("abcd,bd->ac", bv_s, tmp, **tco)  # lkjc,kc->lj
        t_iajb.contract(
            "abcd,ce->abed", tmp, **to_d, factor=-1.0
        )  # ialb,lj->iajb

        return sum0_, sigma_s, sigma_d, bv_s, bv_d

    def update_hamiltonian(self, mo1, mo2):

        """Derive all auxiliary matrices. Derive all matrices that are common
        for all EOM-LCCSD flavours.

        **Arguments:**

        mo1, mo2
             one- and two-electron integrals to be sorted.
        """
        t_ia = self.checkpoint["t_1"]
        t_iajb = self.checkpoint["t_2"]
        tco = {"select": self.tco}
        occ = self.nacto
        vir = self.nactv
        act = self.nact
        #
        # Get ranges
        #
        ov2 = self.get_range("ov", offset=2)
        oo2 = self.get_range("oo", offset=2)
        vv2 = self.get_range("vv", offset=2)
        ov4 = self.get_range("ov", offset=4)
        oooo = self.get_range("oooo")
        ooov = self.get_range("ooov")
        oovo = self.get_range("oovo")
        oovv = self.get_range("oovv")
        ovvo = self.get_range("ovvo")
        ovov = self.get_range("ovov")
        ovvv = self.get_range("ovvv")
        vovv = self.get_range("vovv")
        vvvv = self.get_range("vvvv")
        oovv4 = self.get_range("oovv", offset=4)
        ovvv4 = self.get_range("ovvv", offset=4)
        #
        # Get auxiliary matrices
        #
        #
        # <pq|pq> and 2<pq|pq>-<pq|pq>
        #
        gpqpq = self.init_cache("gpqpq", act, act)
        mo2.contract("abab->ab", gpqpq, select="einsum")
        lpqpq = gpqpq.copy()
        lpqpq.iscale(2.0)
        mo2.contract("abba->ab", lpqpq, factor=-1.0, select="einsum")
        #
        # <pq|rq> and <pq||rq>+<pq|rq>
        #
        gpqrq = self.init_cache("gpqrq", act, act, act)
        mo2.contract("abcb->abc", gpqrq, select="einsum")
        lpqrq = self.init_cache("lpqrq", act, act, act)
        lpqrq.assign(gpqrq)
        lpqrq.iscale(2.0)
        #
        # <pq|rr>
        # This is slow but faster than the alternative and we do it only once
        gpqrr = self.lf.create_three_index(act)
        mo2.contract("abcc->abc", gpqrr, select="einsum")
        #
        # add exchange part to lpqrq using gpqrr
        #
        tmp3 = self.lf.create_three_index(self.nact)
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
            # <kb|cd> tka
            mo2.contract(
                "abcd,ae->ebcd", t_ia, m22abcd, factor=-1.0, **ovvv, **tco
            )
            # tkalb <kl|cd>
            t_iajb.contract(
                "abcd,acef->bdef", mo2, m22abcd, factor=0.5, **tco, **oovv4
            )
            if self.dump_cache:
                self.cache.dump("m22abcd")
        #
        # <oo||ov>+<oo|ov>
        #
        looov = self.init_cache("looov", occ, occ, occ, vir)
        mo2.contract("abcd->abcd", looov, factor=2.0, **ooov, select="einsum")
        # temporary matrix needed
        gooov = looov.copy()
        mo2.contract("abcd->abdc", looov, factor=-1.0, **oovo, select="einsum")
        #
        # <ov||vv>+<ov|vv>
        #
        if not isinstance(self.lf, CholeskyLinalgFactory):
            lovvv = self.init_cache("lovvv", occ, vir, vir, vir)
            mo2.contract(
                "abcd->abcd", lovvv, factor=2.0, **ovvv, select="einsum"
            )
            # temporary matrix needed
            mo2.contract(
                "abcd->abdc", lovvv, factor=-1.0, **ovvv, select="einsum"
            )
            if self.dump_cache:
                self.cache.dump("lovvv")
        #
        # Aux matrix for Mia,ka (ik)
        # (2) X_ik
        miaka = self.init_cache("miaka", occ, occ)
        # fki
        miaka.iadd(fock, -1.0, **oo2)
        # tie fke
        t_ia.contract("ab,cb->ac", fock, out=miaka, factor=-1.0, **ov2, **tco)
        # -L_kmie t_me
        looov.contract("abcd,bd->ca", t_ia, miaka, factor=-1.0, **tco)
        # -L_lkdc tldic / -Gikee cie
        loovv = self.from_cache("loovv")
        t_iajb.contract("abcd,aebd->ce", loovv, miaka, factor=-1.0, **tco)
        if self.dump_cache:
            self.cache.dump("loovv")
        #
        # Aux matrix for Mia,ic (ac)
        # (3) X_ac
        miaic = self.init_cache("miaic", vir, vir)
        # fac
        miaic.iadd(fock, 1.0, **vv2)
        # tma fmc
        t_ia.contract("ab,ac->bc", fock, miaic, factor=-1.0, **ov2, **tco)
        # L_maec t_me
        mo2.contract("abcd,ac->bd", t_ia, miaic, factor=2.0, **ovvv, **tco)
        mo2.contract("abcd,ad->bc", t_ia, miaic, factor=-1.0, **ovvv, **tco)
        # tldka -L_lkdc / -Gacmm cma
        loovv = self.from_cache("loovv")
        t_iajb.contract("abcd,acbe->de", loovv, miaic, factor=-1.0, **tco)
        if self.dump_cache:
            self.cache.dump("loovv")
        #
        # Aux matrix for Mia,kc (iakc)
        # (1) X_iakc
        miakc = self.init_cache("miakc", occ, vir, occ, vir)
        # L_icak
        mo2.contract("abcd->acdb", miakc, factor=2.0, **ovvo, select="einsum")
        mo2.contract("abcd->adcb", miakc, factor=-1.0, **ovov)
        # L_mkic t_ma
        looov.contract("abcd,ae->cebd", t_ia, miakc, factor=-1.0, **tco)
        # L_kacd t_id
        mo2.contract("abcd,ed->ebac", t_ia, miakc, factor=2.0, **ovvv, **tco)
        mo2.contract("abcd,ec->ebad", t_ia, miakc, factor=-1.0, **ovvv, **tco)
        # L_lkdc (2t_iald-tidla) / Likac cia
        loovv = self.from_cache("loovv")
        t_iajb.contract("abcd,cedf->abef", loovv, miakc, factor=2.0, **tco)
        t_iajb.contract("abcd,cebf->adef", loovv, miakc, factor=-1.0, **tco)
        if self.dump_cache:
            self.cache.dump("loovv")
            self.cache.dump("miakc")
        #
        # Aux matrix for Mia,kald (klid)
        # (6) X_klci
        m1kald = self.init_cache("m1kald", occ, occ, occ, vir)
        # L_klid
        looov.contract("abcd->abcd", m1kald, factor=-1.0, select="einsum")
        # L_kled tie
        loovv = self.from_cache("loovv")
        loovv.contract("abcd,ec->abed", t_ia, m1kald, factor=-1.0, **tco)
        if self.dump_cache:
            self.cache.dump("loovv")
        #
        # Aux matrix for Mia,kcid (Xkcda)
        # (7) X_kcda (saved as kacd)
        if not isinstance(self.lf, CholeskyLinalgFactory):
            x1kcda = self.init_cache("x1kcda", occ, vir, vir, vir)
            # L_kacd
            lovvv = self.from_cache("lovvv")
            lovvv.contract("abcd->abcd", x1kcda, select="einsum")
            if self.dump_cache:
                self.cache.dump("lovvv")
            # L_lkdc tla
            loovv = self.from_cache("loovv")
            loovv.contract("abcd,ae->bedc", t_ia, x1kcda, factor=-1.0, **tco)
            if self.dump_cache:
                self.cache.dump("x1kcda")
                self.cache.dump("loovv")
        #
        # Aux matrix for Mia,iald (ld)
        # (4/5) X_kc
        m1iald = self.init_cache("m1iald", occ, vir)
        # F_ld
        m1iald.iadd(fock, 1.0, **ov2)
        # L_mled tme
        loovv = self.from_cache("loovv")
        loovv.contract("abcd,ac->bd", t_ia, m1iald, **tco)
        if self.dump_cache:
            self.cache.dump("loovv")
        #
        # Aux matrix for M21iajbjc (icab)
        # (8) X_abcj
        if not isinstance(self.lf, CholeskyLinalgFactory):
            m21icab = self.init_cache("m21icab", occ, vir, vir, vir)
            # <ic|ab>
            mo2.contract("abcd->abcd", m21icab, **ovvv, select="einsum")
            # Flc t_ialb
            t_iajb.contract(
                "abcd,ce->aebd", fock, m21icab, factor=-1.0, **ov4, **tco
            )
            # <ic|al> tlb
            mo2.contract(
                "abcd,de->abce", t_ia, m21icab, factor=-1.0, **ovvo, **tco
            )
            # <ic|lb> tla
            mo2.contract(
                "abcd,ce->abed", t_ia, m21icab, factor=-1.0, **ovov, **tco
            )
            # <dc|ab> tid
            mo2.contract("abcd,ea->ebcd", t_ia, m21icab, **vvvv, **tco)
            # <lm|ic> tlamb
            t_iajb.contract(
                "abcd,acef->efbd", gooov, m21icab, factor=0.5, **tco
            )
            # t_iald Llbdc
            lovvv = self.from_cache("lovvv")
            t_iajb.contract("abcd,cedf->afbe", lovvv, m21icab, **tco)
            if self.dump_cache:
                self.cache.dump("lovvv")
            # tidla <lb|dc>
            t_iajb.contract(
                "abcd,cebf->afde", mo2, m21icab, factor=-1.0, **tco, **ovvv4
            )
            # tidlb <la|cd>
            t_iajb.contract(
                "abcd,cefb->afed", mo2, m21icab, factor=-1.0, **tco, **ovvv4
            )
        #
        # Aux matrix for M21iajb,kb (ijak)
        # (9) X_ijkb
        m21ijak = self.init_cache("m21ijak", occ, occ, vir, occ)
        # <ij|ak>
        mo2.contract(
            "abcd->abcd", m21ijak, factor=-1.0, **oovo, select="einsum"
        )
        # Fkd t_iajd
        t_iajb.contract(
            "abcd,ed->acbe", fock, m21ijak, factor=-1.0, **ov4, **tco
        )
        # <id|ak> tjd
        mo2.contract(
            "abcd,eb->aecd", t_ia, m21ijak, factor=-1.0, **ovvo, **tco
        )
        # <jd|ka> tid
        mo2.contract(
            "abcd,eb->eadc", t_ia, m21ijak, factor=-1.0, **ovov, **tco
        )
        # <ij|lk> tla
        mo2.contract("abcd,ce->abed", t_ia, m21ijak, **oooo, **tco)
        # tidjc <ak|dc>
        # temporary (ijak)
        mo2.contract(
            "abcd,ecfd->efab", t_iajb, m21ijak, factor=-1.0, **vovv, **tco
        )
        # t_iald Lkljd
        t_iajb.contract("abcd,ecfd->afbe", looov, m21ijak, factor=-1.0, **tco)
        # tidla <kl|jd>
        t_iajb.contract("abcd,ecfb->afde", gooov, m21ijak, factor=0.5, **tco)
        # tlajd <lk|id>
        t_iajb.contract("abcd,aefd->fcbe", gooov, m21ijak, factor=0.5, **tco)
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
        # Lkbcd tjd
        mo2.contract("abcd,ed->ebac", t_ia, m22jbkc, factor=2.0, **ovvv, **tco)
        mo2.contract(
            "abcd,ec->ebad", t_ia, m22jbkc, factor=-1.0, **ovvv, **tco
        )
        # Llkjc tlb
        looov.contract("abcd,ae->cebd", t_ia, m22jbkc, factor=-1.0, **tco)
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
        # <ak|dc> tid
        mo2.contract(
            "abcd,ec->bade", t_ia, m22kadi, factor=-1.0, **vovv, **tco
        )
        # <mk|id> tma
        mo2.contract("abcd,ae->bedc", t_ia, m22kadi, **ooov, **tco)
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
            self.cache.dump("loovv")
        #
        # Aux matrix for M22iajb,kjad (kbid)
        # (15) X_ajkc
        m22kbid = self.init_cache("m22kbid", occ, vir, occ, vir)
        # <kb|id>
        mo2.contract(
            "abcd->abcd", m22kbid, factor=-1.0, **ovov, select="einsum"
        )
        # <kb|ed> tie
        mo2.contract(
            "abcd,ec->abed", t_ia, m22kbid, factor=-1.0, **ovvv, **tco
        )
        # <km|id> tmb
        mo2.contract("abcd,be->aecd", t_ia, m22kbid, **ooov, **tco)
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
        # <kl|ej> tie
        mo2.contract("abcd,ec->edab", t_ia, m22ijkl, **oovo, **tco)
        # tiejf <kl|ef>
        goovv = self.from_cache("goovv")
        t_iajb.contract("abcd,efbd->acef", goovv, m22ijkl, factor=0.5, **tco)
        if self.dump_cache:
            self.cache.dump("goovv")
        #
        # Aux matrix for M22iajb,kjab (ki) and Mp2iaia,kiaa (ki)
        # (11) X_jk
        m22ki = self.init_cache("m22ki", occ, occ)
        # fki
        m22ki.iadd(fock, -1.0, **oo2)
        # tie fke
        t_ia.contract("ab,cb->ca", fock, m22ki, factor=-1.0, **ov2, **tco)
        # Lkmie tme
        looov.contract("abcd,bd->ac", t_ia, m22ki, factor=-1.0, **tco)
        # Lmkef tmeif
        loovv = self.from_cache("loovv")
        loovv.contract("abcd,aced->be", t_iajb, m22ki, factor=-1.0, **tco)
        if self.dump_cache:
            self.cache.dump("loovv")
        #
        # Aux matrix for M22iajb,ijcb (ac) and Mp2iaia,iica (ac)
        # (12) X_bc
        m22ac = self.init_cache("m22ac", vir, vir)
        # fac
        m22ac.iadd(fock, 1.0, **vv2)
        # tma fmc
        t_ia.contract("ab,ac->bc", fock, m22ac, factor=-1.0, **ov2, **tco)
        # Lmaec tme
        mo2.contract("abcd,ac->bd", t_ia, m22ac, factor=2.0, **ovvv, **tco)
        mo2.contract("abcd,ad->bc", t_ia, m22ac, factor=-1.0, **ovvv, **tco)
        # Lmnec tmena
        loovv = self.from_cache("loovv")
        loovv.contract("abcd,acbe->ed", t_iajb, m22ac, factor=-1.0, **tco)
        if self.dump_cache:
            self.cache.dump("loovv")

        gc.collect()

    #
    # Expensive effective Hamiltonian terms
    #

    def get_effective_hamiltonian_term_kcda(self, bv_d, sigma):
        """Compute effective Hamiltonian term involving an ovvv block

        **Arguments:**

        :bv_d: (DenseFourIndex) the current approximation to the CI doubles
               coefficient

        :sigma: (DenseTwoIndex) the output sigma vector
        """
        to_s = {"out": sigma, "clear": False, "select": self.tco}
        tco = {"select": self.tco}
        t_ia = self.checkpoint["t_1"]
        if isinstance(self.lf, CholeskyLinalgFactory):
            eri = self.from_cache("mo2")
            ovvv = self.get_range("ovvv")
            # Lkacd rkcid
            eri.contract("abcd,aced->eb", bv_d, **to_s, factor=2.0, **ovvv)
            eri.contract("abcd,adec->eb", bv_d, **to_s, factor=-1.0, **ovvv)
            # Lklcd tla rkcid
            tmp = self.lf.create_two_index(self.nacto)
            loovv = self.from_cache("loovv")
            loovv.contract("abcd,aced->be", bv_d, tmp, **tco)
            tmp.contract("ab,ac->bc", t_ia, **to_s, factor=-1.0)
            if self.dump_cache:
                self.cache.dump("loovv")
        else:
            x1kcda = self.from_cache("x1kcda")
            x1kcda.contract("abcd,aced->eb", bv_d, **to_s)  # ladc,ldic
            if self.dump_cache:
                self.cache.dump("x1kcda")

    def get_effective_hamiltonian_term_abcd(self, bv_d, sigma):
        """Compute effective Hamiltonian term involving an vvvv block

        **Arguments:**

        :bv_d: (DenseFourIndex) the current approximation to the CI doubles
               coefficient

        :sigma: (DenseFourIndex) the output sigma vector
        """
        to_d = {"out": sigma, "clear": False, "select": self.tco}
        if isinstance(self.lf, CholeskyLinalgFactory):
            t_ia = self.checkpoint["t_1"]
            t_iajb = self.checkpoint["t_2"]
            eri = self.from_cache("mo2")
            oovv = self.get_range("oovv")
            ovvv = self.get_range("ovvv")
            vvvv = self.get_range("vvvv")
            occ = self.nacto
            vir = self.nactv
            tco = {"select": self.tco}
            # (16) Xabcd ricjd
            # <abcd>
            eri.contract("abcd,ecfd->eafb", bv_d, **to_d, factor=0.5, **vvvv)
            # -<kbcd> tka ricjd
            tmp = self.dense_lf.create_four_index(occ, occ, vir, occ)
            eri.contract("abcd,ecfd->efba", bv_d, tmp, **ovvv, **tco)
            tmp.contract("abcd,de->aebc", t_ia, **to_d, factor=-1.0)
            # <klcd> tkalb ricjd
            tmp = self.dense_lf.create_four_index(occ, occ, occ, occ)
            eri.contract("abcd,ecfd->efab", bv_d, tmp, **oovv, **tco)
            tmp.contract("abcd,cedf->aebf", t_iajb, **to_d, factor=0.5)
        else:
            m22abcd = self.from_cache("m22abcd")
            bv_d.contract("abcd,efbd->aecf", m22abcd, **to_d)
            if self.dump_cache:
                self.cache.dump("m22abcd")

    def get_effective_hamiltonian_term_abcj(self, bv_s, sigma):
        """Compute effective Hamiltonian term involving an ovvv block

        **Arguments:**

        :bv_s: (DenseTwoIndex) the current approximation to the CI singles
               coefficient

        :sigma: (DenseFourIndex) the output sigma vector
        """
        to_d = {"out": sigma, "clear": False, "select": self.tco}
        if isinstance(self.lf, CholeskyLinalgFactory):
            t_ia = self.checkpoint["t_1"]
            t_iajb = self.checkpoint["t_2"]
            fock = self.from_cache("fock")
            eri = self.from_cache("mo2")
            ov2 = self.get_range("ov", offset=2)
            oovo = self.get_range("oovo")
            vovo = self.get_range("vovo")
            ovvo = self.get_range("ovvo")
            ovvv = self.get_range("ovvv")
            vovv = self.get_range("vovv")
            vvvv = self.get_range("vvvv")
            occ = self.nacto
            vir = self.nactv
            tco = {"select": self.tco}
            # <ja|bc> tic
            eri.contract("abcd,ed->ebac", bv_s, **to_d, **ovvv)
            # NOTE: Try to improve
            # <ab|cd> ric tjd
            eri.contract("abcd,ec,fd->eafb", bv_s, t_ia, **to_d, **vvvv)
            # NOTE: Try to improve
            # <jc|bk> ric tka
            eri.contract(
                "abcd,eb,df->efac", bv_s, t_ia, **to_d, factor=-1.0, **ovvo
            )
            # -ric fkc tkajb
            tmp = self.lf.create_two_index(occ, occ)
            bv_s.contract("ab,cb->ac", fock, tmp, **ov2, **tco)  # ik
            t_iajb.contract("abcd,ea->ebcd", tmp, **to_d, factor=-1.0)
            # NOTE: Try to improve
            # -<ak|cj> ric tkb
            eri.contract(
                "abcd,ec,bf->eadf", bv_s, t_ia, **to_d, factor=-1.0, **vovo
            )
            # Lladc ric tldjb
            tmp = self.dense_lf.create_four_index(occ, vir, occ, vir)
            eri.contract("abcd,ed->ebac", bv_s, tmp, factor=2.0, **ovvv, **tco)
            eri.contract(
                "abcd,ec->ebad", bv_s, tmp, factor=-1.0, **ovvv, **tco
            )  # iald
            tmp.contract("abcd,efcd->abef", t_iajb, **to_d)
            # NOTE: Try to improve
            # -<ak|cd> ric tjdkb
            eri.contract(
                "abcd,ec,fdbg->eafg", bv_s, t_iajb, **to_d, factor=-1.0, **vovv
            )
            # -<bk|dc> ric tjdka
            tmp = self.dense_lf.create_four_index(occ, occ, vir, vir)
            eri.contract("abcd,ed->ebac", bv_s, tmp, **vovv, **tco)  # ikbd
            tmp.contract("abcd,edbf->afec", t_iajb, **to_d, factor=-1.0)
            tmp = None
            # <kl|cj> ric tkalb
            tmp = self.dense_lf.create_four_index(occ, occ, occ, occ)
            eri.contract("abcd,ec->edab", bv_s, tmp, **oovo, **tco)  # ijkl
            tmp.contract("abcd,cedf->aebf", t_iajb, **to_d)
            tmp = None
        else:
            m21icab = self.from_cache("m21icab")
            # icab,jc->iajb
            m21icab.contract("abcd,eb->aced", bv_s, **to_d)
            if self.dump_cache:
                self.cache.dump("m21icab")

    def get_effective_hamiltonian_term_ijabkc(self, bv_s, sigma):
        """Compute effective Hamiltonian term involving an ovvv block

        **Arguments:**

        :bv_s: (DenseTwoIndex) the current approximation to the CI singles
               coefficient

        :sigma: (DenseFourIndex) the output sigma vector
        """
        t_iajb = self.checkpoint["t_2"]
        tmp = self.lf.create_two_index(self.nactv)
        to_d = {"out": sigma, "clear": False, "select": self.tco}
        to_t = {"out": tmp, "clear": False, "select": self.tco}
        if isinstance(self.lf, CholeskyLinalgFactory):
            ovvv = self.get_range("ovvv")
            eri = self.from_cache("mo2")
            # kbce,kc->be
            eri.contract("abcd,ac->bd", bv_s, **to_t, factor=2.0, **ovvv)
            # kbce,kc->be
            eri.contract("abcd,ad->bc", bv_s, **to_t, factor=-1.0, **ovvv)
        else:
            lovvv = self.from_cache("lovvv")
            # kbce,kc->be
            lovvv.contract("abcd,ac->bd", bv_s, **to_t)
            if self.dump_cache:
                self.cache.dump("lovvv")
        # iaje,be->iaj
        t_iajb.contract("abcd,ed->abce", tmp, **to_d)
