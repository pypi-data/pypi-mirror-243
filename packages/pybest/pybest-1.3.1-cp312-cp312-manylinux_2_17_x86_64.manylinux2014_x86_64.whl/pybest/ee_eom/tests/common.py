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

from pybest.context import context
from pybest.gbasis import (
    compute_cholesky_eri,
    compute_eri,
    compute_kinetic,
    compute_nuclear,
    compute_nuclear_repulsion,
    compute_overlap,
    get_gobasis,
)
from pybest.io import IOData, load_fcidump
from pybest.linalg import CholeskyLinalgFactory, DenseLinalgFactory
from pybest.occ_model import AufbauOccModel
from pybest.wrappers import RHF


class Molecule:
    def __init__(self, basis, molfile, **kwargs):
        fn_basis = context.get_fn(basis)
        fn_mol = context.get_fn(molfile)

        obasis = get_gobasis(fn_basis, fn_mol)
        factory = kwargs.pop("factory", CholeskyLinalgFactory)
        self.lf = factory(obasis.nbasis)
        self.dense_lf = DenseLinalgFactory(obasis.nbasis)

        self.occ_model = AufbauOccModel(obasis, **kwargs)

        self.orb_a = self.lf.create_orbital(obasis.nbasis)
        self.olp = compute_overlap(obasis)

        self.kin = compute_kinetic(obasis)
        self.ne = compute_nuclear(obasis)
        if isinstance(self.lf, CholeskyLinalgFactory):
            self.eri = compute_cholesky_eri(obasis, threshold=1e-12)
        else:
            self.eri = compute_eri(obasis)
        self.external = compute_nuclear_repulsion(obasis)
        # combine all Hamiltonian terms
        self.ham = (self.kin, self.ne, self.eri)

        n_o = self.occ_model.nacto[0]
        n_v = self.occ_model.nactv[0]
        t_1 = self.dense_lf.create_two_index(n_o, n_v, label="t_1")
        t_p = self.dense_lf.create_two_index(n_o, n_v, label="t_p")
        t_2 = self.dense_lf.create_four_index(n_o, n_v, n_o, n_v, label="t_2")
        self.t = (t_1, t_2, t_p)

    def do_rhf(self):
        """Do a Hartree-Fock calculation"""
        hf = RHF(self.lf, self.occ_model)
        self.rhf = hf(*self.ham, self.external, self.olp, self.orb_a)


class FromFile:
    def __init__(self, filen, nocc, nbasis, ncore=0, orb=None):
        fn = context.get_fn(filen)
        #
        # Define Occupation model, expansion coefficients and overlap
        #
        self.lf = DenseLinalgFactory(nbasis)
        self.occ_model = AufbauOccModel(self.lf, nel=nocc * 2, ncore=ncore)
        orb_a = self.lf.create_orbital(nbasis)
        olp = self.lf.create_two_index(nbasis, label="olp")
        olp.assign_diagonal(1.0)
        orb_a.assign(olp)
        if orb is not None:
            fn_orb = context.get_fn(orb)
            orb_a.coeffs[:] = np.fromfile(fn_orb, sep=",").reshape(
                nbasis, nbasis
            )
        #
        # Read Hamiltonian from data dir
        #
        integrals = load_fcidump(fn, self.lf)
        self.one = integrals["one"]
        self.eri = integrals["two"]
        core = integrals["e_core"]

        self.iodata = IOData(
            **{"orb_a": orb_a, "olp": olp, "e_core": core, "e_ref": 0.0}
        )
