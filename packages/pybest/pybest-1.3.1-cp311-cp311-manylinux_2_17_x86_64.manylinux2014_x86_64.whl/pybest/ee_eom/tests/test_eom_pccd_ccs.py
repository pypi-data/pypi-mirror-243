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

from pybest.cc.rccs import RpCCDCCS
from pybest.ee_eom import REOMpCCDCCS
from pybest.ee_eom.tests.common import FromFile
from pybest.geminals.rpccd import RpCCD

# Reference energies
# pCCD orbitals
epccd_opt_ref = -37.991225550170
epccdccs_opt_ref = -37.99124837
epccdccs1_opt_ref = -0.00002282
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
epccd_opt_ref_fc = -37.980850814377
epccdccs_opt_ref_fc = -37.98087197
epccdccs1_opt_ref_fc = -0.00002115
e_ex_pccds_opt_ref_fc = [
    0.000000e00,
    1.569983e-01,
    1.569983e-01,
    5.346267e-01,
    6.076026e-01,
    6.076026e-01,
]

test_set = [
    (
        "Davidson",
        0,
        {"nroot": 15, "davidson": True, "tolerance": 1e-8},
        {
            "e_ref": epccd_opt_ref,
            "e_ex": e_ex_pccd_ccs_opt_ref,
            "e_ccs": epccdccs_opt_ref,
            "e_ccs_corr": epccdccs1_opt_ref,
        },
    ),
    (
        "Exact diagonalization",
        0,
        {"nroot": 15, "davidson": False},
        {
            "e_ref": epccd_opt_ref,
            "e_ex": e_ex_pccd_ccs_opt_ref,
            "e_ccs": epccdccs_opt_ref,
            "e_ccs_corr": epccdccs1_opt_ref,
        },
    ),
    (
        "Davidson",
        1,
        {"nroot": 5, "davidson": True, "nguessv": 60, "tolerance": 1e-8},
        {
            "e_ref": epccd_opt_ref_fc,
            "e_ex": e_ex_pccds_opt_ref_fc,
            "e_ccs": epccdccs_opt_ref_fc,
            "e_ccs_corr": epccdccs1_opt_ref_fc,
        },
    ),
    (
        "Exact diagonalization",
        1,
        {"nroot": 5, "davidson": False, "nguessv": 60},
        {
            "e_ref": epccd_opt_ref_fc,
            "e_ex": e_ex_pccds_opt_ref_fc,
            "e_ccs": epccdccs_opt_ref_fc,
            "e_ccs_corr": epccdccs1_opt_ref_fc,
        },
    ),
]


@pytest.mark.parametrize("diag,ncore,options,results", test_set)
def test_pccd_ccs_opt_davidson(diag, ncore, options, results):
    data = FromFile("test/chplus.fcidump", 3, 25, ncore, "test/chplus_opt.dat")

    # pCCD
    rpccd = RpCCD(data.lf, data.occ_model)
    rpccd_ = rpccd(data.one, data.eri, data.iodata)

    assert abs(rpccd_.e_tot - results["e_ref"]) < 1e-6

    # pCCD-CCS
    ccs = RpCCDCCS(data.lf, data.occ_model)
    ccs_ = ccs(data.one, data.eri, rpccd_, threshold_r=1e-10)

    assert abs(ccs_.e_tot - results["e_ccs"]) < 1e-6
    assert abs(ccs_.e_corr - results["e_ccs_corr"]) < 1e-6

    # EOM-pCCD-CCS
    eom = REOMpCCDCCS(data.lf, data.occ_model)
    eom_ = eom(data.one, data.eri, ccs_, **options)

    for i, val in enumerate(eom_.e_ee):
        assert abs(val - results["e_ex"][i]) < 1e-6
