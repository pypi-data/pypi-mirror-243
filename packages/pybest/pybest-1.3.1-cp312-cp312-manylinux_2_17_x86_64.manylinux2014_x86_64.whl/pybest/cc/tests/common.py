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
""" Common routines, classes, fixtures for CC tests. """

import numpy as np

from pybest.context import context
from pybest.gbasis import (
    compute_cholesky_eri,
    compute_eri,
    compute_kinetic,
    compute_nuclear,
    compute_nuclear_repulsion,
    compute_overlap,
    get_gobasis,
)
from pybest.gbasis.gobasis import PYBEST_CHOLESKY_ENABLED
from pybest.geminals.rpccd import RpCCD
from pybest.io.iodata import IOData
from pybest.linalg import DenseLinalgFactory, DenseTwoIndex, FourIndex
from pybest.occ_model import AufbauOccModel
from pybest.wrappers.hf import RHF


class Model:
    """Handles all common pre-CC operations."""

    def __init__(self, path_xyz, basis, read=True, **kwargs):
        self.init_input(context.get_fn(path_xyz), basis, **kwargs)
        name = path_xyz.split(".")[0]
        rhf = RHF(self.lf, self.occ_model)
        self.rhf = rhf(*self.ints(), self.olp, self.orb_a)
        if read:
            # Read pCCD orbitals and compute other pCCD-related quantities
            data = IOData.from_file(context.get_fn(name + "_pccd.molden"))
            pccd = RpCCD(self.lf, self.occ_model)
            self.pccd = pccd(*self.ints(), self.olp, data.orb_a, e_core=0.0)

    def init_input(self, xyz_file, basis, **kwargs):
        "Construct basis object and linear algebra factory, compute integrals."
        obasis = get_gobasis(basis, xyz_file, print_basis=False)
        self.occ_model = AufbauOccModel(obasis, **kwargs)
        self.lf = DenseLinalgFactory(obasis.nbasis)
        self.olp = compute_overlap(obasis)
        self.orb_a = self.lf.create_orbital(obasis.nbasis)
        # Integrals
        self.kin = compute_kinetic(obasis)
        self.ne = compute_nuclear(obasis)
        self.eri = compute_eri(obasis)
        self.cholesky_eri = None
        if PYBEST_CHOLESKY_ENABLED:
            self.cholesky_eri = compute_cholesky_eri(obasis, threshold=1e-9)
        self.ext = compute_nuclear_repulsion(obasis)

    def ints(self, linalg_factory=DenseLinalgFactory):
        "Returns list of one-body and two-body integrals."
        if linalg_factory is DenseLinalgFactory:
            return [self.kin, self.ne, self.eri]
        return [self.kin, self.ne, self.cholesky_eri]


def check_fock_in_cache(cache, labels, nocc=5, nvirt=8):
    "Checks if labels correspond to Fock matrix blocks in cache."
    dim = {"o": nocc, "v": nvirt}
    for label in labels:
        msg = f"{label} block in cc.hamiltonian: \n"
        matrix = cache.load(label)
        assert isinstance(matrix, DenseTwoIndex), msg + "incorrect type"
        assert matrix.shape[0] == dim[label[-2]], msg + "incorrect size"
        assert matrix.shape[1] == dim[label[-1]], msg + "incorrect size"
        # occupied-virtual block for RHF orbitals is zeros by nature
        if not label == "fock_ov":
            is_zeros = np.allclose(matrix.array, np.zeros(matrix.shape))
            assert not is_zeros, msg + " is filled with zeros!"


def check_eri_in_cache(cache, labels, nocc=5, nvirt=8):
    "Checks if labels correspond to 2-body CC Hamiltonian blocks in cache."
    dim = {"o": nocc, "v": nvirt}
    for label in labels:
        msg = f"Checking {label} block in cc.hamiltonian...\n"
        matrix = cache.load(label)
        assert isinstance(matrix, FourIndex), msg + "wrong type!"
        for i in range(4):
            assert matrix.shape[i] == dim[label[i - 4]], msg + "incorrect size"
        assert not np.allclose(matrix.array, np.zeros(matrix.array.shape))
        assert not np.isnan(matrix.array).any()
