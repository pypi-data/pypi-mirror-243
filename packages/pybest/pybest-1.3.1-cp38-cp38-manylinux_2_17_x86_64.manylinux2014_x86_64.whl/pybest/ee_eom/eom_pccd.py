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
"""Equation of Motion Coupled Cluster implementation for a pCCD reference
   function.

   Variables used in this module:
    :ncore:     number of frozen core orbitals
    :nocc:      number of occupied orbitals in the principle configuration
    :nacto:     number of active occupied orbitals in the principle configuration
    :nvirt:     number of virtual orbitals in the principle configuration
    :nactv:     number of active virtual orbitals in the principle configuration
    :nbasis:    total number of basis functions
    :nact:      total number of active orbitals (nacto+nactv)

    Indexing convention:
     :i,j,k,..: occupied orbitals of principle configuration
     :a,b,c,..: virtual orbitals of principle configuration
     :p,q,r,..: general indices (occupied, virtual)

    P^bc_jk performs a pair permutation, i.e., P^bc_jk o_(bcjk) = o_(cbkj)

    Abbreviations used (if not mentioned in doc-strings):
     :L_pqrs: 2<pq|rs>-<pq|sr>
     :g_pqrs: <pq|rs>

   Child class of REOMCC class.
"""

import numpy as np

from pybest.auxmat import get_diag_fock_matrix
from pybest.exceptions import ArgumentError
from pybest.log import log, timer
from pybest.utils import unmask

from .eom_base import REOMCC


class REOMpCCD(REOMCC):
    """Performs an EOM-pCCD calculation."""

    long_name = "Equation of Motion pair Coupled Cluster Doubles"
    acronym = "EOM-pCCD"
    reference = "pCCD"
    singles_ref = False
    pairs_ref = True
    doubles_ref = False
    singles_ci = False
    pairs_ci = True
    doubles_ci = False

    @property
    def dimension(self):
        """The number of unknowns (total number of excited states incl. ground
        state) for each EOM-CC flavor. Variable used by the Davidson module."""
        return self.nacto * self.nactv + 1

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
        #
        # Remove reference state index
        #
        index_ = index - 1
        #
        # Print contribution of pair excitation
        #
        i, a = self.get_index_s(index_)
        # Account for frozen core, occupied orbitals, and numpy index convention
        i, a = i + self.ncore + 1, a + self.ncore + self.nacto + 1
        log(
            f"          t_iaia:  ({i:3d},{a:3d},{i:3d},{a:3d})   {ci_vector[index]: 1.5f}"
        )

    def print_weights(self, ci_vector):
        """Print weights of excitations.

        **Arguments:**

        ci_vector:
            (np.array) the CI coefficient vector that contains all coefficients
            for one specific state
        """
        log(
            f"          weight(p): {np.dot(ci_vector[1:], ci_vector[1:]): 1.5f}"
        )

    @timer.with_section("Hamiltonian EOM-pCCD")
    def build_full_hamiltonian(self):
        """Construct full Hamiltonian matrix used in exact diagonalization"""
        eom_ham = self.lf.create_two_index(self.dimension)
        occ = self.nacto
        vir = self.nactv
        #
        # Get auxiliary matrices
        #
        G_ppqq = self.from_cache("gppqq")
        mppia = self.from_cache("mppia")
        mppiaic = self.from_cache("mppiaic")
        mppiaka = self.from_cache("mppiaka")
        #
        # Assign matrix elements
        #
        eom_ham.assign(G_ppqq.array[:occ, occ:].ravel(), end0=1, begin1=1)
        miakc = self.dense_lf.create_four_index(occ, vir, occ, vir)
        miakc.iadd_expand_two_to_four("diag", mppia, 1.0)
        miakc.iadd_expand_three_to_four("abc->abac", mppiaic, 1.0)
        miakc.iadd_expand_three_to_four("abc->abcb", mppiaka, 1.0)
        eom_ham.assign(miakc.array, begin0=1, begin1=1)

        return eom_ham

    @timer.with_section("Hdiag EOM-pCCD")
    def compute_h_diag(self, *args):

        """Used by Davidson module for pre-conditioning

        **Arguments:**

        args:
            required for Davidson module (not used here)
        """
        eom_ham_diag = self.lf.create_one_index(self.dimension, label="h_diag")
        #
        # Get auxiliary matrices
        #
        mppia = self.from_cache("mppia")
        mppiaic = self.from_cache("mppiaic")
        mppiaka = self.from_cache("mppiaka")
        #
        # Assign matrix elements
        #
        diagp = mppia.copy()
        mppiaic.contract("abb->ab", out=diagp, select="einsum")
        mppiaka.contract("aba->ab", out=diagp, select="einsum")
        eom_ham_diag.assign(diagp.ravel(), begin0=1)

        return eom_ham_diag

    @timer.with_section("SubHam EOM-pCCD")
    def build_subspace_hamiltonian(self, bvector, hdiag, *args):

        """
        Used by Davidson module to construct subspace Hamiltonian

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
        # Get auxiliary matrices
        #
        G_ppqq = self.from_cache("gppqq")
        mppiaka = self.from_cache("mppiaka")
        mppiaic = self.from_cache("mppiaic")
        mppia = self.from_cache("mppia")
        #
        # Get ranges
        #
        ov2 = self.get_range("ov", offset=2)
        #
        # Calculate sigma vector (H.bvector)_kc
        #
        sigma_p = self.lf.create_two_index(self.nacto, self.nactv)
        bv_p = self.lf.create_two_index(self.nacto, self.nactv)
        sigma = self.lf.create_one_index(self.nacto * self.nactv + 1)
        bv_p.assign(bvector, begin2=1)
        #
        # Reference state
        #
        sum0 = bv_p.contract("ab,ab", G_ppqq, **ov2)
        sigma.set_element(0, sum0)
        #
        # Pair excitations
        #
        # Xlk rlclc
        mppiaka.contract("abc,cb->ab", bv_p, sigma_p, clear=True)
        # Xcd rkdkd
        mppiaic.contract("abc,ac->ab", bv_p, sigma_p)
        # Xkc rkckc
        sigma_p.iadd_mult(mppia, bv_p, 1.0)
        #
        # Assign new sigma vector
        #
        sigma.assign(sigma_p.ravel(), begin0=1)
        return sigma

    @timer.with_section("Cache EOM-pCCD")
    def update_hamiltonian(self, mo1, mo2):
        """Derive all auxiliary matrices.
        fock_pq:     one_pq + sum_m(2<pm|qm> - <pm|mq>),
        lpqpq:   2<pq|pq>-<pq|qp>,
        gpqpq:   <pq|pq>,

        **Arguments:**

        mo1, mo2
             one- and two-electron integrals to be sorted.
        """
        cia = self.checkpoint["t_p"]
        #
        # Get ranges
        #
        ov = self.get_range("ov")
        vo2 = self.get_range("vo", offset=2)
        ov2 = self.get_range("ov", offset=2)
        occ = self.nacto
        vir = self.nactv
        act = self.nact
        #
        # 2<pq|pq>-<pq|pq>
        #
        aux_mat1 = self.init_cache("lpqpq", act, act)
        mo2.contract(
            "abab->ab", out=aux_mat1, factor=2.0, clear=True, select="einsum"
        )
        mo2.contract("abba->ab", out=aux_mat1, factor=-1.0, select="einsum")
        #
        # Inactive Fock matrix
        #
        aux_mat2 = self.lf.create_one_index(act)
        get_diag_fock_matrix(aux_mat2, mo1, mo2, occ)
        #
        # <pp|qq>
        #
        gppqq = self.init_cache("gppqq", act, act)
        mo2.contract("aabb->ab", out=gppqq, clear=True, select="einsum")
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
        cia.contract(
            "ab,bc->abc", gppqq, mppiaka, factor=-2.0, **vo2, select="einsum"
        )
        # <kk|ee> cie
        tmp = self.lf.create_two_index(occ)
        cia.contract("ab,bc->ac", gppqq, tmp, **vo2)
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
        cia.contract(
            "ab,ac->abc", gppqq, mppiaic, factor=-2.0, **ov2, select="einsum"
        )
        # <mm|cc> cma
        tmp = self.lf.create_two_index(vir)
        cia.contract("ab,ac->bc", gppqq, tmp, **ov2)
        mppiaic.iadd_expand_two_to_three("bc->abc", tmp, 1.0)
        #
        # Aux matrix for Mppiaia,iaia (ia)
        #
        mppia = self.init_cache("mppia", occ, vir)
        # F_aa - F_ii
        mppia.iadd_expand_one_to_two("a->ab", aux_mat2, -2.0, end0=occ)
        mppia.iadd_expand_one_to_two("b->ab", aux_mat2, 2.0, begin0=occ)
        # L_iaia
        mppia.iadd(aux_mat1, -2.0, **ov2)
        # <ii|aa> cia
        mppia.iadd_mult(gppqq, cia, 4.0, **ov)
        # <ii|dd> cid
        tempk = self.lf.create_one_index(occ)
        cia.contract("ab,ab->a", gppqq, tempk, **ov2)
        mppia.iadd_expand_one_to_two("a->ab", tempk, -2.0)
        # <kk|aa> cka
        tempc = self.lf.create_one_index(vir)
        cia.contract("ab,ab->b", gppqq, tempc, **ov2)
        mppia.iadd_expand_one_to_two("b->ab", tempc, -2.0)
        #
        # Remove ERI (MO) to save memory as they are not required anymore
        #
        mo2.__del__()
