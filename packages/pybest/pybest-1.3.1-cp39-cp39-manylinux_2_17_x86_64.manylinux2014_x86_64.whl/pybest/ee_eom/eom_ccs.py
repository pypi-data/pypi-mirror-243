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
"""Equation of Motion Coupled Cluster implementations of EOM-CCS

   Child class of REOMCC class.
"""

import gc

import numpy as np

from pybest.auxmat import get_fock_matrix
from pybest.log import log, timer
from pybest.utils import unmask

from .eom_base import REOMCC


class REOMCCS(REOMCC):
    """Performs an EOM-CCS calculation, which is equivalent to CIS."""

    long_name = "Equation of Motion Coupled Cluster Singles"
    acronym = "EOM-CCS"
    reference = "CCS"
    singles_ref = True
    pairs_ref = False
    doubles_ref = False
    singles_ci = True
    pairs_ci = False
    doubles_ci = False

    @property
    def dimension(self):
        """The number of unknowns (total number of excited states incl. ground
        state) for each EOM-CC flavor. Variable used by the Davidson module."""
        return self.nacto * self.nactv + 1

    def unmask_args(self, *args, **kwargs):
        """Extract all tensors/quantities from function arguments and keyword
        arguments. Arguments/kwargs have to contain:
        * t_1: some CC T_1 amplitudes
        """
        #
        # t_1
        #
        t_1 = unmask("t_1", *args, **kwargs)
        if t_1 is not None:
            self.checkpoint.update("t_1", t_1)
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
        # get excitation (remove reference state from composite index)
        #
        i, a = self.get_index_s(index - 1)
        #
        # Print contribution
        #
        log(
            f"            t_ia:          ({i + 1:3},"
            f"{a + 1 + self.nacto:3})   {ci_vector[index]: 1.5f}"
        )

    def print_weights(self, ci_vector):
        """Print weights of excitations.

        **Arguments:**

        ci_vector:
            (np.array) the CI coefficient vector that contains all coefficients
            for one specific state
        """
        log(
            f"          weight(s): {np.dot(ci_vector[1:], ci_vector[1:]): 1.5f}"
        )

    @timer.with_section("HamiltonianEOMCCS")
    def build_full_hamiltonian(self):
        """Construct full Hamiltonian matrix used in exact diagonalization"""
        eom_ham = self.lf.create_two_index(
            self.nactv * self.nacto + 1, self.nacto * self.nactv + 1
        )
        occ = self.nacto
        #
        # Get auxiliary matrices
        #
        fock = self.from_cache("fock")
        miaka = self.from_cache("miaka")
        miaic = self.from_cache("miaic")
        miakc = self.from_cache("miakc")
        miakc_ = miakc.copy()
        if self.dump_cache:
            self.cache.dump("miakc")
        #
        # Assign matrix elements
        #
        eom_ham.assign(fock.array[:occ, occ:].ravel(), end0=1, begin1=1)
        eom_ham.iscale(2.0)
        miakc_.iadd_expand_two_to_four("bc->abac", miaic, 1.0)
        miakc_.iadd_expand_two_to_four("ac->abcb", miaka, 1.0)
        eom_ham.assign(miakc_.array, begin0=1, begin1=1)

        return eom_ham

    @timer.with_section("BHDiagpCCDCCS")
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
        miaka = self.from_cache("miaka")
        miaic = self.from_cache("miaic")
        #
        # Singles
        #
        diag_s = self.lf.create_two_index(self.nacto, self.nactv)
        miakc = self.from_cache("miakc")
        miakc.contract("abab->ab", out=diag_s, clear=True, select="einsum")
        if self.dump_cache:
            self.cache.dump("miakc")
        tmp = miaka.copy_diagonal()
        diag_s.iadd_expand_one_to_two("a->ab", tmp, 1.0)
        tmp = miaic.copy_diagonal()
        diag_s.iadd_expand_one_to_two("b->ab", tmp, 1.0)

        eom_ham_diag.assign(diag_s.ravel(), begin0=1)
        return eom_ham_diag

    @timer.with_section("SubHam EOM-CCS")
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
        fock = self.from_cache("fock")
        miaka = self.from_cache("miaka")
        miaic = self.from_cache("miaic")
        #
        # Get ranges
        #
        ov2 = self.get_range("ov", offset=2)
        #
        # Calculate sigma vector (H.bvector)_kc
        #
        sigma_s = self.lf.create_two_index(self.nacto, self.nactv)
        bv_s = self.dense_lf.create_two_index(self.nacto, self.nactv)
        #
        # reshape bvector
        #
        bv_s.assign(bvector, begin2=1)
        #
        # Reference vector R_0
        #
        # X0,kc rkc
        sum0_ = bv_s.contract("ab,ab", fock, **ov2) * 2.0
        #
        # Single excitations
        #
        # Xkcld rld
        miakc = self.from_cache("miakc")
        miakc.contract("abcd,cd->ab", bv_s, sigma_s, clear=True)
        if self.dump_cache:
            self.cache.dump("miakc")
        # Xkclc rlc
        miaka.contract("ab,bc->ac", bv_s, sigma_s)
        # Xkckd rkd
        bv_s.contract("ab,cb->ac", miaic, sigma_s)
        #
        # output vector
        #
        sigma = self.lf.create_one_index(self.dimension)
        sigma.set_element(0, sum0_)
        sigma.assign(sigma_s.ravel(), begin0=1)

        return sigma

    @timer.with_section("CacheEOMCCS")
    def update_hamiltonian(self, mo1, mo2):
        """Derive all auxiliary matrices.

        **Arguments:**

        mo1, mo2
             one- and two-electron integrals to be sorted.
        """
        t_ia = self.checkpoint["t_1"]
        tco = {"select": self.tco}
        #
        # Get ranges
        #
        ov2 = self.get_range("ov", offset=2)
        oo2 = self.get_range("oo", offset=2)
        vv2 = self.get_range("vv", offset=2)
        voov = self.get_range("voov")
        vovo = self.get_range("vovo")
        ooov = self.get_range("ooov")
        oovo = self.get_range("oovo")
        ovvv = self.get_range("ovvv")
        occ = self.nacto
        vir = self.nactv
        act = self.nact
        #
        # Inactive Fock matrix
        #
        fock = self.init_cache("fock", act, act)
        get_fock_matrix(fock, mo1, mo2, occ)
        #
        # <vo||ov>+<vo|ov>
        #
        lvoov = self.dense_lf.create_four_index(vir, occ, occ, vir)
        mo2.contract(
            "abcd->abcd",
            out=lvoov,
            factor=2.0,
            clear=True,
            **voov,
            select="einsum",
        )
        mo2.contract(
            "abcd->abdc",
            out=lvoov,
            factor=-1.0,
            **vovo,
            select="einsum",
        )
        #
        # <oo||ov>+<oo|ov>
        #
        looov = self.dense_lf.create_four_index(occ, occ, occ, vir)
        mo2.contract(
            "abcd->abcd",
            out=looov,
            factor=2.0,
            clear=True,
            **ooov,
            select="einsum",
        )
        mo2.contract(
            "abcd->abdc",
            out=looov,
            factor=-1.0,
            **oovo,
            select="einsum",
        )
        #
        # Mia,ka
        #
        miaka = self.init_cache("miaka", occ, occ)
        # fik
        miaka.iadd(fock, -1.0, **oo2)
        # tie fke
        t_ia.contract("ab,cb->ac", fock, miaka, **ov2, **tco)
        # -L_kmie t_me
        looov.contract("abcd,bd->ca", t_ia, miaka, factor=-1.0, **tco)
        #
        # Mia,ic
        #
        miaic = self.init_cache("miaic", vir, vir)
        # fac
        miaic.iadd(fock, 1.0, **vv2)
        # -tma fmc
        t_ia.contract("ab,ac->bc", fock, miaic, factor=-1.0, **ov2, **tco)
        # -L_maec t_me
        mo2.contract("abcd,ac->bd", t_ia, miaic, factor=-2.0, **ovvv, **tco)
        mo2.contract("abcd,ad->bc", t_ia, miaic, **ovvv, **tco)
        #
        # Aux matrix for Mia,kc
        #
        miakc = self.init_cache("miakc", occ, vir, occ, vir)
        # L_akic
        lvoov.contract(
            "abcd->cabd", out=miakc, factor=1.0, clear=True, select="einsum"
        )
        # L_mkic t_ma
        looov.contract("abcd,ae->cebd", t_ia, miakc, factor=-1.0, **tco)
        # L_kace t_ie
        mo2.contract("abcd,ed->ebac", t_ia, miakc, factor=2.0, **ovvv, **tco)
        mo2.contract("abcd,ec->ebad", t_ia, miakc, factor=-1.0, **ovvv, **tco)
        if self.dump_cache:
            self.cache.dump("miakc")

        del looov
        del lvoov
        gc.collect()
        #
        # Delete mo2 as they are not required anymore
        #
        mo2.__del__()
