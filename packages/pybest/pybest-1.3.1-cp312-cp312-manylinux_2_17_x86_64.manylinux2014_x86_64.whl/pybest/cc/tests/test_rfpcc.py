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

""" Unit tests for RfpCCD and RfpCCSD methods from rfpcc module. """

import pytest

from pybest.cc.rfpcc import RfpCCD, RfpCCSD
from pybest.linalg import DenseFourIndex, DenseLinalgFactory, DenseTwoIndex
from pybest.occ_model import AufbauOccModel

###############################################################################
#  Unit test  #################################################################
###############################################################################


def check_pair_amplitudes(t_2, value):
    "Checks if t_2 (DenseFourIndex) array has a given value at diagonal abab."
    assert t_2.get_element(0, 0, 0, 0) == value
    assert t_2.get_element(0, 1, 0, 1) == value
    assert t_2.get_element(0, 2, 0, 2) == value
    assert t_2.get_element(0, 0, 0, 1) != value
    assert t_2.get_element(0, 1, 0, 0) != value
    assert t_2.get_element(0, 1, 0, 2) != value
    assert t_2.get_element(0, 2, 0, 1) != value


@pytest.mark.parametrize("select", ["random", "constant"])
def test_rfpccd_generate_guess(select, h2_molecule):
    "Checks if initial guess is dict and contains t_2 amplitudes."
    model = h2_molecule["model"]
    fpcc = RfpCCD(model.lf, model.occ_model)
    fpcc.initguess = select
    nocc = model.occ_model.nocc[0]
    fpcc.t_p = DenseTwoIndex(nocc, model.lf.default_nbasis - nocc)
    fpcc.t_p.assign(2.0)
    initguess = fpcc.generate_guess()
    assert isinstance(initguess, dict)
    assert isinstance(initguess["t_2"], DenseFourIndex)
    check_pair_amplitudes(initguess["t_2"], 2.0)


@pytest.mark.parametrize("select", ["random", "constant"])
def test_rfpccsd_generate_guess(select, h2_molecule):
    "Checks if initial guess is dict and contains t_1 and t_2 amplitudes."
    model = h2_molecule["model"]
    fpcc = RfpCCSD(model.lf, model.occ_model)
    fpcc.initguess = select
    nocc = model.occ_model.nocc[0]
    fpcc.t_p = DenseTwoIndex(nocc, model.lf.default_nbasis - nocc)
    fpcc.t_p.assign(2.0)
    initguess = fpcc.generate_guess()
    assert isinstance(initguess, dict)
    assert isinstance(initguess["t_2"], DenseFourIndex)
    assert isinstance(initguess["t_1"], DenseTwoIndex)
    check_pair_amplitudes(initguess["t_2"], 2.0)


def test_rfpccd_vfunction(h2_molecule):
    "Checks if vector function has 0 for seniority 0 amplitudes."
    model = h2_molecule["model"]
    fpcc = RfpCCD(model.lf, model.occ_model)
    kin, _, eri = model.ints()
    fpcc.set_hamiltonian(kin, eri, model.rhf.orb_a)
    initguess = fpcc.generate_constant_guess(constant=0.125)
    vfunc = fpcc.vfunction(fpcc.ravel(initguess))
    check_pair_amplitudes(fpcc.unravel(vfunc)["t_2"], 0.0)


def test_rfpccsd_vfunction(h2_molecule):
    "Checks if vector function has 0 for seniority 0 amplitudes."
    model = h2_molecule["model"]
    fpcc = RfpCCSD(model.lf, model.occ_model)
    kin, _, eri = model.ints()
    fpcc.set_hamiltonian(kin, eri, model.rhf.orb_a)
    initguess = fpcc.generate_constant_guess(constant=0.125)
    vfunc = fpcc.vfunction(fpcc.ravel(initguess))
    check_pair_amplitudes(fpcc.unravel(vfunc)["t_2"], 0.0)


def test_set_pair_amplitudes():
    "Checks if pair-amplitudes are set properly."
    t_p = DenseTwoIndex(2, 3)
    t_p.assign(1.0)
    t_2 = DenseFourIndex(2, 3, 2, 3)
    lf = DenseLinalgFactory(5)
    cc_solver = RfpCCD(lf, AufbauOccModel(lf, nel=4))
    four_index = cc_solver.set_pair_amplitudes(t_2, t_p)
    assert four_index.get_element(0, 0, 0, 0) == 1
    assert four_index.get_element(0, 2, 0, 2) == 1
    assert four_index.get_element(1, 0, 1, 0) == 1
    assert four_index.get_element(0, 2, 0, 0) == 0
    assert four_index.get_element(0, 0, 1, 0) == 0
    assert four_index.get_element(1, 1, 0, 0) == 0
    assert four_index.get_element(0, 1, 1, 2) == 0
