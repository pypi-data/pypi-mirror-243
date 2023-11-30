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
"""
   Variables used in this module:
    :ncore:     number of frozen core orbitals
    :nocc:      number of occupied orbitals in the principal configuration
    :nacto:     number of active occupied orbitals in the principal configuration
    :nvirt:     number of virtual orbitals in the principal configuration
    :nactv:     number of active virtual orbitals in the principal configuration
    :nbasis:    total number of basis functions
    :nact:      total number of active orbitals (nacto+nactv)
    :e_ci:      eigenvalues of CI Hamiltonian (IOData container attribute)
    :civ:       eigenvectors of CI Hamiltonian (IOData container attribute)

    Indexing convention:
     :i,j,k,..: occupied orbitals of principal configuration
     :a,b,c,..: virtual orbitals of principal configuration
"""
from functools import partial
from math import sqrt

import numpy as np

from pybest.auxmat import get_fock_matrix
from pybest.ci.csf_cis import CSFRCIS
from pybest.ci.rci_base import RCI
from pybest.ci.rci_utils import display, display_csf
from pybest.ci.sd_cis import SDRCIS
from pybest.linalg import CholeskyFourIndex
from pybest.log import log


class RCIS(RCI):
    """Restricted Configuration Interaction Singles module
    for Slater Determinant (SD) and Configuration State Function (CSF) basis.
    """

    long_name = "Restricted Configuration Interaction Singles"
    acronym = "CIS"
    reference = "any single-reference wavefunction"

    def __init__(self, lf, occ_model, csf=True):
        super().__init__(lf, occ_model)
        self._csf = csf
        if self.csf:
            self._ci_method = CSFRCIS(self)
        else:
            self._ci_method = SDRCIS(self)
        self.dimension = self.acronym
        self._ci_method._dimension = self.dimension

    @property
    def ci_method(self):
        """Instance of SD- or CSF-type class"""
        return self._ci_method

    @RCI.dimension.setter
    def dimension(self, new=None):
        if new is not None:
            self._dimension = self.ci_method.set_dimension(
                new, self.nacto, self.nactv
            )
        else:
            log.warn(
                "The dimension may be wrong!"
                "Please set the dimension property with one of the strings (RCIS, RCID, RCISD)"
            )

    @RCI.nroot.setter
    def nroot(self, new):
        self._nroot = new + 1

    @RCI.size_consistency_correction.setter
    def size_consistency_correction(self, new):
        self._size_consistency_correction = False

    @RCI.threshold_c_0.setter
    def threshold_c_0(self, new):
        self._threshold_c_0 = False

    def calculate_exact_hamiltonian(self):
        """Calculate exact Hamiltonian of the CIS model."""

        #
        # Auxiliary objects
        #
        fock = self.from_cache("fock")
        govvo = self.from_cache("govvo")
        govov = self.from_cache("govov")

        #
        # Hamiltonian
        #
        hamiltonian = self.lf.create_two_index(self.dimension, self.dimension)

        #
        # Scale matrix elements if CSF are used
        #
        scale_factor_1 = 1.0
        scale_factor_2 = 1.0
        if self.csf:
            scale_factor_1 = 1.0 / sqrt(2.0)
            scale_factor_2 = 2.0 / sqrt(2.0)

        for i in range(self.nacto):
            for a in range(self.nactv):
                i_a = i * self.nactv + a
                hamiltonian.set_element(
                    0,
                    i_a + 1,
                    fock.get_element(i, a + self.nacto) * 2.0 * scale_factor_1,
                    symmetry=1,
                )
                hamiltonian.set_element(
                    i_a + 1,
                    0,
                    fock.get_element(i, a + self.nacto) * scale_factor_2,
                    symmetry=1,
                )
                for j in range(self.nacto):
                    for b in range(self.nactv):
                        tmp = 0.0
                        j_b = j * self.nactv + b
                        if a == b:
                            tmp -= fock.get_element(i, j)
                        if i == j:
                            tmp += fock.get_element(
                                a + self.nacto, b + self.nacto
                            )
                        tmp += 2 * govvo.get_element(j, a, b, i)
                        tmp -= govov.get_element(j, a, i, b)
                        hamiltonian.set_element(
                            i_a + 1, j_b + 1, tmp, symmetry=1
                        )
        return hamiltonian

    def set_hamiltonian(self, mo1, mo2):
        """Compute auxiliary matrices.

        **Arguments:**

        mo1, mo2
            One- and two-electron integrals (some Hamiltonian matrix
            elements) in the MO basis.
        """
        self.clear_cache()

        # 1) Fock matrix: fpq
        fock = self.init_cache("fock", self.nact, self.nact)
        get_fock_matrix(fock, mo1, mo2, self.nacto)

        #
        # 4-Index slices of ERI
        #
        def alloc(arr, block):
            "Determines alloc keyword argument for init_cache method."
            # We keep one whole CholeskyFourIndex to rule them all.
            # Non-redundant blocks are accessed as views.
            if isinstance(arr, CholeskyFourIndex):
                return (partial(arr.view, **self.get_range(block)),)
            # But we store only non-redundant blocks of DenseFourIndex
            return (partial(arr.copy, **self.get_range(block)),)

        #
        # Get blocks
        #
        slices = ["ovov", "ovvo"]
        for slice_ in slices:
            self.init_cache(f"g{slice_}", alloc=alloc(mo2, slice_))

    def setup_dict(self):
        """Initializes the proper dictionary to store the data for SD or CSF."""

        if self.print_csf:
            return {
                "spin_block_1",
                "c_1",
            }
        return {
            "spin_block_a",
            "spin_block_b",
            "c_a",
            "c_b",
        }

    def printer(self):
        """Printing the results."""
        #
        # Local variables
        #
        evals = self.checkpoint["e_ci"]
        evecs = self.checkpoint["civ"]
        threshold = self.threshold
        alpha = "\u03B1"
        beta = "\u03B2"
        data = self.setup_dict()
        #
        # Printing
        #
        log.hline("*")
        log(f"RESULTS OF {self.acronym}")
        log.hline("*")
        log(
            f"{'Root':>5s} {'Exc.Energy[au]':>16s} {'Tot.Energy[au]':>17s}"
            f" {'Weight(s)':>15s}"
        )
        log.hline("_")
        for ind, val in enumerate(evals):
            data = {key: [] for key in data}
            evecsj = evecs[:, ind]
            n_c = np.where(abs(evecsj) > threshold)[0]
            log(
                f"{ind:>3d} {val:> 16.6e} {self.e_ref+val:> 17.8f}"
                f"{np.dot(evecsj[1:], evecsj[1:]):> 17.6f}"
            )
            log(" ")
            for ind2 in n_c:
                if ind2 == 0:
                    log(f"{'Reference state   C_0:':>30s}")
                    log(f"{evecsj[ind2]:> 34.5f}")
                else:
                    self.collect_data(ind2, data, evecsj)

            if self.print_csf:
                if len(data["spin_block_1"]) > 0:
                    log(" ")
                    log(f"{'(i->a):':>15s} {'C_ia:':>16s}")
                display_csf(data, "1", self.acronym)
            else:
                if len(data["spin_block_a"]) > 0:
                    log(" ")
                    log(f"{'(i->a):':>15s} {'C_ia:':>16s}")
                display(data, "a", alpha)
                display(data, "b", beta)

            log.hline("-")
            log.hline("*")

    def collect_data(self, index, data, evecsj):
        """Collect the data and prepare them for printing:

        **Arguments:**

        *index:
            (int) Number indicating the SD contribution in the CI solution.

        *data:
            (dictionary) Contains two types of data:
            indices (spin_block_a) of the proper SD spin block contributions
            and the corresponding coefficients (c_a).

        *evecsj:
            Eigenvectors of CI Hamiltonian (without the reference
            state contribution).
        """
        if (self.csf and self.print_csf) or (not self.csf and self.print_csf):
            if abs(evecsj[index]) > self.threshold:
                i, a = self.get_index_s(index - 1)
                data["spin_block_1"].append(
                    [i + self.ncore + 1, a + self.ncore + 1 + self.nacto]
                )
                data["c_1"].append(evecsj[index])

        if self.csf and not self.print_csf:
            if abs(evecsj[index] / sqrt(2)) > self.threshold:
                i, a = self.get_index_s(index - 1)
                data["spin_block_a"].append(
                    [i + self.ncore + 1, a + self.ncore + 1 + self.nacto]
                )
                data["c_a"].append(evecsj[index] / sqrt(2))
                data["spin_block_b"].append(
                    [i + self.ncore + 1, a + self.ncore + 1 + self.nacto]
                )
                data["c_b"].append(evecsj[index] / sqrt(2))

        if not self.csf and not self.print_csf:
            if abs(evecsj[index] / sqrt(2)) > self.threshold:
                i, a = self.get_index_s(index - 1)
                data["spin_block_a"].append(
                    [i + self.ncore + 1, a + self.ncore + 1 + self.nacto]
                )
                data["c_a"].append(evecsj[index] / sqrt(2))
                data["spin_block_b"].append(
                    [i + self.ncore + 1, a + self.ncore + 1 + self.nacto]
                )
                data["c_b"].append(evecsj[index] / sqrt(2))

        return data

    def get_index_s(self, index):
        """Get index for single excitation."""
        b = index % self.nactv
        j = ((index - b) / self.nactv) % self.nacto
        return int(j), int(b)
