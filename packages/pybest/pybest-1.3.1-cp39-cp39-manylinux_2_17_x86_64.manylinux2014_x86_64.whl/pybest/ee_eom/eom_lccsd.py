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
"""Equation of Motion Coupled Cluster implementations of EOM-LCCSD

   Child class of REOMLCCSDBase(REOMCC) class.
"""

from pybest.linalg import CholeskyLinalgFactory
from pybest.log import timer

from .eom_lccsd_base import REOMLCCSDBase


class REOMLCCSD(REOMLCCSDBase):
    """Performs an EOM-LCCSD calculation"""

    long_name = (
        "Equation of Motion Linearized Coupled Cluster Singles and Doubles"
    )
    acronym = "EOM-LCCSD"
    reference = "LCCSD"
    singles_ref = True
    pairs_ref = False
    doubles_ref = True
    singles_ci = True
    pairs_ci = False
    doubles_ci = True

    @timer.with_section("Hdiag EOM-LCCSD")
    def compute_h_diag(self, *args):
        """Used by Davidson module for pre-conditioning.

        **Arguments:**

        args:
            required for Davidson module (not used here)
        """
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
        # Assign only symmetry-unique elements
        #
        h_diag.assign(h_diag_s.ravel(), begin0=1, end0=end_s)
        h_diag.assign(h_diag_d.get_triu(), begin0=end_s)

        return h_diag

    @timer.with_section("SubHam EOM-LCCSD")
    def build_subspace_hamiltonian(self, bvector, hdiag, *args):
        """
        Used by Davidson module to construct subspace Hamiltonian. Here, the
        base class method is called, which returns all sigma vector contributions
        and the b vector, while all symmetry-unique elements are returned.

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
        # Get ranges
        #
        end_s = self.nacto * self.nactv + 1
        #
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
        # Add permutation to doubles (not considered in base class)
        #
        sigma_d.iadd_transpose((2, 3, 0, 1))
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

        return sigma

    @timer.with_section("Cache EOM-LCCSD")
    def update_hamiltonian(self, mo1, mo2):
        """Derive all auxiliary matrices. Here only used to define proper timer
        sections.

        **Arguments:**

        mo1, mo2
             one- and two-electron integrals to be sorted.
        """
        #
        # Call base class method
        #
        REOMLCCSDBase.update_hamiltonian(self, mo1, mo2)
        #
        # Store also ERI in case of Cholesky decomposition
        #
        if isinstance(self.lf, CholeskyLinalgFactory):
            mo2_ = self.init_cache("mo2", self.nact, nvec=mo2.nvec)
            mo2_.assign(mo2)
        #
        # Delete ERI (MO) as they are not required anymore
        #
        mo2.__del__()
