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

from .common import Model


@pytest.fixture
def h2_molecule():
    "Returns RHF/pCCD results and reference CC energies."
    model = Model("test/h2.xyz", "cc-pvdz")
    reference_correlation_energy = {
        "RCCD": -0.034582180698988885,
        "RCCSD": -0.034709514282981926,
        "RfpCCD": -0.034840613788246884,
        "RfpCCSD": -0.03484061735867886,
    }
    return {"model": model, "energies": reference_correlation_energy}


@pytest.fixture
def hf_molecule():
    "Returns RHF/pCCD results and reference CC energies."
    model = Model("test/hf.xyz", "3-21g")
    reference_correlation_energy = {
        "RCCD": -0.12911913585251084,
        "RCCSD": -0.12987666859843192,
        "RfpCCD": -0.13459134995132008,
        "RfpCCSD": -0.13465477029776618,
    }
    return {"model": model, "energies": reference_correlation_energy}


@pytest.fixture
def h2o_molecule():
    "Returns RHF/pCCD results and reference CC energies."
    model = Model("test/h2o.xyz", "3-21g")
    reference_correlation_energy = {
        "RCCD": -0.1499368041545847,
        "RCCSD": -0.15213686280456384,
        "RfpCCD": -0.16072464912359646,
        "RfpCCSD": -0.16094396980907438,
    }
    return {"model": model, "energies": reference_correlation_energy}


@pytest.fixture
def h2o_molecule_fc():
    "Returns RHF/pCCD results and reference CC energies."
    model = Model("test/h2o.xyz", "3-21g", ncore=1)
    reference_correlation_energy = {
        "RCCD": -0.1499368041545847,
        "RCCSD": -0.15213686280456384,
        "RfpCCD": -0.16072464912359646,
        "RfpCCSD": -0.16094396980907438,
    }
    return {"model": model, "energies": reference_correlation_energy}
