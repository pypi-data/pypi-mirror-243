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

from pybest import filemanager
from pybest.context import context
from pybest.exceptions import ArgumentError
from pybest.gbasis import get_gobasis
from pybest.gbasis.gobasis import (
    compute_eri,
    compute_kinetic,
    compute_nuclear,
    compute_nuclear_repulsion,
    compute_overlap,
)
from pybest.geminals.roopccd import ROOpCCD
from pybest.geminals.rpccd import RpCCD
from pybest.io.iodata import IOData
from pybest.linalg.dense.dense_linalg_factory import DenseLinalgFactory
from pybest.occ_model import AufbauOccModel
from pybest.orbital_utils import project_orbitals
from pybest.wrappers import RHF


class Molecule:
    """Set some molecule."""

    def __init__(self, basis, filen="test/h2.xyz", **kwargs):

        fn_xyz = context.get_fn(filen)
        self.obasis = get_gobasis(basis, fn_xyz, print_basis=False)
        self.lf = DenseLinalgFactory(self.obasis.nbasis)

        self.olp = compute_overlap(self.obasis)
        self.kin = compute_kinetic(self.obasis)
        self.ne = compute_nuclear(self.obasis)
        self.eri = compute_eri(self.obasis)
        self.external = compute_nuclear_repulsion(self.obasis)
        self.hamiltonian = [self.kin, self.ne, self.eri]

        self.orb_a = self.lf.create_orbital()
        self.occ_model = AufbauOccModel(self.obasis, **kwargs)

        self.rhf = None

    def do_hf(self):
        """Do a RHF calculation and store result in self.rhf"""
        hf = RHF(self.lf, self.occ_model)
        self.rhf = hf(*self.hamiltonian, self.external, self.olp, self.orb_a)

    def do_pccd(self, *args, **kwargs):
        # Do pCCD optimization:
        pccd = RpCCD(self.lf, self.occ_model)
        self.pccd = pccd(
            self.kin, self.ne, self.eri, self.rhf, *args, **kwargs
        )

    def do_oopccd(self, *args, **kwargs):
        # Do pCCD optimization:
        pccd = ROOpCCD(self.lf, self.occ_model)
        self.oopccd = pccd(
            self.kin, self.ne, self.eri, self.rhf, *args, **kwargs
        )

    def do_oopccd_restart(self, *args, **kwargs):
        # Do pCCD optimization:
        pccd = ROOpCCD(self.lf, self.occ_model)
        self.oopccd = pccd(self.kin, self.ne, self.eri, *args, **kwargs)


hf_h2 = Molecule("6-31G")
hf_h2.do_hf()

e_tot = -1.143420629378
e_wo_ext = -1.143420629378 - hf_h2.external
e_w2_ext = -1.143420629378 + hf_h2.external

orb_a_ = hf_h2.orb_a.copy()
orb_a_.clear()


testdata_external = [
    (0.0, e_wo_ext),
    (hf_h2.external, e_tot),
    (2 * hf_h2.external, e_w2_ext),
]


testdata_orbs = [
    (hf_h2.orb_a, None, e_tot),
    (None, hf_h2.orb_a, e_tot),
    (orb_a_, hf_h2.orb_a, e_tot),
    (hf_h2.orb_a, orb_a_, None),  # FloatingPointError, ValueError
    (orb_a_, None, None),  # FloatingPointError, ValueError
    # FIX this test in a future PR
    #   (None, None, None),  # ArgumentError
]


def test_pccd_cs():
    # Do pCCD optimization:
    hf_h2.do_pccd()
    assert abs(hf_h2.pccd.e_tot - e_tot) < 1e-6


@pytest.mark.parametrize("core,expected", testdata_external)
def test_pccd_sp_args_external(core, expected):
    # Take only external energy from kwargs
    hf_h2.do_pccd(e_core=core)
    assert abs(hf_h2.pccd.e_tot - expected) < 1e-6


@pytest.mark.parametrize("orbs1,orbs2,expected", testdata_orbs)
def test_pccd_sp_args_orbs(orbs1, orbs2, expected):
    # local hf data
    orb = hf_h2.rhf.orb_a.copy()
    hf_h2.rhf.orb_a = None
    # copy eri as they get deleted
    eri = hf_h2.eri.copy()
    try:
        hf_h2.do_pccd(orbs1, orb_a=orbs2)
        # reset
        hf_h2.rhf.orb_a = orb
        assert abs(hf_h2.pccd.e_tot - expected) < 1e-6
    except (ArgumentError, FloatingPointError, ValueError):
        # reset
        hf_h2.rhf.orb_a = orb
        # load eri
        hf_h2.eri = eri.copy()


def test_pccd_cs_scf():
    # Do pCCD optimization:
    hf_h2.do_oopccd(checkpoint=-1)
    assert abs(hf_h2.oopccd.e_tot - -1.151686291339) < 1e-6


def test_pccd_cs_scf_restart():
    # Redo the pCCD optimization to get checkpoints
    hf_h2.do_oopccd()

    # Just check wether we have the proper results
    assert abs(hf_h2.oopccd.e_tot - -1.151686291339) < 1e-6

    old = IOData.from_file(f"{filemanager.result_dir}/checkpoint_pccd.h5")

    assert hasattr(old, "olp")
    assert hasattr(old, "orb_a")
    assert hasattr(old, "e_tot")
    assert hasattr(old, "e_ref")
    assert hasattr(old, "e_core")
    assert hasattr(old, "e_corr")
    assert hasattr(old, "dm_1")
    assert hasattr(old, "dm_2")

    # Update to slightly stretch geometry of H2
    h2_stretched = Molecule("6-31G", "test/h2_2.xyz")
    h2_stretched.do_hf()

    # re-orthogonalize orbitals
    project_orbitals(old.olp, h2_stretched.olp, old.orb_a, h2_stretched.orb_a)

    # recompute
    h2_stretched.do_oopccd(checkpoint_fn="checkpoint_restart.h5")

    assert abs(h2_stretched.oopccd.e_tot - -1.150027881389) < 1e-6

    # recompute
    h2_stretched.do_oopccd(
        restart=f"{filemanager.result_dir}/checkpoint_restart.h5"
    )

    assert abs(h2_stretched.oopccd.e_tot - -1.150027881389) < 1e-6

    # recompute using only restart file
    h2_stretched.do_oopccd_restart(
        restart=f"{filemanager.result_dir}/checkpoint_restart.h5"
    )

    assert abs(h2_stretched.oopccd.e_tot - -1.150027881389) < 1e-6

    e_corr = h2_stretched.oopccd.e_corr
    e_core = h2_stretched.oopccd.e_core
    e_ref = h2_stretched.oopccd.e_ref

    # recompute with wrong core energy
    h2_stretched.do_oopccd(
        restart=f"{filemanager.result_dir}/checkpoint_restart.h5",
        e_core=10.000,
    )

    with pytest.raises(AssertionError):
        assert abs(h2_stretched.oopccd.e_tot - -1.150027881389) < 1e-6
    assert abs(e_corr - h2_stretched.oopccd.e_corr) < 1e-6
    assert (
        abs(
            e_ref
            - e_core
            - h2_stretched.oopccd.e_ref
            + h2_stretched.oopccd.e_core
        )
        < 1e-6
    )


test_core = [
    (RpCCD, "water", "cc-pvdz", 0, {}, {"e_tot": -76.07225799852085}),
    (RpCCD, "water", "cc-pvdz", 1, {}, {"e_tot": -76.07210055926937}),
    (
        ROOpCCD,
        "water",
        "cc-pvdz",
        1,
        {"sort": False},
        {"e_tot": -76.0994990025405},
    ),
]


@pytest.mark.parametrize("cls,mol,basis,ncore,kwargs,result", test_core)
def test_pccd_core(cls, mol, basis, ncore, kwargs, result):

    # create molecule
    mol_ = Molecule(basis, f"test/{mol}.xyz", ncore=ncore)
    # do RHF
    mol_.do_hf()
    # do pccd
    if isinstance(cls, RpCCD):
        mol_.do_pccd(**kwargs)
        assert abs(mol_.pccd.e_tot - result["e_tot"]) < 1e-6
    elif isinstance(cls, ROOpCCD):
        mol_.do_oopccd(**kwargs)
        assert abs(mol_.oopccd.e_tot - result["e_tot"]) < 1e-6


test_stepsearch = [
    (
        ROOpCCD,
        "water",
        "cc-pvdz",
        "trust-region",
        {
            "stepsearch": {"method": "trust-region"},
            "thresh": {
                "energy": 5e-7,
                "gradientmax": 5e-3,
                "gradientnorm": 5e-3,
            },
            "sort": False,
        },
        {"e_tot": -76.099785827958},
    ),
    (
        ROOpCCD,
        "water",
        "cc-pvdz",
        "backtracking",
        {
            "stepsearch": {"method": "backtracking"},
            "thresh": {
                "energy": 5e-7,
                "gradientmax": 5e-3,
                "gradientnorm": 5e-3,
            },
            "sort": False,
        },
        {"e_tot": -76.099785827958},
    ),
    (
        ROOpCCD,
        "water",
        "cc-pvdz",
        "None",
        {
            "stepsearch": {"method": "None"},
            "thresh": {
                "energy": 5e-7,
                "gradientmax": 5e-3,
                "gradientnorm": 5e-3,
            },
            "sort": False,
        },
        {"e_tot": -76.099785827958},
    ),
]


@pytest.mark.parametrize(
    "cls, mol, basis, stepsearch, kwargs, result", test_stepsearch
)
def test_pccd_stepsearch(cls, mol, basis, stepsearch, kwargs, result):

    # create molecule
    mol_ = Molecule(basis, f"test/{mol}.xyz")
    # do RHF
    mol_.do_hf()
    # do pccd
    if cls.__name__ == RpCCD.__name__:
        mol_.do_pccd(**kwargs)
        assert abs(mol_.pccd.e_tot - result["e_tot"]) < 1e-6
    elif cls.__name__ == ROOpCCD.__name__:
        mol_.do_oopccd(**kwargs)
        assert abs(mol_.oopccd.e_tot - result["e_tot"]) < 1e-6
    else:
        raise ArgumentError(f"Do not know how to handle {cls}")


test_orb_copy = [
    (
        "water",
        "cc-pvdz",
    ),
]


test_pccd = [
    (RpCCD, {}),
    (ROOpCCD, {"sort": False, "maxiter": {"orbiter": 2}}),
]


@pytest.mark.parametrize("mol,basis", test_orb_copy)
@pytest.mark.parametrize("cls,kwargs", test_pccd)
def test_pccd_orbs(mol, basis, cls, kwargs):

    # create molecule
    mol_ = Molecule(basis, f"test/{mol}.xyz")
    # do RHF
    mol_.do_hf()
    # do pccd
    if cls.__name__ == RpCCD.__name__:
        mol_.do_pccd(**kwargs)
        assert mol_.rhf.orb_a == mol_.pccd.orb_a
    elif cls.__name__ == ROOpCCD.__name__:
        mol_.do_oopccd(**kwargs)
        assert not (mol_.rhf.orb_a == mol_.oopccd.orb_a)
    else:
        raise ArgumentError(f"Do not know how to handle {cls}")
