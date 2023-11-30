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

from pybest.cc import RLCCSD
from pybest.ee_eom import REOMLCCSD
from pybest.ee_eom.tests.common import FromFile

# Reference energies
# HF orbitals
e_hf_ref = -37.90128041
elccsd_hf_ref = -38.02108130
elccsd2_hf_ref = -0.11980091
elccsd1_hf_ref = 0.0
e_ex_lccsd_hf_ref = [
    0.000000e00,
    1.217281e-01,
    1.217281e-01,
    2.930604e-01,
    2.930604e-01,
    3.382883e-01,
    4.951236e-01,
    5.223829e-01,
    5.223829e-01,
    6.284830e-01,
    6.284830e-01,
    6.325114e-01,
    6.500966e-01,
    6.517547e-01,
    6.517547e-01,
    6.545916e-01,
]

test_set = [
    (
        "Davidson",
        0,
        {"nroot": 15, "davidson": True},
        {
            "e_ref": elccsd_hf_ref,
            "e_corr_s": elccsd1_hf_ref,
            "e_corr_d": elccsd2_hf_ref,
            "e_ex": e_ex_lccsd_hf_ref,
        },
    ),
]


@pytest.mark.parametrize("diag,ncore,options,results", test_set)
def test_lccsd_hf_davidson(diag, ncore, options, results):
    data = FromFile("test/chplus.fcidump", 3, 25, ncore)

    data.iodata.e_ref = e_hf_ref
    # LCCSD
    lccsd = RLCCSD(data.lf, data.occ_model)
    lccsd_ = lccsd(data.one, data.eri, data.iodata, threshold_r=1e-10)
    assert abs(lccsd_.e_tot - results["e_ref"]) < 1e-6
    assert abs(lccsd_.e_corr_d - results["e_corr_d"]) < 1e-6
    assert abs(lccsd_.e_corr_s - results["e_corr_s"]) < 1e-6

    # EOM-pCCD-LCCSD
    eom = REOMLCCSD(data.lf, data.occ_model)
    eom_ = eom(data.one, data.eri, lccsd_, **options)

    for i, val in enumerate(eom_.e_ee):
        assert abs(val - results["e_ex"][i]) < 1e-6
