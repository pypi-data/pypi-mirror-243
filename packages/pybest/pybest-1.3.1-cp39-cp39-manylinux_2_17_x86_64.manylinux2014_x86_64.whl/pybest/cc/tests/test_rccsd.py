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

""" Unit tests for RCCSD method from rccsd module. """

import copy

import numpy as np
import pytest

from pybest.cache import Cache
from pybest.cc.rccsd import RCCSD
from pybest.linalg import DenseFourIndex, DenseTwoIndex

from .common import check_eri_in_cache, check_fock_in_cache

###############################################################################
#  Unit test  #################################################################
###############################################################################


def check_guess(amplitudes):
    """Checks if argument is a dictionary containing t_1 and t_2."""
    assert isinstance(amplitudes, dict)
    t_1 = amplitudes["t_1"]
    t_2 = amplitudes["t_2"]
    assert isinstance(t_1, DenseTwoIndex)
    assert isinstance(t_2, DenseFourIndex)
    assert t_1.shape == (1, 9)
    assert t_2.shape == (1, 9, 1, 9)
    assert np.allclose(t_2.array, t_2.array.transpose(2, 3, 0, 1))


def test_rccsd_generate_random_guess(h2_molecule):
    """Checks if generate_random_guess method returns expected output."""
    model = h2_molecule["model"]
    solver = RCCSD(model.lf, model.occ_model)
    check_guess(getattr(solver, "generate_random_guess")())


def test_rccsd_generate_constant_guess(h2_molecule):
    """Checks if generate_constant_guess method returns expected output."""
    model = h2_molecule["model"]
    solver = RCCSD(model.lf, model.occ_model)
    solver.initguess = "constant"
    initguess_1 = solver.generate_constant_guess(0.5)
    initguess_2 = solver.generate_guess(constant=0.5)
    check_guess(initguess_1)
    assert initguess_1["t_1"].get_element(0, 0) == 0.5
    assert initguess_1["t_2"].get_element(0, 0, 0, 0) == 0.5
    assert initguess_1["t_2"].get_element(0, 0, 0, 1) == 0.5
    check_guess(initguess_2)
    assert initguess_2["t_1"].get_element(0, 0) == 0.5
    assert initguess_2["t_2"].get_element(0, 0, 0, 0) == 0.5
    assert initguess_2["t_2"].get_element(0, 0, 0, 1) == 0.5


def test_rccsd_generate_mp2_guess(h2_molecule):
    """Checks if generate_mp2_guess method returns expected output."""
    model = h2_molecule["model"]
    kin, ne, eri = model.ints()
    ao1 = kin.copy()
    ao1.iadd(ne)
    ccsd = RCCSD(model.lf, model.occ_model)
    # we need to calculate the effective Hamiltonian for an MP2 guess
    ccsd.set_hamiltonian(ao1, eri, model.rhf.orb_a)
    check_guess(getattr(ccsd, "generate_mp2_guess")())


@pytest.mark.parametrize("select", ["mp2", "random", "constant"])
def test_rcc_generate_guess(select, h2_molecule):
    """Checks if generate_guess method returns expected output."""
    model = h2_molecule["model"]
    kin, ne, eri = model.ints()
    ao1 = kin.copy()
    ao1.iadd(ne)
    kwargs = {"orbital": model.rhf.orb_a, "ao1": ao1, "ao2": eri}
    solver = RCCSD(model.lf, model.occ_model)
    solver.initguess = select
    # we need to calculate the effective Hamiltonian for an MP2 guess
    solver.set_hamiltonian(ao1, eri, model.rhf.orb_a)
    amplitudes = getattr(solver, "generate_guess")(**kwargs)
    assert isinstance(amplitudes["t_2"], DenseFourIndex)
    assert isinstance(amplitudes["t_1"], DenseTwoIndex)


def test_rccsd_ravel(h2_molecule):
    """Checks if ravel method returns a vector with expected length."""
    model = h2_molecule["model"]
    solver = RCCSD(model.lf, model.occ_model)
    initguess = solver.generate_constant_guess(0.5)
    assert len(solver.ravel(initguess)) == 54


def test_rccsd_unravel(h2_molecule):
    """Checks if ravel method returns t_1 and t_2 amplitudes."""
    model = h2_molecule["model"]
    vector = np.ndarray((54))
    solver = RCCSD(model.lf, model.occ_model)
    amplitudes = solver.unravel(vector)
    assert isinstance(amplitudes, dict)
    assert isinstance(amplitudes["t_1"], DenseTwoIndex)
    assert isinstance(amplitudes["t_2"], DenseFourIndex)


def test_unravel_ravel(h2_molecule):
    """Checks if unravel(ravel(X)) = X."""
    model = h2_molecule["model"]
    ccd = RCCSD(model.lf, model.occ_model)
    amplitudes = ccd.generate_constant_guess(0.5)
    # Need to copy as we remove the arrays
    amplitudes_ = copy.deepcopy(amplitudes)
    vector = ccd.ravel(amplitudes)
    unraveled_amplitudes = ccd.unravel(vector)
    assert amplitudes_ == unraveled_amplitudes


def test_rccsd_vfunction(h2_molecule):
    """Checks if vector fucntion has a proper symmetry."""
    model = h2_molecule["model"]
    solver = RCCSD(model.lf, model.occ_model)
    kin, _, eri = model.ints()
    solver.set_hamiltonian(kin, eri, model.rhf.orb_a)
    initguess = solver.generate_constant_guess(constant=0.125)
    vfunc = solver.vfunction(solver.ravel(initguess))
    amplitudes = solver.unravel(vfunc)
    assert "t_1" in amplitudes
    assert "t_2" in amplitudes
    vfunc_t2 = amplitudes["t_2"]
    assert np.allclose(vfunc_t2.array, vfunc_t2.array.transpose(2, 3, 0, 1))


def test_can_construct_hamiltonian_blocks(linalg, h2o_molecule):
    "Check if hamiltonian property contains expected blocks."
    model = h2o_molecule["model"]
    rcc = RCCSD(linalg(model.lf.default_nbasis), model.occ_model)
    kin, ne, eri = model.ints()
    one = kin.copy()
    one.iadd(ne)
    rcc.set_hamiltonian(one, eri, model.rhf.orb_a)
    assert isinstance(rcc.cache, Cache)

    # Check Fock matrix blocks
    fock_labels = ["fock_oo", "fock_ov", "fock_vv"]
    check_fock_in_cache(rcc.cache, fock_labels, nocc=5, nvirt=8)

    # Check 2-body Hamiltonian blocks and exchange blocks
    ham_2 = ["eri_oooo", "eri_ooov", "eri_oovv", "eri_ovov", "eri_ovvv"]
    ham_exc = ["exchange_oovv", "exchange_ooov"]
    check_eri_in_cache(rcc.cache, ham_2 + ham_exc, nocc=5, nvirt=8)


def test_rccsd_compute_t1_diagnostic(h2_molecule):
    """Compares T1 diagnostic with reference data."""
    model = h2_molecule["model"]
    solver = RCCSD(model.lf, model.occ_model)
    kin, ne, eri = model.ints()
    out = solver(kin, ne, eri, model.rhf.orb_a)
    t1_diag = solver.compute_t1_diagnostic(out.t_1, out.nocc)
    assert abs(out.e_tot + 0.034709514) < 1e-8
    assert abs(t1_diag - 0.00518216985) < 1e-8


def test_get_max_amplitudes(h2_molecule):
    "Check if amplitudes can be converted from tensor to index-value format."
    model = h2_molecule["model"]
    ccsd = RCCSD(model.lf, model.occ_model)
    out = ccsd(*model.ints(), model.orb_a, initguess="constant")
    assert np.isclose(out.e_corr, -0.034709514282981926, atol=1e-7)
    t_1 = ccsd.get_max_amplitudes(threshold=1e-3)["t_1"]
    t_2 = ccsd.get_max_amplitudes(threshold=5e-2)["t_2"]
    # Check single-excitation amplitudes.
    assert t_1[0][0] == (1, 3), "Did not find expected index."
    assert t_1[1][0] == (1, 7), "Did not find expected index."
    assert len(t_1) == 2, "The number of max amplitudes is not correct."
    # Check double-excitation amplitudes
    assert t_2[0][0] == (1, 2, 1, 2), "Did not find expected index."
    assert np.isclose(t_2[0][1], -0.053721), "Did not find expected value."
    assert t_2[1][0] == (1, 4, 1, 4), "Did not find expected index."
    assert np.isclose(t_2[1][1], -0.053181), "Did not find expected value."
    assert t_2[2][0] == (1, 3, 1, 3), "Did not find expected index."
    assert len(t_2) == 3, "The number of max amplitudes is not correct."
