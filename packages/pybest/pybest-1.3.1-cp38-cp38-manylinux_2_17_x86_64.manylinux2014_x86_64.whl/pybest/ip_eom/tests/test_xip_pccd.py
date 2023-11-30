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

from pybest.ip_eom import RDIPpCCD, RIPpCCD
from pybest.ip_eom.dip_pccd0 import RDIPpCCD0
from pybest.ip_eom.dip_pccd2 import RDIPpCCD2
from pybest.ip_eom.dip_pccd4 import RDIPpCCD4
from pybest.ip_eom.sip_pccd1 import RIPpCCD1
from pybest.ip_eom.sip_pccd3 import RIPpCCD3
from pybest.linalg import DenseLinalgFactory
from pybest.occ_model import AufbauOccModel

test_data_alpha = [
    (RIPpCCD, {"alpha": 1}, 1),
    (RIPpCCD, {"alpha": 3}, 3),
    (RDIPpCCD, {"alpha": 0}, 0),
    (RDIPpCCD, {"alpha": 2}, 2),
    (RDIPpCCD, {"alpha": 4}, 4),
]


@pytest.mark.parametrize("cls,kwargs,expected", test_data_alpha)
def test_alpha(cls, kwargs, expected):
    """Check if alpha agrees after RIPpCCD/RDIPpCCD inits."""
    # some preliminaries
    lf = DenseLinalgFactory(10)
    occ_model = AufbauOccModel(lf, nel=8)
    # Initialize empty class
    ipcc = cls(lf, occ_model, **kwargs)

    assert ipcc.alpha == expected


test_data_instance = [
    (RIPpCCD, {"alpha": 1}, RIPpCCD1),
    (RIPpCCD, {"alpha": 3}, RIPpCCD3),
    (RDIPpCCD, {"alpha": 0}, RDIPpCCD0),
    (RDIPpCCD, {"alpha": 2}, RDIPpCCD2),
    (RDIPpCCD, {"alpha": 4}, RDIPpCCD4),
]


@pytest.mark.parametrize("cls,kwargs,expected", test_data_instance)
def test_instance(cls, kwargs, expected):
    """Check if __new__ overwrite works properly."""
    # some preliminaries
    lf = DenseLinalgFactory(10)
    occ_model = AufbauOccModel(lf, nel=8)
    # Initialize empty class
    ipcc = cls(lf, occ_model, **kwargs)

    assert isinstance(ipcc, expected)
