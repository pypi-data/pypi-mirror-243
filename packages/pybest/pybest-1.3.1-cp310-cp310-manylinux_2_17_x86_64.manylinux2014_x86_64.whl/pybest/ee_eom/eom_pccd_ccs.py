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
"""Equation of Motion Coupled Cluster implementations of EOM-pCCD-CCS,
   that is, pCCD-CCS with single excitations.

   Child class of REOMpCCDSBase(REOMCC) class.
"""

from pybest.exceptions import ArgumentError
from pybest.log import timer
from pybest.utils import unmask

from .eom_pccd_s_base import REOMpCCDSBase


class REOMpCCDCCS(REOMpCCDSBase):
    """Perform an EOM-pCCD-CCS calculation."""

    long_name = "Equation of Motion pair Coupled Cluster Doubles Singles"
    acronym = "EOM-pCCD-CCS"
    reference = "pCCD-CCS"
    singles_ref = True
    pairs_ref = True
    doubles_ref = False
    singles_ci = True
    pairs_ci = True
    doubles_ci = False

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
        elif self.singles_ref:
            raise ArgumentError("Cannot find T1 amplitudes")
        #
        # Call base class method
        #
        return REOMpCCDSBase.unmask_args(self, *args, **kwargs)

    @timer.with_section("BuildHamEOM-pCCD-CCS")
    def build_full_hamiltonian(self):
        """Construct full Hamiltonian matrix used in exact diagonalization"""
        #
        # Call base class method
        #
        return REOMpCCDSBase.build_full_hamiltonian(self)

    @timer.with_section("Hdiag EOM-pCCD-CCS")
    def compute_h_diag(self, *args):
        """Used by Davidson module for pre-conditioning. Here only used to
        define proper timer sections.

        **Arguments:**

        args:
            required for Davidson module (not used here)
        """
        #
        # Call base class method
        #
        return REOMpCCDSBase.compute_h_diag(self, *args)

    @timer.with_section("SubHam EOM-pCCD-CCS")
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
        #
        # Full sigma vector from base method
        #
        return REOMpCCDSBase.build_subspace_hamiltonian(
            self, bvector, hdiag, *args
        )

    @timer.with_section("Cache EOM-pCCD-CCS")
    def update_hamiltonian(self, mo1, mo2):
        """Derive all auxiliary matrices.

        **Arguments:**

        mo1, mo2
             one- and two-electron integrals to be sorted.

        """
        #
        # Call base class method first
        #
        REOMpCCDSBase.update_hamiltonian(self, mo1, mo2)
        #
        # Modify auxiliary matrices from base class
        #
        t_ia = self.checkpoint["t_1"]
        #
        # Get auxiliary matrices including those that need to be updated
        #
        fock = self.from_cache("fock")
        miaka = self.from_cache("miaka")
        miaic = self.from_cache("miaic")
        miakc = self.from_cache("miakc")
        m1kald = self.from_cache("m1kald")
        x1kdda = self.from_cache("x1kdda")
        m1iald = self.from_cache("m1iald")
        #
        # Get ranges
        #
        ov2 = self.get_range("ov", offset=2)
        ooov = self.get_range("ooov")
        oovo = self.get_range("oovo")
        oovv = self.get_range("oovv")
        ovvv = self.get_range("ovvv")
        #
        # Aux matrix for Mia,ka
        #
        # tie fke
        t_ia.contract("ab,cb->ac", fock, miaka, **ov2)
        # -L_kmie t_me
        mo2.contract("abcd,bd->ca", t_ia, miaka, factor=-2.0, **ooov)
        mo2.contract("abcd,bc->da", t_ia, miaka, **oovo)
        #
        # Aux matrix for Mia,ic
        #
        # tma fmc
        t_ia.contract("ab,ac->bc", fock, miaic, factor=-1.0, **ov2)
        # L_maec t_me
        mo2.contract("abcd,ac->bd", t_ia, miaic, factor=2.0, **ovvv)
        mo2.contract("abcd,ad->bc", t_ia, miaic, factor=-1.0, **ovvv)
        #
        # Aux matrix for Mia,kc
        #
        # -L_mkic t_ma
        mo2.contract("abcd,ae->cebd", t_ia, miakc, factor=-2.0, **ooov)
        mo2.contract("abcd,ae->debc", t_ia, miakc, **oovo)
        # L_kace t_ie
        mo2.contract("abcd,ed->ebac", t_ia, miakc, factor=2.0, **ovvv)
        mo2.contract("abcd,ec->ebad", t_ia, miakc, factor=-1.0, **ovvv)
        #
        # Aux matrix for Mia,kald (klid)
        #
        # L_kled tie
        mo2.contract("abcd,ec->abed", t_ia, m1kald, factor=-2.0, **oovv)
        mo2.contract("abcd,ed->abec", t_ia, m1kald, **oovv)
        #
        # Aux matrix for Mia,icld (lacd) (c=d)
        #
        # -L_mlcc tma
        mo2.contract("abcc,ae->bec", t_ia, x1kdda, factor=-1.0, **oovv)
        #
        # Aux matrix for Mia,iald (ld)
        #
        # L_mled tme
        mo2.contract("abcd,ac->bd", t_ia, m1iald, factor=2.0, **oovv)
        mo2.contract("abcd,ad->bc", t_ia, m1iald, factor=-1.0, **oovv)
        #
        # Delete ERI (MO) as they are not required anymore
        #
        mo2.__del__()
