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
"""Equation of Motion Coupled Cluster implementations of EOM-pCCD-LCCD.

   Child class of REOMLCCDBase(REOMCC).
"""

import gc

from pybest.linalg import CholeskyLinalgFactory
from pybest.log import log, timer

from .eom_lccd_base import REOMLCCDBase


class REOMpCCDLCCD(REOMLCCDBase):
    """Performs an EOM-pCCD-LCCD calculation"""

    long_name = (
        "Equation of Motion pair Coupled Cluster Doubles with a linearized "
        "Coupled Cluster Doubles correction"
    )
    acronym = "EOM-pCCD-LCCD"
    reference = "pCCD-LCCD"
    singles_ref = False
    pairs_ref = True
    doubles_ref = True
    singles_ci = False
    pairs_ci = True
    doubles_ci = True

    @timer.with_section("Hdiag EOM-pCCD-LCCD")
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
        h_diag_d = REOMLCCDBase.compute_h_diag(self, *args)
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
        h_diag.assign(h_diag_d.get_triu(), begin0=1)

        return h_diag

    @timer.with_section("SubHam EOM-pCCD-LCCD")
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
        self.set_seniority_0(t_iajb, t_p)
        #
        # Call base class method
        #
        sum0, sigma_d, bv_d = REOMLCCDBase.build_subspace_hamiltonian(
            self, bvector, hdiag, *args
        )
        #
        # Get auxiliary matrices for pair excitations
        #
        mp2ki = self.from_cache("mp2ki")
        mp2ikl = self.from_cache("mp2ikl")
        mp2ac = self.from_cache("mp2ac")
        mp2acd = self.from_cache("mp2acd")
        #
        # Pair excitations
        #
        sigma_p = self.lf.create_two_index(self.nacto, self.nactv)
        #
        # Terms for R=R2
        # Xki rkaia
        bv_d.contract("abcb,ac->cb", mp2ki, sigma_p, factor=2.0)
        # Xac ricia
        bv_d.contract("abad,db->ad", mp2ac, sigma_p, factor=2.0)
        # Xacd ricid
        bv_d.contract("abac,dbc->ad", mp2acd, sigma_p)
        # Xikl rkala
        bv_d.contract("abcb,dac->db", mp2ikl, sigma_p)
        # Lklca cia rkcla
        tmp = self.lf.create_one_index(self.nactv)
        loovv = self.from_cache("loovv")
        loovv.contract("abcd,acbd->d", bv_d, tmp)  # a
        t_p.contract("ab,b->ab", tmp, sigma_p, factor=-2.0)
        # Likdc cia rkcid
        tmp = self.lf.create_one_index(self.nacto)
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
        # Add permutation
        #
        sigma_d.iadd_transpose((2, 3, 0, 1))
        # Update sigma_d with correct pair contribution
        self.set_seniority_0(sigma_d, sigma_p)
        #
        # Clean-up
        #
        del bv_d
        #
        # Assign to sigma vector
        #
        sigma = self.lf.create_one_index(self.dimension)
        sigma.set_element(0, sum0)
        sigma.assign(sigma_d.get_triu(), begin0=1)
        #
        # Delete pair amplitudes again
        #
        self.set_seniority_0(t_iajb, 0.0)

        return sigma

    @timer.with_section("Cache EOM-pCCD-LCCD")
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
        t_iajb = self.checkpoint["t_2"]
        self.set_seniority_0(t_iajb, t_p)
        tco = {"select": self.tco}
        #
        # Call base class method
        #
        REOMLCCDBase.update_hamiltonian(self, mo1, mo2)
        #
        # Add missing terms in exisiting auxiliary matrices and generate
        # additional ones
        #
        fock = self.from_cache("fock")
        gppqq = self.from_cache("gppqq")
        gpqpq = self.from_cache("gpqpq")
        lpqrq = self.from_cache("lpqrq")
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
        mo2.contract("abba->ab", out=lpqpq, factor=-1.0, select="einsum")
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
        gpqrr.contract(
            "abc->cab", out=mp2ikl, **ooo, clear=True, select="einsum"
        )
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
