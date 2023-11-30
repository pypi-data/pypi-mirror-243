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

from pybest.ee_eom import REOMpCCD
from pybest.ee_eom.tests.common import FromFile
from pybest.geminals.rpccd import RpCCD

# Reference energies
# pCCD orbitals
epccd_opt_ref = -37.991225550170
e_ex_pccd_opt_ref = [
    0.000000e00,
    6.889018e-01,
    7.930113e-01,
    1.355189e00,
    1.373127e00,
    1.833921e00,
    2.074985e00,
    2.224260e00,
    2.259740e00,
    2.277095e00,
    2.310193e00,
    2.343555e00,
    2.350504e00,
    2.384404e00,
    2.427066e00,
    2.496954e00,
]
epccd_opt_ref_fc = -37.980850814377
e_ex_pccd_opt_ref_fc = [
    0.000000e00,
    6.889361e-01,
    7.930974e-01,
    1.355166e00,
]


test_set = [
    (
        "Davidson",
        0,
        {"nroot": 15, "davidson": True},
        {"e_ref": epccd_opt_ref, "e_ex": e_ex_pccd_opt_ref},
    ),
    (
        "Exact diagonalization",
        0,
        {"nroot": 15, "davidson": False},
        {"e_ref": epccd_opt_ref, "e_ex": e_ex_pccd_opt_ref},
    ),
    (
        "Davidson",
        1,
        {"nroot": 3, "davidson": True},
        {"e_ref": epccd_opt_ref_fc, "e_ex": e_ex_pccd_opt_ref_fc},
    ),
    (
        "Exact diagonalization",
        1,
        {"nroot": 3, "davidson": False},
        {"e_ref": epccd_opt_ref_fc, "e_ex": e_ex_pccd_opt_ref_fc},
    ),
]


@pytest.mark.parametrize("diag,ncore,options,results", test_set)
def test_pccd(diag, ncore, options, results):
    data = FromFile("test/chplus.fcidump", 3, 25, ncore, "test/chplus_opt.dat")

    # pCCD
    geminal_solver = RpCCD(data.lf, data.occ_model)
    pccd = geminal_solver(data.one, data.eri, data.iodata)

    assert abs(pccd.e_tot - results["e_ref"]) < 1e-6

    # EOM-pCCD
    eom = REOMpCCD(data.lf, data.occ_model)
    eom_ = eom(data.one, data.eri, pccd, **options)

    for i, val in enumerate(eom_.e_ee):
        assert abs(val - results["e_ex"][i]) < 1e-6
