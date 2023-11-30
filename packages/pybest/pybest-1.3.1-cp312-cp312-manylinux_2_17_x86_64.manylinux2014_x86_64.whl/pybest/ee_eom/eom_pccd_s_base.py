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
"""Equation of Motion Coupled Cluster implementations of a common base class of
   EOM-pCCD+S and EOM-pCCD-CCS, that is, pCCD with single excitations.

   Child class of REOMCC class.
"""

import gc

import numpy as np

from pybest.auxmat import get_fock_matrix
from pybest.ee_eom.eom_base import REOMCC
from pybest.exceptions import ArgumentError
from pybest.log import log
from pybest.utils import unmask


class REOMpCCDSBase(REOMCC):
    """Base class for EOM-pCCD+S and EOM-pCCD-CCS."""

    long_name = ""
    acronym = ""
    reference = "pCCD"
    singles_ref = ""
    pairs_ref = True
    doubles_ref = False
    singles_ci = True
    pairs_ci = True
    doubles_ci = False

    @property
    def dimension(self):
        """The number of unknowns (total number of excited states incl. ground
        state) for each EOM-CC flavor. Variable used by the Davidson module."""
        return 2 * self.nacto * self.nactv + 1

    def unmask_args(self, *args, **kwargs):
        """Extract all tensors/quantities from function arguments and keyword
        arguments. Arguments/kwargs have to contain:
        * t_p: some CC T_p amplitudes
        """
        #
        # t_p
        #
        t_p = unmask("t_p", *args, **kwargs)
        if t_p is not None:
            self.checkpoint.update("t_p", t_p)
        else:
            raise ArgumentError("Cannot find Tp amplitudes.")
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
        # Add citations
        #
        log.cite(
            "the EOM-pCCD-based methods",
            "boguslawski2016a",
            "boguslawski2017c",
        )
        #
        # Remove reference state index
        #
        index_ = index - 1
        #
        # Either single or pair excitation
        #
        pairs = index_ - self.nacto * self.nactv >= 0
        if pairs:
            index_ -= self.nacto * self.nactv
        #
        # Get excitation
        #
        i, a = self.get_index_s(index_)
        # Account for frozen core, occupied orbitals, and numpy index convention
        i, a = i + self.ncore + 1, a + self.ncore + self.nacto + 1
        #
        # Print contribution
        #
        if pairs:
            log(
                f"          t_iaia:  ({i:3d},{a:3d},{i:3d},{a:3d})   {ci_vector[index]: 1.5f}"
            )
        else:
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
            f"          weight(p): {np.dot(ci_vector[nov:], ci_vector[nov:]): 1.5f}"
        )

    def build_full_hamiltonian(self):
        """Construct full Hamiltonian matrix used in exact diagonalization"""
        t_p = self.checkpoint["t_p"]
        eom_ham = self.lf.create_two_index(self.dimension)
        occ = self.nacto
        vir = self.nactv
        #
        # effective Hamiltonian matrix elements
        #
        fock = self.from_cache("fock")
        G_ppqq = self.from_cache("gppqq")
        L_pqrq = self.from_cache("lpqrq")
        miaka = self.from_cache("miaka")
        miaic = self.from_cache("miaic")
        m1kald = self.from_cache("m1kald")
        x1_kcdd = self.from_cache("x1kdda")
        m1iald = self.from_cache("m1iald")
        mpiaka = self.from_cache("mpiaka")
        mpiaic = self.from_cache("mpiaic")
        mppiaka = self.from_cache("mppiaka")
        mppiaic = self.from_cache("mppiaic")
        mppia = self.from_cache("mppia")
        # get slices/views thereof
        g_kc = G_ppqq.copy(end0=occ, begin1=occ)
        x1_kcll = m1kald.contract("aabc->bca", clear=True, select="einsum")
        mp_kdc = mpiaic.contract("abc->bca", clear=True, select="einsum")
        mp_lck = mpiaka.contract("abc->cab", clear=True, select="einsum")
        #
        # Get ranges
        #
        ovv = self.get_range("ovv")
        oov = self.get_range("oov")
        #
        # temporary storage
        #
        temp_h = self.dense_lf.create_four_index(occ, vir, occ, vir)
        #
        # some dimensions
        #
        end_s = occ * vir + 1
        shape = (occ * vir, occ * vir)
        #
        # Single excitations:
        #
        # H_0,kc
        eom_ham.assign(
            2.0 * fock.array[:occ, occ:].ravel(), end0=1, begin1=1, end1=end_s
        )
        # H_kc,kd
        temp_h.iadd_expand_two_to_four("bc->abac", miaic)
        # H_kc,lc
        temp_h.iadd_expand_two_to_four("ac->abcb", miaka)
        # H_kc,ld
        miakc = self.from_cache("miakc")
        temp_h.iadd(miakc)
        if self.dump_cache:
            self.cache.dump("miakc")
        # Assign to eom_ham
        # reshape abcd->(ab)(cd)
        tmp = temp_h.reshape(shape)
        # assign
        eom_ham.iadd(tmp, begin0=1, end0=end_s, begin1=1, end1=end_s)
        del tmp
        #
        # coupling singles-pairs <S|P>
        #
        # H_kc,kkcc
        tmp = self.lf.create_two_index(occ * vir)
        tmp.iadd_diagonal(m1iald.ravel())
        eom_ham.iadd(tmp, begin0=1, end0=end_s, begin1=end_s)
        # H_kc,kkdd
        temp_h.clear()
        temp_h.iadd_expand_three_to_four("abc->abac", x1_kcdd)
        # H_kc,llcc
        temp_h.iadd_expand_three_to_four("abc->abcb", x1_kcll)
        # Assign to eom_ham
        # reshape abcd->(ab)(cd)
        tmp = temp_h.reshape(shape)
        # assign (S,P)
        eom_ham.iadd(tmp, begin0=1, end0=end_s, begin1=end_s)
        del tmp
        #
        # Pair excitations:
        #
        # Diagonal elements H_kkcc,kkcc
        eom_ham.iadd_diagonal(mppia.ravel(), begin0=end_s)
        # H_0,kkcc
        eom_ham.iadd_t(g_kc.ravel(), end0=1, begin1=end_s)
        # H_kkcc,kkdd
        temp_h.clear()
        temp_h.iadd_expand_three_to_four("abc->abac", mppiaic)
        # H_kkcc,llcc
        temp_h.iadd_expand_three_to_four("abc->abcb", mppiaka)
        # Assign to eom_ham
        tmp = temp_h.reshape(shape)
        eom_ham.iadd(tmp, begin0=end_s, begin1=end_s)
        del tmp
        #
        # coupling pairs-singles <P|S>
        #
        # H_kkdd,kc
        temp_h.clear()
        temp_h.iadd_expand_three_to_four("abc->abac", mp_kdc)
        # H_llcc,kc
        temp_h.iadd_expand_three_to_four("abc->abcb", mp_lck)
        # H_lldd,kc
        L_pqrq.contract("abc,db->dbac", t_p, temp_h, factor=2.0, **ovv)
        L_pqrq.contract("abc,bd->bdac", t_p, temp_h, factor=-2.0, **oov)
        # Assign to eom_ham
        # reshape abcd->(ab)(cd)
        tmp = temp_h.reshape(shape)
        # assign (P,S)
        eom_ham.iadd(tmp, begin0=end_s, begin1=1, end1=end_s)
        del tmp

        return eom_ham

    def compute_h_diag(self, *args):

        """Used by Davidson module for pre-conditioning

        **Arguments:**

        args:
            required for Davidson module (not used here)
        """
        occ = self.nacto
        vir = self.nactv
        end_s = vir * occ + 1
        eom_ham_diag = self.lf.create_one_index(self.dimension, label="h_diag")
        #
        # Get auxiliary matrices
        #
        miaka = self.from_cache("miaka")
        miaic = self.from_cache("miaic")
        mppia = self.from_cache("mppia")
        mppiaic = self.from_cache("mppiaic")
        mppiaka = self.from_cache("mppiaka")
        # temp storage
        tmp = self.lf.create_two_index(occ, vir)
        #
        # Singles
        #
        miakc = self.from_cache("miakc")
        miakc.contract("abab->ab", out=tmp, clear=True, select="einsum")
        if self.dump_cache:
            self.cache.dump("miakc")
        tmp_ = miaka.copy_diagonal()
        tmp.iadd_expand_one_to_two("a->ab", tmp_, 1.0)
        tmp_ = miaic.copy_diagonal()
        tmp.iadd_expand_one_to_two("b->ab", tmp_, 1.0)
        # assign to h_diag
        eom_ham_diag.assign(tmp.ravel(), begin0=1, end0=end_s)
        #
        # Pairs
        #
        tmp = mppia.copy()
        mppiaic.contract("abb->ab", out=tmp, factor=1.0, select="einsum")
        mppiaka.contract("aba->ab", out=tmp, factor=1.0, select="einsum")
        # assign to h_diag
        eom_ham_diag.assign(tmp.ravel(), begin0=end_s)

        return eom_ham_diag

    def build_subspace_hamiltonian(self, bvector, hdiag, *args):
        """
        Used by Davidson module to construct subspace Hamiltonian. Includes all
        terms that are similar for all EOM-pCCD flavours with single excitations.

        **Arguments:**

        bvector:
            (OneIndex object) contains current approximation to CI coefficients

        hdiag:
            Diagonal Hamiltonian elements required in Davidson module (not used
            here)

        args:
            Set of arguments passed by the Davidson module (not used here)
        """
        t_p = self.checkpoint["t_p"]
        #
        # Get ranges
        #
        ov2 = self.get_range("ov", offset=2)
        oov = self.get_range("oov")
        ovv = self.get_range("ovv")
        occ = self.nacto
        vir = self.nactv
        #
        # Get auxiliary matrices
        #
        fock = self.from_cache("fock")
        G_ppqq = self.from_cache("gppqq")
        L_pqrq = self.from_cache("lpqrq")
        miaka = self.from_cache("miaka")
        miaic = self.from_cache("miaic")
        m1kald = self.from_cache("m1kald")
        x1kdda = self.from_cache("x1kdda")
        m1iald = self.from_cache("m1iald")
        mpiaka = self.from_cache("mpiaka")
        mpiaic = self.from_cache("mpiaic")
        mppiaka = self.from_cache("mppiaka")
        mppiaic = self.from_cache("mppiaic")
        mppia = self.from_cache("mppia")
        #
        # Calculate sigma vector (H.bvector)_kc
        #
        end_s = vir * occ + 1
        bv_s = self.dense_lf.create_two_index(occ, vir)
        bv_p = self.dense_lf.create_two_index(occ, vir)
        #
        # reshape bvector
        #
        bv_s.assign(bvector, begin2=1, end2=end_s)
        bv_p.assign(bvector, begin2=end_s)
        #
        # Full sigma vector and temporary storage sigma_
        #
        sigma = self.lf.create_one_index(self.dimension)
        sigma_ = self.lf.create_two_index(occ, vir)
        #
        # Reference vector R_0
        #
        # X0,kc rkc
        sum0_ = bv_s.contract("ab,ab", fock, **ov2) * 2.0
        sum0_ += bv_p.contract("ab,ab", G_ppqq, **ov2)
        sigma.set_element(0, sum0_)
        #
        # Single excitations
        #
        # Xkcld rld
        miakc = self.from_cache("miakc")
        miakc.contract("abcd,cd->ab", bv_s, sigma_, clear=True)
        if self.dump_cache:
            self.cache.dump("miakc")
        # Xkclc rlc
        miaka.contract("ab,bc->ac", bv_s, sigma_)
        # Xkckd rkd
        bv_s.contract("ab,cb->ac", miaic, sigma_)
        # Xllkc rlclc
        m1kald.contract("aabc,ac->bc", bv_p, sigma_)
        # Xclde rkdle
        x1kdda.contract("abc,ac->ab", bv_p, sigma_)
        # Xkc rkckc
        sigma_.iadd_mult(m1iald, bv_p, 1.0)
        # Assign to sigma vector
        sigma.assign(sigma_.ravel(), begin0=1, end0=end_s)
        #
        # Pair excitations
        #
        mppiaka.contract("abc,cb->ab", bv_p, sigma_, clear=True)
        # Xcd rkdkd
        mppiaic.contract("abc,ac->ab", bv_p, sigma_)
        # Xkc rkckc
        sigma_.iadd_mult(mppia, bv_p, 1.0)
        # Coupling pairs-singles
        mpiaka.contract("abc,ba->ca", bv_s, sigma_)
        # Xdkc rkd
        mpiaic.contract("abc,ba->bc", bv_s, sigma_)
        # Xldck rld
        tmp = self.lf.create_one_index(vir)
        L_pqrq.contract("abc,ac->b", bv_s, tmp, **ovv)
        t_p.contract("ab,b->ab", tmp, sigma_, factor=2.0)
        tmp = self.lf.create_one_index(occ)
        L_pqrq.contract("abc,ac->b", bv_s, tmp, **oov)
        t_p.contract("ab,a->ab", tmp, sigma_, factor=-2.0)
        # Assign to sigma vector
        sigma.assign(sigma_.ravel(), begin0=end_s)

        return sigma

    def update_hamiltonian(self, mo1, mo2):
        """Derive all auxiliary matrices.

        **Arguments:**

        mo1, mo2
             one- and two-electron integrals to be sorted.

        """
        t_p = self.checkpoint["t_p"]
        #
        # Get ranges
        #
        ov = self.get_range("ov")
        vo = self.get_range("vo")
        ov2 = self.get_range("ov", offset=2)
        oo2 = self.get_range("oo", offset=2)
        vv2 = self.get_range("vv", offset=2)
        vo2 = self.get_range("vo", offset=2)
        voo = self.get_range("voo")
        vov = self.get_range("vov")
        voo3 = self.get_range("voo", 3)
        vov3 = self.get_range("vov", 3)
        vvo = self.get_range("vvo")
        oov = self.get_range("oov")
        ovv = self.get_range("ovv")
        oovv = self.get_range("oovv")
        ovvo = self.get_range("ovvo")
        ovov = self.get_range("ovov")
        ooov = self.get_range("ooov")
        oovo = self.get_range("oovo")
        occ = self.nacto
        vir = self.nactv
        act = self.nact
        #
        # <pq||rq>+<pq|rq>
        #
        lpqrq = self.init_cache("lpqrq", act, act, act)
        mo2.contract(
            "abcb->abc", out=lpqrq, factor=2.0, clear=True, select="einsum"
        )
        #
        # <pq|rr>
        #
        gpqrr = self.lf.create_three_index(act)
        mo2.contract("abcc->abc", out=gpqrr, clear=True, select="einsum")
        #
        # add exchange part to lpqrq
        #
        lpqrq.iadd_transpose((0, 2, 1), other=gpqrr, factor=-1.0)
        #
        # Inactive Fock matrix
        #
        fock = self.init_cache("fock", act, act)
        get_fock_matrix(fock, mo1, mo2, occ)
        #
        # <pp|qq>
        #
        gppqq = self.init_cache("gppqq", act, act)
        mo2.contract("aabb->ab", out=gppqq, clear=True, select="einsum")
        #
        # Aux matrix for Mia,ka
        #
        miaka = self.init_cache("miaka", occ, occ)
        # fki
        miaka.iadd(fock, -1.0, **oo2)
        # -Gikee cie
        gpqrr.contract("abc,ac->ab", t_p, miaka, factor=-1.0, **oov)
        #
        # Aux matrix for Mia,ic
        #
        miaic = self.init_cache("miaic", vir, vir)
        # fac
        miaic.iadd(fock, 1.0, **vv2)
        # -Gacmm cma
        gpqrr.contract("abc,ca->ab", t_p, miaic, factor=-1.0, **vvo)
        #
        # Aux matrix for Mia,kc
        #
        miakc = self.init_cache("miakc", occ, vir, occ, vir)
        # L_akic
        mo2.contract("abcd->acdb", miakc, factor=2.0, **ovvo, select="einsum")
        mo2.contract("abcd->abcd", miakc, factor=-1.0, **ovov, select="einsum")
        # Likac cia
        mo2.contract("abcd,ac->acbd", t_p, miakc, factor=2.0, **oovv)
        mo2.contract("abcd,ad->adbc", t_p, miakc, factor=-1.0, **oovv)
        if self.dump_cache:
            self.cache.dump("miakc")
        #
        # Aux matrix for Mia,kald (klid)
        #
        m1kald = self.init_cache("m1kald", occ, occ, occ, vir)
        # L_klid
        mo2.contract(
            "abcd->abcd", m1kald, factor=-2.0, **ooov, select="einsum"
        )
        mo2.contract("abcd->abdc", m1kald, **oovo, select="einsum")
        #
        # Aux matrix for Mia,icld (lac)
        #
        x1kdda = self.init_cache("x1kdda", occ, vir, vir)
        # L_lacc
        gpqrr.contract(
            "abc->abc", out=x1kdda, clear=True, **ovv, select="einsum"
        )
        #
        # Aux matrix for Mia,iald (ld)
        #
        m1iald = self.init_cache("m1iald", occ, vir)
        # F_ld
        m1iald.iadd(fock, 1.0, **ov2)
        #
        # Aux matrix for Miaia,ka (aki)
        #
        mpiaka = self.init_cache("mpiaka", vir, occ, occ)
        # G_akii
        mpiaka.iadd(gpqrr, -2.0, **voo3)
        # F_ak cia
        fock.contract(
            "ab,ca->abc", t_p, mpiaka, factor=-2.0, **vo, select="einsum"
        )
        # <ak|ee> cie
        gpqrr.contract("abc,dc->abd", t_p, mpiaka, factor=-2.0, **vov)
        # L_aiki cia
        lpqrq.contract("abc,ba->acb", t_p, mpiaka, factor=2.0, **voo)
        #
        # Aux matrix for Miaia,ic (cia)
        #
        mpiaic = self.init_cache("mpiaic", vir, occ, vir)
        # G_ciaa
        mpiaic.iadd(gpqrr, 2.0, **vov3)
        # F_ci cia
        fock.contract(
            "ab,bc->abc", t_p, mpiaic, factor=-2.0, **vo, select="einsum"
        )
        # <ci|ll> cla
        gpqrr.contract("abc,cd->abd", t_p, mpiaic, factor=2.0, **voo)
        # L_caia cia
        lpqrq.contract("abc,cb->acb", t_p, mpiaic, factor=-2.0, **vvo)
        #
        # Aux matrix for Mppiaia,kaka (iak)
        #
        mppiaka = self.init_cache("mppiaka", occ, vir, occ)
        # G_iikk
        mppiaka.iadd_expand_two_to_three(
            "ac->abc", gppqq, 1.0, end0=occ, end1=occ
        )
        # <kk|aa> cia
        t_p.contract(
            "ab,bc->abc", gppqq, mppiaka, factor=-2.0, **vo2, select="einsum"
        )
        # <kk|ee> cie
        tmp = self.lf.create_two_index(occ)
        t_p.contract("ab,bc->ac", gppqq, tmp, **vo2)
        mppiaka.iadd_expand_two_to_three("ac->abc", tmp, 1.0)
        #
        # Aux matrix for Mppiaia,icic (iac)
        #
        mppiaic = self.init_cache("mppiaic", occ, vir, vir)
        # G_aacc
        mppiaic.iadd_expand_two_to_three(
            "bc->abc", gppqq, 1.0, begin0=occ, begin1=occ
        )
        # <ii|cc> cia
        t_p.contract(
            "ab,ac->abc", gppqq, mppiaic, factor=-2.0, **ov2, select="einsum"
        )
        # <mm|cc> cma
        tmp = self.lf.create_two_index(vir, vir)
        t_p.contract("ab,ac->bc", gppqq, tmp, **ov2)
        mppiaic.iadd_expand_two_to_three("bc->abc", tmp, 1.0)
        #
        # Aux matrix for Mppiaia,iaia (ia)
        #
        mppia = self.init_cache("mppia", occ, vir)
        # F_aa - F_ii
        fockdiag = fock.copy_diagonal()
        mppia.iadd_expand_one_to_two("a->ab", fockdiag, -2.0, end0=occ)
        mppia.iadd_expand_one_to_two("b->ab", fockdiag, 2.0, begin0=occ)
        # L_iaia
        tmp = self.lf.create_two_index(act)
        mo2.contract(
            "abab->ab", out=tmp, factor=2.0, clear=True, select="einsum"
        )
        mo2.contract("abba->ab", out=tmp, factor=-1.0, select="einsum")
        mppia.iadd(tmp, -2.0, **ov2)
        # <ii|aa> cia
        mppia.iadd_mult(gppqq, t_p, 4.0, **ov)
        # <ii|dd> cid
        tmp = self.lf.create_one_index(occ)
        t_p.contract("ab,ab->a", gppqq, tmp, **ov2)
        mppia.iadd_expand_one_to_two("a->ab", tmp, -2.0)
        # <kk|aa> cka
        tmp = self.lf.create_one_index(vir)
        t_p.contract("ab,ab->b", gppqq, tmp, **ov2)
        mppia.iadd_expand_one_to_two("b->ab", tmp, -2.0)

        gc.collect()
