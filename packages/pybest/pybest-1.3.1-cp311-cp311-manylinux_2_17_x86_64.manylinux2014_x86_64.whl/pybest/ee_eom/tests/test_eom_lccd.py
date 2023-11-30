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

from pybest.cc import RHFLCCD
from pybest.ee_eom import REOMLCCD
from pybest.ee_eom.tests.common import FromFile

# Reference energies
# HF orbitals
e_hf_ref = -37.90128041
elccd_hf_ref = -38.01971649
elccd2_hf_ref = -0.11843608
e_ex_lccd_hf_ref = [
    0.000000e00,
    2.950165e-01,
    2.950166e-01,
    3.390149e-01,
    6.084581e-01,
    6.084581e-01,
    6.653189e-01,
    6.653191e-01,
    7.194481e-01,
    7.317086e-01,
    7.523464e-01,
    7.523464e-01,
    7.906870e-01,
    7.906870e-01,
    7.913210e-01,
    8.329974e-01,
]

test_set = [
    (
        "Davidson",
        0,
        {"nroot": 15, "davidson": True},
        {
            "e_ref": elccd_hf_ref,
            "e_corr_d": elccd2_hf_ref,
            "e_ex": e_ex_lccd_hf_ref,
        },
    ),
]


@pytest.mark.parametrize("diag,ncore,options,results", test_set)
def test_lccd_hf(diag, ncore, options, results):
    data = FromFile("test/chplus.fcidump", 3, 25, ncore)

    data.iodata.e_ref = e_hf_ref
    # LCCD
    lccd = RHFLCCD(data.lf, data.occ_model)
    lccd_ = lccd(data.one, data.eri, data.iodata, threshold_r=1e-10)
    assert abs(lccd_.e_tot - results["e_ref"]) < 1e-6
    assert abs(lccd_.e_corr_d - results["e_corr_d"]) < 1e-6

    # EOM-pCCD-LCCD
    eom = REOMLCCD(data.lf, data.occ_model)
    eom_ = eom(data.one, data.eri, lccd_, **options)

    for i, val in enumerate(eom_.e_ee):
        assert abs(val - results["e_ex"][i]) < 1e-6
