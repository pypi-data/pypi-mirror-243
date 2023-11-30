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

""" Unit tests for methods from rcc module and E2E tests for different CC
flavours. """

import pytest

from pybest import filemanager
from pybest.cc.rccd import RCCD
from pybest.cc.rccsd import RCCSD
from pybest.cc.rfpcc import RfpCCD, RfpCCSD
from pybest.exceptions import ArgumentError
from pybest.io.iodata import IOData
from pybest.linalg import DenseLinalgFactory
from pybest.occ_model import AufbauOccModel

###############################################################################
#  Unit test  #################################################################
###############################################################################


def test_read_input():
    """Checks if arguments are properly interpreted by read_input method."""

    class DenseNIndexMockObject:
        """Mocks DenseNIndex instance."""

        def __init__(self, label):
            self.label = label
            self._array = None

    # Create input data
    one = DenseNIndexMockObject("one")
    eri = DenseNIndexMockObject("eri")
    orb = DenseNIndexMockObject("orb")
    iodata_ = IOData(eri=eri, orb_a=orb, e_ref="e_ref", x="x")
    # Make RCCD instance and read input
    lf = DenseLinalgFactory(2)
    # use lf to initialize OccModel
    occ_model = AufbauOccModel(lf, nel=2)
    solver = RCCD(lf, occ_model)
    out = solver.read_input(iodata_, orb, one=one)
    assert len(out) == 3
    assert solver.e_ref == "e_ref"
    assert not hasattr(solver, "x")
    assert isinstance(one, DenseNIndexMockObject)
    assert one.label == "one"
    assert isinstance(eri, DenseNIndexMockObject)
    assert eri.label == "eri"
    assert isinstance(orb, DenseNIndexMockObject)
    assert orb.label == "orb"


def test_get_range():
    "Checks if method returns expected output."
    lf = DenseLinalgFactory(3)
    occ_model = AufbauOccModel(lf, nel=2)
    solver = RCCD(lf, occ_model)
    block = solver.get_range("ovov")
    assert block["begin0"] == 0
    assert block["begin1"] == 1
    assert block["begin2"] == 0
    assert block["begin3"] == 1
    assert block["end0"] == 1
    assert block["end1"] == 3
    assert block["end2"] == 1
    assert block["end3"] == 3


def test_get_range_frozencore():
    "Checks if method returns expected output if core is frozen (not active)."
    lf = DenseLinalgFactory(5)
    occ_model = AufbauOccModel(lf, nel=4, ncore=1)
    solver = RCCD(lf, occ_model)
    block = solver.get_range("ovov")
    assert block["begin0"] == 0
    assert block["begin1"] == 1
    assert block["begin2"] == 0
    assert block["begin3"] == 1
    assert block["end0"] == 1
    assert block["end1"] == 4
    assert block["end2"] == 1
    assert block["end3"] == 4


def test_set_seniority_0():
    "Check if seniority 0 amplitudes are set to 1 while all other remain 0."
    lf = DenseLinalgFactory(5)
    four_index = lf.create_four_index(2, 3, 2, 3)
    cc_solver = RCCD(lf, AufbauOccModel(lf, nel=4))
    four_index = cc_solver.set_seniority_0(four_index, value=1.0)
    assert four_index.get_element(0, 0, 0, 0) == 1
    assert four_index.get_element(0, 2, 0, 2) == 1
    assert four_index.get_element(1, 0, 1, 0) == 1
    assert four_index.get_element(0, 2, 0, 0) == 0
    assert four_index.get_element(0, 0, 1, 0) == 0
    assert four_index.get_element(1, 1, 0, 0) == 0
    assert four_index.get_element(0, 1, 1, 2) == 0


def test_set_seniority_2():
    "Check if seniority 2 amplitudes are set to 1 while all other remain 0."
    lf = DenseLinalgFactory(5)
    four_index = lf.create_four_index(2, 3, 2, 3)
    cc_solver = RCCD(lf, AufbauOccModel(lf, nel=4))
    four_index = cc_solver.set_seniority_2(four_index, value=1.0)
    assert four_index.get_element(0, 0, 0, 0) == 0
    assert four_index.get_element(0, 2, 0, 2) == 0
    assert four_index.get_element(1, 0, 1, 0) == 0
    assert four_index.get_element(0, 2, 0, 0) == 1
    assert four_index.get_element(1, 1, 1, 0) == 1
    assert four_index.get_element(1, 1, 0, 0) == 0
    assert four_index.get_element(0, 1, 1, 2) == 0


###############################################################################
## E2E tests ##################################################################
###############################################################################

# Define default reference wave function type for different CC methods
REF_WFN = {RCCD: "rhf", RCCSD: "rhf", RfpCCD: "pccd", RfpCCSD: "pccd"}


@pytest.mark.parametrize("method", [RCCD, RCCSD, RfpCCD, RfpCCSD])
@pytest.mark.parametrize("t_solver", ["krylov", "pbqn"])
def test_rcc_energy_h2(linalg, method, t_solver, h2_molecule):
    """Do calculations and compare energy with reference."""
    model = h2_molecule["model"]
    reference_energy = h2_molecule["energies"][method.__name__]
    linalg_factory = linalg(model.lf.default_nbasis)
    solver = method(linalg_factory, model.occ_model)
    result = solver(
        getattr(model, REF_WFN[method]), *model.ints(linalg), solver=t_solver
    )
    assert isinstance(solver.lf, linalg)
    assert result.converged is True
    assert abs(result.e_corr - reference_energy) < 1e-7


@pytest.mark.parametrize("method", [RCCD, RCCSD, RfpCCD, RfpCCSD])
@pytest.mark.parametrize("t_solver", ["krylov", "pbqn"])
def test_rcc_energy_hf(linalg_slow, method, t_solver, hf_molecule):
    """Do calculations and compare energy with reference."""
    model = hf_molecule["model"]
    reference_energy = hf_molecule["energies"][method.__name__]
    linalg_factory = linalg_slow(model.lf.default_nbasis)
    solver = method(linalg_factory, model.occ_model)
    result = solver(
        getattr(model, REF_WFN[method]),
        *model.ints(linalg_slow),
        solver=t_solver,
    )
    assert result.converged is True
    assert abs(result.e_corr - reference_energy) < 1e-7


@pytest.mark.parametrize("method", [RCCD, RCCSD, RfpCCD, RfpCCSD])
def test_rcc_energy_hf_dump_cache(linalg_slow, method, hf_molecule):
    """Do calculations and compare energy with reference for dumping cache."""
    model = hf_molecule["model"]
    reference_energy = hf_molecule["energies"][method.__name__]
    linalg_factory = linalg_slow(model.lf.default_nbasis)
    solver = method(linalg_factory, model.occ_model)
    result = solver(
        getattr(model, REF_WFN[method]),
        *model.ints(linalg_slow),
        solver="pbqn",
        dump_cache=True,
    )
    assert result.converged is True
    assert abs(result.e_corr - reference_energy) < 1e-7


@pytest.mark.parametrize("method", [RCCD, RCCSD, RfpCCD, RfpCCSD])
@pytest.mark.parametrize("t_solver", ["krylov", "pbqn"])
def test_rcc_energy_h2o(linalg_slow, method, t_solver, h2o_molecule):
    """Do calculations and compare energy with reference."""
    model = h2o_molecule["model"]
    reference_energy = h2o_molecule["energies"][method.__name__]
    linalg_factory = linalg_slow(model.lf.default_nbasis)
    solver = method(linalg_factory, model.occ_model)
    result = solver(
        getattr(model, REF_WFN[method]),
        *model.ints(linalg_slow),
        solver=t_solver,
    )
    assert result.converged is True
    assert abs(result.e_corr - reference_energy) < 1e-7


@pytest.mark.parametrize("method", [RCCD, RCCSD])
@pytest.mark.parametrize("t_solver", ["krylov", "pbqn"])
def test_rcc_energy_h2o_frozencore(linalg, method, t_solver, h2o_molecule_fc):
    """Tests if frozen core option works. Check only correlation energy."""
    model = h2o_molecule_fc["model"]
    energies = {
        "RCCD": -0.1483244346548191,
        "RCCSD": -0.1505224410065914,
    }
    linalg_factory = linalg(model.lf.default_nbasis)
    solver = method(linalg_factory, model.occ_model)
    result = solver(model.rhf, *model.ints(linalg), solver=t_solver)
    assert result.converged is True
    assert abs(result.e_corr - energies[method.__name__]) < 1e-7


@pytest.mark.parametrize("method", [RCCD, RCCSD])
def test_rcc_restart_h2(method, h2_molecule):
    "Test passes if error does not occur while reading the checkpoint."
    model = h2_molecule["model"]
    path = filemanager.temp_path(f"checkpoint_{method.__name__}.h5")
    rcc = method(model.lf, model.occ_model)
    out = rcc(model.rhf, *model.ints())
    out.to_file(path)
    out = rcc(model.rhf, *model.ints(), restart=path, maxiter=2)


def test_rcc_rccsd_rccsd(h2_molecule):
    "Check if nothing necessary (e.g. ERI) is deleted by RCCsd."
    model = h2_molecule["model"]
    rcc1 = RCCSD(model.lf, model.occ_model)
    rcc1(model.rhf, *model.ints(), initguess="mp2")
    rcc2 = RCCSD(model.lf, model.occ_model)
    rcc2(model.rhf, *model.ints(), initguess="mp2")


def test_rcc_ccd_fpccd(h2_molecule):
    "Check if RCCD cache is cleared."
    model = h2_molecule["model"]
    rcc1 = RCCD(model.lf, model.occ_model)
    out1 = rcc1(model.rhf, *model.ints(), initguess="mp2")
    rcc2 = RfpCCD(model.lf, model.occ_model)
    out2 = rcc2(model.pccd, *model.ints(), initguess="mp2")
    assert abs(out1.e_corr - h2_molecule["energies"]["RCCD"]) < 1e-7
    assert abs(out2.e_corr - h2_molecule["energies"]["RfpCCD"]) < 1e-7


def test_rcc_ccsd_fpccsd(h2_molecule):
    "Check if RCCSD cache is cleared."
    model = h2_molecule["model"]
    rcc1 = RCCSD(model.lf, model.occ_model)
    out1 = rcc1(model.rhf, *model.ints(), initguess="mp2")
    rcc2 = RfpCCSD(model.lf, model.occ_model)
    out2 = rcc2(model.pccd, *model.ints(), initguess="mp2")
    assert abs(out1.e_corr - h2_molecule["energies"]["RCCSD"]) < 1e-7
    assert abs(out2.e_corr - h2_molecule["energies"]["RfpCCSD"]) < 1e-7


@pytest.mark.parametrize("method", [RCCD, RCCSD, RfpCCD, RfpCCSD])
@pytest.mark.parametrize("cache_item", ["exchange_oovv"])
def test_rcc_dump_cache(linalg, method, cache_item, h2o_molecule):
    """Test if items are properly dumped to disk."""
    model = h2o_molecule["model"]
    linalg_factory = linalg(model.lf.default_nbasis)
    solver = method(linalg_factory, model.occ_model)
    # set some class attributes explicitly as they are set during function call
    one, two, orb = solver.read_input(model.kin, model.eri, model.rhf)
    solver._dump_cache = True
    solver.set_hamiltonian(one, two, orb)

    # Check if cache has been dumped properly
    # We need to access _store directly, otherwise the load function of the
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
    amplitudes = {
        "t_1": solver.lf.create_two_index(occ, virt),
        "t_2": solver.denself.create_four_index(occ, virt, occ, virt),
    }
    # all elements should be loaded from the disk and dumped to the disk again
    solver.cc_residual_vector(amplitudes)
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
