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
    :nact:      total number of active orbitals (nacto+nactv)
    :e_ci:      eigenvalues of CI Hamiltonian (IOData container attribute)
    :civ:       eigenvectors of CI Hamiltonian (IOData container attribute)

    Indexing convention:
     :i,j,k,..: occupied orbitals of principal configuration
     :a,b,c,..: virtual orbitals of principal configuration
"""
from abc import ABC, abstractmethod
from functools import partial
from itertools import count

import numpy as np

from pybest import filemanager
from pybest.auxmat import get_fock_matrix
from pybest.ci.rci_base import RCI
from pybest.exceptions import ArgumentError
from pybest.io import IOData
from pybest.linalg import CholeskyFourIndex
from pybest.log import log
from pybest.utils import check_options


class SpinFree(RCI, ABC):
    """Spin-free base class. Contains all required methods to diagonalize the
    Hamiltonian using the spin-free basis."""

    def __init__(self, lf, occ_model, pairs=False):
        log.cite("the pCCD-CI methods", "nowak2023")

        super().__init__(lf, occ_model)
        self.csf = False
        self._pairs = pairs
        self.dimension = self.acronym

    @property
    def ci_method(self):
        """Instance of SD- or CSF-type class.
        Currently not supported."""
        return None

    @property
    def pairs(self):
        """Boolean argument.
        True: include the pairs excitation
        False: exclude the pairs excitations"""
        return self._pairs

    @pairs.setter
    def pairs(self, new):
        if not isinstance(new, bool):
            raise ArgumentError(
                "Unkown type for keyword pairs. Boolean type required."
            )
        self._pairs = new

    @RCI.dimension.setter
    def dimension(self, new=None):
        if new is not None:
            self._dimension = SpinFree.set_dimension(
                new,
                self.nacto,
                self.nactv,
                pairs=self.pairs,
            )

    @RCI.nroot.setter
    def nroot(self, new):
        self._nroot = new

    @RCI.davidson.setter
    def davidson(self, new):
        if not isinstance(new, bool):
            raise ArgumentError(
                "Unkown type for keyword davidson. Boolean type required."
            )
        self._davidson = new

    def calculate_exact_hamiltonian(self):
        """Calculate the exact Hamiltonian of the pCCD-CIS model."""
        raise NotImplementedError

    @abstractmethod
    def build_subspace_hamiltonian(self, bvector, hamiltonian, *args):
        """Construction of sigma vector."""

    @abstractmethod
    def compute_h_diag(self, *arg):
        """The diagonal of the Hamiltonian."""

    def build_guess_vectors(self, nguess, todisk, *args):
        """Used by davidson module to construct guess"""
        bvector = []
        hdiag = args[0]
        sortedind = hdiag.sort_indices(True)

        np.delete(sortedind, np.where(sortedind == 0))
        np.insert(sortedind, 0, 0)

        dim = self.dimension
        #
        # Construct guess vectors according to hdiag
        #
        b = self.lf.create_one_index(dim)
        counter = 0
        for ind in count(start=0, step=1):
            if ind >= nguess:
                break
            if ind >= dim:
                if log.do_medium:
                    log.warn(f"Maximum number of guess vectors reached: {dim}")
                break
            b.clear()
            b.set_element(sortedind[ind], 1)
            if todisk:
                b_v = IOData(vector=b)
                filename = filemanager.temp_path(f"bvector_{ind}.h5")
                b_v.to_file(filename)
                counter += 1
            else:
                # have to append a copy
                bvector.append(b.copy())
        if todisk:
            return None, counter
        return bvector, len(bvector)

    def get_mask(self):
        """The function returns a 4-dimensional boolean np.array. True values
        are assigned to all non-redundant and symmetry-unique elements of the
        CI coefficient tensor for double excitations."""
        mask = np.zeros(
            (self.nacto, self.nactv, self.nacto, self.nactv), dtype=bool
        )
        indices_o = np.triu_indices(self.nacto, 1)
        indices_v = np.triu_indices(self.nactv, 1)

        for i, j in zip(indices_o[0], indices_o[1]):
            mask[i, indices_v[0], j, indices_v[1]] = True
        return mask

    def get_index_of_mask(self):
        """Get the indices where the True values are assigned."""
        mask = self.get_mask()
        indices = np.where(mask)
        return indices

    @staticmethod
    def set_dimension(acronym, nacto, nactv, pairs=False):
        """Sets the dimension/number of unknowns of the chosen CI flavour."""
        check_options(
            "acronym",
            acronym,
            "pCCD-CIS",
            "pCCD-CID",
            "pCCD-CISD",
        )
        if acronym == "pCCD-CIS":
            return nacto * nactv + 1

        if acronym == "pCCD-CID":
            dim = (
                (nacto * nacto * nactv * nactv + nacto * nactv) // 2
                - nacto * nactv
                + 1
            )
            if pairs:
                return dim + nacto * nactv
            return dim
        if acronym == "pCCD-CISD":
            dim = (nacto * nacto * nactv * nactv + nacto * nactv) // 2 + 1
            if pairs:
                return dim + nacto * nactv
            return dim
        raise NotImplementedError

    def set_hamiltonian(self, mo1, mo2):
        """Compute auxiliary matrices.

        **Arguments:**

        mo1, mo2
            One- and two-electron integrals (some Hamiltonian matrix
            elements) in the MO basis.
        """
        self.clear_cache()
        #
        # 1) Fock matrix: fpq
        #
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
        slices = ["ovvo", "ovov"]
        for slice_ in slices:
            self.init_cache(f"g{slice_}", alloc=alloc(mo2, slice_))

        if self.acronym in ["pCCD-CIS", "pCCD-CID", "pCCD-CISD"]:
            #
            # Get blocks
            #
            slices = ["ooov", "oooo", "ovvv", "vvvv"]
            for slice_ in slices:
                self.init_cache(f"g{slice_}", alloc=alloc(mo2, slice_))

            # 6) temporary matrix: gppqq
            gppqq = self.init_cache("gppqq", self.nact, self.nact)
            mo2.contract("aabb->ab", gppqq)

    def get_index_s(self, index):
        """Get index for single excitation."""
        b = index % self.nactv
        j = ((index - b) / self.nactv) % self.nacto
        return int(j), int(b)

    def get_index_d(self, index):
        """Get the unique indices of some doubly excited CSF. Returns the set of
        active orbital indices without adding shift related to the frozen core
        orbitals.

        **Arguments:**

        *index:
            (int) The number that encodes a doubly excited spin-free determinant
            contributing to the CI solution.
        """
        nacto = self.nacto
        nactv = self.nactv
        k = 1
        if self.pairs:
            k = 0
        if nacto < 2:
            ind = np.triu_indices(nactv, k)
            i = 1
            a = ind[0][index] + 1 + nacto
            j = i
            b = ind[1][index] + 1 + nacto
            return i, a, j, b

        mask = np.ones((nacto, nactv, nacto, nactv))
        mask = np.reshape(mask, (nacto * nactv, nacto * nactv))
        mask = np.triu(mask, k)
        mask = np.reshape(mask, (nacto, nactv, nacto, nactv))

        ind = np.where(mask)
        i = ind[0][index] + 1
        a = ind[1][index] + 1 + nacto
        j = ind[2][index] + 1
        b = ind[3][index] + 1 + nacto

        return i, a, j, b
