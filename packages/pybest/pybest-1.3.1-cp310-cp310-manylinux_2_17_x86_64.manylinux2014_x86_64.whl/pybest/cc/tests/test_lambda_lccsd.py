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

import pybest.gbasis.gobasis as pybest_basis
from pybest.cc import RLCCD, RLCCSD, RpCCDLCCD, RpCCDLCCSD
from pybest.context import context
from pybest.gbasis import get_gobasis
from pybest.gbasis.gobasis import (
    compute_cholesky_eri,
    compute_eri,
    compute_kinetic,
    compute_nuclear,
    compute_nuclear_repulsion,
    compute_overlap,
)
from pybest.geminals.roopccd import ROOpCCD
from pybest.linalg import DenseLinalgFactory
from pybest.linalg.cholesky import CholeskyLinalgFactory
from pybest.occ_model import AufbauOccModel
from pybest.utils import fda_1order, numpy_seed
from pybest.wrappers.hf import RHF

scalingfactor = 5e-7


@pytest.mark.slow
def test_rhflccd_lambda():
    """Perform a finite difference test of the Lambda equations. The finite
    difference approximation of sum function ``fun`` is compared to the analytical
    derivative defined in ``fun_deriv``.
    """
    fn_xyz = context.get_fn("test/c2-12.xyz")
    obasis = get_gobasis("cc-pvdz", fn_xyz, print_basis=False)
    lf = DenseLinalgFactory(obasis.nbasis)
    occ_model = AufbauOccModel(obasis)
    orb = lf.create_orbital(obasis.nbasis)
    olp = compute_overlap(obasis)
    kin = compute_kinetic(obasis)
    ne = compute_nuclear(obasis)
    external = {"nn": compute_nuclear_repulsion(obasis)}

    eri = compute_eri(obasis)

    one = lf.create_two_index(obasis.nbasis, label="one")
    one.iadd(kin)
    one.iadd(ne)

    rhf = RHF(lf, occ_model)
    rhf_output = rhf(kin, ne, eri, external, orb, olp)

    lccd_solver = RLCCD(lf, occ_model)
    with numpy_seed():
        lccd_solver(
            one,
            eri.copy(),
            rhf_output,
            tco="td",
            lambda_equations=True,
            threshold_r=1e-6,
        )
        lccd_solver.l_amplitudes["l_2"].assign(np.random.rand(6, 22, 6, 22))
        # Symmetrize
        lccd_solver.l_amplitudes["l_2"].iadd_transpose((2, 3, 0, 1))
        lccd_solver.l_amplitudes["l_2"].iscale(0.5)
        xt2 = lccd_solver.amplitudes["t_2"].get_triu().ravel(order="C")

        def fun(x):
            l2 = lccd_solver.l_amplitudes["l_2"].get_triu().ravel(order="C")
            x_ = lccd_solver.unravel(x)

            lagrangian = lccd_solver.calculate_energy(rhf_output.e_tot, **x_)[
                "e_tot"
            ]
            lagrangian += np.dot(l2, lccd_solver.vfunction(x.ravel(order="C")))
            return lagrangian

        def fun_deriv(x):
            l2 = lccd_solver.l_amplitudes["l_2"].get_triu().ravel(order="C")

            gradient = lccd_solver.vfunction_l(l2)
            return gradient

        x = xt2
        dx2 = []
        for i in range(5):
            tmp = np.random.rand(6, 22, 6, 22) * scalingfactor
            tmp[:] = tmp + tmp.transpose((2, 3, 0, 1))
            indtriu = np.triu_indices(6 * 22)
            tmp = tmp.reshape(6 * 22, 6 * 22)[indtriu]
            dx2.append(tmp.ravel())
        dx2 = np.array(dx2)
        dxs = dx2
        # recalculate auxiliary matrices because they are deleted after call function exists
        lccd_solver.set_hamiltonian(one, eri, orb)
        fda_1order(fun, fun_deriv, x, dxs)


@pytest.mark.slow
def test_lccsd_rhf_lambda():
    """Perform a finite difference test of the Lambda equations. The finite
    difference approximation of sum function ``fun`` is compared to the analytical
    derivative defined in ``fun_deriv``.
    """
    fn_xyz = context.get_fn("test/c2-12.xyz")
    obasis = get_gobasis("cc-pvdz", fn_xyz, print_basis=False)
    lf = DenseLinalgFactory(obasis.nbasis)
    occ_model = AufbauOccModel(obasis)
    orb = lf.create_orbital(obasis.nbasis)
    olp = compute_overlap(obasis)
    kin = compute_kinetic(obasis)
    ne = compute_nuclear(obasis)
    external = {"nn": compute_nuclear_repulsion(obasis)}

    eri = compute_eri(obasis)

    one = lf.create_two_index(obasis.nbasis, label="one")
    one.iadd(kin)
    one.iadd(ne)

    rhf = RHF(lf, occ_model)
    rhf_ = rhf(kin, ne, eri, external, orb, olp)

    lccsd_solver = RLCCSD(lf, occ_model)
    with numpy_seed():
        _ = lccsd_solver(one, eri, rhf_, tco="td", lambda_equations=True)
        lccsd_solver.l_amplitudes["l_1"].assign(np.random.rand(6, 22))
        lccsd_solver.l_amplitudes["l_2"].assign(np.random.rand(6, 22, 6, 22))
        # Symmetrize
        lccsd_solver.l_amplitudes["l_2"].iadd_transpose((2, 3, 0, 1))
        lccsd_solver.l_amplitudes["l_2"].iscale(0.5)
        xt1 = lccsd_solver.amplitudes["t_1"]._array.ravel(order="C")
        xt2 = lccsd_solver.amplitudes["t_2"].get_triu().ravel(order="C")

        def fun(x):
            l1 = lccsd_solver.l_amplitudes["l_1"]._array.ravel(order="C")
            l2 = lccsd_solver.l_amplitudes["l_2"].get_triu().ravel(order="C")
            coeff = np.hstack((l1, l2))
            x_ = lccsd_solver.unravel(coeff)

            lagrangian = lccsd_solver.calculate_energy(rhf_.e_tot, **x_)[
                "e_tot"
            ]

            lagrangian += np.dot(
                coeff, lccsd_solver.vfunction(x.ravel(order="C"))
            )
            return lagrangian

        def fun_deriv(x):
            l1 = lccsd_solver.l_amplitudes["l_1"]._array.ravel(order="C")
            l2 = lccsd_solver.l_amplitudes["l_2"].get_triu().ravel(order="C")
            coeff = np.hstack((l1, l2)).ravel(order="C")
            t1 = lccsd_solver.lf.create_two_index(6, 22)
            t2 = lccsd_solver.lf.create_four_index(6, 22, 6, 22)
            t1.assign(x[: 6 * 22])
            t2.assign_triu(x[6 * 22 :])

            gradient = lccsd_solver.vfunction_l(coeff)
            return gradient.ravel(order="C")

        x = np.hstack((xt1, xt2))
        dx1 = np.random.rand(5, (6 * 22)) * scalingfactor
        dx2 = []
        for i in range(5):
            tmp = np.random.rand(6, 22, 6, 22) * scalingfactor
            tmp[:] = tmp + tmp.transpose((2, 3, 0, 1))
            indtriu = np.triu_indices(6 * 22)
            tmp = tmp.reshape(6 * 22, 6 * 22)[indtriu]
            dx2.append(tmp.ravel())
        dx2 = np.array(dx2)
        dxs = np.hstack((dx1, dx2))
        # recalculate auxiliary matrices because they are deleted after call function exists
        lccsd_solver.set_hamiltonian(one, eri, orb)
        fda_1order(fun, fun_deriv, x, dxs)


@pytest.mark.slow
def test_lccd_lambda():
    """Perform a finite difference test of the Lambda equations. The finite
    difference approximation of sum function ``fun`` is compared to the analytical
    derivative defined in ``fun_deriv``.
    """
    fn_xyz = context.get_fn("test/c2_30.xyz")
    obasis = get_gobasis("cc-pvdz", fn_xyz, print_basis=False)
    lf = DenseLinalgFactory(obasis.nbasis)
    occ_model = AufbauOccModel(obasis)
    olp = compute_overlap(obasis)
    kin = compute_kinetic(obasis)
    ne = compute_nuclear(obasis)
    external = {"nn": compute_nuclear_repulsion(obasis)}

    eri = compute_eri(obasis)

    one = lf.create_two_index(obasis.nbasis, label="one")
    one.iadd(kin)
    one.iadd(ne)

    fn_orb = context.get_fn("test/ap1rog_c2_30.txt")
    orb_ = np.fromfile(fn_orb, sep=",").reshape(obasis.nbasis, obasis.nbasis)
    orb_a = lf.create_orbital(obasis.nbasis)
    orb_a._coeffs = orb_
    # Do AP1roG optimization:
    geminal_solver = ROOpCCD(lf, occ_model)
    lccd_solver = RpCCDLCCD(lf, occ_model)
    with numpy_seed():
        ap1rog = geminal_solver(
            one,
            eri,
            orb_a,
            olp,
            e_core=external["nn"],
            checkpoint=-1,
            maxiter={"orbiter": 0},
        )
        _ = lccd_solver(one, eri, ap1rog, tco="td", lambda_equations=True)
        lccd_solver.l_amplitudes["l_2"].assign(np.random.rand(6, 22, 6, 22))
        # Symmetrize
        lccd_solver.l_amplitudes["l_2"].iadd_transpose((2, 3, 0, 1))
        lccd_solver.l_amplitudes["l_2"].iscale(0.5)
        xt2 = lccd_solver.amplitudes["t_2"].get_triu().ravel(order="C")
        ind1, ind2 = np.indices((6, 22))
        indices = [ind1, ind2, ind1, ind2]
        # Get rid of pairs
        lccd_solver.l_amplitudes["l_2"].assign(0.0, indices)

        def fun(x):
            l2 = lccd_solver.l_amplitudes["l_2"].get_triu().ravel(order="C")
            x_ = lccd_solver.unravel(x)

            lagrangian = lccd_solver.calculate_energy(lccd_solver.e_ref, **x_)[
                "e_tot"
            ]
            lagrangian += np.dot(
                l2,
                lccd_solver.vfunction(x.ravel(order="C")),
            )
            return lagrangian

        def fun_deriv(x):
            l2 = lccd_solver.l_amplitudes["l_2"].get_triu().ravel(order="C")

            gradient = lccd_solver.vfunction_l(l2)
            return gradient.ravel(order="C")

        x = xt2
        dx2 = []
        for i in range(5):
            tmp = np.random.rand(6, 22, 6, 22) * scalingfactor
            tmp[:] = tmp + tmp.transpose((2, 3, 0, 1))
            tmp[tuple(indices)] = 0.0
            indtriu = np.triu_indices(6 * 22)
            tmp = tmp.reshape(6 * 22, 6 * 22)[indtriu]
            dx2.append(tmp.ravel())
        dx2 = np.array(dx2)
        dxs = dx2
        # recalculate auxiliary matrices because they are deleted after call function exists
        lccd_solver.set_hamiltonian(one, eri, orb_a)
        fda_1order(fun, fun_deriv, x, dxs)


@pytest.mark.slow
def test_lccsd_lambda():
    """Perform a finite difference test of the Lambda equations. The finite
    difference approximation of sum function ``fun`` is compared to the analytical
    derivative defined in ``fun_deriv``.
    """
    fn_xyz = context.get_fn("test/c2_30.xyz")
    obasis = get_gobasis("cc-pvdz", fn_xyz, print_basis=False)
    lf = DenseLinalgFactory(obasis.nbasis)
    occ_model = AufbauOccModel(obasis)
    olp = compute_overlap(obasis)
    kin = compute_kinetic(obasis)
    ne = compute_nuclear(obasis)
    external = {"nn": compute_nuclear_repulsion(obasis)}

    eri = compute_eri(obasis)

    one = lf.create_two_index(obasis.nbasis, label="one")
    one.iadd(kin)
    one.iadd(ne)

    fn_orb = context.get_fn("test/ap1rog_c2_30.txt")
    orb_ = np.fromfile(fn_orb, sep=",").reshape(obasis.nbasis, obasis.nbasis)
    orb_a = lf.create_orbital(obasis.nbasis)
    orb_a._coeffs = orb_
    # Do AP1roG optimization:
    geminal_solver = ROOpCCD(lf, occ_model)
    lccsd_solver = RpCCDLCCSD(lf, occ_model)
    with numpy_seed():
        ap1rog = geminal_solver(
            one,
            eri,
            orb_a,
            olp,
            e_core=external["nn"],
            checkpoint=-1,
            maxiter={"orbiter": 0},
        )
        _ = lccsd_solver(
            one, eri, ap1rog, tco="td", lambda_equations=True, threshold_r=1e-6
        )
        lccsd_solver.l_amplitudes["l_1"].assign(np.random.rand(6, 22))
        lccsd_solver.l_amplitudes["l_2"].assign(np.random.rand(6, 22, 6, 22))
        # Symmetrize
        lccsd_solver.l_amplitudes["l_2"].iadd_transpose((2, 3, 0, 1))
        lccsd_solver.l_amplitudes["l_2"].iscale(0.5)
        xt1 = lccsd_solver.amplitudes["t_1"]._array.ravel(order="C")
        xt2 = lccsd_solver.amplitudes["t_2"].get_triu().ravel(order="C")
        ind1, ind2 = np.indices((6, 22))
        indices = [ind1, ind2, ind1, ind2]
        # Get rid of pairs
        lccsd_solver.l_amplitudes["l_2"].assign(0.0, indices)

        def fun(x):
            l1 = lccsd_solver.l_amplitudes["l_1"]._array.ravel(order="C")
            l2 = lccsd_solver.l_amplitudes["l_2"].get_triu().ravel(order="C")
            coeff = np.hstack((l1, l2))
            x_ = lccsd_solver.unravel(coeff)

            lagrangian = lccsd_solver.calculate_energy(
                lccsd_solver.e_ref, **x_
            )["e_tot"]

            lagrangian += np.dot(
                coeff, lccsd_solver.vfunction(x.ravel(order="C"))
            )
            return lagrangian

        def fun_deriv(x):
            l1 = lccsd_solver.l_amplitudes["l_1"]._array.ravel(order="C")
            l2 = lccsd_solver.l_amplitudes["l_2"].get_triu().ravel(order="C")
            coeff = np.hstack((l1, l2)).ravel(order="C")
            t1 = lccsd_solver.lf.create_two_index(6, 22)
            t2 = lccsd_solver.lf.create_four_index(6, 22, 6, 22)
            t1.assign(x[: 6 * 22])
            t2.assign_triu(x[6 * 22 :])

            gradient = lccsd_solver.vfunction_l(coeff)
            return gradient.ravel(order="C")

        x = np.hstack((xt1, xt2))
        dx1 = np.random.rand(5, (6 * 22)) * scalingfactor
        dx2 = []
        for i in range(5):
            tmp = np.random.rand(6, 22, 6, 22) * scalingfactor
            tmp[:] = tmp + tmp.transpose((2, 3, 0, 1))
            tmp[tuple(indices)] = 0.0
            indtriu = np.triu_indices(6 * 22)
            tmp = tmp.reshape(6 * 22, 6 * 22)[indtriu]
            dx2.append(tmp.ravel())
        dx2 = np.array(dx2)
        dxs = np.hstack((dx1, dx2))
        # recalculate auxiliary matrices because they are deleted after call function exists
        lccsd_solver.set_hamiltonian(one, eri, orb_a)
        fda_1order(fun, fun_deriv, x, dxs)


@pytest.mark.skipif(
    not pybest_basis.PYBEST_CHOLESKY_ENABLED,
    reason="Cholesky-decomposition ERI are not available. Build libchol and re-run build --enable-cholesky",
)
@pytest.mark.slow
def test_lccsd_chol_lambda():
    """Perform a finite difference test of the Lambda equations. The finite
    difference approximation of sum function ``fun`` is compared to the analytical
    derivative defined in ``fun_deriv``.
    """
    fn_xyz = context.get_fn("test/c2_30.xyz")
    obasis = get_gobasis("cc-pvdz", fn_xyz, print_basis=False)
    lf = CholeskyLinalgFactory(obasis.nbasis)
    occ_model = AufbauOccModel(obasis)
    olp = compute_overlap(obasis)
    kin = compute_kinetic(obasis)
    ne = compute_nuclear(obasis)
    external = {"nn": compute_nuclear_repulsion(obasis)}

    eri = compute_cholesky_eri(obasis)

    one = lf.create_two_index(obasis.nbasis, label="one")
    one.iadd(kin)
    one.iadd(ne)

    fn_orb = context.get_fn("test/ap1rog_c2_30.txt")
    orb_ = np.fromfile(fn_orb, sep=",").reshape(obasis.nbasis, obasis.nbasis)
    orb_a = lf.create_orbital(obasis.nbasis)
    orb_a._coeffs = orb_
    # Do AP1roG optimization:
    geminal_solver = ROOpCCD(lf, occ_model)
    lccsd_solver = RpCCDLCCSD(lf, occ_model)
    with numpy_seed():
        ap1rog = geminal_solver(
            one,
            eri,
            orb_a,
            olp,
            e_core=external["nn"],
            checkpoint=-1,
            maxiter={"orbiter": 0},
        )
        _ = lccsd_solver(
            one, eri, ap1rog, tco="td", lambda_equations=True, threshold_r=1e-6
        )
        lccsd_solver.l_amplitudes["l_1"].assign(np.random.rand(6, 22))
        lccsd_solver.l_amplitudes["l_2"].assign(np.random.rand(6, 22, 6, 22))
        # Symmetrize
        lccsd_solver.l_amplitudes["l_2"].iadd_transpose((2, 3, 0, 1))
        lccsd_solver.l_amplitudes["l_2"].iscale(0.5)
        xt1 = lccsd_solver.amplitudes["t_1"]._array.ravel(order="C")
        xt2 = lccsd_solver.amplitudes["t_2"].get_triu().ravel(order="C")
        ind1, ind2 = np.indices((6, 22))
        indices = [ind1, ind2, ind1, ind2]
        # Get rid of pairs
        lccsd_solver.l_amplitudes["l_2"].assign(0.0, indices)

        def fun(x):
            l1 = lccsd_solver.l_amplitudes["l_1"]._array.ravel(order="C")
            l2 = lccsd_solver.l_amplitudes["l_2"].get_triu().ravel(order="C")
            coeff = np.hstack((l1, l2))
            x_ = lccsd_solver.unravel(coeff)

            lagrangian = lccsd_solver.calculate_energy(
                lccsd_solver.e_ref, **x_
            )["e_tot"]

            lagrangian += np.dot(
                coeff, lccsd_solver.vfunction(x.ravel(order="C"))
            )

            return lagrangian

        def fun_deriv(x):
            l1 = lccsd_solver.l_amplitudes["l_1"]._array.ravel(order="C")
            l2 = lccsd_solver.l_amplitudes["l_2"].get_triu().ravel(order="C")
            coeff = np.hstack((l1, l2)).ravel(order="C")
            t1 = lccsd_solver.lf.create_two_index(6, 22)
            t2 = lccsd_solver.denself.create_four_index(6, 22, 6, 22)
            t1.assign(x[: 6 * 22])
            t2.assign_triu(x[6 * 22 :])

            gradient = lccsd_solver.vfunction_l(coeff)
            return gradient.ravel(order="C")

        x = np.hstack((xt1, xt2))
        dx1 = np.random.rand(5, (6 * 22)) * scalingfactor
        dx2 = []
        for i in range(5):
            tmp = np.random.rand(6, 22, 6, 22) * scalingfactor
            tmp[:] = tmp + tmp.transpose((2, 3, 0, 1))
            tmp[tuple(indices)] = 0.0
            indtriu = np.triu_indices(6 * 22)
            tmp = tmp.reshape(6 * 22, 6 * 22)[indtriu]
            dx2.append(tmp.ravel())
        dx2 = np.array(dx2)
        dxs = np.hstack((dx1, dx2))
        #    recalculate auxiliary matrices because they are deleted after call function exists
        lccsd_solver.set_hamiltonian(one, eri, orb_a)
        fda_1order(fun, fun_deriv, x, dxs)
