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

""" Unit tests for RCCD method from rccd module. """

import copy

import numpy as np
import pytest

from pybest.cache import Cache
from pybest.cc.rccd import RCCD
from pybest.exceptions import ArgumentError
from pybest.io.iodata import IOData
from pybest.linalg import DenseFourIndex

from .common import check_eri_in_cache, check_fock_in_cache

###############################################################################
#  Unit test  #################################################################
###############################################################################


def check_guess(initguess):
    """Checks if argument is a dictionary containing t_2 amplitudes."""
    assert isinstance(initguess, dict)
    t_2 = initguess["t_2"]
    assert isinstance(t_2, DenseFourIndex)
    assert t_2.shape == (1, 9, 1, 9)
    assert np.allclose(t_2.array, t_2.array.transpose(2, 3, 0, 1))


def test_rccd_can_get_t_2_amplitudes_from_dict(h2_molecule):
    """Checks if method get_amplitudes_from_dict works."""
    model = h2_molecule["model"]
    ccd = RCCD(model.lf, model.occ_model)
    legit_dicts = [{"a": 0, "t_2": 2}, {"t_1": 1, "t_2": 2}, {"c_2": 2}]
    for item in legit_dicts:
        assert ccd.get_amplitudes_from_dict(item)["t_2"] == 2
    with pytest.raises(ArgumentError):
        ccd.get_amplitudes_from_dict({"ampl": "nope"})


def test_rccd_can_get_t_2_amplitudes_from_iodata(h2_molecule):
    """Checks if method get_amplitudes_from_dict works."""
    model = h2_molecule["model"]
    ccd = RCCD(model.lf, model.occ_model)
    legit_io = [IOData(a=0, t_2=2), IOData(t_1=1, t_2=2), IOData(c_2=2)]
    for item in legit_io:
        assert ccd.get_amplitudes_from_iodata(item)["t_2"] == 2
    with pytest.raises(ArgumentError):
        ccd.get_amplitudes_from_iodata(IOData(ampl="nope"))


def test_rccd_generate_random_guess(h2_molecule):
    """Checks if method generate_random_guess returns an expected output."""
    model = h2_molecule["model"]
    ccd = RCCD(model.lf, model.occ_model)
    check_guess(ccd.generate_random_guess())


def test_rccd_generate_constant_guess(h2_molecule):
    """Checks if method generate_constant_guess returns an expected output."""
    model = h2_molecule["model"]
    ccd = RCCD(model.lf, model.occ_model)
    check_guess(ccd.generate_constant_guess(0.5))


def test_rccd_generate_mp2_guess(h2_molecule):
    """Checks if method generate_mp2_guess returns an expected output."""
    model = h2_molecule["model"]
    kin, ne, eri = model.ints()
    ao1 = kin.copy()
    ao1.iadd(ne)
    ccd = RCCD(model.lf, model.occ_model)
    # we need to calculate the effective Hamiltonian for an MP2 guess
    ccd.set_hamiltonian(ao1, eri, model.rhf.orb_a)
    check_guess(ccd.generate_mp2_guess())


@pytest.mark.parametrize("select", ["mp2", "random", "constant"])
def test_rccd_generate_guess(select, h2_molecule):
    """Checks if method generate_guess returns an expected output."""
    model = h2_molecule["model"]
    kin, ne, eri = model.ints()
    ao1 = kin.copy()
    ao1.iadd(ne)
    kwargs = {"orbital": model.rhf.orb_a, "ao1": ao1, "ao2": eri}
    ccd = RCCD(model.lf, model.occ_model)
    ccd.initguess = select
    # we need to calculate the effective Hamiltonian for an MP2 guess
    ccd.set_hamiltonian(ao1, eri, model.rhf.orb_a)
    initguess = ccd.generate_guess(**kwargs)
    assert isinstance(initguess, dict)
    assert isinstance(initguess["t_2"], DenseFourIndex)


def test_ravel(h2_molecule):
    """Checks if ravel method returns vector with expected length."""
    model = h2_molecule["model"]
    ccd = RCCD(model.lf, model.occ_model)
    amplitudes = ccd.generate_constant_guess(0.5)
    assert len(ccd.ravel(amplitudes)) == 45


def test_unravel(h2_molecule):
    """Checks if unravel method returns DenseFourIndex inst of proper size."""
    model = h2_molecule["model"]
    vector = np.ndarray((45))
    ccd = RCCD(model.lf, model.occ_model)
    amplitudes = ccd.unravel(vector)
    assert isinstance(amplitudes, dict)
    assert isinstance(amplitudes["t_2"], DenseFourIndex)


def test_unravel_ravel(h2_molecule):
    """Checks if unravel(ravel(X)) = X."""
    model = h2_molecule["model"]
    ccd = RCCD(model.lf, model.occ_model)
    amplitudes = ccd.generate_constant_guess(0.5)
    # Need to copy as we remove the arrays
    amplitudes_ = copy.deepcopy(amplitudes)
    vector = ccd.ravel(amplitudes)
    unraveled_amplitudes = ccd.unravel(vector)
    assert amplitudes_ == unraveled_amplitudes


def test_rcc_vfunction_symmetry_and_type(h2_molecule):
    """Checks if vector function has a proper symmetryi and type."""
    model = h2_molecule["model"]
    ccd = RCCD(model.lf, model.occ_model)
    kin, _, eri = model.ints()
    ccd.set_hamiltonian(kin, eri, model.rhf.orb_a)
    t_2 = ccd.generate_constant_guess(constant=0.125)
    vfunc = ccd.vfunction(ccd.ravel(t_2))
    assert isinstance(vfunc, np.ndarray)
    vfunc_t2 = ccd.unravel(vfunc)["t_2"]
    assert np.allclose(vfunc_t2.array, vfunc_t2.array.transpose(2, 3, 0, 1))


def test_can_construct_hamiltonian_blocks(linalg, h2o_molecule):
    "Check if hamiltonian property contains expected blocks."
    model = h2o_molecule["model"]
    rcc = RCCD(linalg(model.lf.default_nbasis), model.occ_model)
    kin, ne, eri = model.ints(linalg)
    one = kin.copy()
    one.iadd(ne)
    rcc.set_hamiltonian(one, eri, model.rhf.orb_a)
    assert isinstance(rcc.cache, Cache)

    # Check Fock matrix blocks
    fock_labels = ["fock_oo", "fock_vv"]
    check_fock_in_cache(rcc.cache, fock_labels, nocc=5, nvirt=8)

    # Check 2-body Hamiltonian blocks and exchange blocks
    ham_2 = ["eri_oooo", "eri_oovv", "eri_ovov"]
    ham_exc = ["exchange_oovv"]
    check_eri_in_cache(rcc.cache, ham_2 + ham_exc, nocc=5, nvirt=8)


def test_rccd_init_fails_if_kwarg_not_recognized(h2o_molecule):
    "Check if RCC init raises error if kwarg is not recognized."
    model = h2o_molecule["model"]
    with pytest.raises(ArgumentError):
        RCCD(model.lf, model.occ_model, badkwarg="Wrong kwarg.")


def test_rccd_call_fails_if_kwarg_not_recognized(h2o_molecule):
    "Check if RCC init raises error if kwarg is not recognized."
    model = h2o_molecule["model"]
    with pytest.raises(ArgumentError):
        rcc = RCCD(model.lf, model.occ_model)
        rcc(*model.ints(), model.rhf.orb_a, badkwarg="Wrong kwarg.")


def test_get_max_amplitudes(h2_molecule):
    "Check if amplitudes can be converted from tensor to index-value format."
    model = h2_molecule["model"]
    ccd = RCCD(model.lf, model.occ_model)
    ccd(*model.ints(), model.orb_a, initguess="constant")
    t_2 = ccd.get_max_amplitudes()["t_2"]
    assert t_2[0][0] == (1, 2, 1, 2), "Did not find expected index."
    assert np.isclose(t_2[0][1], -0.053531), "Did not find expected value."
    assert t_2[1][0] == (1, 4, 1, 4), "Did not find expected index."
    assert np.isclose(t_2[1][1], -0.052408), "Did not find expected value."
    assert t_2[11][0] == (1, 10, 1, 4), "Did not find expected index."
    assert len(t_2) == 12, "The number of max amplitudes is not correct."
    t_2 = ccd.get_max_amplitudes(limit=4)["t_2"]
    assert t_2[0][0] == (1, 2, 1, 2), "Did not find expected index."
    assert np.isclose(t_2[0][1], -0.053531), "Did not find expected value."
    assert t_2[1][0] == (1, 4, 1, 4), "Did not find expected index."
    assert np.isclose(t_2[1][1], -0.052408), "Did not find expected value."
    assert len(t_2) == 4, "The number of max amplitudes is not correct."
    t_2 = ccd.get_max_amplitudes(threshold=0.05)["t_2"]
    assert t_2[0][0] == (1, 2, 1, 2), "Did not find expected index."
    assert np.isclose(t_2[0][1], -0.053531), "Did not find expected value."
    assert t_2[1][0] == (1, 4, 1, 4), "Did not find expected index."
    assert np.isclose(t_2[1][1], -0.052408), "Did not find expected value."
    assert len(t_2) == 3, "The number of max amplitudes is not correct."
