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


import pytest

from pybest.context import context
from pybest.exceptions import (
    ArgumentError,
    ConsistencyError,
    ElectronCountError,
)
from pybest.gbasis import Basis, get_gobasis
from pybest.linalg import DenseLinalgFactory
from pybest.occ_model import AufbauOccModel

test_aufbau = [
    # basis, molecule, {charge, #unpaired electrons (alpha), ncore}
    # test also different combinations of alpha/charge/unrestricted
    (
        "cc-pvdz",
        "test/water.xyz",
        {"charge": 0, "alpha": 0, "ncore": 0},
        {
            "occ": [[1, 1, 1, 1, 1]],
            "charge": 0,
            "nel": 10,
            "nbasis": [24],
            "nact": [24],
            "nocc": [5],
            "nvirt": [19],
            "nacto": [5],
            "nactv": [19],
            "ncore": [0],
        },
    ),
    (
        "cc-pvdz",
        "test/water.xyz",
        {"charge": 0, "alpha": 0, "ncore": 0, "unrestricted": True},
        {
            "occ": [[1, 1, 1, 1, 1], [1, 1, 1, 1, 1]],
            "charge": 0,
            "nel": 10,
            "nbasis": [24, 24],
            "nact": [24, 24],
            "nocc": [5, 5],
            "nvirt": [19, 19],
            "nacto": [5, 5],
            "nactv": [19, 19],
            "ncore": [0, 0],
        },
    ),
    (
        "cc-pvdz",
        "test/water.xyz",
        {"charge": 0, "alpha": 0, "ncore": 1, "unrestricted": True},
        {
            "occ": [[1, 1, 1, 1, 1], [1, 1, 1, 1, 1]],
            "charge": 0,
            "nel": 10,
            "nbasis": [24, 24],
            "nact": [23, 23],
            "nocc": [5, 5],
            "nvirt": [19, 19],
            "nacto": [4, 4],
            "nactv": [19, 19],
            "ncore": [1, 1],
        },
    ),
    (
        "cc-pvdz",
        "test/water.xyz",
        {"charge": 0, "alpha": 0, "ncore": 1},
        {
            "occ": [[1, 1, 1, 1, 1]],
            "charge": 0,
            "nel": 10,
            "nbasis": [24],
            "nact": [23],
            "nocc": [5],
            "nvirt": [19],
            "nacto": [4],
            "nactv": [19],
            "ncore": [1],
        },
    ),
    (
        "cc-pvdz",
        "test/water.xyz",
        {"charge": 1, "alpha": 1, "ncore": 0},
        {
            "occ": [[1, 1, 1, 1, 1], [1, 1, 1, 1]],
            "charge": 1,
            "nel": 9,
            "nbasis": [24, 24],
            "nact": [24, 24],
            "nocc": [5, 4],
            "nvirt": [19, 20],
            "nacto": [5, 4],
            "nactv": [19, 20],
            "ncore": [0, 0],
        },
    ),
    (
        "cc-pvdz",
        "test/water.xyz",
        {"charge": 1, "ncore": 0},  # test default value for alpha = 1
        {
            "occ": [[1, 1, 1, 1, 1], [1, 1, 1, 1]],
            "charge": 1,
            "nel": 9,
            "nbasis": [24, 24],
            "nact": [24, 24],
            "nocc": [5, 4],
            "nvirt": [19, 20],
            "nacto": [5, 4],
            "nactv": [19, 20],
            "ncore": [0, 0],
        },
    ),
    (
        "cc-pvdz",
        "test/water.xyz",
        {"charge": 1, "alpha": 1, "ncore": 1},
        {
            "occ": [[1, 1, 1, 1, 1], [1, 1, 1, 1]],
            "charge": 1,
            "nel": 9,
            "nbasis": [24, 24],
            "nact": [23, 23],
            "nocc": [5, 4],
            "nvirt": [19, 20],
            "nacto": [4, 3],
            "nactv": [19, 20],
            "ncore": [1, 1],
        },
    ),
]


@pytest.mark.parametrize("basis,mol,kwargs,expected", test_aufbau)
def test_occ_aufbau_gobasis(basis, mol, kwargs, expected):
    """Test Aufbau model for gobasis, charge, alpha, and ncore arguments as
    input."""
    fn_xyz = context.get_fn(mol)
    gobasis = get_gobasis(basis, fn_xyz, print_basis=False)
    lf = DenseLinalgFactory(gobasis.nbasis)
    # either restricted (alpha=0) or unrestricted orbitals (alpha>0)
    norbs = 1 if kwargs.get("alpha") == 0 else 2
    if kwargs.get("unrestricted", False):
        norbs = 2
    orb = [lf.create_orbital() for n in range(norbs)]

    occ_model = AufbauOccModel(gobasis, **kwargs)
    occ_model.assign_occ_reference(*orb)

    for key, value in expected.items():
        if key == "occ":
            # check occupation numbers of each orbital (alpha, beta)
            assert len(orb) == len(value)
            for orb_, el in zip(orb, value):
                assert abs(orb_.occupations[: len(el)] - el).max() < 1e-10
        else:
            # check all other attributes
            assert getattr(occ_model, key) == value


@pytest.mark.parametrize("basis,mol,kwargs,expected", test_aufbau)
def test_occ_aufbau_lf(basis, mol, kwargs, expected):
    """Test Aufbau model for lf, charge, alpha, and ncore arguments as
    input. We have to explicitly give ``nel`` otherwise we get an error.
    """
    # construct gobasis only to create some lf instance
    fn_xyz = context.get_fn(mol)
    gobasis = get_gobasis(basis, fn_xyz, print_basis=False)
    lf = DenseLinalgFactory(gobasis.nbasis)
    # either restricted (alpha=0) or unrestricted orbitals (alpha>0)
    norbs = 1 if kwargs.get("alpha") == 0 else 2
    if kwargs.get("unrestricted", False):
        norbs = 2
    orb = [lf.create_orbital() for n in range(norbs)]

    occ_model = AufbauOccModel(lf, **kwargs, nel=expected["nel"])
    occ_model.assign_occ_reference(*orb)

    for key, value in expected.items():
        if key == "occ":
            # check occupation numbers of each orbital (alpha, beta)
            assert len(orb) == len(value)
            for orb_, el in zip(orb, value):
                assert abs(orb_.occupations[: len(el)] - el).max() < 1e-10
        else:
            # check all other attributes
            assert getattr(occ_model, key) == value


#
# Additional tests for AufbauOccModel using lf instance
#

expected_lf_nel = {
    "occ": [[1, 1, 1, 1]],
    "charge": 0,
    "nel": 8,
    "nbasis": [8],
    "nact": [8],
    "nocc": [4],
    "nvirt": [4],
    "nacto": [4],
    "nactv": [4],
    "ncore": [0],
}


test_aufbau_lf_nel = [
    # nbasis, nel, nocc (as kwargs)
    (8, 8, {}, expected_lf_nel),
    (8, 8, {"nocc_a": 4}, expected_lf_nel),
    (8, None, {"nocc_a": 4}, expected_lf_nel),
    (8, None, {"nocc_a": 4, "nocc_b": 4}, expected_lf_nel),
    (8, 8, {"unrestricted": False}, expected_lf_nel),
]


@pytest.mark.parametrize("nbasis,nel,nocc,expected", test_aufbau_lf_nel)
def test_occ_aufbau_lf_nel(nbasis, nel, nocc, expected):
    """Test Aufbau model for lf, nel, and occ_a, occ_b as only input.
    Such an Aufbau model is used, for instance, in model Hamiltonians like
    Hubbard.
    """
    # construct gobasis only to create some lf instance
    lf = DenseLinalgFactory(nbasis)
    orb = [lf.create_orbital()]

    occ_model = AufbauOccModel(lf, nel=nel, **nocc)
    occ_model.assign_occ_reference(*orb)

    for key, value in expected.items():
        if key == "occ":
            # check occupation numbers of each orbital (alpha, beta)
            assert len(orb) == len(value)
            for orb_, el in zip(orb, value):
                assert abs(orb_.occupations[: len(el)] - el).max() < 1e-10
        else:
            # check all other attributes
            assert getattr(occ_model, key) == value


#
# Tests for unrestricted (open-shell) cases using AufbauOccModel
#

expected_lf_nel_os = {
    "occ": [[1, 1, 1, 1, 1], [1, 1, 1, 1]],
    "charge": 0,
    "nel": 9,
    "nbasis": [8, 8],
    "nact": [8, 8],
    "nocc": [5, 4],
    "nvirt": [3, 4],
    "nacto": [5, 4],
    "nactv": [3, 4],
    "ncore": [0, 0],
}


test_aufbau_lf_nel_os = [
    # nbasis, nel, nocc (as kwargs)
    (8, 9, {"alpha": 1}, expected_lf_nel_os),
    (8, 9, {}, expected_lf_nel_os),
    (8, 9, {"unrestricted": True}, expected_lf_nel_os),
    (8, 9, {"nocc_a": 5, "nocc_b": 4}, expected_lf_nel_os),
    (8, None, {"nocc_a": 5, "nocc_b": 4}, expected_lf_nel_os),
]


@pytest.mark.parametrize("nbasis,nel,nocc,expected", test_aufbau_lf_nel_os)
def test_occ_aufbau_lf_nel_os(nbasis, nel, nocc, expected):
    """Test Aufbau model for lf, nel, and occ_a, occ_b as only input.
    Such an Aufbau model is used, for instance, in model Hamiltonians like
    Hubbard.
    """
    # construct gobasis only to create some lf instance
    lf = DenseLinalgFactory(nbasis)
    orb = [lf.create_orbital(), lf.create_orbital()]

    occ_model = AufbauOccModel(lf, nel=nel, **nocc)
    occ_model.assign_occ_reference(*orb)

    for key, value in expected.items():
        if key == "occ":
            # check occupation numbers of each orbital (alpha, beta)
            assert len(orb) == len(value)
            for orb_, el in zip(orb, value):
                assert abs(orb_.occupations[: len(el)] - el).max() < 1e-10
        else:
            # check all other attributes
            assert getattr(occ_model, key) == value


#
# Invalid calls, all test should raise an error
#


test_wrong_arguments = [
    ({"foo": 5}, ArgumentError),  # unknown kwargs
    ({"nocc_b": 5}, ArgumentError),  # missing arguments nocc_a
    ({"nocc_a": 4, "nocc_b": 5}, ElectronCountError),  # nocc_a < nocc_b
    (
        {"nocc_a": 4, "nel": 9},
        ElectronCountError,
    ),  # nocc_a does not agree with nel
    ({"nocc_a": 5, "nocc_b": 5, "nel": 9}, ElectronCountError),
    # nel does not agree with gobasis information or nocc_a/nocc_b (for lf)
    ({"nocc_a": 5.5}, ConsistencyError),
    # nocc_a/nocc_b does not agree with nel
    (
        {
            "nocc_a": 5,
            "nocc_b": 4,
            "charge": 1,
            "nel": 8,
        },  # correct occupation and charge
        ElectronCountError,
    ),  # nocc_a/nocc_b or charge does not agree with nel
    (
        {
            "nocc_a": 5.1,
            "nocc_b": 3.9,
            "charge": 1,
        },  # correct occupation and charge
        ConsistencyError,
    ),  # only integer occupations are allowed
    (
        {
            "charge": 1,
            "unrestricted": False,
            "nel": 9,
        },
        ConsistencyError,
    ),  # cannot enforce restricted occupation pattern
]

test_instance = ["gobasis", "lf"]


@pytest.mark.parametrize("kwargs,error", test_wrong_arguments)
@pytest.mark.parametrize("factory", [Basis, DenseLinalgFactory])
def test_occ_aufbau_arguments(kwargs, error, factory):
    """Test Aufbau model for gobasis, nocc_a/nocc_b, and ncore arguments as
    input.
    """
    fn_xyz = context.get_fn("test/water.xyz")
    gobasis = get_gobasis("cc-pvdz", fn_xyz, print_basis=False)

    factory_map = {
        Basis: gobasis,
        DenseLinalgFactory: DenseLinalgFactory(gobasis.nbasis),
    }

    with pytest.raises(error):
        assert AufbauOccModel(factory_map[factory], **kwargs)


#
# Test all valid kwargs
#

test_kwargs = [
    (
        "cc-pvdz",
        "test/water.xyz",
        {
            "unrestricted": True,
            "alpha": 0,
            "charge": 0,
            "nel": 10,
            "ncore": 0,
            "nocc_a": 5,
            "nocc_b": 5,
        },
    ),
]

test_instance = ["gobasis", "lf"]


@pytest.mark.parametrize("basis,mol,kwargs", test_kwargs)
@pytest.mark.parametrize("factory", [Basis, DenseLinalgFactory])
def test_occ_aufbau_kwargs(basis, mol, kwargs, factory):
    """Test Aufbau model for gobasis, nocc_a/nocc_b, and ncore arguments as
    input.
    """
    fn_xyz = context.get_fn(mol)
    gobasis = get_gobasis(basis, fn_xyz, print_basis=False)
    factory_map = {
        Basis: gobasis,
        DenseLinalgFactory: DenseLinalgFactory(gobasis.nbasis),
    }

    assert isinstance(
        AufbauOccModel(factory_map[factory], **kwargs), AufbauOccModel
    )
