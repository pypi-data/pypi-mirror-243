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
"""Equation of Motion Coupled Cluster implementations of EOM-pCCD-LCCSD

   Child class of REOMLCCSDBase(REOMCC) class.
"""

import gc

from pybest.linalg import CholeskyLinalgFactory
from pybest.log import log, timer

from .eom_lccsd_base import REOMLCCSDBase


class REOMpCCDLCCSD(REOMLCCSDBase):
    """Performs an EOM-pCCD-LCCSD calculation"""

    long_name = (
        "Equation of Motion pair Coupled Cluster Doubles with a linearized "
        "Coupled Cluster Singles and Doubles correction"
    )
    acronym = "EOM-pCCD-LCCSD"
    reference = "pCCD-LCCSD"
    singles_ref = True
    pairs_ref = True
    doubles_ref = True
    singles_ci = True
    pairs_ci = True
    doubles_ci = True

    @timer.with_section("Hdiag EOM-pCCD-LCCSD")
    def compute_h_diag(self, *args):
        """Used by Davidson module for pre-conditioning. Here, the base class
        method is called and all missing terms are updated/included.

        **Arguments:**

        args:
            required for Davidson module (not used here)
        """
        #
        # Add citation
        #
        log.cite(
            "the EOM-pCCD-LCC-based methods",
            "boguslawski2019",
        )
        h_diag = self.lf.create_one_index(self.dimension, label="h_diag")
        #
        # Call base class method
        #
        h_diag_s, h_diag_d = REOMLCCSDBase.compute_h_diag(self, *args)
        #
        # Get ranges
        #
        end_s = self.nacto * self.nactv + 1
        #
        # Get auxiliary matrices for pair contributions
        #
        mppia = self.from_cache("mppia")
        mppiaic = self.from_cache("mppiaic")
        mppiaka = self.from_cache("mppiaka")
        #
        # Calculate pair contributions
        #
        h_diag_p = mppia.copy()
        mppiaic.contract("abb->ab", out=h_diag_p, factor=1.0, select="einsum")
        mppiaka.contract("aba->ab", out=h_diag_p, factor=1.0, select="einsum")
        #
        # Update h_diag_d with proper pair contribution
        #
        self.set_seniority_0(h_diag_d, h_diag_p)
        #
        # Assign only symmetry-unique elements
        #
        h_diag.assign(h_diag_s.ravel(), begin0=1, end0=end_s)
        h_diag.assign(h_diag_d.get_triu(), begin0=end_s)

        return h_diag

    @timer.with_section("SubHam EOM-pCCDLCCSD")
    def build_subspace_hamiltonian(self, bvector, hdiag, *args):
        """
        Used by Davidson module to construct subspace Hamiltonian. Here, the
        base class method is called, which returns all sigma vector contributions
        and the b vector, while all symmetry-unique elements are returned.
        All missing contributions (including their coupling terms) are also
        added.

        **Arguments:**

        bvector:
            (OneIndex object) contains current approximation to CI coefficients

        hdiag:
            Diagonal Hamiltonian elements required in Davidson module (not used
            here)

        args:
            Set of arguments passed by the Davidson module (not used here)
        """
        #
        # Modify T_2 to contain pair amplitudes. This will reduce the number of
        # contractions
        #
        t_p = self.checkpoint["t_p"]
        t_iajb = self.checkpoint["t_2"]
        tco = {"select": self.tco}
        self.set_seniority_0(t_iajb, t_p)
        #
        # Call base class method
        #
        (
            sum0,
            sigma_s,
            sigma_d,
            bv_s,
            bv_d,
        ) = REOMLCCSDBase.build_subspace_hamiltonian(
            self, bvector, hdiag, *args
        )
        #
        # Get ranges
        #
        ovv = self.get_range("ovv")
        oov = self.get_range("oov")
        occ = self.nacto
        vir = self.nactv
        end_s = occ * vir + 1
        #
        # Get auxiliary matrices for pair excitations
        #
        L_pqrq = self.from_cache("lpqrq")
        m21ikjc = self.from_cache("m21ikjc")
        m21kia = self.from_cache("m21kia")
        m21ica = self.from_cache("m21ica")
        mpiaka = self.from_cache("mpiaka")
        mpiaic = self.from_cache("mpiaic")
        mp2ki = self.from_cache("mp2ki")
        mp2ikl = self.from_cache("mp2ikl")
        mp2ac = self.from_cache("mp2ac")
        mp2acd = self.from_cache("mp2acd")
        m21ikjc = self.from_cache("m21ikjc")
        #
        # Pair excitations
        #
        # Terms for R=R1+R2
        # Xaki rka
        sigma_p = self.lf.create_two_index(occ, vir)
        mpiaka.contract("abc,ba->ca", bv_s, sigma_p, clear=True)
        # Xt_p ric
        mpiaic.contract("abc,ba->bc", bv_s, sigma_p)
        # Xakci rkc
        # Lkaca cia rkc
        tmp = self.lf.create_one_index(vir)
        L_pqrq.contract("abc,ac->b", bv_s, tmp, **ovv, **tco)
        t_p.contract("ab,b->ab", tmp, sigma_p, factor=2.0)
        # Lkici cia rkc
        tmp = self.lf.create_one_index(occ)
        L_pqrq.contract("abc,ac->b", bv_s, tmp, **oov, **tco)
        t_p.contract("ab,a->ab", tmp, sigma_p, factor=-2.0)
        # Xki rkaia
        bv_d.contract("abcb,ac->cb", mp2ki, sigma_p, factor=2.0)
        # Xac ricia
        bv_d.contract("abad,db->ad", mp2ac, sigma_p, factor=2.0)
        # Xacd ricid
        bv_d.contract("abac,dbc->ad", mp2acd, sigma_p)
        # Xikl rkala
        bv_d.contract("abcb,dac->db", mp2ikl, sigma_p)
        # Lklca cia rkcla
        tmp = self.lf.create_one_index(vir)
        loovv = self.from_cache("loovv")
        loovv.contract("abcd,acbd->d", bv_d, tmp)  # a
        t_p.contract("ab,b->ab", tmp, sigma_p, factor=-2.0)
        # Likdc cia rkcid
        tmp = self.lf.create_one_index(occ)
        loovv.contract("abcd,bdac->a", bv_d, tmp)  # i
        if self.dump_cache:
            self.cache.dump("loovv")
        t_p.contract("ab,a->ab", tmp, sigma_p, factor=-2.0)
        # Xiakc riakc
        mp2jbkc = self.from_cache("mp2jbkc")
        bv_d.contract("abcd,abcd->ab", mp2jbkc, sigma_p, factor=2.0)
        if self.dump_cache:
            self.cache.dump("mp2jbkc")
        # Xkadi rkaid
        mp2kadi = self.from_cache("mp2kadi")
        bv_d.contract("abcd,abdc->cb", mp2kadi, sigma_p, factor=2.0)
        if self.dump_cache:
            self.cache.dump("mp2kadi")
        #
        # Coupling to singles
        #
        # Pair contributions:
        # missing terms of m21icab
        self.get_effective_hamiltonian_term_icab(bv_s, sigma_d)
        # delta_ab
        # P Xica rjc
        tmp = self.lf.create_three_index(occ, vir, occ)
        m21ica.contract("abc,db->acd", bv_s, tmp)  # ica,jc->iaj
        # P Xijaakc rkc
        tmp2 = self.lf.create_two_index(occ, occ)
        m21ikjc.contract("abcd,bd->ac", bv_s, tmp2, **tco)  # ij
        t_p.contract("ab,ac->abc", tmp2, tmp)  # ia,ij->iaj
        tmp2 = None
        # expand all intermediates
        sigma_d.iadd_expand_three_to_four("abc->abcb", tmp, factor=1.0)
        # delta_ij
        # P Xiika rkb delta_kn
        tmp = self.lf.create_three_index(occ, vir, vir)
        m21kia.contract("abc,ad->bcd", bv_s, tmp, **tco)  # kia,kb->iab
        # P Xiiabkc rkc
        tmp2 = self.get_effective_hamiltonian_term_kbca(bv_s)
        t_p.contract("ab,bc->abc", tmp2, tmp)  # ia,ab->iab
        tmp2 = None
        # expand all intermediates
        sigma_d.iadd_expand_three_to_four("abc->abac", tmp, factor=1.0)
        #
        # Add permutation
        #
        sigma_d.iadd_transpose((2, 3, 0, 1))
        # Update sigma_d with correct pair contribution
        self.set_seniority_0(sigma_d, sigma_p)
        #
        # Clean-up
        #
        del bv_s, bv_d
        #
        # Assign to sigma vector
        #
        sigma = self.lf.create_one_index(self.dimension)
        sigma.set_element(0, sum0)
        sigma.assign(sigma_s.ravel(), begin0=1, end0=end_s)
        sigma.assign(sigma_d.get_triu(), begin0=end_s)
        #
        # Delete pair amplitudes again
        #
        self.set_seniority_0(t_iajb, 0.0)

        return sigma

    @timer.with_section("Cache EOM-pCCD-LCCSD")
    def update_hamiltonian(self, mo1, mo2):
        """Derive all auxiliary matrices. Here, the base class method is called,
        which returns all basic auxiliary matrices (similar in various EOM-LCCSD
        flavours). All missing contributions (including their coupling terms)
        are then added.

        **Arguments:**

        mo1, mo2
             one- and two-electron integrals to be sorted.
        """
        #
        # Modify T_2 to contain pair amplitudes. This will reduce the number of
        # contractions
        #
        t_p = self.checkpoint["t_p"]
        t_ia = self.checkpoint["t_1"]
        t_iajb = self.checkpoint["t_2"]
        tco = {"select": self.tco}
        self.set_seniority_0(t_iajb, t_p)
        #
        # Call base class method
        #
        REOMLCCSDBase.update_hamiltonian(self, mo1, mo2)
        #
        # Add missing terms in exisiting auxiliary matrices and generate
        # additional ones
        #
        fock = self.from_cache("fock")
        gppqq = self.from_cache("gppqq")
        gpqpq = self.from_cache("gpqpq")
        lpqrq = self.from_cache("lpqrq")
        m21ijak = self.from_cache("m21ijak")
        #
        # Get ranges
        #
        ov = self.get_range("ov")
        vo = self.get_range("vo")
        ov2 = self.get_range("ov", offset=2)
        oo2 = self.get_range("oo", offset=2)
        vv2 = self.get_range("vv", offset=2)
        vo2 = self.get_range("vo", offset=2)
        ooo = self.get_range("ooo")
        oov = self.get_range("oov")
        voo = self.get_range("voo")
        vov = self.get_range("vov")
        vvo = self.get_range("vvo")
        vvv = self.get_range("vvv")
        voo3 = self.get_range("voo", 3)
        vov3 = self.get_range("vov", 3)
        oovv = self.get_range("oovv")
        ovvo = self.get_range("ovvo")
        ovov = self.get_range("ovov")
        occ = self.nacto
        vir = self.nactv
        act = self.nact
        #
        # Compute auxiliary matrices
        #
        lpqpq = gpqpq.copy()
        lpqpq.iscale(2.0)
        mo2.contract("abba->ab", lpqpq, factor=-1.0, select="einsum")
        #
        # <pq|rr> (expensive, but we only do it once)
        #
        gpqrr = self.lf.create_three_index(act)
        mo2.contract("abcc->abc", out=gpqrr, clear=True, select="einsum")
        #
        # Aux matrix for Mp2iaia,iicd (acd)
        #
        mp2acd = self.init_cache("mp2acd", vir, vir, vir)
        # pairs: <aa|cd>
        gpqrr.contract("abc->cab", mp2acd, **vvv, select="einsum")
        # pairs: <cd|mm> cma
        gpqrr.contract("abc,cd->dab", t_p, mp2acd, **vvo, **tco)
        #
        # Aux matrix for Miaia,ka (aki)
        # (9)
        mpiaka = self.init_cache("mpiaka", vir, occ, occ)
        # G_akii
        mpiaka.iadd(gpqrr, -2.0, **voo3)
        # F_ak cia
        fock.contract(
            "ab,ca->abc", t_p, mpiaka, factor=-2.0, **vo, select="einsum"
        )
        # <ak|ee> cie
        gpqrr.contract("abc,dc->abd", t_p, mpiaka, factor=-2.0, **vov, **tco)
        # L_aiki cia
        lpqrq.contract("abc,ba->acb", t_p, mpiaka, factor=2.0, **voo)
        #
        # Aux matrix for Miaia,ic (cia)
        # (8)
        mpiaic = self.init_cache("mpiaic", vir, occ, vir)
        # G_ciaa
        mpiaic.iadd(gpqrr, 2.0, **vov3)
        # F_ci cia
        fock.contract(
            "ab,bc->abc", t_p, mpiaic, factor=-2.0, **vo, select="einsum"
        )
        # <ci|ll> cla
        gpqrr.contract("abc,cd->abd", t_p, mpiaic, factor=2.0, **voo, **tco)
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
        # Used in pCCD-based methods
        # <kk|aa> cia
        t_p.contract(
            "ab,bc->abc", gppqq, mppiaka, factor=-2.0, **vo2, select="einsum"
        )
        # <kk|ee> cie
        tmp = self.lf.create_two_index(occ)
        t_p.contract("ab,bc->ac", gppqq, tmp, **vo2, **tco)
        mppiaka.iadd_expand_two_to_three("ac->abc", tmp, 1.0)
        #
        # Aux matrix for Mppiaia,icic (iac)
        #
        mppiaic = self.init_cache("mppiaic", occ, vir, vir)
        # G_aacc
        mppiaic.iadd_expand_two_to_three(
            "bc->abc", gppqq, 1.0, begin0=occ, begin1=occ
        )
        # Used in pCCD-based methods
        # <ii|cc> cia
        t_p.contract(
            "ab,ac->abc", gppqq, mppiaic, factor=-2.0, **ov2, select="einsum"
        )
        # <mm|cc> cma
        tmp = self.lf.create_two_index(vir)
        t_p.contract("ab,ac->bc", gppqq, tmp, **ov2, **tco)
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
        mppia.iadd(lpqpq, -2.0, **ov2)
        # <ii|aa> cia
        mppia.iadd_mult(gppqq, t_p, 4.0, **ov)
        # <ii|dd> cid
        tmp = self.lf.create_one_index(occ)
        t_p.contract("ab,ab->a", gppqq, tmp, **ov2, select="einsum")
        mppia.iadd_expand_one_to_two("a->ab", tmp, -2.0)
        # <kk|aa> cka
        tmp = self.lf.create_one_index(vir)
        t_p.contract("ab,ab->b", gppqq, tmp, **ov2, select="einsum")
        mppia.iadd_expand_one_to_two("b->ab", tmp, -2.0)
        del lpqpq
        #
        # Aux matrix for M21iajakc (ikjc)
        # (10) delta_ab
        m21ikjc = self.init_cache("m21ikjc", occ, occ, occ, vir)
        # L_ikdc tjd
        mo2.contract(
            "abcd,ec->abed", t_ia, m21ikjc, factor=-2.0, **oovv, **tco
        )
        mo2.contract("abcd,ed->abec", t_ia, m21ikjc, **oovv, **tco)
        #
        # Aux matrix for M21iaibkc (kbca)
        # (10) delta_ij
        if not isinstance(self.lf, CholeskyLinalgFactory):
            m21kbca = self.init_cache("m21kbca", occ, vir, vir, vir)
            # L_klca tlb
            mo2.contract(
                "abcd,be->aecd", t_ia, m21kbca, factor=-2.0, **oovv, **tco
            )
            mo2.contract("abcd,be->aedc", t_ia, m21kbca, **oovv, **tco)
            if self.dump_cache:
                self.cache.dump("m21kbca")
        #
        # Aux matrix for M21iaibkb (kia)
        # (9) delta_ij
        m21kia = self.init_cache("m21kia", occ, occ, vir)
        # L_klad tld cia
        tmpka = self.lf.create_two_index(occ, vir)
        mo2.contract(
            "abcd,bd->ac", t_ia, tmpka, factor=2.0, **oovv, **tco
        )  # ka
        mo2.contract(
            "abcd,bc->ad", t_ia, tmpka, factor=-1.0, **oovv, **tco
        )  # ka
        tmpka.contract("ac,bc->abc", t_p, m21kia, factor=-1.0)  # ka,ia->kia
        # G_klee tla cie
        tmp = self.lf.create_three_index(occ)
        gpqrr.contract("abc,dc->abd", t_p, tmp, **oov, **tco)  # klee,ie->kli
        tmp.contract("abc,bd->acd", t_ia, m21kia, **tco)  # kli,la->kia
        #
        # Aux matrix for M21iajajc (ica)
        # (8) delta_ij
        m21ica = self.init_cache("m21ica", occ, vir, vir)
        # L_ilcd tld cia
        tmpka.contract("ab,ac->abc", t_p, m21ica, factor=-1.0)  # ic,ia->ica
        # G_cell tie cla
        tmp = self.lf.create_three_index(occ, vir, occ)
        gpqrr.contract("abc,db->dac", t_ia, tmp, **vvo, **tco)  # cell,ie->icl
        tmp.contract("abc,cd->abd", t_p, m21ica, **tco)  # icl,la->ica
        #
        # Aux matrix for M21iajbjc (icab)
        # (8) X_abcj
        if not isinstance(self.lf, CholeskyLinalgFactory):
            # Lmica tmb cia
            tmp = self.dense_lf.create_four_index(occ, vir, vir, vir)
            mo2.contract("abcd,ae->bcde", t_ia, tmp, factor=2.0, **oovv)
            mo2.contract("abcd,ae->bdce", t_ia, tmp, factor=-1.0, **oovv)
            m21icab = self.from_cache("m21icab")
            tmp.contract(
                "abcd,ac->abcd", t_p, m21icab, factor=-1.0, select="einsum"
            )
            # <mi|bc> tma cib
            mo2.contract("abcd,ae->bdec", t_ia, tmp, clear=True, **oovv, **tco)
            tmp.contract("abcd,ad->abcd", t_p, m21icab)
            # <mi|ca> tmb cia
            mo2.contract("abcd,ae->bcde", t_ia, tmp, clear=True, **oovv)
            tmp.contract("abcd,ac->abcd", t_p, m21icab, select="einsum")
            tmp = None
            if self.dump_cache:
                self.cache.dump("m21icab")
        #
        # Aux matrix for M21iajb,kb (ijak)
        #
        # Likae tje cia
        tmp = self.dense_lf.create_four_index(occ, occ, vir, occ)
        mo2.contract(
            "abcd,ed->aecb", t_ia, tmp, factor=2.0, **oovv, **tco
        )  # ijak
        mo2.contract(
            "abcd,ec->aedb", t_ia, tmp, factor=-1.0, **oovv, **tco
        )  # ijak
        tmp.contract("abcd,ac->abcd", t_p, m21ijak, factor=-1.0)
        # <jk|ea> tie cja
        #       tmp = m21ijak.new()
        mo2.contract("abcd,ec->eadb", t_ia, tmp, clear=True, **oovv, **tco)
        tmp.contract("abcd,bc->abcd", t_p, m21ijak)
        # <ik|ae> tje cia
        mo2.contract("abcd,ed->aecb", t_ia, tmp, clear=True, **oovv, **tco)
        tmp.contract("abcd,ac->abcd", t_p, m21ijak)
        tmp = None
        #
        # Aux matrix for Mp2iaia,kica (jbkc)
        #
        mp2jbkc = self.init_cache("mp2jbkc", occ, vir, occ, vir)
        mo2.contract(
            "abcd->acdb", mp2jbkc, factor=2.0, **ovvo, select="einsum"
        )
        mo2.contract(
            "abcd->abcd", mp2jbkc, factor=-1.0, **ovov, select="einsum"
        )
        # pairs: Lkica cia
        mo2.contract("abcd,bd->bdac", t_p, mp2jbkc, factor=2.0, **oovv)
        mo2.contract("abcd,bc->bcad", t_p, mp2jbkc, factor=-1.0, **oovv)
        if self.dump_cache:
            self.cache.dump("mp2jbkc")
        #
        # Aux matrix for M2piaia,kiad
        #
        mp2kadi = self.init_cache("mp2kadi", occ, vir, vir, occ)
        # pairs
        mo2.contract(
            "abcd->abcd", mp2kadi, factor=-1.0, **ovvo, select="einsum"
        )
        # pairs: <ka|id>
        mo2.contract(
            "abcd->abdc", mp2kadi, factor=-1.0, **ovov, select="einsum"
        )
        # pairs: Lkiad cia
        mo2.contract("abcd,bc->acdb", t_p, mp2kadi, factor=2.0, **oovv)
        mo2.contract("abcd,bd->adcb", t_p, mp2kadi, factor=-1.0, **oovv)
        if self.dump_cache:
            self.cache.dump("mp2kadi")
        #
        # Aux matrix for Mp2iaia,klaa (ikl)
        #
        mp2ikl = self.init_cache("mp2ikl", occ, occ, occ)
        # pairs: <ii|kl>
        gpqrr.contract("abc->cab", mp2ikl, **ooo, select="einsum")
        # pairs: <kl|ee> cie
        gpqrr.contract("abc,dc->dab", t_p, mp2ikl, **oov, **tco)
        #
        # Aux matrix for Mp2iaia,kiaa (ki)
        #
        mp2ki = self.init_cache("mp2ki", occ, occ)
        # pairs: fki
        mp2ki.iadd(fock, -1.0, **oo2)
        # pairs: <ki|ee> cie
        gpqrr.contract("abc,bc->ab", t_p, mp2ki, factor=-1.0, **oov)
        #
        # Aux matrix for Mp2iaia,iica (ac)
        #
        mp2ac = self.init_cache("mp2ac", vir, vir)
        # pairs: fac
        mp2ac.iadd(fock, 1.0, **vv2)
        # pairs: <ac|mm> cma
        gpqrr.contract("abc,ca->ab", t_p, mp2ac, factor=-1.0, **vvo)
        #
        # Delete pair amplitudes again
        #
        self.set_seniority_0(t_iajb, 0.0)
        #
        # Store also ERI in case of Cholesky decomposition
        #
        if isinstance(self.lf, CholeskyLinalgFactory):
            mo2_ = self.init_cache("mo2", act, nvec=mo2.nvec)
            mo2_.assign(mo2)
        #
        # Delete ERI (MO) as they are not required anymore
        #
        mo2.__del__()
        gc.collect()

    #
    # Expensive effective Hamiltonian terms
    #

    def get_effective_hamiltonian_term_icab(self, bv_s, sigma):
        """Compute effective Hamiltonian term involving an ovvv block

        **Arguments:**

        :bv_s: (DenseTwoIndex) the current approximation to the CI singles
               coefficient

        :sigma: (DenseFourIndex) the output sigma vector
        """
        if isinstance(self.lf, CholeskyLinalgFactory):
            t_ia = self.checkpoint["t_1"]
            t_p = self.checkpoint["t_p"]
            eri = self.from_cache("mo2")
            oovv = self.get_range("oovv")
            occ = self.nacto
            vir = self.nactv
            tco = {"select": self.tco}
            # (- kjcb + kjbc) ric tka tjjbb
            tmp = self.dense_lf.create_four_index(occ, occ, occ, vir)
            eri.contract(
                "abcd,ec->ebad", bv_s, tmp, factor=-1.0, **oovv, **tco
            )  # ijkb
            eri.contract("abcd,ed->ebac", bv_s, tmp, **oovv, **tco)  # ijkb
            tmp2 = self.dense_lf.create_four_index(occ, vir, occ, vir)
            tmp.contract("abcd,ce->aebd", t_ia, tmp2, **tco)  # iajb
            tmp2.contract("abcd,cd->abcd", t_p, sigma, select="einsum")
            # <jk|ca> ric tkb tjjaa
            tmp = self.dense_lf.create_four_index(occ, occ, vir, occ)
            eri.contract("abcd,ec->eadb", bv_s, tmp, **oovv, **tco)  # ijak
            tmp2 = self.dense_lf.create_four_index(occ, vir, occ, vir)
            tmp.contract("abcd,de->acbe", t_ia, tmp2, **tco)  # iajb
            tmp2.contract("abcd,cb->abcd", t_p, sigma, select="einsum")

    def get_effective_hamiltonian_term_kbca(self, bv_s):
        """Compute effective Hamiltonian term involving an ovvv block

        **Arguments:**

        :bv_s: (DenseTwoIndex) the current approximation to the CI singles
               coefficient

        :sigma: (DenseFourIndex) the output sigma vector
        """
        vir = self.nactv
        out = self.lf.create_two_index(vir)
        to_o = {"out": out, "clear": False, "select": self.tco}
        if isinstance(self.lf, CholeskyLinalgFactory):
            t_ia = self.checkpoint["t_1"]
            loovv = self.from_cache("loovv")
            occ = self.nacto
            tco = {"select": self.tco}
            # (10) -Llkac rkc cia tlb delta_ij
            tmpla = self.lf.create_two_index(occ, vir)
            loovv.contract("abcd,bd->ac", bv_s, tmpla, **tco)
            tmpla.contract("ab,ac->bc", t_ia, **to_o, factor=-1.0)  # ab
            if self.dump_cache:
                self.cache.dump("loovv")
            return out
        m21kbca = self.from_cache("m21kbca")
        m21kbca.contract("abcd,ac->db", bv_s, **to_o)  # kbca,kc->ab
        if self.dump_cache:
            self.cache.dump("m21kbca")
        return out
