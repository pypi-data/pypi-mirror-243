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

# TODO: enable when, python3.7 is minimal python supported
# from __future__ import annotations

from typing import Union

import h5py as h5
import numpy as np
import pytest

from pybest.context import context
from pybest.gbasis import Basis, get_gobasis
from pybest.io import load_h5
from pybest.linalg import CholeskyLinalgFactory, DenseLinalgFactory
from pybest.occ_model import (
    AufbauOccModel,
    AufbauSpinOccModel,
    FermiOccModel,
    FixedOccModel,
    FractionalOccModel,
)

test_aufbau_base_cases = [
    # basis, molecule, charge, #unpaired electrons (alpha),
    # kwargs (only used by some occupation models)
    (
        "cc-pvdz",
        "test/water.xyz",
        {"charge": 0, "nocc_a": 5},
        {"charge": 0, "nel": 10},
    ),
    (
        "cc-pvdz",
        "test/water.xyz",
        {"charge": 1, "nocc_a": 5, "nocc_b": 4},
        {"charge": 1, "nel": 9},
    ),
]

test_fixed_base_cases = [
    # basis, molecule, charge, #unpaired electrons (alpha),
    # kwargs (only used by some occupation models)
    (
        "cc-pvdz",
        "test/water.xyz",
        {"charge": 0, "occ_a": np.array([1, 1, 1, 1, 1])},
        {"charge": 0, "nel": 10},
    ),
    (
        "cc-pvdz",
        "test/water.xyz",
        {
            "charge": 1,
            "occ_a": np.array([1, 1, 1, 1, 1]),
            "occ_b": np.array([1, 1, 1, 1]),
        },
        {"charge": 1, "nel": 9},
    ),
]

test_occ_model_cases = [
    (AufbauOccModel, ["charge"]),  # NO kwargs
    (AufbauSpinOccModel, ["charge"]),  # NO kwargs
    (
        FractionalOccModel,
        ["nocc_a", "nocc_b", "charge"],
    ),  # requires nocc_a and/or nocc_b
    (FermiOccModel, ["charge"]),  # NO kwargs
]


test_instance = ["gobasis", "lf_dense", "lf_cholesky"]

###############################################################################
## Tests for Base class OccupationModel #######################################
###############################################################################


# All classes based on Aufbau


@pytest.mark.parametrize("basis,mol,kwargs,expected", test_aufbau_base_cases)
@pytest.mark.parametrize("occ_model_class,args", test_occ_model_cases)
@pytest.mark.parametrize(
    "factory", [Basis, DenseLinalgFactory, CholeskyLinalgFactory]
)
def test_aufbau_base(
    basis,
    mol,
    kwargs,
    expected,
    occ_model_class,
    args,
    factory: Union[Basis, DenseLinalgFactory, CholeskyLinalgFactory],
):
    """Test base class for occupation models using gobasis.

    We test only for charge and nel arguments.
    """
    fn_xyz = context.get_fn(mol)
    gobasis = get_gobasis(basis, fn_xyz, print_basis=False)
    # maps factory class to it's fixture instance
    factory_map = {
        Basis: gobasis,
        DenseLinalgFactory: DenseLinalgFactory(gobasis.nbasis),
        CholeskyLinalgFactory: CholeskyLinalgFactory(gobasis.nbasis),
    }
    used_kwargs = {}
    for key, val in kwargs.items():
        for arg in args:
            if key == arg:
                used_kwargs.update({key: val})

    occ_model = occ_model_class(
        factory_map[factory], **used_kwargs, nel=expected["nel"]
    )
    assert isinstance(occ_model, occ_model_class)
    for key, value in expected.items():
        # check all other attributes
        assert getattr(occ_model, key) == value


# All classes based on Fixed


@pytest.mark.parametrize("basis,mol,kwargs,expected", test_fixed_base_cases)
@pytest.mark.parametrize(
    "factory", [Basis, DenseLinalgFactory, CholeskyLinalgFactory]
)
def test_fixed_base(
    basis,
    mol,
    kwargs,
    expected,
    factory: Union[Basis, DenseLinalgFactory, CholeskyLinalgFactory],
):
    """Test base class for occupation models using gobasis.

    We test only for charge and nel arguments.
    """
    fn_xyz = context.get_fn(mol)
    gobasis = get_gobasis(basis, fn_xyz, print_basis=False)

    # maps factory class to it's fixture instance
    factory_map = {
        Basis: gobasis,
        DenseLinalgFactory: DenseLinalgFactory(gobasis.nbasis),
        CholeskyLinalgFactory: CholeskyLinalgFactory(gobasis.nbasis),
    }

    occ_model = FixedOccModel(factory_map[factory], **kwargs)
    assert isinstance(occ_model, FixedOccModel)

    for key, value in expected.items():
        # check all other attributes
        assert getattr(occ_model, key) == value


#
# Test dumping/loading occupation model to disk
#

gobasis1 = get_gobasis(
    "cc-pvdz", context.get_fn("test/water.xyz"), print_basis=False
)

test_data_hdf5 = [
    (gobasis1, {}),
    (DenseLinalgFactory(12), {"nel": 10}),
    (CholeskyLinalgFactory(12), {"nel": 10}),
]

test_occ_model_hdf5 = [
    (AufbauOccModel, {}),
    (FractionalOccModel, {"nocc_a": 5.0}),
    (AufbauSpinOccModel, {}),
    (FermiOccModel, {}),
    (FixedOccModel, {"occ_a": np.array([1, 1, 1, 1, 1])}),
]


@pytest.mark.parametrize("occ_model_class,kwargs1", test_occ_model_hdf5)
@pytest.mark.parametrize("basis,kwargs2", test_data_hdf5)
def test_hdf5(occ_model_class, kwargs1, basis, kwargs2):
    """Test dumping and reading of hdf5 files. We test only the base class
    names."""
    om1 = occ_model_class(basis, **kwargs1, **kwargs2)
    # without default nbasis
    with h5.File(
        f"{occ_model_class.__name__}_hdf5",
        driver="core",
        backing_store=False,
        mode="w",
    ) as f:
        # dump to file
        om1.to_hdf5(f)
        # read from file using class implementation
        om2 = occ_model_class.from_hdf5(f)
        assert isinstance(
            om2, occ_model_class
        ), "failed reading file using cls method"
        assert om1.charge == om2.charge, "wrong charge"
        assert om1.nel == om2.nel, "wrong number of electrons"
        assert om1.nbasis == om2.nbasis, "wrong list of nbasis"
        # test if type of factory agrees
        assert isinstance(
            om2.factory, type(om1.factory)
        ), "wrong factory instance"

        # load again using io implementation
        om3 = load_h5(f)
        assert isinstance(om3, occ_model_class), "failed reading file using io"
        assert om1.charge == om3.charge
        assert om1.nel == om3.nel, "wrong number of electrons"
        assert om1.nbasis == om3.nbasis, "wrong list of nbasis"
        # test if type of gobasis agrees
        assert isinstance(
            om3.factory, type(om1.factory)
        ), "wrong factory instance"
