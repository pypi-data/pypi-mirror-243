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
#


from pybest.context import context
from pybest.gbasis.gobasis import (
    compute_cholesky_eri,
    compute_eri,
    compute_kinetic,
    compute_nuclear,
    compute_nuclear_repulsion,
    compute_overlap,
    get_gobasis,
)
from pybest.ip_eom.xip_pccd import RDIPpCCD, RIPpCCD
from pybest.linalg import CholeskyLinalgFactory, DenseLinalgFactory
from pybest.occ_model import AufbauOccModel
from pybest.wrappers import RHF


class Molecule:
    def __init__(self, molfile, basis, lf_cls, **kwargs):
        fn = context.get_fn(f"test/{molfile}.xyz")
        self.obasis = get_gobasis(basis, fn, print_basis=False)
        #
        # Define Occupation model, expansion coefficients and overlap
        #
        self.lf = lf_cls(self.obasis.nbasis)
        self.occ_model = AufbauOccModel(self.obasis, **kwargs)
        self.orb = [self.lf.create_orbital(self.obasis.nbasis)]
        self.olp = compute_overlap(self.obasis)
        #
        # Construct Hamiltonian
        #
        kin = compute_kinetic(self.obasis)
        na = compute_nuclear(self.obasis)
        if isinstance(self.lf, CholeskyLinalgFactory):
            er = compute_cholesky_eri(self.obasis, threshold=1e-8)
        elif isinstance(self.lf, DenseLinalgFactory):
            er = compute_eri(self.obasis)
        external = compute_nuclear_repulsion(self.obasis)

        self.hamiltonian = [kin, na, er, external]
        self.one = kin.copy()
        self.one.iadd(na)
        self.two = er

        self.hf = None
        self.pccd = None
        self.ip_pccd = None
        self.dip_pccd = None
        self.args = (self.olp, *self.orb, *self.hamiltonian, self.t_p)

    @property
    def t_p(self):
        if self.pccd is None:
            no, nv = self.occ_model.nacto[0], self.occ_model.nactv[0]
            return self.lf.create_two_index(no, nv, label="t_p")
        return self.pccd.t_p

    def do_rhf(self):
        """Do RHF optimization"""
        hf = RHF(self.lf, self.occ_model)
        self.hf = hf(*self.hamiltonian, self.olp, *self.orb)

    def do_pccd(self, pccd_cls, **kwargs):
        """Do pCCD optimization based on input class pccd_cls using this class'
        RHF solution
        """
        if self.hf is None:
            raise ValueError("No RHF solution found.")
        pccd = pccd_cls(self.lf, self.occ_model)
        self.pccd = pccd(*self.hamiltonian, self.hf, **kwargs)

    def do_ip_pccd(self, alpha, nroot, nhole):
        """Do IPpCCD optimization based on input class pccd_cls using this
        class' pCCD solution
        """
        if self.pccd is None:
            raise ValueError("No pCCD solution found.")
        ippccd = RIPpCCD(self.lf, self.occ_model, alpha=alpha)
        self.ip_pccd = ippccd(
            *self.hamiltonian, self.pccd, nroot=nroot, nhole=nhole
        )

    def do_dip_pccd(self, alpha, nroot, nhole):
        """Do DIPpCCD optimization based on input class pccd_cls using this
        class' pCCD solution
        """
        if self.pccd is None:
            raise ValueError("No pCCD solution found.")
        dippccd = RDIPpCCD(self.lf, self.occ_model, alpha=alpha)
        self.dip_pccd = dippccd(
            *self.hamiltonian,
            self.pccd,
            nroot=nroot,
            nhole=nhole,
            nguessv=nroot * 10,
        )
