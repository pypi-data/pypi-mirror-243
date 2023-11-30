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
    :nactv:     number of active virtual orbitals in the principal configuration
    :nact:      total number of active orbitals (nacto+nactv)
    :e_ci:      eigenactvalues of CI Hamiltonian (IOData container attribute)
    :civ:       eigenactvectors of CI Hamiltonian (IOData container attribute)

    Indexing conactvention:
     :i,j,k,..: occupied orbitals of principal configuration
     :a,b,c,..: virtual orbitals of principal configuration
"""

from abc import ABC, abstractmethod

import numpy as np

from pybest import filemanager
from pybest.io.iodata import IOData
from pybest.log import log
from pybest.utils import check_options


class CSF(ABC):
    """Configuration State Function (CSF) base class. Contains all required methods
    to diagonalize the Hamiltonian using SD basis."""

    def __init__(self, rci):
        """
        **Arguments:**

        rci
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
        """Used by the davidson module to construct guess"""
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

    def get_index_d_csf(self, index):
        """Get the unique indices of some doubly excited CSF. Returns the set of
        active orbital indices without adding shift related to the frozen core
        orbitals.

        **Arguments:**

        *index:
            (int) The number that indicates doubly excited CSF which
            is contributing in the CI solution.
        """
        rci = self.object
        nacto = rci.nacto
        nactv = rci.nactv
        end_1 = nacto * nactv
        end_2 = end_1 + nacto * (nactv * (nactv - 1)) // 2
        end_3 = end_2 + nacto * (nacto - 1) // 2 * nactv
        end_4 = end_3 + (nacto * (nacto - 1) // 2 * nactv * (nactv - 1) // 2)
        if index < end_1:
            i = index // (nactv) + 1
            j = i
            a = index % nactv + nacto + 1
            b = a
            return i, a, j, b
        if index < end_2:
            index = index - end_1
            indices = np.where(CSF.get_mask_csf(self, "iab"))

        elif index < end_3:
            index = index - end_2
            indices = np.where(CSF.get_mask_csf(self, "iaj"))

        elif index < end_4:
            index = index - end_3
            indices = np.where(CSF.get_mask_csf(self, "iajb"))
        else:
            index = index - end_4
            indices = np.where(CSF.get_mask_csf(self, "iajb"))

        i, a, j, b = (
            indices[0][index],
            indices[1][index],
            indices[2][index],
            indices[3][index],
        )
        return (
            i + 1,
            a + 1 + nacto,
            j + 1,
            b + 1 + nacto,
        )

    def get_index_of_mask_csf(self, select):
        """Get the indices where the True values are assigned."""
        mask = self.get_mask_csf(select)
        indices = np.where(mask)
        return indices

    def get_mask_csf(self, select):
        """The function returns a 4-dimensional boolean np.array. True values
        are assigned to all non-redundant and symmetry-unique elements of the
        CI coefficient tensor for double excitations."""

        check_options(
            "select",
            select,
            "iab",
            "iaj",
            "iajb",
        )
        rci = self.object
        nacto = rci.nacto
        nactv = rci.nactv
        mask = np.zeros((nacto, nactv, nacto, nactv), dtype=bool)

        if select in ["iab"]:
            indices_o = np.triu_indices(nacto, 0)
            indices_v = np.triu_indices(nactv, 1)

            for i, j in zip(indices_o[0], indices_o[1]):
                mask[i, indices_v[0], i, indices_v[1]] = True

        elif select in ["iaj"]:
            indices_o = np.triu_indices(nacto, 1)
            indices_v = np.triu_indices(nactv, 0)

            for a in indices_v[0]:
                mask[indices_o[0], a, indices_o[1], a] = True

        else:
            indices_o = np.triu_indices(nacto, 1)
            indices_v = np.triu_indices(nactv, 1)
            for i, j in zip(indices_o[0], indices_o[1]):
                mask[i, indices_v[0], j, indices_v[1]] = True
        return mask

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
                nacto * nactv
                + nacto * (nactv * (nactv - 1)) // 2
                + nacto * (nacto - 1) // 2 * nactv
                + nacto * (nacto - 1) * nactv * (nactv - 1) // 2
            ) + 1
        return (
            nacto * nactv
            + (
                nacto * nactv
                + nacto * (nactv * (nactv - 1)) // 2
                + nacto * (nacto - 1) // 2 * nactv
                + nacto * (nacto - 1) * nactv * (nactv - 1) // 2
            )
            + 1
        )
