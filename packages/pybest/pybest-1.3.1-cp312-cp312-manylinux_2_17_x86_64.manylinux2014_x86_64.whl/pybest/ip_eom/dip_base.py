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
"""Double Ionization Potential Equation of Motion Coupled Cluster implementations.
   This is a base class for all double IP implementations.

   Variables used in this module:
    :ncore:     number of frozen core orbitals
                (abbreviated as nc)
    :nocc:      number of occupied orbitals in the principle configuration
    :nacto:     number of active occupied orbitals in the principle configuration
                (abbreviated as no)
    :nvirt:     number of virtual orbitals in the principle configuration
    :nactv:     number of active virtual orbitals in the principle configuration
                (abbreviated as nv)
    :nbasis:    total number of basis functions
    :nact:      total number of active orbitals (nacto+nactv)
                (abbreviated as na)
    :e_ip:      the energy correction for DIP
    :civ_ip:    the CI amplitudes from a given EOM model
    :rij:       2 holes operator
    :rijkc:     3 holes 1 particle operator (same spin)
    :rijKC:     3 holes 1 particle operator (opposite spin)
    :alpha:     number of unpaired electrons

  Indexing convention:
    :i,j,k,..: occupied orbitals of principle configuration
    :a,b,c,..: virtual orbitals of principle configuration
    :p,q,r,..: general indices (occupied, virtual)

  Abbreviations used (if not mentioned in doc-strings):
    :2h:    2 holes
    :3h:    3 holes
    :aa:    same-spin component
    :ab:    opposite-spin component
"""

import math
from itertools import combinations

import numpy as np

from pybest.exceptions import ArgumentError, ConsistencyError
from pybest.ip_eom.xip_base import RXIPCC
from pybest.log import log
from pybest.utils import check_options


class RDIPCC(RXIPCC):
    """
    Restricted Double Ionization Potential Equation of Motion Coupled Cluster
    class restricted to Double IP

    Purpose:
    Determine the excitation energies from a given EOMCC model
    (a) Build the non-symmetric effective EOM Hamiltonian
    (b) Diagonalize EOM Hamiltonian

    Currently supported wavefunction models:
     * RpCCD

    """

    long_name = (
        "Double Ionization Potential Equation of Motion Coupled Cluster"
    )
    acronym = "DIP-EOM-CC"
    reference = ""
    order = "DIP"
    alpha = -1

    @RXIPCC.nhole.setter
    def nhole(self, new):
        """Set number of hole operators.

        **Arguments**

        new
            Allowed values are either in [2,3] or None. If None is passed,
            nhole is defaulted to 3 hole operators.
        """
        if new is None:
            # set default value to three hole operators
            self._nhole = 3
        elif new in [2, 3]:
            self._nhole = new
        if not self._check_nhole():
            raise ArgumentError(
                f"Inconsistent number of hole operators ({new}) and electrons "
                f"({2 * self.occ_model.nacto[0]}). For S_z = [0, 1], 2 and 3 hole "
                "operators are supported, while for S_z = 2, only 3 hole "
                "operators are implemented. Decrease the "
                f"number of hole operators from {new} to {new-1} for "
                f"{int(self.s_z*2.0)} unpaired electrons if possible."
            )

    @property
    def dimension(self):
        """Total number of unknowns of chosen DIP model"""
        raise NotImplementedError

    def _check_nhole(self):
        """Check for consistency of the number of hole operators. Returns False
        if the number of hole operators does not agree with the spin projection
        and the number of active occupied orbitals.
        """
        raise NotImplementedError

    def set_hamiltonian(self, mo1, mo2):
        """Update auxiliary tensors for specific IP model"""
        raise NotImplementedError

    def compute_h_diag(self, *args):
        """Used by the Davidson module for pre-conditioning"""
        raise NotImplementedError

    def build_subspace_hamiltonian(self, b_vector, h_diag, *args):
        """Used by the Davidson module to construct subspace Hamiltonian"""
        raise NotImplementedError

    ###########################################################################
    # Printing operations for all DIP models
    ###########################################################################

    def print_ci_vector(self, ci_dict):
        """Print eigenvectors for various S_z

        **Arguments:**

        ci_dict:
            (OrderedDict) composite index as key, CI vector as value
        """
        raise NotImplementedError

    def print_weights(self, e_vec_j):
        """Print weights of R operators for various S_z

        **Arguments:**

        e_vec_j:
            (np.array) CI vector
        """
        raise NotImplementedError

    ###########################################################################
    # Indexing operations
    ###########################################################################

    def get_mask(self, select):
        """Get unique indices that are returned during diagonalization

        **Arguments:**

        select:
            (boolean) True for same spin, False for opposite spin
        """
        no, nv = self.occ_model.nacto[0], self.occ_model.nactv[0]
        mask = np.zeros((no, no, no, nv), dtype=bool)
        if self.s_z == 2.0 or (self.s_z == 1.0 and select):
            # case i<j<k
            indices_ = list(combinations(range(no), r=3))
            indices = tuple(np.array(indices_).T)
            mask[indices] = True
        elif self.s_z == 1.0:
            # case i<j, all k
            indices = np.triu_indices(no, 1)
            mask[indices] = True
        elif self.s_z == 0.0 and select:
            # case i<k, all i,J
            indices_ = np.triu_indices(no, 1)
            mask[indices_[0], :, indices_[1], :] = True
        elif self.s_z == 0.0 and not select:
            # case j<k, all i,J
            indices_ = np.triu_indices(no, 1)
            mask[:, indices_[0], indices_[1], :] = True
        return mask

    def get_index_of_mask(self, select):
        """Get unique indices of mask to assign during diagonalization

        **Arguments:**

        select:
            (boolean) True for same spin, False for opposite spin
        """
        mask = self.get_mask(select)
        indices = np.where(mask)
        return indices

    def get_index_ij(self, index):
        """
        Return hole-hole indices from composite index of CI vector

        ** Arguments: **

        index
            The composite index to be resolved
        """
        no = self.occ_model.nacto[0]
        # Triu index:
        if self.s_z == 0.0:
            j = index % no
            i = ((index - j) // no) % no
            return i, j
        if self.s_z == 1.0:
            triu = np.triu_indices(no, k=1)
        i = triu[0][index]
        j = triu[1][index]
        return i, j

    def get_index_ijkc(self, index):
        """
        Return hole-hole-hole-particle indices from composite index of CI vector

        ** Arguments: **

        index
            The composite index to be resolved
        """
        no, nv = self.occ_model.nacto[0], self.occ_model.nactv[0]
        if self.s_z == 0.0:
            end = no * no * (no - 1) // 2 * nv
            if index < end:
                spin = True
            else:
                index = index - end
                spin = False
            mask = self.get_mask(spin)
            # return True indices
            ind = np.where(mask)
            return (
                ind[0][index],
                ind[1][index],
                ind[2][index],
                ind[3][index],
                spin,
            )
        if self.s_z == 1.0:
            end = no * (no - 1) * (no - 2) // 6 * nv
            if index < end:
                # with symmetry i < j < k
                ijk, c = np.unravel_index(
                    int(index), ((no - 2) * (no - 1) * no // 6, nv)
                )
                i, j, k = list(combinations(range(no), r=3))[int(ijk)]
                return i, j, k, c, True
            # else:
            # with symmetry i < j, all k
            i_j, k, c = np.unravel_index(
                int(index - end), ((no - 1) * no // 2, no, nv)
            )
            tril = np.triu_indices(no, k=1)
            # Triu index:
            i = tril[0][i_j]
            j = tril[1][i_j]
            return i, j, k, c, False
        if self.s_z == 2.0:
            # with symmetry i < j < k
            ijk, c = np.unravel_index(
                int(index), ((no - 2) * (no - 1) * no // 6, nv)
            )
            i, j, k = list(combinations(range(no), r=3))[int(ijk)]
            return i, j, k, c, None
        raise NotImplementedError


class RDIPCC0(RDIPCC):
    """
    Restricted Double Ionization Potential Equation of Motion Coupled Cluster
    class restricted to Double IP for any CC reference function and 0 unpaired
    electrons (S_z=0.0 components)

    This class defines only the function that are universal for any DIP-CC model
    with 0 unpaired electron:

        * dimension (number of degrees of freedom)
        * _check_nhole (checks the maximum number of hole operators allowed)
        * print functions (ci vector and weights)
    """

    long_name = (
        "Double Ionization Potential Equation of Motion Coupled Cluster"
    )
    acronym = "DIP-EOM-CC"
    reference = "CC"
    order = "DIP"
    alpha = 0

    @property
    def dimension(self):
        """Total number of unknowns of chosen DIP model"""
        no, nv = self.occ_model.nacto[0], self.occ_model.nactv[0]
        if self.nhole == 3:
            return no * no + no * no * (no - 1) * nv
        if self.nhole == 2:
            return no * no
        raise NotImplementedError

    def _check_nhole(self):
        """Check for consistency of the number of hole operators. Returns False
        if the number of hole operators does not agree with the spin projection
        and the number of active occupied orbitals.
        """
        check_options("nhole", self.nhole, 2, 3)
        # s_z is set prior to the nhole property
        return self.nhole <= self.occ_model.nacto[0] * 2.0

    def print_ci_vector(self, ci_dict):
        """Print eigenvectors for S_z = 0.0

        **Arguments:**

        ci_dict:
            (OrderedDict) composite index as key, CI vector as value
        """
        nc, no = self.occ_model.ncore[0], self.occ_model.nacto[0]
        nco = nc + no
        # Loop over all composite indices above threshold
        for ind, ci in ci_dict.items():
            r_ijkc = ind - no * no
            if r_ijkc >= 0:
                i, j, k, c, same_spin = self.get_index_ijkc(r_ijkc)
                state = "r_iJkc" if same_spin else "r_iJKC"
                log(
                    f"{state:>17}:   ({i+nc+1: 4},{j+nc+1: 3},"
                    f"{k+nc+1: 3},{c+nco+1: 3})   {ci: 1.5f}"
                )
            else:
                i, j = self.get_index_ij(ind)
                log(
                    f"{'r_iJ':>17}:          ({i+nc+1: 4},"
                    f"{j+nc+1: 4})   {ci: 1.5f}"
                )

    def print_weights(self, e_vec_j):
        """Print weights of R operators for S_z = 0.0

        **Arguments:**

        e_vec_j:
            (np.array) CI vector
        """
        no, nv = self.occ_model.nacto[0], self.occ_model.nactv[0]
        no2 = no * no
        w_iJ = np.dot(e_vec_j[:no2], e_vec_j[:no2])
        log(f"{'weight(r_iJ)':>17}: {w_iJ: 1.5f}")
        if self.nhole > 2:
            end = no * no * (no - 1) // 2 * nv + no2
            w_iJkc = np.dot(e_vec_j[no2:end], e_vec_j[no2:end])
            w_iJKC = np.dot(e_vec_j[end:], e_vec_j[end:])
            log(f"{'weight(r_iJkc)':>17}: {w_iJkc: 1.5f}")
            log(f"{'weight(r_iJKC)':>17}: {w_iJKC: 1.5f}")
        #
        # Assess spin symmetry of state. Since we do not have a spin-adapted
        # implementation, we can make an educated check/guess here.
        multiplicity = self._check_multiplicity(e_vec_j, w_iJ)
        log(f"Suggested spin multiplicity: {multiplicity}")
        log(" ")

    def _check_multiplicity(self, e_vec_j, w_iJ):
        """Check and guess the multiplicity of a state based on CI weights"""
        no, nv = self.occ_model.nacto[0], self.occ_model.nactv[0]
        no2 = no * no
        # First check for approximate symmetry of R_iJ (R_iJ == R_Ji or -R_Ji)
        r_iJ = e_vec_j[:no2].reshape(no, no)
        r_iI = r_iJ.diagonal()
        triplet = np.allclose(
            r_iJ, -r_iJ.transpose(), rtol=1e-3, atol=1e-5
        ) and np.all(abs(r_iI) < 1e-8)
        if w_iJ > 1e-5:
            # If R_ij contributions are not zero, decide solely on its symmetry
            multiplicity = "triplet" if triplet else "singlet"
            return multiplicity
        # Second: compare symmetry of vectors R_iJkc and R_iJKC, for pure
        # singlet states we have R_iJkc ~ R_Jikc
        # This is a bit more complicated and requires more operations
        if self.nhole > 2:
            end = no * no * (no - 1) // 2 * nv + no2
            r_iJkc = self.denself.create_four_index(no, no, no, nv)
            r_iJKC = self.denself.create_four_index(no, no, no, nv)
            # assign R_iJkc
            mask = self.get_index_of_mask(True)
            r_iJkc.assign(e_vec_j[no2:end], ind=mask)
            # account for symmetry (ik)
            r_iJkc.iadd_transpose((2, 1, 0, 3), factor=-1.0)
            # assign R_iJKC
            mask = self.get_index_of_mask(False)
            r_iJKC.assign(e_vec_j[end:], ind=mask)
            # account for symmetry (JK)
            r_iJKC.iadd_transpose((0, 2, 1, 3), factor=-1.0)
            # transpose inplace to compare values
            r_iJKC.itranspose((1, 0, 2, 3))
            # assess multiplicity
            # R_iJkc ~= R_JiKC (R_iJKC is transposed here)
            singlet = np.allclose(r_iJkc.array, r_iJKC.array, 1e-3, 1e-5)
            # R_iJkc ~= -R_iJKC (R_iJKC is transposed here)
            triplet = np.allclose(r_iJkc.array, -r_iJKC.array, 1e-3, 1e-5)
            # R_iJkc ~= -R_ikJc
            quintet = np.allclose(
                r_iJkc.array, -r_iJkc.array.transpose(0, 2, 1, 3), 1e-3, 1e-5
            )
            if singlet and not triplet and not quintet:
                return "singlet"
            if triplet and not quintet:
                return "triplet"
            if quintet:
                return "quintet"
        return "inconclusive"


class RDIPCC2(RDIPCC):
    """
    Restricted Double Ionization Potential Equation of Motion Coupled Cluster
    class restricted to Double IP for any CC reference function and 2 unpaired
    electrons (S_z=1.0 components)

    This class defines only the function that are universal for the DIP-CC model
    with 2 unpaired electron:

        * dimension (number of degrees of freedom)
        * _check_nhole (checks the maximum number of hole operators allowed)
        * print functions (ci vector and weights)
    """

    long_name = (
        "Double Ionization Potential Equation of Motion Coupled Cluster"
    )
    acronym = "DIP-EOM-CC"
    reference = "CC"
    order = "DIP"
    alpha = 2

    @property
    def dimension(self):
        """Total number of unknowns of chosen DIP model"""
        no, nv = self.occ_model.nacto[0], self.occ_model.nactv[0]
        if self.nhole == 3:
            return (
                no * (no - 1) // 2
                + no * (no - 1) * (no - 2) // 6 * nv
                + (no * (no - 1) // 2) * no * nv
            )
        if self.nhole == 2:
            return no * (no - 1) // 2
        raise NotImplementedError

    def _check_nhole(self):
        """Check for consistency of the number of hole operators. Returns False
        if the number of hole operators does not agree with the spin projection
        and the number of active occupied orbitals.
        """
        check_options("nhole", self.nhole, 2, 3)
        # s_z is set prior to the nhole property
        return self.nhole <= self.occ_model.nacto[0]

    def print_ci_vector(self, ci_dict):
        """Print eigenvectors for S_z = 1.0

        **Arguments:**

        ci_dict:
            (OrderedDict) composite index as key, CI vector as value
        """
        nc, no = self.occ_model.ncore[0], self.occ_model.nacto[0]
        noo = no * (no - 1) // 2
        nco = nc + no
        # Loop over all composite indices above threshold
        for ind, ci in ci_dict.items():
            r_ijkc = ind - noo
            if r_ijkc >= 0:
                i, j, k, c, same_spin = self.get_index_ijkc(r_ijkc)
                state = "r_ijkc" if same_spin else "r_ijKC"
                log(
                    f"{state:>17}:   ({i+nc+1: 4},{j+nc+1: 3},"
                    f"{k+nc+1: 3},{c+nco+1: 3})   {ci: 1.5f}"
                )
            else:
                i, j = self.get_index_ij(ind)
                log(
                    f"{'r_ij':>17}:          ({i+nc+1: 4},"
                    f"{j+nc+1: 4})   {ci: 1.5f}"
                )

    def print_weights(self, e_vec_j):
        """Print weights of R operators for S_z = 1.0

        **Arguments:**

        e_vec_j:
            (np.array) CI vector
        """
        no, nv = self.occ_model.nacto[0], self.occ_model.nactv[0]
        noo = no * (no - 1) // 2
        w_ij = np.dot(e_vec_j[:noo], e_vec_j[:noo])
        w_ijkc = 0.0
        w_ijKC = 0.0
        log(f"{'weight(r_ij)':>17}: {w_ij: 1.5f}")
        if self.nhole > 2:
            end = no * (no - 1) * (no - 2) // 6 * nv + noo
            w_ijkc = np.dot(e_vec_j[noo:end], e_vec_j[noo:end])
            w_ijKC = np.dot(e_vec_j[end:], e_vec_j[end:])
            log(f"{'weight(r_ijkc)':>17}: {w_ijkc: 1.5f}")
            log(f"{'weight(r_ijKC)':>17}: {w_ijKC: 1.5f}")
        #
        # Assess spin symmetry of state. Since we do not have a spin-adapted
        # implementation, we can make an educated check/guess here.
        multiplicity = self._check_multiplicity(e_vec_j, w_ij, w_ijkc, w_ijKC)
        log(f"Suggested spin multiplicity: {multiplicity}")
        log(" ")

    def _check_multiplicity(self, e_vec_j, w_ij, w_ijkc, w_ijKC):
        """Check and guess the multiplicity of a state based on CI weights"""
        no = self.occ_model.nacto[0]
        noo = no * (no - 1) // 2
        # First: check for R_ij (if any, we assume triplet states)
        check = np.any(abs(e_vec_j[:noo]) > 1e-6) and w_ij > 1e-6
        # Second: compare weights of R_ijkc and R_ijKC, for pure quartet states
        # we have w_ijKC ~ 3*w_ijkc
        if (
            not math.isclose(w_ijKC, 3 * w_ijkc, rel_tol=1e-3, abs_tol=1e-5)
            or check
        ):
            return "triplet"
        return "quintet"


class RDIPCC4(RDIPCC):
    """
    Restricted Double Ionization Potential Equation of Motion Coupled Cluster
    class restricted to Double IP for any CC reference function and 4 unpaired
    electrons (S_z=2.0 components)

    This class defines only the function that are universal for any DIP-CC model
    with 4 unpaired electron:

        * dimension (number of degrees of freedom)
        * _check_nhole (checks the maximum number of hole operators allowed)
        * print functions (ci vector and weights)
    """

    long_name = (
        "Double Ionization Potential Equation of Motion Coupled Cluster"
    )
    acronym = "DIP-EOM-CC"
    reference = "CC"
    order = "DIP"
    alpha = 4

    @property
    def dimension(self):
        """Total number of unknowns of chosen DIP model"""
        no, nv = self.occ_model.nacto[0], self.occ_model.nactv[0]
        if self.nhole == 3:
            return no * (no - 1) * (no - 2) // 6 * nv
        if self.nhole == 2:
            raise ConsistencyError(
                "For S_z = 2.0, at least 3 hole operators are required."
            )
        raise NotImplementedError

    def _check_nhole(self):
        """Check for consistency of the number of hole operators. Returns False
        if the number of hole operators does not agree with the spin projection
        and the number of active occupied orbitals.
        """
        check_options("nhole", self.nhole, 2, 3)
        return self.nhole == 3 and self.occ_model.nacto[0] >= 3.0

    def print_ci_vector(self, ci_dict):
        """Print eigenvectors for S_z = 2.0

        **Arguments:**

        ci_dict:
            (OrderedDict) composite index as key, CI vector as value
        """
        nc, no = self.occ_model.ncore[0], self.occ_model.nacto[0]
        nco = nc + no
        # Loop over all composite indices above threshold
        for ind, ci in ci_dict.items():
            i, j, k, c, _ = self.get_index_ijkc(ind)
            log(
                f"{'r_ijkC':>17}:   ({i+nc+1: 4},{j+nc+1: 3},{k+nc+1: 3},"
                f"{c+nco+1: 3})   {ci: 1.5f}"
            )

    def print_weights(self, e_vec_j):
        """Print weights of R operators for S_z = 2.0

        **Arguments:**

        e_vec_j:
            (np.array) CI vector
        """
        log(f"{'weight(r_ijkC)':>17}: {np.dot(e_vec_j[:], e_vec_j[:]): 1.5f}")
        log(" ")
