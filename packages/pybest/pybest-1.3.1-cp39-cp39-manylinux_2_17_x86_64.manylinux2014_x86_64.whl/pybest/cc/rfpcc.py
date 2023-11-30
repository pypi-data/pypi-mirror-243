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
"""Restricted Frozen-pair Coupled Cluster Singles Doubles Class

   Variables used in this module:
    :nocc:      number of occupied orbitals in the principle configuration
    :nvirt:     number of virtual orbitals in the principle configuration
    :ncore:     number of frozen core orbitals in the principle configuration
    :nbasis:    total number of basis functions
    :energy:    the CCSD energy, dictionary that contains different
                contributions
    :t_1, t_2:  the optimized amplitudes

    Indexing convention:
    :o:        matrix block corresponding to occupied orbitals of principle
               configuration
    :v:        matrix block corresponding to virtual orbitals of principle
               configuration

    EXAMPLE APPLICATION

    pccd_solver = RAp1roG(linalg_factory, occupation_model)
    pccd_result - pccd_solver(
        AO_one_body_ham, AO_two_body_ham, external_potential, orbitals, overlap
    )

    fpcc_solver = RfpCCSD(linalg_factory, occupation_model)
    fpcc_result = fpcc_solver(AO_one_body_ham, AO_two_body_ham, pCCD_output)
"""
from abc import ABC

import numpy as np

from pybest.exceptions import MatrixShapeError
from pybest.linalg import DenseFourIndex
from pybest.log import log
from pybest.utils import unmask

from .rcc import RCC
from .rccd import RCCD
from .rccsd import RCCSD


class RfpCC(RCC, ABC):
    """Class containing methods characteristic for frozen-pair CC."""

    reference = "pCCD"

    def read_input(self, *args, **kwargs):
        """Looks for Hamiltonian terms, orbitals, and geminal amplitudes."""
        log.cite("the fpCC methods", "leszczyk2022")
        self.t_p = unmask("t_p", *args, **kwargs)
        return RCC.read_input(self, *args, **kwargs)

    def set_pair_amplitudes(self, t_2, t_p):
        """Assign seniority 0 amplitudes to some DenseFourIndex object.
        t_2 : DenseFourIndex object with amplitudes
        t_p : DenseTwoIndex object with geminal amplitudes
        """
        if t_p.shape != (self.nacto, self.nactv):
            raise MatrixShapeError(
                "Geminal matrix shape is not proper. "
                f"Expected shape: ({self.nacto}, {self.nactv}). "
                f"Current shape: {t_p.shape} ",
                "Check if you specified correct number of core orbitals.",
            )
        ind1, ind2 = np.indices((self.nacto, self.nactv))
        t_2.assign(0.0, [ind1, ind2, ind1, ind2])
        t_2.iadd_expand_two_to_four("diag", t_p)
        return t_2

    def generate_guess(self, **kwargs):
        """Generates initial guess for amplitudes and filles it with t_p."""
        initguess = RCC.generate_guess(self, **kwargs)
        for item in initguess.values():
            if isinstance(item, DenseFourIndex):
                self.set_pair_amplitudes(item, self.t_p)
        return initguess

    def vfunction(self, vector):
        """Shorter version of residual vector to accelerate solving."""
        amplitudes = self.unravel(vector)
        residual = self.cc_residual_vector(amplitudes)
        self.set_seniority_0(residual["out_d"], 0.0)
        return self.ravel(residual)


class RfpCCD(RfpCC, RCCD):
    """Restricted Coupled Cluster Doubles"""

    acronym = "RfpCCD"
    long_name = "Restricted frozen-pair Coupled Cluster Doubles"
    cluster_operator = "T2 - Tp"


class RfpCCSD(RfpCC, RCCSD):
    """Restricted Coupled Cluster Singles and Doubles"""

    acronym = "RfpCCSD"
    long_name = "Restricted frozen-pair Coupled Cluster Singles and Doubles"
    cluster_operator = "T1 + T2 - Tp"
