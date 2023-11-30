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
from pybest.cc import RpCCDLCCD
from pybest.ee_eom import REOMpCCDLCCD
from pybest.ee_eom.tests.common import FromFile, Molecule
from pybest.geminals.rpccd import RpCCD

# Reference energies
# HF orbitals
epccd_hf_ref = -37.94369596
epccdlccd_hf_ref = -38.01051733
epccdlccd2_hf_ref = -0.06682138
e_ex_pccdlccd_hf_ref = [
    0.000000e00,
    2.331030e-01,
    2.771713e-01,
    2.863425e-01,
    6.001479e-01,
    6.001479e-01,
    6.539911e-01,
    6.572480e-01,
    7.103465e-01,
    7.158915e-01,
]
# pCCD orbitals
epccd_opt_ref = -37.991225550170
epccdlccd_opt_ref = -38.01414672
epccdlccd2_opt_ref = -0.02292117
e_ex_pccdlccd_opt_ref = [
    0.000000e00,
    2.801303e-01,
    2.898505e-01,
    3.236840e-01,
    6.029520e-01,
    6.029528e-01,
    6.488371e-01,
    6.622286e-01,
    7.140494e-01,
    7.144518e-01,
]


test_set = [
    (
        "Davidson",
        "RHF",
        0,
        {"nroot": 9, "davidson": True, "nguessv": 60},
        None,
        {
            "e_pccd": epccd_hf_ref,
            "e_pccdlcc": epccdlccd_hf_ref,
            "e_pccdlcc_corr_d": epccdlccd2_hf_ref,
            "e_ex": e_ex_pccdlccd_hf_ref,
        },
    ),
    (
        "Davidson",
        "pCCD",
        0,
        {"nroot": 9, "davidson": True, "nguessv": 60},
        "test/chplus_opt.dat",
        {
            "e_pccd": epccd_opt_ref,
            "e_pccdlcc": epccdlccd_opt_ref,
            "e_pccdlcc_corr_d": epccdlccd2_opt_ref,
            "e_ex": e_ex_pccdlccd_opt_ref,
        },
    ),
]


@pytest.mark.parametrize("diag,orb,ncore,options,orbf,results", test_set)
def test_pccd_lccd(diag, orb, ncore, options, orbf, results):
    data = FromFile("test/chplus.fcidump", 3, 25, ncore, orbf)

    # pCCD
    geminal_solver = RpCCD(data.lf, data.occ_model)
    pccd = geminal_solver(data.one, data.eri, data.iodata)

    assert abs(pccd.e_tot - results["e_pccd"]) < 1e-6

    # pCCD-LCCD
    lccd = RpCCDLCCD(data.lf, data.occ_model)
    lccd_ = lccd(data.one, data.eri, pccd, threshold_r=1e-10)

    assert abs(lccd_.e_tot - results["e_pccdlcc"]) < 1e-6
    assert abs(lccd_.e_corr_d - results["e_pccdlcc_corr_d"]) < 1e-6

    # EOM-pCCD-LCCD
    eom = REOMpCCDLCCD(data.lf, data.occ_model)
    eom_ = eom(data.one, data.eri, lccd_, **options)

    for i, val in enumerate(eom_.e_ee):
        assert abs(val - results["e_ex"][i]) < 1e-6


test_chol = [
    ("test/chplus.g94", "test/chplus.xyz", {"charge": 1}),
]


@pytest.mark.skipif(
    not pybest_basis.PYBEST_CHOLESKY_ENABLED,
    reason="Cholesky-decomposition ERI are not available. Build libchol and re-run build --enable-cholesky=1",
)
@pytest.mark.slow
@pytest.mark.parametrize("basisfile,mol,kwargs", test_chol)
def test_pccd_lccd_cholesky(basisfile, mol, kwargs):
    mol = Molecule(basisfile, mol, **kwargs)

    # RHF
    mol.do_rhf()

    # pCCD
    geminal_solver = RpCCD(mol.lf, mol.occ_model)
    pccd = geminal_solver(*mol.ham, mol.rhf)
    assert abs(pccd.e_tot - epccd_hf_ref) < 1e-6

    # pCCD-LCCD
    lccd = RpCCDLCCD(mol.lf, mol.occ_model)
    lccd_ = lccd(*mol.ham, pccd, threshold_r=1e-10)

    assert abs(lccd_.e_tot - epccdlccd_hf_ref) < 1e-6
    assert abs(lccd_.e_corr_d - epccdlccd2_hf_ref) < 1e-6

    # EOM-pCCD-LCCD
    eom = REOMpCCDLCCD(mol.lf, mol.occ_model)
    eom_ = eom(*mol.ham, lccd_, nroot=9, nguessv=60)

    for i in range(9):
        assert abs(eom_.e_ee[i] - e_ex_pccdlccd_hf_ref[i]) < 1e-4
