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

# Detailed changelog:
# This module has been originally written and updated by Paweł Tecmer (see CHANGELOG).
# Its current version contains updates from the PyBEST developer team.
#
# This implementation can also be found in `Horton 2.0.0`.
# However, this file has been updated and debugged. Compatibility with Horton is NOT
# guaranteed.
#
# Detailed changes (see also CHANGELOG):
# 2020-07-01: use abs class
# 2020-07-01: rename [compute_] functions
# 2020-07-01: exploit labels of NIndex objects
# 2023-01-01: added 1D ContactPotential (written by Filip Brzek, Piotr Zuchowski)


"""Physical Model Hamiltonians"""


import abc
from itertools import product
from typing import Callable, Tuple, Union

import numpy as np

from pybest.linalg import DenseFourIndex, DenseLinalgFactory, DenseTwoIndex
from pybest.log import log

__all__ = ["Hubbard", "ContactInteraction1D"]


class PhysModHam(abc.ABC):
    """Base class for the Physical Model Hamiltonians:
    * 1-D Hubbard
    * Contact Interaction Potential
    """

    def __init__(self, lf):
        """
        **Arguments:**
        lf - linalg factory (only dense is supported and tested)
        """

        self._lf = lf
        self._denself = DenseLinalgFactory(lf.default_nbasis)

    @property
    def lf(self):
        """The LinalgFactory"""
        return self._lf

    @property
    def denself(self):
        """The dense LinalgFactory"""
        return self._denself

    @abc.abstractmethod
    def compute_one_body(self) -> DenseTwoIndex:
        """Calculate the one-body term of the 1D Hubbard Hamiltonian"""
        raise NotImplementedError

    @abc.abstractmethod
    def compute_two_body(self) -> DenseFourIndex:
        """Calculate the two-body term of the 1D Hubbard Hamiltonian"""
        raise NotImplementedError

    def compute_overlap(self) -> DenseTwoIndex:
        """Calculate overlap of the 1-D contact interactions Hamiltonian,
        (identity matrix)"""
        result = self.lf.create_two_index(label="olp")
        result.assign_diagonal(1.0)
        return result


class Hubbard(PhysModHam):
    """The 1-D Hubbard class Hamiltonian"""

    def __init__(self, lf, pbc=True):
        """
        **Attributes:**

         pdb
             Periodic boundary conditions. Default, pdb=true

        """
        super().__init__(lf)
        self._pbc = pbc
        log.cite(
            "the implementation of Hubbard model Hamiltonian",
            "boguslawski2014a",
        )

    @property
    def pbc(self):
        """The periodic boundary conditions"""
        return self._pbc

    def compute_one_body(self, tparam=-1) -> DenseTwoIndex:
        """Calculate the one-body term of the 1D Hubbard Hamiltonian"""
        result = self.lf.create_two_index(label="kin")
        for i in range(self.lf.default_nbasis - 1):
            result.set_element(i, i + 1, tparam, 2)
        if self.pbc:
            result.set_element(self.lf.default_nbasis - 1, 0, tparam, 2)
        return result

    def compute_two_body(self, uparam=1) -> DenseFourIndex:
        """Calculate the two-body term of the 1D Hubbard Hamiltonian"""
        result = self.denself.create_four_index(label="eri")
        for i in range(self.denself.default_nbasis):
            result.set_element(i, i, i, i, uparam)
        return result


class ContactInteraction1D(PhysModHam):
    """The 1-D contact interactions in arbitrary external potential"""

    def __init__(
        self,
        lf: DenseLinalgFactory,
        domain: Union[Tuple[float, float, float], None] = None,
        mass: float = 1.0,
        potential: Union[Callable, None] = None,
    ):
        """
        **Attributes:**
        lf -- A DenseLinalgFactory instance
        domain -- list containing [x_min, x_max, dx] which defines the grid for
                  DVR (discrete variable representation), the default grid is
                  [-10:10] with a step of 0.1 which is suitable for the simple
                  harmonic oscillator
        mass -- mass of the particle in atomic units (hbar=1, electron mass=1)
                to avoid confusion, any type of fermions can be modeled
        potential -- external 1 variable function defining the potential
        """
        log.cite("DVR representation via the S-matrix Kohn method", "dvr-1991")

        # if no potential given, default to harmonic oscillator potential,
        # set other defaults to safe harmonic oscillator as well,
        if domain is None:
            domain = (-10, 10, 0.1)

        if potential is None:
            self._potential = self.harmonic_oscillator
        else:
            self._potential = potential

        # init base class
        super().__init__(lf)

        # here m_size should be same as lf.default_nbasis
        self._mass = mass
        self._m_size = lf.default_nbasis
        self._domain = domain

        # compute standard QC stuff, but on DVR grid
        self.compute_orbitals()

    @property
    def mass(self) -> float:
        """Mass of the fermions in the potential in atomic units"""
        return self._mass

    @property
    def grid(self) -> np.ndarray:
        """Integration grid"""
        return self._grid

    @property
    def energies(self) -> np.ndarray:
        """Orbital energies for DVR solution"""
        return self._energies

    @property
    def orbitals(self) -> np.ndarray:
        """Orbital coefficients for DVR solution, size grid x m_size"""
        return self._orbitals

    @property
    def potential(self) -> Callable:
        """The fermion-trapping potential"""
        return self._potential

    @property
    def domain(self) -> Tuple[float, float, float]:
        """Grid definition [min, max, step]"""
        return self._domain

    @property
    def m_size(self) -> int:
        """The number of DVR solutions to return for any standard QC scheme (it
        equals the number of orbitals)
        """
        return self._m_size

    @staticmethod
    def harmonic_oscillator(r):
        """Default harmonic oscillator potential"""
        return 0.5 * r**2

    @staticmethod
    def derivative_2order(x):
        """A second order derivative in DVR (discrete variable representation)
        for uni-distant grid in cartesian coordinates"""
        dx = x[1] - x[0]
        dx2 = dx * dx
        n_x = len(x)
        imatrix = np.kron(np.ones([n_x, 1]), np.arange(1, n_x + 1))
        # NOTE: mat_1 = (alternating -1 and +1)
        # [[-1  1 -1  1 ...]
        # [ 1 -1  1 -1 ...]
        # ...
        # Element-wise multiplication of row and column vector (order does not matter)
        mat_1 = np.resize([-1.0, 1.0], n_x) * np.resize(
            [1.0, -1.0], n_x
        ).reshape((n_x, 1))
        # TODO: what's the desired look-up of the state
        mat_2 = (imatrix - imatrix.T) ** (2)

        np.fill_diagonal(mat_2, 2 * 3.0 * np.pi ** (-2))
        mat_2[:] = 1 / mat_2
        return 2 * mat_1 * mat_2 / dx2

    def compute_orbitals(self):
        """Calculate the orbitals by diagonalizing the DVR (discrete variable
        representation)"""
        x_min, x_max, dx = self.domain
        if log.do_medium:
            log(
                "  Fermions in arbitrary 1D-potential, interacting via contact potential\n"
                " Grid size for integration of potential:\n"
                f"    x_min = {x_min}, x_max = {x_max}, dx = {dx}: "
            )
        # prepare grid
        grid = np.arange(x_min, x_max + dx, dx)

        # construct kinetic energy operator on the grid
        kinetic = (-1.0 / (2 * self.mass)) * self.derivative_2order(grid)

        # construct potential energy operator on the grid
        potential = np.zeros((grid.size, grid.size))
        np.fill_diagonal(potential, self.potential(grid))

        # construct full Hamiltonian on the grid
        hamiltonian = kinetic + potential

        # solve Hamiltonian on the grid
        energies, eigen_vectors = np.linalg.eigh(hamiltonian)

        # sort by energy
        idx = energies.argsort()[:-1:]
        sorted_energies = energies[idx]
        # re-normalize, as eigh returns eigenvectors normalize to 1
        sorted_eigen_vectors = eigen_vectors[:, idx] / np.sqrt(dx)

        # set the outputs
        self._energies = sorted_energies[0 : self.m_size + 1]
        self._orbitals = sorted_eigen_vectors[:, 0 : self.m_size + 1]
        self._grid = grid

    def compute_one_body(self) -> DenseTwoIndex:
        """Calculate the one-body term of the 1-D contact interactions
        Hamiltonian"""
        result: DenseTwoIndex = self.lf.create_two_index(label="one")
        result.assign_diagonal(self.energies, factor=1.0)
        return result

    def compute_two_body(self) -> DenseFourIndex:
        """Calculate the two-body term of the 1-D contact interactions
        Hamiltonian"""
        result: DenseFourIndex = self.denself.create_four_index(label="eri")
        #
        #  calculate integrals (ij|kl) = \int \psi_i(r) \psi_j(r) \psi_k(r) \psi_l(r) dr
        #     =  \sum_a  w_a \psi_i (x_a) \psi_j (x_a)

        # NOTE: this can be optimized in c++ extension
        # NOTE: pre-compute grid x (nbasis, nbasis, nbasis) primitive, that's O(N^4)!
        w_grid_ij = np.einsum("gi,gj->gij", self.orbitals, self.orbitals)
        w_grid_ijk = np.einsum("gij,gk->gijk", w_grid_ij, self.orbitals)

        for i, j, k, l in product(
            range(self.m_size),
            range(self.m_size),
            range(self.m_size),
            range(self.m_size),
        ):
            if (i + j + k + l) % 2 == 0:
                w_grid_ijkl = w_grid_ijk[:, i, j, k] * self.orbitals[:, l]
                # NOTE: integrate on the grid
                contact_integral = np.trapz(w_grid_ijkl, self.grid)
                result.set_element(i, j, k, l, contact_integral, symmetry=1)

        return result
