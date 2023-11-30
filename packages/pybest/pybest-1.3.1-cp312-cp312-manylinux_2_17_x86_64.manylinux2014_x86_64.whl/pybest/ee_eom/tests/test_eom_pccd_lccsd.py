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

import pybest.gbasis.gobasis as pybest_basis
from pybest.cc import RpCCDLCCSD
from pybest.ee_eom import REOMpCCDLCCSD
from pybest.ee_eom.tests.common import FromFile, Molecule
from pybest.geminals.rpccd import RpCCD

# Reference energies
# HF orbitals
epccd_hf_ref = -37.94369596
epccdlccsd_hf_ref = -38.01120327
epccdlccsd2_hf_ref = -0.06750735
epccdlccsd1_hf_ref = 0.0
e_ex_pccdlccsd_hf_ref = [
    0.000000e00,
    1.143401e-01,
    1.143401e-01,
    2.299983e-01,
    2.754901e-01,
    2.835823e-01,
    4.885279e-01,
    5.155197e-01,
    5.155197e-01,
    6.204875e-01,
    6.204875e-01,
    6.241381e-01,
    6.373234e-01,
    6.454567e-01,
    6.454567e-01,
    6.480106e-01,
]
# pCCD orbitals
epccd_opt_ref = -37.991225550170
epccdlccsd_opt_ref = -38.01452545
epccdlccsd2_opt_ref = -0.02328628
epccdlccsd1_opt_ref = -0.00001362
e_ex_pccdlccsd_opt_ref = [
    0.000000e00,
    1.169010e-01,
    1.169010e-01,
    2.770937e-01,
    2.870472e-01,
    3.220840e-01,
    4.908727e-01,
    5.183331e-01,
    5.183331e-01,
    6.229231e-01,
    6.229231e-01,
    6.273942e-01,
    6.323419e-01,
    6.449658e-01,
    6.475729e-01,
    6.475729e-01,
]

test_set = [
    (
        "Davidson",
        "RHF",
        0,
        {"nroot": 8, "davidson": True, "nguessv": 20},
        None,
        {
            "e_pccd": epccd_hf_ref,
            "e_pccdlcc": epccdlccsd_hf_ref,
            "e_pccdlcc_corr_s": epccdlccsd1_hf_ref,
            "e_pccdlcc_corr_d": epccdlccsd2_hf_ref,
            "e_ex": e_ex_pccdlccsd_hf_ref,
        },
    ),
    (
        "Davidson",
        "pCCD",
        0,
        {"nroot": 8, "davidson": True, "nguessv": 20},
        "test/chplus_opt.dat",
        {
            "e_pccd": epccd_opt_ref,
            "e_pccdlcc": epccdlccsd_opt_ref,
            "e_pccdlcc_corr_s": epccdlccsd1_opt_ref,
            "e_pccdlcc_corr_d": epccdlccsd2_opt_ref,
            "e_ex": e_ex_pccdlccsd_opt_ref,
        },
    ),
]


@pytest.mark.parametrize("diag,orb,ncore,options,orbf,results", test_set)
def test_pccd_lccsd(diag, orb, ncore, options, orbf, results):
    data = FromFile("test/chplus.fcidump", 3, 25, ncore, orbf)

    # pCCD
    geminal_solver = RpCCD(data.lf, data.occ_model)
    pccd = geminal_solver(data.one, data.eri, data.iodata)

    assert abs(pccd.e_tot - results["e_pccd"]) < 1e-6

    # pCCD-LCCSD
    lccsd = RpCCDLCCSD(data.lf, data.occ_model)
    lccsd_ = lccsd(data.one, data.eri, pccd, threshold_r=1e-7, solver="pbqn")

    assert abs(lccsd_.e_tot - results["e_pccdlcc"]) < 1e-6
    assert abs(lccsd_.e_corr_d - results["e_pccdlcc_corr_d"]) < 1e-6
    assert abs(lccsd_.e_corr_s - results["e_pccdlcc_corr_s"]) < 1e-6

    # EOM-pCCD-LCCSD
    eom = REOMpCCDLCCSD(data.lf, data.occ_model)
    eom_ = eom(data.one, data.eri, lccsd_, **options)

    for i, val in enumerate(eom_.e_ee):
        assert abs(val - results["e_ex"][i]) < 5e-6


test_chol = [
    ("test/chplus.g94", "test/chplus.xyz", {"charge": 1}),
]


@pytest.mark.skipif(
    not pybest_basis.PYBEST_CHOLESKY_ENABLED,
    reason="Cholesky-decomposition ERI are not available. Build libchol and re-run build --enable-cholesky",
)
@pytest.mark.slow
@pytest.mark.parametrize("basisfile,mol,kwargs", test_chol)
def test_pccd_lccsd_cholesky(basisfile, mol, kwargs):
    mol = Molecule(basisfile, mol, **kwargs)
    # RHF
    mol.do_rhf()
    # pCCD
    geminal_solver = RpCCD(mol.lf, mol.occ_model)
    pccd = geminal_solver(*mol.ham, mol.rhf)
    energy = pccd.e_tot
    assert abs(energy - epccd_hf_ref) < 1e-6

    # pCCD-LCCSD
    lccsd = RpCCDLCCSD(mol.lf, mol.occ_model)
    lccsd_ = lccsd(*mol.ham, pccd, threshold_r=1e-7, solver="pbqn")

    assert abs(lccsd_.e_tot - epccdlccsd_hf_ref) < 1e-6
    assert abs(lccsd_.e_corr_d - epccdlccsd2_hf_ref) < 1e-6
    assert abs(lccsd_.e_corr_s - epccdlccsd1_hf_ref) < 1e-6

    # EOM-pCCD-LCCSD
    eom = REOMpCCDLCCSD(mol.lf, mol.occ_model)
    eom_ = eom(*mol.ham, lccsd_, nroot=6, nguessv=20)

    for i, val in enumerate(eom_.e_ee):
        assert abs(val - e_ex_pccdlccsd_hf_ref[i]) < 5e-5
