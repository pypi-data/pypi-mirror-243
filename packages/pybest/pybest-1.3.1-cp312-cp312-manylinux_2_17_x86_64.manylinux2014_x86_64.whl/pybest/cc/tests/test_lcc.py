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

from pybest import filemanager
from pybest.cc import RLCCD, RLCCSD, RpCCDLCCD, RpCCDLCCSD
from pybest.context import context
from pybest.exceptions import ArgumentError
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
from pybest.linalg import DenseLinalgFactory
from pybest.linalg.cholesky import CholeskyLinalgFactory
from pybest.occ_model import AufbauOccModel


class Molecule:
    def __init__(self, test_dict, linalg, ncore=0):
        fn_xyz = context.get_fn(test_dict["xyz"])
        self.obasis = get_gobasis(
            test_dict["basis"], fn_xyz, print_basis=False
        )
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

        fn_orb = context.get_fn(test_dict["orb"])
        orb_ = np.fromfile(fn_orb, sep=",").reshape(
            self.obasis.nbasis, self.obasis.nbasis
        )
        self.orb_a = self.lf.create_orbital()
        self.orb_a._coeffs = orb_

        self.occ_model = AufbauOccModel(self.obasis, ncore=ncore)


rhf_set = [
    (
        RLCCD,
        "nh3/cc-pvdz",
        "krylov",
        {
            "xyz": "test/nh3.xyz",
            "orb": "test/nh3_hf.txt",
            "basis": "cc-pvdz",
            "solver": "krylov",
            "e_ref": -56.195341335133,
            "e_tot": -56.40363609015413,
            "e_corr": -0.20829475502103717,
            "e_corr_d": -0.20829475502103717,
        },
    ),
    (
        RLCCSD,
        "nh3/cc-pvdz",
        "krylov",
        {
            "xyz": "test/nh3.xyz",
            "orb": "test/nh3_hf.txt",
            "basis": "cc-pvdz",
            "solver": "krylov",
            "e_ref": -56.195341335133,
            "e_tot": -56.404534989197664,
            "e_corr": -0.2091936543105653,
            "e_corr_d": -0.2091936543105653,
            "e_corr_s": 0.0000000000000000,
        },
    ),
]

pccd_set = [
    (
        RpCCDLCCD,
        "nh3/cc-pvdz/can",
        {
            "xyz": "test/nh3.xyz",
            "orb": "test/nh3_hf.txt",
            "basis": "cc-pvdz",
            "e_tot_pccd": -56.235650029799,
            "e_tot": -56.40112996066194,
            "e_corr": -0.16547993086294,
            "e_corr_d": -0.16547993086294,
        },
    ),
    (
        RpCCDLCCSD,
        "nh3/cc-pvdz/can",
        {
            "xyz": "test/nh3.xyz",
            "orb": "test/nh3_hf.txt",
            "basis": "cc-pvdz",
            "e_tot_pccd": -56.235650029799,
            "e_tot": -56.40187108073425,
            "e_corr": -0.16622105102133822,
            "e_corr_s": 0.00000000000000000,
            "e_corr_d": -0.16622105102133822,
        },
    ),
    (
        RpCCDLCCD,
        "nh3/cc-pvdz/opt",
        {
            "xyz": "test/nh3.xyz",
            "orb": "test/nh3_ap1rog.txt",
            "basis": "cc-pvdz",
            "e_tot_pccd": -56.288865344795,
            "e_tot": -56.40401867,
            "e_corr": -0.11515332,
            "e_corr_d": -0.11515332,
        },
    ),
    (
        RpCCDLCCSD,
        "nh3/cc-pvdz/opt",
        {
            "xyz": "test/nh3.xyz",
            "orb": "test/nh3_ap1rog.txt",
            "basis": "cc-pvdz",
            "e_tot_pccd": -56.28886534,
            "e_tot": -56.40491460,
            "e_corr": -0.11604926,
            "e_corr_s": -0.00024475,
            "e_corr_d": -0.11580450,
        },
    ),
]

pbqn_set = [
    (
        "pbqn/6/f/2",
        {
            "solver": "pbqn",
            "diis": {"diismax": 6, "diisreset": False},
            "jacobian": 2,
        },
    ),
    (
        "pbqn/6/f/1",
        {
            "solver": "pbqn",
            "diis": {"diismax": 6, "diisreset": False},
            "jacobian": 1,
        },
    ),
    (
        "pbqn/6/t/1",
        {
            "solver": "pbqn",
            "diis": {"diismax": 6, "diisreset": True},
            "jacobian": 1,
        },
    ),
    (
        "pbqn/6/t/2",
        {
            "solver": "pbqn",
            "diis": {"diismax": 6, "diisreset": True},
            "jacobian": 2,
        },
    ),
]

# test only one module, frozen core is assigned using the same code in all modules
frozen_core_set = [
    (
        RpCCDLCCSD,
        "nh3/cc-pvdz",
        0,
        {
            "xyz": "test/nh3.xyz",
            "orb": "test/nh3_ap1rog.txt",
            "basis": "cc-pvdz",
            "e_tot_pccd": -56.28886534,
            "e_tot": -56.40491460,
            "e_corr": -0.11604926,
            "e_corr_s": -0.00024475,
            "e_corr_d": -0.11580450,
        },
    ),
    (
        RpCCDLCCSD,
        "nh3/cc-pvdz",
        1,
        {
            "xyz": "test/nh3.xyz",
            "orb": "test/nh3_ap1rog.txt",
            "basis": "cc-pvdz",
            "e_tot_pccd": -56.28858327,
            "e_tot": -56.40252139,
            "e_corr": -0.11393812,
            "e_corr_s": -0.00024662,
            "e_corr_d": -0.11369150,
        },
    ),
]


@pytest.mark.parametrize("cls,name,solver,dict_", rhf_set)
def test_rhflcc(cls, name, solver, dict_, linalg):
    mol = Molecule(dict_, linalg)

    iodata = IOData(
        **{
            "orb_a": mol.orb_a,
            "olp": mol.olp,
            "e_core": mol.external,
            "e_ref": dict_["e_ref"],
        }
    )
    lcc = cls(mol.lf, mol.occ_model)
    lcc_ = lcc(mol.one, mol.er, iodata, threshold_r=1e-8)
    assert abs(lcc_.e_tot - dict_["e_tot"]) < 1e-6
    assert abs(lcc_.e_corr - dict_["e_corr"]) < 1e-6
    assert abs(lcc_.e_corr_d - dict_["e_corr_d"]) < 1e-6
    if "e_corr_s" in dict_:
        assert abs(lcc_.e_corr_s - dict_["e_corr_s"]) < 1e-6


@pytest.mark.parametrize("cls,name,solver,dict_", rhf_set)
def test_rhflcc_restart(cls, name, solver, dict_):
    mol = Molecule(dict_, DenseLinalgFactory)

    iodata = IOData(
        **{
            "orb_a": mol.orb_a,
            "olp": mol.olp,
            "e_core": mol.external,
            "e_ref": dict_["e_ref"],
        }
    )
    #
    # Converge not too tight
    #
    lcc = cls(mol.lf, mol.occ_model)
    lcc_ = lcc(mol.one, mol.er, iodata, threshold_r=1e-2)
    #
    # Test restart
    #
    lcc = cls(mol.lf, mol.occ_model)
    lcc_ = lcc(
        mol.one,
        mol.er,
        iodata,
        initguess=f"{filemanager.result_dir}/checkpoint_{cls.__name__}.h5",
        threshold_r=1e-8,
    )
    assert abs(lcc_.e_tot - dict_["e_tot"]) < 1e-6
    assert abs(lcc_.e_corr - dict_["e_corr"]) < 1e-6
    assert abs(lcc_.e_corr_d - dict_["e_corr_d"]) < 1e-6
    if "e_corr_s" in dict_:
        assert abs(lcc_.e_corr_s - dict_["e_corr_s"]) < 1e-6


@pytest.mark.parametrize(
    "dump_cache", [True, False], ids=["dump_cache on", "dump_cache off"]
)
@pytest.mark.parametrize("solver", ["krylov"])
@pytest.mark.parametrize("cls,name,dict_", pccd_set)
def test_pccdlcc(cls, name, dict_, solver, dump_cache, linalg):
    mol = Molecule(dict_, linalg)

    # Do pCCD optimization:
    pccd = RpCCD(mol.lf, mol.occ_model)
    pccd_ = pccd(mol.one, mol.er, mol.orb_a, mol.olp, e_core=mol.external)
    assert abs(pccd_.e_tot - dict_["e_tot_pccd"]) < 1e-6

    lcc = cls(mol.lf, mol.occ_model)
    lcc_ = lcc(mol.one, mol.er, pccd_, threshold_r=1e-8, dump_cache=dump_cache)
    assert abs(lcc_.e_tot - dict_["e_tot"]) < 1e-6
    assert abs(lcc_.e_corr - dict_["e_corr"]) < 1e-6
    assert abs(lcc_.e_corr_d - dict_["e_corr_d"]) < 1e-6
    if "e_corr_s" in dict_:
        assert abs(lcc_.e_corr_s - dict_["e_corr_s"]) < 1e-6


@pytest.mark.parametrize("solver", ["krylov"])
@pytest.mark.parametrize("cls,name,dict_", pccd_set)
def test_pccdlcc_restart(cls, name, dict_, solver):
    mol = Molecule(dict_, DenseLinalgFactory)

    # Do pCCD optimization:
    pccd = RpCCD(mol.lf, mol.occ_model)
    pccd_ = pccd(mol.one, mol.er, mol.orb_a, mol.olp, e_core=mol.external)
    assert abs(pccd_.e_tot - dict_["e_tot_pccd"]) < 1e-6
    #
    # Converge not too tight
    #
    lcc = cls(mol.lf, mol.occ_model)
    lcc_ = lcc(mol.one, mol.er, pccd_, threshold_r=1e-2)
    #
    # Test restart
    #
    lcc = cls(mol.lf, mol.occ_model)
    lcc_ = lcc(
        mol.one,
        mol.er,
        pccd_,
        initguess=f"{filemanager.result_dir}/checkpoint_{cls.__name__}.h5",
        threshold_r=1e-8,
    )
    assert abs(lcc_.e_tot - dict_["e_tot"]) < 1e-6
    assert abs(lcc_.e_corr - dict_["e_corr"]) < 1e-6
    assert abs(lcc_.e_corr_d - dict_["e_corr_d"]) < 1e-6
    if "e_corr_s" in dict_:
        assert abs(lcc_.e_corr_s - dict_["e_corr_s"]) < 1e-6


@pytest.mark.parametrize("solver, solver_dict", pbqn_set)
@pytest.mark.parametrize("cls,name,dict_", pccd_set)
def test_pccdlcc_solver(cls, name, dict_, solver, solver_dict):
    mol = Molecule(dict_, DenseLinalgFactory)

    # Do pCCD optimization:
    pccd = RpCCD(mol.lf, mol.occ_model)
    pccd_ = pccd(mol.one, mol.er, mol.orb_a, mol.olp, e_core=mol.external)
    assert abs(pccd_.e_tot - dict_["e_tot_pccd"]) < 1e-6

    lcc = cls(mol.lf, mol.occ_model)
    lcc_ = lcc(mol.one, mol.er, pccd_, threshold_r=1e-8, **solver_dict)
    assert abs(lcc_.e_tot - dict_["e_tot"]) < 1e-6
    assert abs(lcc_.e_corr - dict_["e_corr"]) < 1e-6
    assert abs(lcc_.e_corr_d - dict_["e_corr_d"]) < 1e-6
    if "e_corr_s" in dict_:
        assert abs(lcc_.e_corr_s - dict_["e_corr_s"]) < 1e-6


@pytest.mark.parametrize("cls,name,ncore,dict_", frozen_core_set)
def test_pccdlcc_frozen_core(cls, name, ncore, dict_):
    mol = Molecule(dict_, DenseLinalgFactory, ncore=ncore)

    # Do pCCD optimization:
    pccd = RpCCD(mol.lf, mol.occ_model)
    pccd_ = pccd(mol.one, mol.er, mol.orb_a, mol.olp, e_core=mol.external)
    assert abs(pccd_.e_tot - dict_["e_tot_pccd"]) < 1e-6

    # Do LCC calculations with scipy.root 'krylov' solver
    lcc = cls(mol.lf, mol.occ_model)
    lcc_ = lcc(mol.one, mol.er, pccd_, threshold_r=1e-8)
    assert abs(lcc_.e_tot - dict_["e_tot"]) < 1e-6
    assert abs(lcc_.e_corr - dict_["e_corr"]) < 1e-6
    assert abs(lcc_.e_corr_d - dict_["e_corr_d"]) < 1e-6
    if "e_corr_s" in dict_:
        assert abs(lcc_.e_corr_s - dict_["e_corr_s"]) < 1e-6

    # Do LCC calculations with PyBEST's Quasi-Newton solver
    lcc = cls(mol.lf, mol.occ_model)
    lcc_ = lcc(mol.one, mol.er, pccd_, threshold_r=1e-8, solver="pbqn")
    assert abs(lcc_.e_tot - dict_["e_tot"]) < 1e-6
    assert abs(lcc_.e_corr - dict_["e_corr"]) < 1e-6
    assert abs(lcc_.e_corr_d - dict_["e_corr_d"]) < 1e-6
    if "e_corr_s" in dict_:
        assert abs(lcc_.e_corr_s - dict_["e_corr_s"]) < 1e-6

    # Overwrite core energy and thus total energy
    # Can only be done in pCCD, affects only total energy
    pccd = RpCCD(mol.lf, mol.occ_model)
    pccd_ = pccd(
        mol.one, mol.er, mol.orb_a, mol.olp, e_core=(mol.external + 10.0)
    )
    assert abs(pccd_.e_tot - dict_["e_tot_pccd"] - 10.0) < 1e-6

    lcc = cls(mol.lf, mol.occ_model)
    lcc_ = lcc(mol.one, mol.er, pccd_, threshold_r=1e-8)
    assert abs(lcc_.e_tot - dict_["e_tot"] - 10.0) < 1e-6
    assert abs(lcc_.e_corr - dict_["e_corr"]) < 1e-6
    assert abs(lcc_.e_corr_d - dict_["e_corr_d"]) < 1e-6
    if "e_corr_s" in dict_:
        assert abs(lcc_.e_corr_s - dict_["e_corr_s"]) < 1e-6


@pytest.mark.parametrize("method", [RpCCDLCCD, RpCCDLCCSD])
@pytest.mark.parametrize("cache_item", ["govvo"])
def test_rcc_dump_cache(linalg, method, cache_item, h2o_molecule):
    """Test if items are properly dumped to disk."""
    model = h2o_molecule["model"]
    linalg_factory = linalg(model.lf.default_nbasis)
    solver = method(linalg_factory, model.occ_model)
    # set some class attributes explicitly as they are set during function call
    one, two, orb = solver.read_input(model.kin, model.eri, model.pccd)
    solver._dump_cache = True
    solver.set_hamiltonian(one, two, orb)

    # Check if cache has been dumped properly
    # We need to access _store directly otherwise the load function of the
    # Cache class is called and test will fail by construction
    #
    # 1) Check set_hamiltonian
    try:
        assert not hasattr(solver.cache._store[cache_item]._value, "_array"), (
            f"Cache element {cache_item} not properly dumped to disk in "
            "set_hamiltonian"
        )
    except KeyError:
        pass
    # 2) Check cc_residual_vector
    occ, virt = solver.occ_model.nacto[0], solver.occ_model.nactv[0]
    unknowns = int(occ * virt * (occ * virt + 1) / 2)
    if solver.acronym == "RpCCDLCCSD":
        unknowns += occ * virt
    amplitudes = solver.lf.create_one_index(unknowns)
    # all elements should be loaded from the disk and dumped to the disk again
    solver.vfunction(amplitudes)
    try:
        with pytest.raises(ArgumentError):
            assert not hasattr(
                solver.cache._store[cache_item].value, "_array"
            ), (
                f"Cache element {cache_item} not properly dumped to disk in "
                "build_subspace_hamiltonian"
            )
    except KeyError:
        pass
