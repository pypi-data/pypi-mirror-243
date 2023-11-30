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
"""Restricted Tailored Coupled Cluster Class

   Variables used in this module:
    :nocc:      number of occupied orbitals in the principle configuration
    :nvir:      number of virtual orbitals in the principle configuration
    :ncore:     number of frozen core orbitals in the principle configuration
    :energy:    the CCSD energy, dictionary that contains different
                contributions
    :t_1, t_2:  the optimized amplitudes

    Indexing convention:
    :o:        matrix block corresponding to occupied orbitals of principle
               configuration
    :v:        matrix block corresponding to virtual orbitals of principle
               configuration


    EXAMPLE APPLICATION

    solver = RtCCSD(linalg_factory, occupation_model)
    result = solver(
        AO_one_body_ham, AO_two_body_ham, orbitals,
        external_core= number_of_inactive_orbitals_in_external_calculations,
        external_file='./example_path_to_/file_with_external_amplitudes'
    )
"""
import numpy as np

from pybest.log import log, timer
from pybest.utils import unmask

from .rcc import RCC
from .rccd import RCCD
from .rccsd import RCCSD


class RtCC(RCC):
    """Restricted tailored Coupled Cluster"""

    reference = "CAS-type wave function"

    def read_input(self, *args, **kwargs):
        """Looks for Hamiltonian terms, orbitals, and external amplitudes."""
        log.cite("the tCC methods", "leszczyk2022")
        external_file = unmask("external_file", *args, **kwargs)
        self.read_external_amplitudes(external_file)
        return RCC.read_input(self, *args, **kwargs)

    def read_header(self, filename):
        """Reads header of a file with external CC amplitudes. Works only with
        Budapest DMRG program. Returns length of header and number of frozen
        electrons in external calculations.
        """
        t_file = open(filename, "r")
        first_line = t_file.readline()

        if "%" in first_line:
            for i, line in enumerate(t_file.readlines()):
                if "Indices" in line:
                    indices = line.split()
                    nacto = int(indices[4]) - int(indices[3]) + 1
                elif "CCampl" in line:
                    header_length = i + 2
                    break
        else:
            header_length = 1
            indices = first_line.split()
            nacto = int(indices[1]) - int(indices[0]) + 1

        t_file.close()
        external_core = self.nocc - nacto
        return header_length, external_core

    def read_external_amplitudes(self, filename):
        """Reads amplitudes from external file self.external_file
        (e.g. DMRG-tailored T). Sets values and indices as attributes that are
        used during tailored CC calculations. Indices and values are kept
        separately since values are used only for creation the initial guess
        while indices are required also in the amplitudes optimization process
        (to keep them fixed).
        """
        header_length, external_core = self.read_header(filename)
        data = np.loadtxt(filename, skiprows=header_length)
        self.fixed_t1_index = []
        self.fixed_t1_value = []
        self.fixed_t2_index = []
        self.fixed_t2_value = []

        for row in data:
            if row[3] > 0:
                i = int(row[1]) - 1 + external_core
                j = int(row[2]) - 1 + external_core
                a = int(row[3]) - 1 + external_core - self.nocc
                b = int(row[4]) - 1 + external_core - self.nocc
                self.fixed_t2_index.append((i, a, j, b))
                self.fixed_t2_value.append(row[0])
            elif row[1] > 0:
                i = int(row[1]) - 1 + external_core
                a = int(row[2]) - 1 + external_core - self.nocc
                self.fixed_t1_index.append((i, a))
                self.fixed_t1_value.append(row[0])

    @staticmethod
    def assign_fourindex(four_index, indices, values=0.0):
        """Assign amplitudes from external source to ndarray dim=4 object.

        Arguments:

        four_index : DenseFourIndex

        values : float or list of floats
            the values that are assigned

        indices : list of 4-element tuples
        """
        for k, index in enumerate(indices):
            if isinstance(values, list):
                value = values[k]
            elif isinstance(values, float):
                value = values
            four_index.set_element(*index, value, symmetry=1)
            index_ = (index[2], index[3], index[0], index[1])
            four_index.set_element(*index_, value, symmetry=1)

    @staticmethod
    def assign_twoindex(two_index, indices, values=0.0):
        """Assign amplitudes from external source to ndarray dim=2 object.

        Arguments:

        two_index : DenseTwoIndex

        values : float or list of floats
            the values that are assigned

        indices : list of 2-element tuples
        """
        for k, index in enumerate(indices):
            if isinstance(values, list):
                value = values[k]
            elif isinstance(values, float):
                value = values
            two_index.set_element(*index, value, symmetry=1)


class RtCCD(RtCC, RCCD):
    """Restricted tailored Coupled Cluster Doubles"""

    acronym = "RtCCD"
    long_name = "Restricted DMRG-tailored Coupled Cluster Doubles"
    cluster_operator = "T2 - T_CAS"

    def generate_guess(self, **kwargs):
        """Generates initial guess for amplitudes (dict) with some amplitudes
        from external source."""
        initguess = RCC.generate_guess(self, **kwargs)
        t_2 = initguess["t_2"]
        self.assign_fourindex(t_2, self.fixed_t2_index, self.fixed_t2_value)
        return initguess

    @timer.with_section("VecFct RtCCSD")
    def vfunction(self, vector):
        """Shorter version of residual vector to accelerate solving."""
        amplitudes = self.unravel(vector)
        residual = self.cc_residual_vector(amplitudes)
        self.assign_fourindex(residual["out_d"], self.fixed_t2_index)
        return self.ravel(residual)


class RtCCSD(RtCC, RCCSD):
    """Restricted tailored Coupled Cluster Singles and Doubles"""

    acronym = "RtCCSD"
    long_name = "Restricted DMRG-tailored Coupled Cluster Singles Doubles"
    cluster_operator = "T1 + T2 - T_CAS"

    def generate_guess(self, **kwargs):
        """Generates initial guess for amplitudes (dict) with some amplitudes
        from external source."""
        initguess = RCC.generate_guess(self, **kwargs)
        t_1 = initguess["t_1"]
        t_2 = initguess["t_2"]
        self.assign_twoindex(t_1, self.fixed_t1_index, self.fixed_t1_value)
        self.assign_fourindex(t_2, self.fixed_t2_index, self.fixed_t2_value)
        return initguess

    @timer.with_section("VecFct RtCCSD")
    def vfunction(self, vector):
        """Shorter version of residual vector to accelerate solving."""
        amplitudes = self.unravel(vector)
        residual = self.cc_residual_vector(amplitudes)
        self.assign_twoindex(residual["out_s"], self.fixed_t1_index)
        self.assign_fourindex(residual["out_d"], self.fixed_t2_index)
        return self.ravel(residual)
