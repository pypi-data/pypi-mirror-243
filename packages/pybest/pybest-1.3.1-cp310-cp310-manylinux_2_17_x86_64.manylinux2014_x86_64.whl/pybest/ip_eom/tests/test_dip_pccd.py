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

from pybest.context import context
from pybest.geminals import ROOpCCD, RpCCD
from pybest.ip_eom.dip_pccd0 import RDIPpCCD0
from pybest.ip_eom.dip_pccd2 import RDIPpCCD2
from pybest.ip_eom.dip_pccd4 import RDIPpCCD4
from pybest.ip_eom.tests.common import Molecule
from pybest.ip_eom.xip_pccd import RDIPpCCD
from pybest.linalg import DenseLinalgFactory
from pybest.occ_model import AufbauOccModel

testdata_class = [(RDIPpCCD0, 0), (RDIPpCCD2, 2), (RDIPpCCD4, 4)]


@pytest.mark.parametrize("cls, alpha", testdata_class)
def test_class_instance_dippccd(cls, alpha):
    """Check whether alpha keyword generates proper instance of class."""
    # some preliminaries
    lf = DenseLinalgFactory(10)
    occ_model = AufbauOccModel(lf, nel=8)
    # Initialize empty class
    ipcc = RDIPpCCD(lf, occ_model, alpha=alpha)

    assert isinstance(ipcc, cls)


#
# Test dimension
#

test_data_dim = [
    # nbasis, nhole, nocc, kwargs, expected
    (10, 2, 2, {"ncore": 0, "alpha": 0}, 4),
    (10, 3, 2, {"ncore": 0, "alpha": 0}, 36),
    (10, 2, 2, {"ncore": 0, "alpha": 2}, 1),
    (10, 3, 2, {"ncore": 0, "alpha": 2}, 17),
    (10, 3, 2, {"ncore": 0, "alpha": 4}, 0),
    (10, 2, 2, {"ncore": 1, "alpha": 0}, 1),
    (10, 3, 2, {"ncore": 1, "alpha": 0}, 1),
    (10, 2, 2, {"ncore": 1, "alpha": 2}, 0),
    (10, 3, 2, {"ncore": 1, "alpha": 2}, 0),
    (10, 3, 2, {"ncore": 1, "alpha": 4}, 0),
    (10, 2, 4, {"ncore": 0, "alpha": 0}, 16),
    (10, 3, 4, {"ncore": 0, "alpha": 0}, 304),
    (10, 2, 4, {"ncore": 0, "alpha": 2}, 6),
    (10, 3, 4, {"ncore": 0, "alpha": 2}, 174),
    (10, 3, 4, {"ncore": 0, "alpha": 4}, 24),
    (10, 2, 4, {"ncore": 1, "alpha": 0}, 9),
    (10, 3, 4, {"ncore": 1, "alpha": 0}, 117),
    (10, 2, 4, {"ncore": 1, "alpha": 2}, 3),
    (10, 3, 4, {"ncore": 1, "alpha": 2}, 63),
    (10, 3, 4, {"ncore": 1, "alpha": 4}, 6),
    (10, 2, 8, {"ncore": 0, "alpha": 0}, 64),
    (10, 3, 8, {"ncore": 0, "alpha": 0}, 960),
    (10, 2, 8, {"ncore": 0, "alpha": 2}, 28),
    (10, 3, 8, {"ncore": 0, "alpha": 2}, 588),
    (10, 3, 8, {"ncore": 0, "alpha": 4}, 112),
]


@pytest.mark.parametrize("nbasis,nhole,nocc,kwargs,expected", test_data_dim)
def test_dip_pccd_dimension(nbasis, nhole, nocc, kwargs, expected):
    """Test number of unkowns (CI coefficients) for various parameter sets
    (alpha, ncore, nocc)
    """
    # Create DIPpCCD instance
    lf = DenseLinalgFactory(nbasis)
    occ_model = AufbauOccModel(lf, nel=nocc * 2, ncore=kwargs.get("ncore"))
    dippccd = RDIPpCCD(lf, occ_model, **kwargs)
    # overwrite private attribute
    dippccd._nhole = nhole

    assert expected == dippccd.dimension


#
# Test unmask function
#

test_unmask = [
    # everything should be fine
    {"alpha": 0},
    {"alpha": 2},
    {"alpha": 4},
]


@pytest.mark.parametrize("kwargs", test_unmask)
def test_ip_pccd_unmask(kwargs, c_2m):
    """Test unmask_arg function by passing proper arguments"""
    # Create DIPpCCD instance
    dippccd = RDIPpCCD(c_2m.lf, c_2m.occ_model, **kwargs)

    # we do not need to check the arrays, just the objects
    assert dippccd.unmask_args(*c_2m.args) == (c_2m.one, c_2m.two, c_2m.orb[0])


#
# Test effective Hamiltonian (only initialization)
#

# h_alpha_nhole:
h_0_2 = {"fock", "x1im", "goovv", "goooo"}
h_0_3 = {
    "fock",
    "x1im",
    "goovv",
    "goooo",
    "x1cd",
    "gooov",
    "xjkcm",
    "xkcmd",
    "xkcMD",
    "xjcmD",
    "xjkmN",
    "xikcm",
}
h_2_2 = {"fock", "x1im", "goooo"}
h_2_3 = {
    "fock",
    "x1im",
    "goooo",
    "goovv",
    "x1cd",
    "gooov",
    "xjkcm",
    "xkcmd",
    "xkcMD",
    "xjcmD",
    "xjkmN",
}
h_4_3 = {"fock", "x1im", "x1cd", "goooo", "x2kcmd"}

test_set_hamiltonian = [
    # molecule instance, nparticle, alpha, expected
    (2, {"alpha": 0}, h_0_2),
    (2, {"alpha": 2}, h_2_2),
    (3, {"alpha": 0}, h_0_3),
    (3, {"alpha": 2}, h_2_3),
    (3, {"alpha": 4}, h_4_3),
]


@pytest.mark.parametrize("nhole,kwargs,expected", test_set_hamiltonian)
def test_dip_pccd_set_hamiltonian(nhole, kwargs, expected, c_2m):
    """Test if effective Hamiltonian has been constructed at all. We do not
    test the actual elements.
    """
    # Create DIPpCCD instance
    dippccd = RDIPpCCD(c_2m.lf, c_2m.occ_model, **kwargs)
    # set some class attributes
    dippccd.unmask_args(c_2m.t_p, c_2m.olp, *c_2m.orb, *c_2m.hamiltonian)
    dippccd._nhole = nhole

    # we do not need to check the arrays, just the objects
    # we need to copy the arrays as they get deleted
    one, two = c_2m.one.copy(), c_2m.two.copy()
    dippccd.set_hamiltonian(c_2m.one, c_2m.two)
    c_2m.one, c_2m.two = one, two

    # Check if cache instance contains all relevant terms
    assert dippccd.cache._store.keys() == expected, "Cache element not found"
    # Check loading from cache
    for h_eff in expected:
        assert dippccd.from_cache(h_eff), "Loading from cache unsuccesful"


test_dump_cache = [
    # molecule instance, nparticle, alpha, expected
    ({"alpha": 0}, "goovv"),
    ({"alpha": 0}, "xkcmd"),
    ({"alpha": 0}, "xjcmD"),
    ({"alpha": 0}, "xkcMD"),
    ({"alpha": 2}, "goovv"),
    ({"alpha": 2}, "xkcmd"),
    ({"alpha": 2}, "xjcmD"),
    ({"alpha": 2}, "xkcMD"),
    ({"alpha": 4}, "x2kcmd"),
]


@pytest.mark.parametrize("kwargs,cache_item", test_dump_cache)
def test_dip_pccd_dump_cache(kwargs, cache_item, c_2m):
    """Test if effective Hamiltonian is dumped to disk."""
    # Create DIPpCCD instance
    dippccd = RDIPpCCD(c_2m.lf, c_2m.occ_model, **kwargs)
    # set some class attributes explicitly as they are set during function call
    dippccd.unmask_args(c_2m.t_p, c_2m.olp, *c_2m.orb, *c_2m.hamiltonian)
    dippccd._nhole = 3
    dippccd._dump_cache = True

    # we need to copy the arrays as they get deleted
    one, two = c_2m.one.copy(), c_2m.two.copy()
    dippccd.set_hamiltonian(one, two)

    # Check if cache has been dumped properly
    # We need to access _store directly as otherwise the load function of the
    # Cache class is called and test will fail by construction
    assert not hasattr(
        dippccd.cache._store[cache_item], "_array"
    ), f"Cache element {cache_item} not properly dumped to disk"


@pytest.mark.parametrize("kwargs,cache_item", test_dump_cache)
def test_dip_pccd_load_dump_cache(kwargs, cache_item, c_2m):
    """Test if effective Hamiltonian is loaded and dumped again to disk."""
    # Create DIPpCCD instance
    dippccd = RDIPpCCD(c_2m.lf, c_2m.occ_model, **kwargs)
    # set some class attributes explicitly as they are set during function call
    dippccd.unmask_args(c_2m.t_p, c_2m.olp, *c_2m.orb, *c_2m.hamiltonian)
    dippccd._nhole = 3
    dippccd._dump_cache = True

    # we need to copy the arrays as they get deleted
    one, two = c_2m.one.copy(), c_2m.two.copy()
    dippccd.set_hamiltonian(one, two)

    # First load arryas again and check if present
    assert hasattr(
        dippccd.cache[cache_item], "_array"
    ), f"Cache element {cache_item} not properly loaded from disk"

    # Dump again, so cache item should not be present
    dippccd.cache.dump(cache_item)
    assert not hasattr(
        dippccd.cache._store[cache_item], "_array"
    ), f"Cache element {cache_item} not properly dumped to disk"


test_data_dip = [
    (
        RpCCD,
        "c",
        "cc-pvdz",
        {"ncore": 0, "charge": -2, "alpha": 0, "nroot": 4, "nhole": 3},
        {},
        {
            "e_tot": -37.181350747097,
            "e_ip_0": [
                -5.403875e-01,
                -4.853248e-01,
                -4.851959e-01,
                -4.643491e-01,
            ],
            "orbfile": "c_rhf.txt",
        },
    ),
    (
        RpCCD,
        "c",
        "cc-pvdz",
        {"ncore": 0, "charge": -2, "alpha": 2, "nroot": 4, "nhole": 3},
        {},
        {
            "e_tot": -37.181350747097,
            "e_ip_2": [
                -5.403875e-01,
                -4.643491e-01,
                -4.643491e-01,
                -2.845116e-01,
            ],
            "orbfile": "c_rhf.txt",
        },
    ),
    (
        RpCCD,
        "c",
        "cc-pvdz",
        {"ncore": 0, "charge": -2, "alpha": 4, "nroot": 4, "nhole": 3},
        {},
        {
            "e_tot": -37.181350747097,
            "e_ip_4": [
                -2.845116e-01,
                3.529028e-01,
                3.529028e-01,
                4.781519e-01,
                4.961400e-01,
            ],
            "orbfile": "c_rhf.txt",
        },
    ),
    (
        RpCCD,
        "c",
        "cc-pvdz",
        {"ncore": 1, "charge": -2, "alpha": 0, "nroot": 4, "nhole": 3},
        {},
        {
            "e_tot": -37.181056931067,
            "e_ip_0": [
                -5.401817e-01,
                -4.851401e-01,
                -4.850112e-01,
                -4.643028e-01,
            ],
            "orbfile": "c_rhf.txt",
        },
    ),
    (
        RpCCD,
        "c",
        "cc-pvdz",
        {"ncore": 1, "charge": -2, "alpha": 2, "nroot": 4, "nhole": 3},
        {},
        {
            "e_tot": -37.181056931067,
            "e_ip_2": [
                -5.401817e-01,
                -4.643028e-01,
                -4.643028e-01,
                -2.844379e-01,
            ],
            "orbfile": "c_rhf.txt",
        },
    ),
    (
        ROOpCCD,
        "c",
        "cc-pvdz",
        {"ncore": 0, "charge": -2, "alpha": 0, "nroot": 4, "nhole": 3},
        {"sort": False},
        {
            "e_tot": -37.194223264348,
            "e_ip_0": [
                -5.264451e-01,
                -4.749906e-01,
                -4.538110e-01,
                -4.538110e-01,
            ],
            "orbfile": "c_oopccd.txt",
        },
    ),
    (
        ROOpCCD,
        "c",
        "cc-pvdz",
        {"ncore": 0, "charge": -2, "alpha": 2, "nroot": 4, "nhole": 3},
        {"sort": False},
        {
            "e_tot": -37.194223264348,
            "e_ip_2": [
                -5.264451e-01,
                -4.538110e-01,
                -4.538110e-01,
                -2.749086e-01,
            ],
            "orbfile": "c_oopccd.txt",
        },
    ),
    (
        ROOpCCD,
        "c",
        "cc-pvdz",
        {"ncore": 0, "charge": -2, "alpha": 4, "nroot": 5, "nhole": 3},
        {"sort": False},
        {
            "e_tot": -37.194223264348,
            "e_ip_4": [
                -2.749087e-01,
                3.644533e-01,
                3.644533e-01,
                4.870770e-01,
                5.050943e-01,
            ],
            "orbfile": "c_oopccd.txt",
        },
    ),
]


@pytest.mark.parametrize(
    "cls, mol_f, basis, kwargs, kwargs_pccd, expected", test_data_dip
)
def test_dip_pccd(cls, mol_f, basis, kwargs, kwargs_pccd, expected, linalg):
    """Test attachement energies of DIPpCCD models"""
    ncore = kwargs.get("ncore")
    charge = kwargs.get("charge")
    alpha = kwargs.get("alpha")
    nroot = kwargs.get("nroot")
    nhole = kwargs.get("nhole")
    # Prepare molecule
    mol_ = Molecule(mol_f, basis, linalg, ncore=ncore, charge=charge)
    # Do RHF optimization:
    mol_.do_rhf()
    # overwrite orbitals (pCCD convergence speed up)
    fn_orb = context.get_fn(f"test/{expected['orbfile']}")
    mol_.hf.orb_a.coeffs[:] = np.fromfile(fn_orb, sep=",").reshape(
        mol_.obasis.nbasis, mol_.obasis.nbasis
    )
    # Do pCCD optimization:
    mol_.do_pccd(cls, **kwargs_pccd)
    assert abs(mol_.pccd.e_tot - expected["e_tot"]) < 1e-6
    # Do DIPpCCD optimization:
    mol_.do_dip_pccd(alpha, nroot, nhole)

    for ind in range(nroot):
        # get proper key (e_ip_0 or e_ip_2 or e_ip_4)
        (key,) = [key for key in expected if "e_ip" in key.lower()]
        assert (
            abs(getattr(mol_.dip_pccd, key)[ind] - expected[key][ind]) < 5e-6
        )
