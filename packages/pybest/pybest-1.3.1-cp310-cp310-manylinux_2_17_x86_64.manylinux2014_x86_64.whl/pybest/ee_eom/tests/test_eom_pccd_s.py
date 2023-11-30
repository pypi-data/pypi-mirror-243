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

from pybest.ee_eom import REOMpCCDS
from pybest.ee_eom.tests.common import FromFile
from pybest.geminals.rpccd import RpCCD

# Reference energies
# pCCD orbitals
epccd_opt_ref = -37.991225550170
epccd_opt_ref_fc = -37.980850814377
epccdccs_opt_ref = -37.99124837
epccdccs1_opt_ref = -0.00002282
e_ex_pccds_opt_ref = [
    -1.175150e-08,
    1.566229e-01,
    1.566229e-01,
    5.345106e-01,
    6.010138e-01,
    6.010138e-01,
    6.602393e-01,
    6.773517e-01,
    6.802024e-01,
    6.876033e-01,
    6.876033e-01,
    7.651787e-01,
    7.820253e-01,
    7.902141e-01,
    7.902141e-01,
    8.333694e-01,
]
e_ex_pccd_ccs_opt_ref = [
    0.000000e00,
    1.567204e-01,
    1.567204e-01,
    5.343764e-01,
    6.009420e-01,
    6.009420e-01,
    6.602406e-01,
    6.770740e-01,
    6.799853e-01,
    6.873988e-01,
    6.873988e-01,
    7.649222e-01,
    7.819493e-01,
    7.900298e-01,
    7.900298e-01,
    8.332708e-01,
]
e_ex_pccds_opt_ref_fc = [
    -8.059321e-07,
    1.568994e-01,
    1.568995e-01,
    5.347868e-01,
    6.076699e-01,
    6.076699e-01,
    6.603085e-01,
]

test_set = [
    (
        "Davidson",
        0,
        {"nroot": 15, "davidson": True},
        {"e_ref": epccd_opt_ref, "e_ex": e_ex_pccds_opt_ref},
    ),
    (
        "Exact diagonalization",
        0,
        {"nroot": 15, "davidson": False},
        {"e_ref": epccd_opt_ref, "e_ex": e_ex_pccds_opt_ref},
    ),
    (
        "Davidson",
        1,
        {"nroot": 6, "davidson": True},
        {"e_ref": epccd_opt_ref_fc, "e_ex": e_ex_pccds_opt_ref_fc},
    ),
    (
        "Exact diagonalization",
        1,
        {"nroot": 6, "davidson": False},
        {"e_ref": epccd_opt_ref_fc, "e_ex": e_ex_pccds_opt_ref_fc},
    ),
]


@pytest.mark.parametrize("diag,ncore,options,results", test_set)
def test_pccds(diag, ncore, options, results):
    data = FromFile("test/chplus.fcidump", 3, 25, ncore, "test/chplus_opt.dat")

    # pCCD
    geminal_solver = RpCCD(data.lf, data.occ_model)
    pccd = geminal_solver(data.one, data.eri, data.iodata)

    assert abs(pccd.e_tot - results["e_ref"]) < 1e-6

    # EOM-pCCD+S
    eom = REOMpCCDS(data.lf, data.occ_model)
    eom_ = eom(data.one, data.eri, pccd, **options)

    for i, val in enumerate(eom_.e_ee):
        assert abs(val - results["e_ex"][i]) < 1e-6
