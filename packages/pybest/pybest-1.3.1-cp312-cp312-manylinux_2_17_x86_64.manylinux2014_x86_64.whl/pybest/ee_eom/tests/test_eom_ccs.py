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

from pybest.cc import RCCS
from pybest.ee_eom import REOMCCS
from pybest.ee_eom.tests.common import FromFile

# Reference energies
# HF orbitals
e_ex_ccs_hf_ref = [
    0.000000e00,
    1.053411e-01,
    1.053411e-01,
    4.976920e-01,
    5.523241e-01,
    5.523241e-01,
    6.390127e-01,
    6.474507e-01,
    6.474507e-01,
    6.478041e-01,
    7.284261e-01,
    7.498812e-01,
    7.498812e-01,
    7.861793e-01,
    8.673948e-01,
    9.553334e-01,
]

e_ex_ccs_hf_ref_fc = [
    0.000000e00,
    1.054322e-01,
    1.054322e-01,
    4.977093e-01,
    5.527914e-01,
]

test_set = [
    (
        "Davidson",
        0,
        {"nroot": 15, "davidson": True},
        {"e_ex": e_ex_ccs_hf_ref},
    ),
    (
        "Exact diagonalization",
        0,
        {"nroot": 15, "davidson": False},
        {"e_ex": e_ex_ccs_hf_ref},
    ),
    (
        "Davidson",
        1,
        {"nroot": 4, "davidson": True},
        {"e_ex": e_ex_ccs_hf_ref_fc},
    ),
    (
        "Exact diagonalization",
        1,
        {"nroot": 4, "davidson": False},
        {"e_ex": e_ex_ccs_hf_ref_fc},
    ),
]


@pytest.mark.parametrize("diag,ncore,options,results", test_set)
def test_ccs_hf(diag, ncore, options, results):
    data = FromFile("test/chplus.fcidump", 3, 25, ncore)

    # RHF-CCS
    ccs = RCCS(data.lf, data.occ_model)
    ccs_ = ccs(data.one, data.eri, data.iodata, threshold_r=1e-10)

    assert abs(ccs_.e_corr - 0.00) < 1e-6
    assert abs(ccs_.e_corr_s - 0.00) < 1e-6

    # EOM-CCS/CIS
    eom = REOMCCS(data.lf, data.occ_model)
    eom_ = eom(data.one, data.eri, ccs_, **options)

    for i, val in enumerate(eom_.e_ee):
        assert abs(val - results["e_ex"][i]) < 1e-6
