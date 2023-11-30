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

from pybest.context import context
from pybest.exceptions import ArgumentError, GOBasisError
from pybest.gbasis.gobasis import get_gobasis
from pybest.io.iodata import IOData
from pybest.linalg import DenseLinalgFactory, DenseOrbital, DenseTwoIndex
from pybest.linalg.cholesky import CholeskyLinalgFactory
from pybest.utils import check_lf, get_com, unmask, unmask_orb


def test_check_gobasis():

    fn = context.get_fn("test/h2o_ccdz.xyz")
    # Dry runs (basis set consistencies are checked in gobasis tests):
    get_gobasis("cc-pVDZ", fn, print_basis=False)

    with pytest.raises(GOBasisError):
        get_gobasis("cc-pVDZ", fn, dummy=0, print_basis=False)
    with pytest.raises(GOBasisError):
        get_gobasis("cc-pVDZ", fn, active_fragment=0, print_basis=False)
    with pytest.raises(GOBasisError):
        get_gobasis(
            "cc-pVDZ", fn, active_fragment=[0], dummy=[1], print_basis=False
        )

    # basis set does not contain information about atom and has to fail:
    # this error is only captured in check_gobasis function
    fn = context.get_fn("test/u2.xyz")
    with pytest.raises(GOBasisError):
        get_gobasis("cc-pVDZ", fn, print_basis=False)


def test_unmask():

    iodata = IOData(kwarg1="hello", kwarg2=[0, 1], kwarg3=1410)
    not_iodata = DenseTwoIndex(nbasis=1, label="kwarg3")
    assert unmask("kwarg3", iodata) == 1410
    assert isinstance(unmask("kwarg3", iodata, not_iodata), DenseTwoIndex)


orb_a1 = DenseOrbital(nbasis=20, nfn=20)
orb_b1 = DenseOrbital(nbasis=30, nfn=30)
orb_a2 = DenseOrbital(nbasis=23, nfn=23)
orb_b2 = DenseOrbital(nbasis=33, nfn=33)
iodata = IOData(orb_a=orb_a2, orb_b=orb_b2)

test_unmask_cases = [
    ((orb_a1,), {}, {"orb1": orb_a1, "len": 1}),
    ((orb_a1, orb_b1), {}, {"orb1": orb_a1, "orb2": orb_b1, "len": 2}),
    ((orb_b1, orb_a1), {}, {"orb1": orb_b1, "orb2": orb_a1, "len": 2}),
    (
        (),
        {"orb_a": orb_a1, "orb_b": orb_b1},
        {"orb1": orb_a1, "orb2": orb_b1, "len": 2},
    ),
    ((orb_a1,), {"orb_a": orb_a2}, {"orb1": orb_a2, "len": 1}),
    ((orb_a1, orb_b1), {"orb_a": orb_a2}, {"orb1": orb_a2, "len": 1}),
    (
        (orb_a1,),
        {"orb_a": orb_a2, "orb_b": orb_b2},
        {"orb1": orb_a2, "orb_b": orb_b2, "len": 2},
    ),
    ((iodata,), {}, {"orb1": orb_a2, "orb2": orb_b2, "len": 2}),
    ((iodata, orb_a1), {}, {"orb1": orb_a1, "len": 1}),
    ((iodata,), {"orb_a": orb_a1}, {"orb1": orb_a1, "len": 1}),
]


@pytest.mark.parametrize("args, kwargs, result", test_unmask_cases)
def test_unmask_orb(args, kwargs, result):

    assert unmask_orb(*args, **kwargs)[0] == result["orb1"]
    assert len(unmask_orb(*args, **kwargs)) == result["len"]
    if hasattr(result, "orb2"):
        assert unmask_orb(*args, **kwargs)[1] == result["orb2"]


test_cases = [
    ("chplus", [0.0, 0.0, 0.0]),
    ("nh3", [0.0, 0.0, -0.3089891187736095]),
]


@pytest.mark.parametrize("mol, ref", test_cases)
def test_get_com(mol, ref):
    fn = context.get_fn(f"test/{mol}.xyz")
    mol = IOData.from_file(fn)
    com = get_com(mol)

    assert (abs(com - ref) < 1e-6).all()


lf_dense = DenseLinalgFactory(5)
lf_chol = CholeskyLinalgFactory(5)
ind_dense = lf_dense.create_four_index()
ind_chol = lf_chol.create_four_index(nvec=10)

test_cases_lf_pass = [
    (lf_dense, ind_dense),
    (lf_chol, ind_chol),
]

test_cases_lf_raise = [
    (lf_chol, ind_dense),
    (lf_dense, ind_chol),
]


@pytest.mark.parametrize("lf, operand", test_cases_lf_pass)
def test_check_lf_pass(lf, operand):
    check_lf(lf, operand)


@pytest.mark.parametrize("lf, operand", test_cases_lf_raise)
def test_check_lf_raise(lf, operand):
    with pytest.raises(ArgumentError):
        check_lf(lf, operand)
