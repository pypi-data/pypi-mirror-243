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


import itertools

import pytest

from pybest.ip_eom.sip_base import RSIPCC, RSIPCC1, RSIPCC3
from pybest.ip_eom.sip_pccd1 import RIPpCCD1
from pybest.ip_eom.sip_pccd3 import RIPpCCD3
from pybest.linalg import DenseLinalgFactory
from pybest.occ_model import AufbauOccModel

test_data_mask = [(10, 30, 0), (10, 30, 5)]


@pytest.mark.parametrize("occ, nbasis, ncore", test_data_mask)
def test_get_mask_shape(occ, nbasis, ncore):
    """Test ``get_mask`` function of IP base class. Check shape.

    Purpose: return a boolean array with True values for indices that are
             non-redundant and symmetry-unique. Required to assign the proper
             elements to the dense ThreeIndex objects during optimization
             (avoiding for loops).

    Procedure: test for ijb only (ijB is equivalent).
               Small letters indicate alpha electrons, capital letters beta
               electrons (or vice versa).
    """
    # some preliminaries
    lf = DenseLinalgFactory(nbasis)
    occ_model = AufbauOccModel(lf, nel=occ * 2, ncore=ncore)
    # Initialize empty (base) class
    ippccd = RSIPCC(lf, occ_model)

    mask = ippccd.get_mask(0)
    # check shape
    no, nv = occ_model.nacto[0], occ_model.nactv[0]
    assert mask.shape == (no, no, nv)


@pytest.mark.parametrize("occ, nbasis, ncore", test_data_mask)
def test_get_mask_elements(occ, nbasis, ncore):
    """Test ``get_mask`` function of IP base class. Check individual elements.

    Purpose: return a boolean array with True values for indices that are
             non-redundant and symmetry-unique. Required to assign the proper
             elements to the dense ThreeIndex objects during optimization
             (avoiding for loops).

    Procedure: test for ijb only (ijB is equivalent).
               Small letters indicate alpha electrons, capital letters beta
               electrons (or vice versa).
    """
    # some preliminaries
    lf = DenseLinalgFactory(nbasis)
    occ_model = AufbauOccModel(lf, nel=occ * 2, ncore=ncore)
    # Initialize empty (base) class
    ippccd = RSIPCC(lf, occ_model)

    mask = ippccd.get_mask(0)
    # check shape
    no, nv = range(occ_model.nacto[0]), range(occ_model.nactv[0])
    # check elements
    for i, j, b in itertools.product(no, no, nv):
        if i > j:
            assert mask[i, j, b], "wrong mask for ijb, i > j"
        elif i <= j:
            assert not mask[i, j, b], "wrong mask for ijb, i <= j"


@pytest.mark.parametrize("occ, nbasis, ncore", test_data_mask)
def test_get_index_of_mask(occ, nbasis, ncore):
    """Test ``get_index_of_mask`` function of IP base class.

    Purpose: return the indices for which the boolean array ``get_mask`` is
             True. Those contain non-redundant and symmetry-unique elements.
             Required to assign the proper elements from the dense ThreeIndex
             objects to the OneIndex object stored during optimization
             (avoiding for loops).

    Procedure: test only for ijb (ijB is equivalent).
               We test if the indices returned by the ``get_index_of_mask``
               function fulfill the symmetry requirements, like i<j, etc.
               Small letters indicate alpha electrons, capital letters beta
               electrons (or vice versa).
    """
    # some preliminaries
    lf = DenseLinalgFactory(nbasis)
    occ_model = AufbauOccModel(lf, nel=occ * 2, ncore=ncore)
    # Initialize empty (base) class
    ipcc = RSIPCC(lf, occ_model)

    mask = ipcc.get_index_of_mask(0)
    # check elements
    dim = len(mask[0])
    no, nv = occ_model.nacto[0], occ_model.nactv[0]
    for i in range(dim):
        assert mask[0][i] > mask[1][i]
        assert mask[0][i] < no
        assert mask[1][i] < (no - 1)
        assert mask[2][i] < nv


test_data_alpha = [
    (RSIPCC, -1),
    (RSIPCC1, 1),
    (RSIPCC3, 3),
    (RIPpCCD1, 1),
    (RIPpCCD3, 3),
]


@pytest.mark.parametrize("cls,expected", test_data_alpha)
def test_alpha(cls, expected):
    """Test if class has proper alpha instance."""
    # some preliminaries
    lf = DenseLinalgFactory(10)
    occ_model = AufbauOccModel(lf, nel=2)
    # Initialize empty class
    ipcc = cls(lf, occ_model)

    assert ipcc.alpha == expected


test_data_range = [
    (
        "oovv",
        0,
        10,
        4,
        0,
        {
            "begin0": 0,
            "end0": 4,
            "begin1": 0,
            "end1": 4,
            "begin2": 4,
            "end2": 10,
            "begin3": 4,
            "end3": 10,
        },
    ),
    ("oV", 0, 10, 4, 0, {"begin0": 0, "end0": 4, "begin1": 0, "end1": 6}),
    ("nn", 0, 10, 4, 0, {"begin0": 0, "end0": 10, "begin1": 0, "end1": 10}),
    ("nn", 0, 10, 4, 1, {"begin0": 0, "end0": 9, "begin1": 0, "end1": 9}),
    ("ov", 2, 10, 4, 0, {"begin2": 0, "end2": 4, "begin3": 4, "end3": 10}),
    ("ov", 2, 10, 4, 1, {"begin2": 0, "end2": 3, "begin3": 3, "end3": 9}),
]


@pytest.mark.parametrize(
    "range_, start, nbasis, nocc, ncore, expected", test_data_range
)
def test_get_range(range_, start, nbasis, nocc, ncore, expected):
    """Test whether proper ranges of o-v blocks are returned."""
    # some preliminaries
    lf = DenseLinalgFactory(nbasis)
    occ_model = AufbauOccModel(lf, nel=nocc * 2, ncore=ncore)
    # Initialize empty class
    ipcc = RSIPCC(lf, occ_model)

    ip_range = ipcc.get_range(range_, start)
    assert ip_range == expected


test_data_get_index_ijb = [
    (10, 4, 0, 4, (0, 1, 4, True)),
    (10, 4, 0, 10, (0, 2, 4, True)),
    (10, 4, 0, 65, (1, 0, 5, False)),
    (10, 4, 0, 102, (2, 3, 0, False)),
    (10, 4, 0, 124, (3, 2, 4, False)),
    (10, 4, 1, 4, (0, 1, 4, True)),
    (10, 4, 1, 10, (0, 2, 4, True)),
    (10, 4, 1, 65, (2, 1, 5, False)),
    (10, 4, 1, 71, (2, 2, 5, False)),
]


@pytest.mark.parametrize(
    "nbasis, nocc, ncore, ind, expected", test_data_get_index_ijb
)
def test_get_index_ijb(nbasis, nocc, ncore, ind, expected):
    """Test ``get_index_ijb`` function of IP base class.

    Purpose: transform composite index (ijb) of symmetry-unique elements to
             full index i,j,b of a dense ThreeIndex object.
    """
    # some preliminaries
    lf = DenseLinalgFactory(nbasis)
    occ_model = AufbauOccModel(lf, nel=nocc * 2, ncore=ncore)
    # Initialize empty class
    ipcc = RSIPCC(lf, occ_model)

    assert ipcc.get_index_ijb(ind) == expected


test_data_nhole = [
    # nbasis, nocc, ncore, nhole, expected
    # sz = 0.5, ncore = 0,1
    (RIPpCCD1, 10, 2, 0, 1, True),
    (RIPpCCD1, 10, 2, 0, 2, True),
    (RIPpCCD1, 10, 2, 1, 1, True),
    (RIPpCCD1, 10, 2, 1, 2, False),
    (RIPpCCD1, 10, 3, 0, 1, True),
    (RIPpCCD1, 10, 3, 0, 2, True),
    # sz = 1.5, ncore = 0,1
    (RIPpCCD3, 10, 2, 0, 1, False),
    (RIPpCCD3, 10, 1, 0, 1, False),
    (RIPpCCD3, 10, 2, 0, 2, True),
    (RIPpCCD3, 10, 2, 1, 2, False),
    (RIPpCCD3, 10, 4, 0, 2, True),
    (RIPpCCD3, 10, 4, 1, 2, True),
    (RIPpCCD3, 10, 4, 1, 1, False),
]


@pytest.mark.parametrize(
    "cls,nbasis,nocc,ncore,nhole,expected", test_data_nhole
)
def test_check_nhole(cls, nbasis, nocc, ncore, nhole, expected):
    """Test ``_check_nhole`` function of IP base class.

    Purpose: Check if nhole keyword argument (or default) is consistent with
             number of active occupied orbitals and spin projection.
             s_z = 0.5: nacto = 1, nhole = [1]
             s_z = 0.5: nacto >= 2, nhole = [1,2]
             s_z = 1.5: nacto >= 2, nhole = [2]
    """
    # some preliminaries
    lf = DenseLinalgFactory(nbasis)
    occ_model = AufbauOccModel(lf, nel=nocc * 2, ncore=ncore)
    # Initialize empty class
    ipcc = cls(lf, occ_model)
    # have to assign private attribute
    ipcc._nhole = nhole

    assert ipcc._check_nhole() == expected
