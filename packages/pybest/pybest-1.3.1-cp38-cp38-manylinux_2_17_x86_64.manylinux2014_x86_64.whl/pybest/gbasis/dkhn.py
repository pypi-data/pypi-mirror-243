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
# Detailed changelog:
#
# This file has been written by Dariusz Kedziera
#
# Detailed changes (see also CHANGELOG):
# 2023-01-16: Additional transoformations, ppcp, for point charges (P. Tecmer)
#
"""Douglas-Kroll-Hess transformation of

    *pVp (standard for DKH)
    *pPCp (needed for external point charges)

    integrals."""


from pybest.constants import alpha
from pybest.gbasis.gobasis import (
    compute_kinetic,
    compute_nuclear,
    compute_overlap,
    compute_point_charges,
    compute_ppcp,
    compute_pvp,
    get_tform_u2c,
)
from pybest.linalg import DenseLinalgFactory
from pybest.log import log
from pybest.utils import check_options

__all__ = [
    "compute_dkh",
]


def compute_components(
    cbasis,
    charges=None,
    s_int=True,
    t_int=True,
    v_int=True,
    pvp_int=True,
):
    """S, T, V, pc, and pVp uncontracted integrals."""
    output = {}
    if s_int:
        olp = compute_overlap(cbasis, uncontract=True)
        output.update({"olp": olp})
    if t_int:
        kin = compute_kinetic(cbasis, uncontract=True)
        output.update({"kin": kin})
    if v_int:
        nuc = compute_nuclear(cbasis, uncontract=True)
        if charges is not None:
            log(
                "Correcting for picture changes due to presence of external charges"
            )
            pc = compute_point_charges(cbasis, charges, uncontract=True)
            nuc.iadd(pc)
        output.update({"nuc": nuc})
    if pvp_int:
        pvp = compute_pvp(cbasis, uncontract=True)
        if charges is not None:
            ppcp = compute_ppcp(cbasis, charges, uncontract=True)
            pvp.iadd(ppcp)
        output.update({"pvp": pvp})
    return output


def compute_dkh(basis, charges=None, order=2):
    """Compute DKH2 hamiltonian (DenseTwoIndex instances)

    **Arguments:**

    :basis: A PyBasis instance. Contains basis set information
    :charges: External charges. Needed for picture change correction
    :order: (int) the order of the DKH transformation (default: 2)
    """
    check_options(order, order, 1, 2)
    #
    # Get olp (s), p_2 (t), nuc (v), and pvp integrals
    #
    ints = compute_components(basis, charges=charges)
    nuc = ints["nuc"]
    pvp = ints["pvp"]
    #
    # Transform to orthonormal basis diagonalising p^2
    #
    transformation_matrices = get_dkh_transformation_matrices(**ints)
    u_ort = transformation_matrices["u_ort"]
    u_back = transformation_matrices["u_back"]
    e_p_2 = transformation_matrices["e_p_2"]
    #
    # Transform nuc (v) and pvp ints
    #
    nuc.itransform(u_ort)
    pvp.itransform(u_ort)
    #
    # Compute all vectors for DKH transformation
    #
    vectors = get_dkh_vectors(e_p_2)
    #
    # The DKH Hamiltonian
    #
    # DKH1
    # E1 = T_p_at_diag + A_k ( V +1/c^2 b_k pVp b_k ) A_k
    #
    dkh = get_dkh_order_1(nuc, pvp, **vectors)
    #
    # DKH2
    # E2 = -0.5 ( Y + Y^T )
    #
    if order >= 2:
        dkh.iadd(get_dkh_order_2(nuc, pvp, **vectors))
    #
    # Back-transformation
    #
    dkh.itransform(u_back, transpose=True)
    #
    # Transform to contracted basis set
    #
    # create new output array
    l_f = DenseLinalgFactory(basis.nbasis)
    output = l_f.create_two_index(basis.nbasis, label="dkh")
    # get transformation matrix
    tform_matrix = get_tform_u2c(basis)
    output.iadd_transform(dkh, tform_matrix, transpose=True)

    return output


def get_dkh_transformation_matrices(**ints):
    """Obtain transformation matrices that diagonalize p^2. The final basis is
    orthonormal.
    This function returns this transformation and back-transformation as well
    as the eigenvalues.

    **Keyword arguments:**

    :ints: contains the olp and p_2 integrals (TwoIndex instances)
    """
    olp = ints.get("olp", None)
    p_2 = ints.get("kin", None).copy()
    #
    # Transform to orthonormal basis diagonalising p^2
    #
    e_olp, u_olp = olp.diagonalize(eigvec=True, use_eigh=True)
    e_olp_inv_sqrt = (e_olp.inverse()).sqrt()
    # Diagonalize p^2
    p_2.iscale(2.0)
    p_2.itransform(u_olp.contract("ab,b->ab", e_olp_inv_sqrt, out=None))
    e_p_2, u_p_2 = p_2.diagonalize(eigvec=True, use_eigh=True)
    # Get transformation matrices
    u_ort = u_olp.contract("ab,b,bc->ac", e_olp_inv_sqrt, u_p_2, out=None)
    u_back = u_olp.contract("ab,b,bc->ac", e_olp.sqrt(), u_p_2, out=None)

    return {"u_ort": u_ort, "u_back": u_back, "e_p_2": e_p_2}


def get_dkh_vectors(e_p_2):
    """Compute all vectors required for DKH transformation.
    Returns a dictionary containing all required vectors.
    """
    #
    # Vector e_p
    # e_p = sqrt( 1+(p_2/c)^2 )
    e_p = e_p_2.copy()
    e_p.iscale(alpha**2)
    e_p.iadd(1.0)
    e_p.isqrt()
    #
    # Vector a_k
    # A_k = sqrt( (1+e_k)/(2 e_k) )
    a_k = e_p.copy()
    a_k.iadd(1.0)
    a_k.idivide(e_p, 0.5)
    a_k.isqrt()
    #
    # Vector b_k
    # b_k = 1/(1+e_k)
    b_k = e_p.copy()
    b_k.iadd(1.0)
    b_k = b_k.inverse()

    return {"e_p": e_p, "e_p_2": e_p_2, "a_k": a_k, "b_k": b_k}


def get_dkh_order_1(nuc, pvp, **vectors):
    """The 1-order DKH Hamiltonian (DenseTwoIndex).

    **Arguments:**

    :nuc: the nuclear repulsion integrals
    :pvp: the pVp integrals

    **Keyword arguments:**

    :vectors: Contains a dictionary of (OneIndex) instances defined in get_dkh_vectors
    """
    e_p_2 = vectors.get("e_p_2", None)
    b_k = vectors.get("b_k", None)
    a_k = vectors.get("a_k", None)
    #
    # A_k ( V +1/c^2 b_k pVp b_k ) A_k
    #
    # Compute components
    # tmp = 1/c^2 b_k pVp b_k
    tmp = b_k.contract("a,ab,b->ab", pvp, b_k, factor=alpha**2, out=None)
    # V + tmp = (V + 1/c^2 b_k pVp b_k)
    tmp.iadd(nuc)
    # A_k ( V +1/c^2 b_k pVp b_k ) A_k
    e_1 = a_k.contract("a,ab,b->ab", tmp, a_k, out=None)
    #
    # E1 = T_p_at_diag + e_1
    # T_p_at_diag = t_p = c^2(e_k-1) = p_2 * b_k
    t_p = e_p_2.new()
    e_p_2.mult(b_k, out=t_p)
    # Final E1 matrix
    e_1.iadd_diagonal(t_p)

    return e_1


def get_dkh_order_2(nuc, pvp, **vectors):
    """The 1-order DKH Hamiltonian (DenseTwoIndex).

    **Arguments:**

    :nuc: the nuclear repulsion integrals
    :pvp: the pVp integrals

    **Keyword arguments:**

    :vectors: Contains a dictionary of (OneIndex) instances defined in get_dkh_vectors
    """
    e_p = vectors.get("e_p", None)
    e_p_2 = vectors.get("e_p_2", None)
    b_k = vectors.get("b_k", None)
    a_k = vectors.get("a_k", None)
    #
    # E2 = 0.5 ( Y + Y^T )
    # Y = - W p^2 O^T
    # O = 1/c A (1/p2 pVp b_k - b_k V) A
    # W(i,j) = 1/c^2 O(j,i) / (ep(i) +ep(j))
    # O
    # part: 1/p2 pVp b_k
    tmp = (e_p_2.inverse()).contract("a,ab,b->ab", pvp, b_k)
    # part: - b_k V
    b_k.contract("a,ab->ab", nuc, tmp, factor=-1.0)
    # part: A_k tmp A_k
    o_1 = a_k.contract("a,ab,b->ab", tmp, a_k)
    o_1.iscale(alpha)
    # W
    w_1 = o_1.copy()
    w_1.itranspose()
    # denominator 1/(e_p(i) + e_p(j))
    tmp.clear()
    tmp.iadd(e_p, 1.0)
    tmp.iadd(e_p, 1.0, transpose=True)
    denominator = tmp.new()
    denominator.assign(1.0)
    denominator.idivide(tmp, factor=alpha**2)
    # Final W matrix:
    w_1.imul(denominator)
    #
    # Y = - W p^2 O^T
    #
    y_matrix = w_1.contract("ab,b,bc->ac", e_p_2, o_1, out=None, factor=-1.0)
    #
    # E2 = -0.5 ( Y + Y^T )
    #
    e_2 = y_matrix.copy()
    e_2.iadd_t(y_matrix)
    e_2.iscale(-0.5)

    return e_2
