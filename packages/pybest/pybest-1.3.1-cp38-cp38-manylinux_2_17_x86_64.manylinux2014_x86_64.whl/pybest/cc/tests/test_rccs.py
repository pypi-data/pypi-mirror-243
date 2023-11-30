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

import numpy as np
import pytest

from pybest.cc import RCCS, RpCCDCCS
from pybest.context import context
from pybest.gbasis import get_gobasis
from pybest.gbasis.gobasis import (
    compute_cholesky_eri,
    compute_eri,
    compute_kinetic,
    compute_nuclear,
    compute_nuclear_repulsion,
    compute_overlap,
)
from pybest.geminals.rpccd import RpCCD
from pybest.io.iodata import IOData
from pybest.linalg import CholeskyLinalgFactory, DenseLinalgFactory
from pybest.occ_model import AufbauOccModel


class Molecule:
    def __init__(
        self,
        basis,
        linalg,
        ncore=0,
        filen="test/hf.xyz",
        orbfilen="test/hf_ap1rog.txt",
    ):
        fn_xyz = context.get_fn(filen)
        self.obasis = get_gobasis(basis, fn_xyz, print_basis=False)
        self.lf = linalg(self.obasis.nbasis)
        self.olp = compute_overlap(self.obasis)
        self.kin = compute_kinetic(self.obasis)
        self.na = compute_nuclear(self.obasis)
        self.one = self.kin.copy()
        self.one.iadd(self.na)
        if isinstance(self.lf, CholeskyLinalgFactory):
            self.er = compute_cholesky_eri(self.obasis, threshold=1e-8)
        elif isinstance(self.lf, DenseLinalgFactory):
            self.er = compute_eri(self.obasis)
        self.external = compute_nuclear_repulsion(self.obasis)

        fn_orb = context.get_fn(orbfilen)
        orb_ = np.fromfile(fn_orb, sep=",").reshape(
            self.obasis.nbasis, self.obasis.nbasis
        )
        self.orb_a = self.lf.create_orbital()
        self.orb_a._coeffs = orb_

        self.occ_model = AufbauOccModel(self.obasis, ncore=ncore)


core_set_hf = [
    (
        0,
        RCCS,
        {
            "e_ref": -100.00939084,
            "e_tot": -100.00988281,
            "t1_diagnostic": 0.0048352773,
        },
    ),
    (
        1,
        RCCS,
        {
            "e_ref": -100.00939084,
            "e_tot": -100.00988271,
            "t1_diagnostic": 0.0054051907,
        },
    ),
]

core_set_pccd = [
    (
        0,
        RpCCDCCS,
        {
            "e_ref": -100.08906717,
            "e_tot": -100.08905945,
        },
    ),
    (
        1,
        RpCCDCCS,
        {
            "e_ref": -100.08885944,
            "e_tot": -100.08885189,
        },
    ),
]


solver_set = [
    ("krylov", {}),
    ("pbqn", {"jacobian": 1}),
    ("pbqn", {"jacobian": 2}),
]


@pytest.mark.parametrize("ncore,cls,dict_", core_set_hf)
@pytest.mark.parametrize("solver, jacobian", solver_set)
def test_ccs(ncore, cls, dict_, solver, jacobian, linalg):
    mol = Molecule("cc-pvdz", linalg, ncore=ncore)

    iodata = IOData(
        **{
            "orb_a": mol.orb_a,
            "olp": mol.olp,
            "e_ref": dict_["e_ref"],
            "e_core": mol.external,
        }
    )
    options = {"solver": solver, "threshold_r": 1e-7}
    ccs = cls(mol.lf, mol.occ_model)
    ccs_ = ccs(mol.one, mol.er, iodata, **options, **jacobian)
    assert abs(ccs_.e_tot - dict_["e_tot"]) < 1e-6


@pytest.mark.parametrize("ncore,cls,dict_", core_set_pccd)
@pytest.mark.parametrize("solver,jacobian", solver_set)
def test_pccd_ccs(ncore, cls, dict_, solver, jacobian, linalg):
    mol = Molecule("cc-pvdz", linalg, ncore=ncore)

    pccd = RpCCD(mol.lf, mol.occ_model)
    pccd_ = pccd(mol.one, mol.er, mol.orb_a, mol.olp, e_core=mol.external)
    assert abs(pccd_.e_tot - dict_["e_ref"]) < 1e-6

    options = {"solver": solver, "threshold_r": 1e-7}

    ccs = cls(mol.lf, mol.occ_model)
    ccs_ = ccs(mol.one, mol.er, pccd_, **options, **jacobian)

    assert abs(ccs_.e_tot - dict_["e_tot"]) < 1e-6


@pytest.mark.parametrize("ncore,cls,dict_", core_set_hf)
def test_rccs_compute_t1_diagnostic(ncore, cls, dict_):
    """Compares T1 diagnostic with reference data."""
    mol = Molecule("cc-pvdz", DenseLinalgFactory, ncore=ncore)

    iodata = IOData(
        **{
            "orb_a": mol.orb_a,
            "olp": mol.olp,
            "e_ref": dict_["e_ref"],
            "e_core": mol.external,
        }
    )
    ccs = cls(mol.lf, mol.occ_model)
    ccs_ = ccs(mol.one, mol.er, iodata)
    assert abs(ccs_.e_tot - dict_["e_tot"]) < 1e-6

    t1_diag = ccs.compute_t1_diagnostic(ccs_.t_1, ccs.nacto)
    assert abs(t1_diag - dict_["t1_diagnostic"]) < 1e-8
