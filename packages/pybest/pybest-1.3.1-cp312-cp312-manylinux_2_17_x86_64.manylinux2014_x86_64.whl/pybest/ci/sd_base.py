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

import numpy as np

from pybest import filemanager
from pybest.io.iodata import IOData
from pybest.log import log
from pybest.utils import check_options


class SD(ABC):
    """Slater Determinant (SD) base class. Contains all required methods
    to diagonalize the Hamiltonian using SD basis."""

    def __init__(self, rci):
        """
        **Arguments:**

        obj
            The object of RCI class (RCIS/RCID/RCISD).

        """

        self._object = rci
        self._dimension = rci.dimension

    @property
    def dimension(self):
        """The dimension of the Hamiltonian matrix."""
        return self._dimension

    @dimension.setter
    @abstractmethod
    def dimension(self, new=None):
        raise NotImplementedError

    @property
    def object(self):
        """The object of RCI class (RCIS/RCID/RCISD)."""
        return self._object

    @abstractmethod
    def build_subspace_hamiltonian(self, bvector, hamiltonian, *args):
        """Construction of sigma vector."""

    @abstractmethod
    def compute_h_diag(self, *args):
        """The diagonal of the Hamiltonian."""

    def build_guess_vectors(self, nguess, todisk, *args):
        """Used by the Davidson module to construct guess"""
        rci = self.object
        bvector = []
        hdiag = args[0]
        sortedind = hdiag.sort_indices(True)
        dim = self.dimension
        #
        # Construct Guess vectors according to hdiag
        #
        b = rci.lf.create_one_index(dim)
        count = 0
        for ind in range(nguess):
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
                count += 1
            else:
                # have to append a copy
                bvector.append(b.copy())
        if todisk:
            return None, count
        return bvector, len(bvector)

    def get_mask(self):
        """The function returns a 4-dimensional boolean np.array. True values
        are assigned to all non-redundant and symmetry-unique elements of the
        CI coefficient tensor for double excitations."""
        rci = self.object
        mask = np.zeros(
            (rci.nacto, rci.nactv, rci.nacto, rci.nactv), dtype=bool
        )
        indices_o = np.triu_indices(rci.nacto, 1)
        indices_v = np.triu_indices(rci.nactv, 1)

        for i, j in zip(indices_o[0], indices_o[1]):
            mask[i, indices_v[0], j, indices_v[1]] = True
        return mask

    def get_index_of_mask(self):
        """Get the indices where the True values are assigned."""
        mask = self.get_mask()
        indices = np.where(mask)
        return indices

    def get_index_d(self, rci, index):
        """Get the unique indices of some doubly excited SD. Returns the set of
        active orbital indices without adding shift related to the frozen core
        orbitals.

        **Arguments:**

        *index:
            (int) The number that indicates doubly excited SD which
            is contributing in the CI solution.
        """
        # Case 1) C_iaJB:
        end_ab = rci.nacto * rci.nacto * rci.nactv * rci.nactv
        # Case 2) C_iajb:
        end_aa = ((rci.nacto * (rci.nacto - 1)) // 2) * (
            (rci.nactv * (rci.nactv - 1)) // 2
        )
        # 1) we store all i,a,j,b and we can simply use np's unravel_index build-in function
        if index < end_ab:
            (i, a, j, b) = np.unravel_index(
                index, (rci.nacto, rci.nactv, rci.nacto, rci.nactv)
            )
            i, a, j, b = (
                i + 1,
                a + 1 + rci.nacto,
                j + 1,
                b + 1 + rci.nacto,
            )
            return i, a, j, b
        # 2) This is more complicated, one possible way is to use a mask function:
        index = index - end_ab
        # 3) This is the same as case 2) but index has to be shifted by end_aa as well
        if index > end_aa:
            index = index - end_aa
        ind = np.where(self.get_mask())
        i, a, j, b = (
            ind[0][index],
            ind[1][index],
            ind[2][index],
            ind[3][index],
        )
        return (
            i + 1,
            a + 1 + rci.nacto,
            j + 1,
            b + 1 + rci.nacto,
        )

    @staticmethod
    def set_dimension(acronym, nacto, nactv):
        """Sets the dimension/number of unknowns of the chosen CI flavour."""

        check_options(
            "acronym",
            acronym,
            "CIS",
            "CID",
            "CISD",
        )
        if acronym == "CIS":
            return nacto * nactv + 1

        if acronym == "CID":
            return (
                nacto * nacto * nactv * nactv
                + ((nacto * (nacto - 1)) // 2)
                * ((nactv * (nactv - 1)) // 2)
                * 2
            ) + 1
        return (
            nacto * nactv * 2
            + (
                nacto * nacto * nactv * nactv
                + ((nacto * (nacto - 1)) // 2)
                * ((nactv * (nactv - 1)) // 2)
                * 2
            )
            + 1
        )
