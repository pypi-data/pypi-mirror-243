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
"""Equation of Motion Coupled Cluster implementations of EOM-LCCD.

   Child class of REOMLCCDBase(REOMCC).
"""

from pybest.linalg import CholeskyLinalgFactory
from pybest.log import timer

from .eom_lccd_base import REOMLCCDBase


class REOMLCCD(REOMLCCDBase):
    """Performs a EOM-LCCD calculation"""

    long_name = "Equation of Motion Linearized Coupled Cluster Doubles"
    acronym = "EOM-LCCD"
    reference = "LCCD"
    singles_ref = False
    pairs_ref = False
    doubles_ref = True
    singles_ci = False
    pairs_ci = False
    doubles_ci = True

    @timer.with_section("Hdiag EOM-LCCD")
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
        h_diag_d = REOMLCCDBase.compute_h_diag(self, *args)
        #
        # Assign only symmetry-unique elements
        #
        h_diag.assign(h_diag_d.get_triu(), begin0=1)

        return h_diag

    @timer.with_section("SubHam EOM-LCCD")
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
        # Call base class method
        #
        sum0, sigma_d, bv_d = REOMLCCDBase.build_subspace_hamiltonian(
            self, bvector, hdiag, *args
        )
        #
        # Add permutation to doubles (not considered in base class)
        #
        sigma_d.iadd_transpose((2, 3, 0, 1))
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

        return sigma

    @timer.with_section("Cache EOM-LCCD")
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
        REOMLCCDBase.update_hamiltonian(self, mo1, mo2)
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
