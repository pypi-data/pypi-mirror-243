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
"""Utility methods for Restricted Linearized Coupled Cluster

   Variables used in this module:
    :nocc:       total number of occupied orbitals
    :nvirt:      total number of virtual orbitals
    :ncore:      number of frozen core orbitals in the principle configuration
    :nacto:      number of active occupied orbitals
    :nactv:      number of active virtual orbitals
    :energy:     the CCSD energy, dictionary containing different contributions
    :amplitudes: the CCSD amplitudes (dict), contains t_1
    :t_1:        the single-excitation amplitudes

    Indexing convention:
    :o:        matrix block corresponding to occupied orbitals of principle
               configuration
    :v:        matrix block corresponding to virtual orbitals of principle
               configuration

"""

import numpy as np

from pybest.utils import unmask

###############################################################################
# Density Matrices LCCD
###############################################################################


def compute_1dm_lccd(
    select, dm_out, l_amplitudes, amplitudes, factor, *args, **kwargs
):
    """Computes specific block of N-RDM.

    **Arguments:**

    select:
        (str) the block to be calculated

    dm_out:
        (NIndex) the RDM stored in the cache

    l_amplitudes:
        (dict) Contains the Lambda amplitudes

    factor:
        (float, int) some scaling factor for RDM block

    amplitudes:
        (dict) Contains the CC amplitudes

    args, kargs:
        Used to resolve t_p amplitudes
    """
    if select == "pp":
        return compute_1dm_lccd_pp(
            dm_out, l_amplitudes, amplitudes, factor, *args, **kwargs
        )
    if select == "pq":
        return compute_1dm_lccd_pq(
            dm_out, l_amplitudes, amplitudes, factor, *args, **kwargs
        )
    raise NotImplementedError


def compute_2dm_lccd(
    select, dm_out, l_amplitudes, amplitudes, factor, *args, **kwargs
):
    """Computes specific block of N-RDM.

    **Arguments:**

    select:
        (str) the block to be calculated

    dm_out:
        (NIndex) the RDM stored in the cache

    l_amplitudes:
        (dict) Contains the Lambda amplitudes

    factor:
        (float, int) some scaling factor for RDM block

    amplitudes:
        (dict) Contains the CC amplitudes

    args, kargs:
        Used to resolve t_p amplitudes
    """
    if select == "pPPp":
        return compute_2dm_lccd_pPPp(
            dm_out, l_amplitudes, amplitudes, factor, *args, **kwargs
        )
    if select == "pqqp":
        return compute_2dm_lccd_pqqp(
            dm_out, l_amplitudes, amplitudes, factor, *args, **kwargs
        )
    if select == "pQQp":
        return compute_2dm_lccd_pQQp(
            dm_out, l_amplitudes, amplitudes, factor, *args, **kwargs
        )
    if select in ["qQQp", "qQPq"]:
        return compute_2dm_lccd_qQQp(
            dm_out, l_amplitudes, amplitudes, factor, *args, **kwargs
        )
    if select in ["pQPp", "qPPp"]:
        return compute_2dm_lccd_pQPp(
            dm_out, l_amplitudes, amplitudes, factor, *args, **kwargs
        )
    if select == "qQPp":
        return compute_2dm_lccd_qQPp(
            dm_out, l_amplitudes, amplitudes, factor, *args, **kwargs
        )
    if select == "pQPq":
        return compute_2dm_lccd_pQPq(
            dm_out, l_amplitudes, amplitudes, factor, *args, **kwargs
        )
    raise NotImplementedError


def compute_3dm_lccd(
    select, dm_out, l_amplitudes, amplitudes, factor, *args, **kwargs
):
    """Computes specific block of N-RDM.

    **Arguments:**

    select:
        (str) the block to be calculated

    dm_out:
        (NIndex) the RDM stored in the cache

    l_amplitudes:
        (dict) Contains the Lambda amplitudes

    factor:
        (float, int) some scaling factor for RDM block

    amplitudes:
        (dict) Contains the CC amplitudes

    args, kargs:
        Used to resolve t_p amplitudes
    """
    if select == "qPQQPp":
        return compute_3dm_lccd_qPQQPp(
            dm_out, l_amplitudes, amplitudes, factor, *args, **kwargs
        )
    if select == "qpPPpq":
        return compute_3dm_lccd_qpPPpq(
            dm_out, l_amplitudes, amplitudes, factor, *args, **kwargs
        )
    raise NotImplementedError


def compute_4dm_lccd(
    select, dm_out, l_amplitudes, amplitudes, factor, *args, **kwargs
):
    """Computes specific block of N-RDM.

    **Arguments:**

    select:
        (str) the block to be calculated

    dm_out:
        (NIndex) the RDM stored in the cache

    l_amplitudes:
        (dict) Contains the Lambda amplitudes

    factor:
        (float, int) some scaling factor for RDM block

    amplitudes:
        (dict) Contains the CC amplitudes

    args, kargs:
        Used to resolve t_p amplitudes
    """
    if select == "pPqQQqPp":
        return compute_4dm_lccd_pPqQQqPp(
            dm_out, l_amplitudes, amplitudes, factor, *args, **kwargs
        )
    raise NotImplementedError


def compute_1dm_lccd_pp(
    dm_out, l_amplitudes, amplitudes, factor, *args, **kwargs
):
    """Computes specific block of N-RDM.

    **Arguments:**

    dm_out:
        (NIndex) the RDM stored in the cache

    l_amplitudes:
        (dict) Contains the Lambda amplitudes

    factor:
        (float, int) some scaling factor for RDM block

    amplitudes:
        (dict) Contains the CC amplitudes

    args, kargs:
        Used to resolve t_p amplitudes
    """
    t_2 = amplitudes["t_2"]
    l_2 = l_amplitudes["l_2"]
    occ = t_2.nbasis
    #
    # Calculate occupied block
    #
    to_dm = {"out": dm_out, "end8": occ}
    t_2.contract("abcd,abcd->c", l_2, **to_dm, factor=-0.5)
    #
    # Calculate virtual block
    #
    to_dm = {"out": dm_out, "begin8": occ}
    t_2.contract("abcd,abcd->b", l_2, **to_dm, factor=0.5)
    #
    # d_pi contribution
    #
    dm_out.iadd(1.0, end0=occ)
    #
    # Scale
    #
    dm_out.iscale(factor)


def compute_1dm_lccd_pq(
    dm_out, l_amplitudes, amplitudes, factor, *args, **kwargs
):
    """Computes specific block of N-RDM.

    **Arguments:**

    dm_out:
        (NIndex) the RDM stored in the cache

    l_amplitudes:
        (dict) Contains the Lambda amplitudes

    factor:
        (float, int) some scaling factor for RDM block

    amplitudes:
        (dict) Contains the CC amplitudes

    args, kargs:
        Used to resolve t_p amplitudes
    """
    t_2 = amplitudes["t_2"]
    l_2 = l_amplitudes["l_2"]
    occ = t_2.nbasis

    to_oo = {"out": dm_out, "end8": occ, "end9": occ}
    to_vv = {"out": dm_out, "begin8": occ, "begin9": occ}
    #
    # Calculate occupied block
    # 2a -tmeif . lmejf
    t_2.contract("abcd,abed->ce", l_2, **to_oo, factor=-0.5)
    #
    # Calculate virtual block
    # 2a lmanf . tmbnf
    l_2.contract("abcd,aecd->be", t_2, **to_vv, factor=0.5)
    #
    # d_pq contribution (HF)
    #
    dm_out.iadd_diagonal(1.0, end0=occ)
    # scale
    dm_out.iscale(factor)


def compute_2dm_lccd_pPPp(
    dm_out, l_amplitudes, amplitudes, factor, *args, **kwargs
):
    """Computes specific block of N-RDM.

    **Arguments:**

    dm_out:
        (NIndex) the RDM stored in the cache

    l_amplitudes:
        (dict) Contains the Lambda amplitudes

    factor:
        (float, int) some scaling factor for RDM block

    amplitudes:
        (dict) Contains the CC amplitudes

    args, kargs:
        Used to resolve t_p amplitudes
    """
    t_2 = amplitudes["t_2"]
    l_2 = l_amplitudes["l_2"]
    occ = t_2.nbasis

    to_oo = {"out": dm_out, "end8": occ}
    to_vv = {"out": dm_out, "begin8": occ}
    #
    # Calculate occupied block
    #
    t_2.contract("abac,abac->a", l_2, **to_oo, factor=0.5)
    #
    # Calculate virtual block
    #
    t_2.contract("abcb,abcb->b", l_2, **to_vv, factor=0.5)
    #
    # Lower dimensional contributions
    #
    # ii + II
    t_2.contract("abcd,abcd->c", l_2, **to_oo, factor=-1.0)
    #
    # HF
    #
    dm_out.iadd(1.0, end0=occ)
    # scale
    dm_out.iscale(factor)


def compute_2dm_lccd_pqqp(
    dm_out, l_amplitudes, amplitudes, factor, *args, **kwargs
):
    """Computes specific block of N-RDM.

    **Arguments:**

    dm_out:
        (NIndex) the RDM stored in the cache

    l_amplitudes:
        (dict) Contains the Lambda amplitudes

    factor:
        (float, int) some scaling factor for RDM block

    amplitudes:
        (dict) Contains the CC amplitudes

    args, kwargs:
        Used to resolve t_p amplitudes
    """
    t_2 = amplitudes["t_2"]
    l_2 = l_amplitudes["l_2"]
    occ = t_2.nbasis
    act = dm_out.nbasis

    to_oo = {"out": dm_out, "end8": occ, "end9": occ}
    to_vv = {"out": dm_out, "begin8": occ, "begin9": occ}
    to_vo = {"out": dm_out, "begin8": occ, "end9": occ}
    to_ov = {"out": dm_out, "end8": occ, "begin9": occ}

    f = 1.0 / 6.0
    # 1
    # a
    t_2.contract("abcd,abcd->ca", l_2, **to_oo, factor=f)
    # b
    t_2.contract("abcd,adcb->ca", l_2, **to_oo, factor=-f)
    # 2
    # b
    t_2.contract("abcd,abcd->ab", l_2, **to_ov, factor=-0.5)
    # c
    t_2.contract("abcd,abcd->cb", l_2, **to_ov, factor=-f)
    # d
    t_2.contract("abcd,adcb->cb", l_2, **to_ov, factor=f)
    # 3
    # b
    t_2.contract("abcd,abcd->ba", l_2, **to_vo, factor=-0.5)
    # c
    t_2.contract("abcd,abcd->da", l_2, **to_vo, factor=-f)
    # d
    t_2.contract("abcd,adcb->da", l_2, **to_vo, factor=f)
    # 4
    # a
    t_2.contract("abcd,abcd->db", l_2, **to_vv, factor=f)
    # b
    t_2.contract("abcd,adcb->db", l_2, **to_vv, factor=-f)
    #
    # HF
    #
    dm_out.iadd(1.0, 1.0, end0=occ, end1=occ)
    #
    # lower RDM's
    #
    # 1 i/j
    # a
    tmp = t_2.contract("abcd,abcd->c", l_2, out=None, factor=-0.5)
    # add ii/jj to [o,o] block
    dm_out.iadd(tmp, 1.0, 0, occ, 0, occ)
    dm_out.iadd_t(tmp, 1.0, 0, occ, 0, occ)
    # 2 a/b
    # a
    tmp = t_2.contract("abcd,abcd->b", l_2, out=None, factor=0.5)
    # add aa/bb to [o,v]/[v,o] block
    dm_out.iadd_t(tmp, 1.0, 0, occ, occ, act)
    dm_out.iadd(tmp, 1.0, occ, act, 0, occ)
    #
    # Scale
    #
    dm_out.iscale(factor)


def compute_2dm_lccd_pQQp(
    dm_out, l_amplitudes, amplitudes, factor, *args, **kwargs
):
    """Computes specific block of N-RDM.

    **Arguments:**

    dm_out:
        (NIndex) the RDM stored in the cache

    l_amplitudes:
        (dict) Contains the Lambda amplitudes

    factor:
        (float, int) some scaling factor for RDM block

    amplitudes:
        (dict) Contains the CC amplitudes

    args, kargs:
        Used to resolve t_p amplitudes
    """
    t_2 = amplitudes["t_2"]
    l_2 = l_amplitudes["l_2"]
    occ = t_2.nbasis
    act = dm_out.nbasis

    to_oo = {"out": dm_out, "end8": occ, "end9": occ}
    to_vv = {"out": dm_out, "begin8": occ, "begin9": occ}
    to_vo = {"out": dm_out, "begin8": occ, "end9": occ}
    to_ov = {"out": dm_out, "end8": occ, "begin9": occ}
    f = 1.0 / 6.0
    # 1
    # a
    t_2.contract("abcd,abcd->ca", l_2, **to_oo, factor=2 * f)
    # b
    t_2.contract("abcd,adcb->ca", l_2, **to_oo, factor=f)
    # 2
    # a
    t_2.contract("abcd,abcd->cb", l_2, **to_ov, factor=-2 * f)
    # b
    t_2.contract("abcd,adcb->cb", l_2, **to_ov, factor=-f)
    # 3
    # a
    t_2.contract("abcd,abcd->da", l_2, **to_vo, factor=-2 * f)
    # b
    t_2.contract("abcd,adcb->da", l_2, **to_vo, factor=-f)
    # 4
    # a
    t_2.contract("abcd,abcd->db", l_2, **to_vv, factor=2 * f)
    # b
    t_2.contract("abcd,cbad->db", l_2, **to_vv, factor=f)
    #
    # HF
    #
    dm_out.iadd(1.0, 1.0, end0=occ, end1=occ)
    #
    # lower RDM's
    #
    # 1 i/j
    # a
    tmp = t_2.contract("abcd,abcd->c", l_2, out=None, factor=-0.5)
    # add ii/jj to [o,o] block
    dm_out.iadd(tmp, 1.0, 0, occ, 0, occ)
    dm_out.iadd_t(tmp, 1.0, 0, occ, 0, occ)
    # 2 a/b
    # a
    tmp = t_2.contract("abcd,abcd->b", l_2, out=None, factor=0.5)
    # add aa/bb to [o,v]/[v,o] block
    dm_out.iadd_t(tmp, 1.0, 0, occ, occ, act)
    dm_out.iadd(tmp, 1.0, occ, act, 0, occ)
    #
    # scale
    #
    dm_out.iscale(factor)


def compute_2dm_lccd_qQQp(
    dm_out, l_amplitudes, amplitudes, factor, *args, **kwargs
):
    """Computes specific block of N-RDM.

    **Arguments:**

    dm_out:
        (NIndex) the RDM stored in the cache

    l_amplitudes:
        (dict) Contains the Lambda amplitudes

    factor:
        (float, int) some scaling factor for RDM block

    amplitudes:
        (dict) Contains the CC amplitudes

    args, kwargs:
        Used to resolve t_p amplitudes
    """
    t_2 = amplitudes["t_2"]
    l_2 = l_amplitudes["l_2"]
    occ = t_2.nbasis

    to_oo = {"out": dm_out, "end8": occ, "end9": occ}
    to_vv = {"out": dm_out, "begin8": occ, "begin9": occ}
    # 1
    t_2.contract("abcd,adcd->db", l_2, **to_vv, factor=0.5)
    # 2
    t_2.contract("abac,abdc->ad", l_2, **to_oo, factor=0.5)
    #
    # HF
    # 1 ji
    # b -tmeif . lmejf
    t_2.contract("abcd,abed->ce", l_2, **to_oo, factor=-0.5)
    #
    # Scale
    #
    dm_out.iscale(factor)


def compute_2dm_lccd_pQPp(
    dm_out, l_amplitudes, amplitudes, factor, *args, **kwargs
):
    """Computes specific block of N-RDM.

    **Arguments:**

    dm_out:
        (NIndex) the RDM stored in the cache

    l_amplitudes:
        (dict) Contains the Lambda amplitudes

    factor:
        (float, int) some scaling factor for RDM block

    amplitudes:
        (dict) Contains the CC amplitudes

    args, kargs:
        Used to resolve t_p amplitudes
    """
    t_2 = amplitudes["t_2"]
    l_2 = l_amplitudes["l_2"]
    occ = t_2.nbasis

    to_oo = {"out": dm_out, "end8": occ, "end9": occ}
    to_vv = {"out": dm_out, "begin8": occ, "begin9": occ}
    # 1
    t_2.contract("abcd,abad->ca", l_2, **to_oo, factor=0.5)
    # 2
    t_2.contract("abcb,abcd->db", l_2, **to_vv, factor=0.5)
    #
    # Lower RDM's
    # b
    t_2.contract("abcd,abed->ce", l_2, **to_oo, factor=-0.5)
    #
    # Scale
    #
    dm_out.iscale(factor)


def compute_2dm_lccd_pQPq(
    dm_out, l_amplitudes, amplitudes, factor, *args, **kwargs
):
    """Computes specific block of N-RDM.

    **Arguments:**

    dm_out:
        (NIndex) the RDM stored in the cache

    l_amplitudes:
        (dict) Contains the Lambda amplitudes

    factor:
        (float, int) some scaling factor for RDM block

    amplitudes:
        (dict) Contains the CC amplitudes

    args, kargs:
        Used to resolve t_p amplitudes
    """
    t_2 = amplitudes["t_2"]
    l_2 = l_amplitudes["l_2"]
    occ = t_2.nbasis

    to_oo = {"out": dm_out, "end8": occ, "end9": occ}
    to_vv = {"out": dm_out, "begin8": occ, "begin9": occ}
    to_vo = {"out": dm_out, "begin8": occ, "end9": occ}
    to_ov = {"out": dm_out, "end8": occ, "begin9": occ}
    f = 1.0 / 6.0
    # 1
    # a
    t_2.contract("abcd,adcb->db", l_2, **to_vv, factor=2.0 * f)
    # b
    t_2.contract("abcd,abcd->db", l_2, **to_vv, factor=f)
    # 2
    # a
    t_2.contract("abcd,cbad->ca", l_2, **to_oo, factor=2.0 * f)
    # b
    t_2.contract("abcd,abcd->ca", l_2, **to_oo, factor=f)
    # 3
    # b
    t_2.contract("abcd,abcd->ab", l_2, **to_ov, factor=0.5)
    t_2.contract("abcd,abcd->ba", l_2, **to_vo, factor=0.5)
    # c
    t_2.contract("abcd,cbad->cb", l_2, **to_ov, factor=-2.0 * f)
    t_2.contract("abcd,cbad->bc", l_2, **to_vo, factor=-2.0 * f)
    # d
    t_2.contract("abcd,abcd->cb", l_2, **to_ov, factor=-f)
    t_2.contract("abcd,abcd->bc", l_2, **to_vo, factor=-f)
    #
    # Scale
    #
    dm_out.iscale(factor)


def compute_2dm_lccd_qQPp(
    dm_out, l_amplitudes, amplitudes, factor, *args, **kwargs
):
    """Computes specific block of N-RDM.

    **Arguments:**

    dm_out:
        (NIndex) the RDM stored in the cache

    l_amplitudes:
        (dict) Contains the Lambda amplitudes

    factor:
        (float, int) some scaling factor for RDM block

    amplitudes:
        (dict) Contains the CC amplitudes

    args, kwargs:
        Used to resolve t_p amplitudes
    """
    t_2 = amplitudes["t_2"]
    l_2 = l_amplitudes["l_2"]
    occ = t_2.nbasis

    to_oo = {"out": dm_out, "end8": occ, "end9": occ}
    to_vv = {"out": dm_out, "begin8": occ, "begin9": occ}
    # 1
    t_2.contract("abcb,adcd->db", l_2, **to_vv, factor=0.5)
    # 2
    t_2.contract("abac,dbdc->ad", l_2, **to_oo, factor=0.5)
    # Scale
    dm_out.iscale(factor)


def compute_3dm_lccd_qPQQPp(
    dm_out, l_amplitudes, amplitudes, factor, *args, **kwargs
):
    """Computes specific block of N-RDM.

    **Arguments:**

    dm_out:
        (NIndex) the RDM stored in the cache

    l_amplitudes:
        (dict) Contains the Lambda amplitudes

    factor:
        (float, int) some scaling factor for RDM block

    amplitudes:
        (dict) Contains the CC amplitudes

    args, kargs:
        Used to resolve t_p amplitudes
    """
    t_2 = amplitudes["t_2"]
    l_2 = l_amplitudes["l_2"]
    occ = t_2.nbasis

    to_oo = {"out": dm_out, "end8": occ, "end9": occ}

    # 3 jIIi
    # a
    t_2.contract("abcd,cbcd->ac", l_2, **to_oo, factor=0.5)
    # 4 jJJi
    # a
    t_2.contract("abac,abdc->ad", l_2, **to_oo, factor=0.5)
    # 5 ji
    # b
    t_2.contract("abcd,abed->ce", l_2, **to_oo, factor=-0.5)
    #
    # Scale
    #
    dm_out.iscale(factor)


def compute_3dm_lccd_qpPPpq(
    dm_out, l_amplitudes, amplitudes, factor, *args, **kwargs
):
    """Computes specific block of N-RDM.

    **Arguments:**

    dm_out:
        (NIndex) the RDM stored in the cache

    l_amplitudes:
        (dict) Contains the Lambda amplitudes

    factor:
        (float, int) some scaling factor for RDM block

    amplitudes:
        (dict) Contains the CC amplitudes

    args, kargs:
        Used to resolve t_p amplitudes
    """
    t_2 = amplitudes["t_2"]
    l_2 = l_amplitudes["l_2"]
    occ = t_2.nbasis
    act = dm_out.nbasis

    to_oo = {"out": dm_out, "end8": occ, "end9": occ}
    to_vo = {"out": dm_out, "begin8": occ, "end9": occ}
    to_ov = {"out": dm_out, "end8": occ, "begin9": occ}

    f = 1.0 / 6.0
    # 1
    t_2.contract("abac,abac->ba", l_2, **to_vo, factor=0.5)
    # 2
    t_2.contract("abcb,abcb->ab", l_2, **to_ov, factor=-0.5)
    #
    # HF: dqj dpi
    #
    dm_out.iadd(1.0, 1.0, end0=occ, end1=occ)
    #
    # lower RDM's:
    # aAAa dqj + ibbi dpi + iBBi dPI + bb dpidPI + IjjI dpi + ijji dPI+
    # iIIi dqj + jj dpidPI + ii dPIdqj + II dpidqj
    # 1 ibbi
    # b
    t_2.contract("abcd,abcd->ba", l_2, **to_vo, factor=-0.5)
    # c
    t_2.contract("abcd,abcd->da", l_2, **to_vo, factor=-f)
    # d
    t_2.contract("abcd,adcb->da", l_2, **to_vo, factor=f)
    # 2 iBBi
    # a
    t_2.contract("abcd,abcd->da", l_2, **to_vo, factor=-2 * f)
    # b
    t_2.contract("abcd,adcb->da", l_2, **to_vo, factor=-f)
    # 3 bb
    tmp_bb = t_2.contract("abcd,abcd->b", l_2, out=None, factor=0.5)
    # add to [v,o] block
    dm_out.iadd(tmp_bb, 1.0, occ, act, 0, occ)
    # 4 aAAa
    tmp_a = t_2.contract("abcb,abcb->b", l_2, out=None, factor=0.5, clear=True)
    # add to [o,v] block
    dm_out.iadd_t(tmp_a, 1.0, 0, occ, occ, act)
    # 5 IjjI
    # a
    t_2.contract("abcd,abcd->ca", l_2, **to_oo, factor=2 * f)
    # b
    t_2.contract("abcd,adcb->ca", l_2, **to_oo, factor=f)
    # 6 ijji
    # a
    t_2.contract("abcd,abcd->ca", l_2, **to_oo, factor=f)
    # b
    t_2.contract("abcd,adcb->ca", l_2, **to_oo, factor=-f)
    # 7 iIIi
    tmp_i = t_2.contract("abac,abac->a", l_2, out=None, factor=0.5)
    # 9 ii + II
    # b
    t_2.contract("abcd,abcd->c", l_2, tmp_i, factor=-1.0)
    # add to [o,o] block
    dm_out.iadd_t(tmp_i, 1.0, 0, occ, 0, occ)
    # 8 jj
    # a
    tmp_jj = t_2.contract("abcd,abcd->c", l_2, out=None, factor=-0.5)
    # add to [o,o] block
    dm_out.iadd(tmp_jj, 1.0, 0, occ, 0, occ)
    #
    # Scale
    #
    dm_out.iscale(factor)


def compute_4dm_lccd_pPqQQqPp(
    dm_out, l_amplitudes, amplitudes, factor, *args, **kwargs
):
    """Computes specific block of N-RDM.

    **Arguments:**

    dm_out:
        (NIndex) the RDM stored in the cache

    l_amplitudes:
        (dict) Contains the Lambda amplitudes

    factor:
        (float, int) some scaling factor for RDM block

    amplitudes:
        (dict) Contains the CC amplitudes

    args, kwargs:
        Used to resolve t_p amplitudes
    """
    t_2 = amplitudes["t_2"]
    l_2 = l_amplitudes["l_2"]
    occ = t_2.nbasis
    act = dm_out.nbasis

    to_oo = {"out": dm_out, "end8": occ, "end9": occ}
    to_vo = {"out": dm_out, "begin8": occ, "end9": occ}
    to_ov = {"out": dm_out, "end8": occ, "begin9": occ}

    f = 1.0 / 6.0
    #
    # HF
    #
    dm_out.iadd(1.0, 1.0, end0=occ, end1=occ)
    #
    # lower RDM's:
    # aAJJAa dqj + aAjjAa dQJ + aAAa dqj dQJ + bBBb dpi dPI + ibBBbi dIP +
    # IbBBbI dip + iIjjIi +iIJJIi + ijJJji + IjJJjI +
    # iIIi djq + ijji dIP dQJ+ jJJj dip + IJJI dip dqj  + IjjI dip dQJ +
    # iJJi dIP djq + ii dip dqj + II dip dqj + jj dip dqj + JJ dip dqj + HF dip dqj
    # 1
    # a aAJJAa +  aAjjAa
    t_2.contract("abcb,abcb->ab", l_2, **to_ov, factor=-1.0)
    # b aAAa
    tmp_a = t_2.contract("abcb,abcb->b", l_2, out=None, factor=0.5)
    # add to [o,v] block
    dm_out.iadd_t(tmp_a, 1.0, 0, occ, occ, act)
    # 2 bBBb
    tmp_b = t_2.contract("abcb,abcb->b", l_2, out=None, factor=0.5)
    # add to [v,o] block
    dm_out.iadd(tmp_b, 1.0, occ, act, 0, occ)
    # 3 ibBBbi
    t_2.contract("abcb,abcb->ba", l_2, **to_vo, factor=-0.5)
    # 4 IbBBbI
    t_2.contract("abcb,abcb->ba", l_2, **to_vo, factor=-0.5)
    # 5 iIjjIi = 0
    # 6 iIJJIi = 0
    # 7 ijJJji = 0
    # 8 IjJJjI = 0
    # 9 iIIi
    tmp_i = t_2.contract("abac,abac->a", l_2, out=None, factor=0.5)
    # 13 ii + II
    t_2.contract("abcd,abcd->c", l_2, tmp_i, factor=-1.0)
    dm_out.iadd_t(tmp_i, 1.0, 0, occ, 0, occ)
    # 10 ijji + IJJI
    # a
    t_2.contract("abcd,abcd->ca", l_2, **to_oo, factor=2 * f)
    # b
    t_2.contract("abcd,adcb->ca", l_2, **to_oo, factor=-2 * f)
    # 11 jJJj
    tmp_j = t_2.contract("abac,abac->a", l_2, out=None, factor=0.5)
    # 14 jj + JJ
    # b
    t_2.contract("abcd,abcd->c", l_2, tmp_j, factor=-1.0)
    dm_out.iadd(tmp_j, 1.0, 0, occ, 0, occ)
    # 12 IjjI + iJJi
    # a
    t_2.contract("abcd,abcd->ca", l_2, **to_oo, factor=4 * f)
    # b
    t_2.contract("abcd,adcb->ca", l_2, **to_oo, factor=2 * f)
    #
    # Scale
    #
    dm_out.iscale(factor)


###############################################################################
# Density Matrices LCCSD
###############################################################################


def compute_1dm_lccsd(
    select, dm_out, l_amplitudes, amplitudes, factor, *args, **kwargs
):
    """Computes specific block of N-RDM.

    **Arguments:**

    select:
        (str) the block to be calculated

    dm_out:
        (NIndex) the RDM stored in the cache

    l_amplitudes:
        (dict) Contains the Lambda amplitudes

    factor:
        (float, int) some scaling factor for RDM block

    amplitudes:
        (dict) Contains the CC amplitudes

    args, kwargs:
        Used to resolve t_p amplitudes
    """
    #
    # Compute LCCD contribution
    #
    compute_1dm_lccd(
        select, dm_out, l_amplitudes, amplitudes, factor, *args, **kwargs
    )
    #
    # Compute missing terms
    #
    if select == "pp":
        return compute_1dm_lccsd_pp(
            dm_out, l_amplitudes, amplitudes, factor, *args, **kwargs
        )
    if select == "pq":
        return compute_1dm_lccsd_pq(
            dm_out, l_amplitudes, amplitudes, factor, *args, **kwargs
        )
    raise NotImplementedError


def compute_2dm_lccsd(
    select, dm_out, l_amplitudes, amplitudes, factor, *args, **kwargs
):
    """Computes specific block of N-RDM.

    **Arguments:**

    select:
        (str) the block to be calculated

    dm_out:
        (NIndex) the RDM stored in the cache

    l_amplitudes:
        (dict) Contains the Lambda amplitudes

    factor:
        (float, int) some scaling factor for RDM block

    amplitudes:
        (dict) Contains the CC amplitudes

    args, kwargs:
        Used to resolve t_p amplitudes
    """
    #
    # Compute LCCD contribution
    #
    compute_2dm_lccd(
        select, dm_out, l_amplitudes, amplitudes, factor, *args, **kwargs
    )
    #
    # Compute missing terms
    #
    if select == "pPPp":
        compute_2dm_lccsd_pPPp(
            dm_out, l_amplitudes, amplitudes, factor, *args, **kwargs
        )
    elif select == "pqqp":
        compute_2dm_lccsd_pqqp(
            dm_out, l_amplitudes, amplitudes, factor, *args, **kwargs
        )
    elif select == "pQQp":
        compute_2dm_lccsd_pQQp(
            dm_out, l_amplitudes, amplitudes, factor, *args, **kwargs
        )
    elif select == "pQPq":
        compute_2dm_lccsd_pQPq(
            dm_out, l_amplitudes, amplitudes, factor, *args, **kwargs
        )
    elif select in ["qQQp", "qQPq"]:
        compute_2dm_lccsd_qQQp(
            dm_out, l_amplitudes, amplitudes, factor, *args, **kwargs
        )
    elif select in ["pQPp", "qPPp"]:
        compute_2dm_lccsd_pQPp(
            dm_out, l_amplitudes, amplitudes, factor, *args, **kwargs
        )


def compute_3dm_lccsd(
    select, dm_out, l_amplitudes, amplitudes, factor, *args, **kwargs
):
    """Computes specific block of N-RDM.

    **Arguments:**

    select:
        (str) the block to be calculated

    dm_out:
        (NIndex) the RDM stored in the cache

    l_amplitudes:
        (dict) Contains the Lambda amplitudes

    factor:
        (float, int) some scaling factor for RDM block

    amplitudes:
        (dict) Contains the CC amplitudes

    args, kwargs:
        Used to resolve t_p amplitudes
    """
    #
    # Compute LCCD contribution
    #
    compute_3dm_lccd(
        select, dm_out, l_amplitudes, amplitudes, factor, *args, **kwargs
    )
    #
    # Compute missing terms
    #
    if select == "qPQQPp":
        return compute_3dm_lccsd_qPQQPp(
            dm_out, l_amplitudes, amplitudes, factor, *args, **kwargs
        )
    if select == "qpPPpq":
        return compute_3dm_lccsd_qpPPpq(
            dm_out, l_amplitudes, amplitudes, factor, *args, **kwargs
        )
    raise NotImplementedError


def compute_4dm_lccsd(
    select, dm_out, l_amplitudes, amplitudes, factor, *args, **kwargs
):
    """Computes specific block of N-RDM.

    **Arguments:**

    select:
        (str) the block to be calculated

    dm_out:
        (NIndex) the RDM stored in the cache

    l_amplitudes:
        (dict) Contains the Lambda amplitudes

    factor:
        (float, int) some scaling factor for RDM block

    amplitudes:
        (dict) Contains the CC amplitudes

    args, kwargs:
        Used to resolve t_p amplitudes
    """
    #
    # Compute LCCD contribution
    #
    compute_4dm_lccd(
        select, dm_out, l_amplitudes, amplitudes, factor, *args, **kwargs
    )
    #
    # Compute missing terms
    #
    if select == "pPqQQqPp":
        return compute_4dm_lccsd_pPqQQqPp(
            dm_out, l_amplitudes, amplitudes, factor, *args, **kwargs
        )
    raise NotImplementedError


def compute_1dm_lccsd_pp(
    dm_out, l_amplitudes, amplitudes, factor, *args, **kwargs
):
    """Computes specific block of N-RDM.

    **Arguments:**

    dm_out:
        (NIndex) the RDM stored in the cache

    l_amplitudes:
        (dict) Contains the Lambda amplitudes

    factor:
        (float, int) some scaling factor for RDM block

    amplitudes:
        (dict) Contains the CC amplitudes

    args, kargs:
        Used to resolve t_p amplitudes
    """
    t_1 = amplitudes["t_1"]
    l_1 = l_amplitudes["l_1"]
    occ = t_1.nbasis

    to_o = {"out": dm_out, "end4": occ}
    to_v = {"out": dm_out, "begin4": occ}
    #
    # Calculate occupied block
    # rho(ij)
    # 1
    t_1.contract("ab,ab->a", l_1, **to_o, factor=-0.5 * factor)
    #
    # Calculate virtual block
    # 1
    t_1.contract("ab,ab->b", l_1, **to_v, factor=0.5 * factor)


def compute_1dm_lccsd_pq(
    dm_out, l_amplitudes, amplitudes, factor, *args, **kwargs
):
    """Computes specific block of N-RDM.

    **Arguments:**

    dm_out:
        (NIndex) the RDM stored in the cache

    l_amplitudes:
        (dict) Contains the Lambda amplitudes

    factor:
        (float, int) some scaling factor for RDM block

    amplitudes:
        (dict) Contains the CC amplitudes

    args, kargs:
        Used to resolve t_p amplitudes
    """
    t_1 = amplitudes["t_1"]
    t_2 = amplitudes["t_2"]
    l_1 = l_amplitudes["l_1"]
    l_2 = l_amplitudes["l_2"]
    occ = t_1.nbasis

    to_oo = {"out": dm_out, "end4": occ, "end5": occ}
    to_ov = {"out": dm_out, "end6": occ, "begin7": occ}
    to_vo = {"out": dm_out, "begin6": occ, "end7": occ}
    to_vv = {"out": dm_out, "begin4": occ, "begin5": occ}
    vo = {"begin0": occ, "end1": occ}
    ov = {"end0": occ, "begin1": occ}
    #
    # Calculate occupied block
    # rho(ij)
    # 1 -tic.ljc
    t_1.contract("ab,cb->ac", l_1, **to_oo, factor=-0.5 * factor)
    #
    # Calculate virtual block
    # rho(ab)
    # 1 lka tkb
    l_1.contract("ab,ac->bc", t_1, **to_vv, factor=0.5 * factor)
    # 3a lia
    dm_out.iadd_t(l_1, 0.5 * factor, **vo)
    l_2.contract("abcd,cd->ba", t_1, **to_vo, factor=0.5 * factor)
    # 4a tia
    dm_out.iadd(t_1, factor, **ov)
    # 4b tianf . lnf
    t_2.contract("abcd,cd->ab", l_1, **to_ov, factor=1.0 * factor)
    # 4c -tmaif . lmf
    t_2.contract("abcd,ad->cb", l_1, **to_ov, factor=-0.5 * factor)


def compute_2dm_lccsd_pPPp(
    dm_out, l_amplitudes, amplitudes, factor, *args, **kwargs
):
    """Computes specific block of N-RDM.

    **Arguments:**

    dm_out:
        (NIndex) the RDM stored in the cache

    l_amplitudes:
        (dict) Contains the Lambda amplitudes

    factor:
        (float, int) some scaling factor for RDM block

    amplitudes:
        (dict) Contains the CC amplitudes

    args, kargs:
        Used to resolve t_p amplitudes
    """
    t_1 = amplitudes["t_1"]
    l_1 = l_amplitudes["l_1"]
    occ = t_1.nbasis

    to_o = {"out": dm_out, "end4": occ}
    #
    # lower RDM's:
    # ii + II
    t_1.contract("ab,ab->a", l_1, **to_o, factor=-1.0 * factor)


def compute_2dm_lccsd_pqqp(
    dm_out, l_amplitudes, amplitudes, factor, *args, **kwargs
):
    """Computes specific block of N-RDM.

    **Arguments:**

    dm_out:
        (NIndex) the RDM stored in the cache

    l_amplitudes:
        (dict) Contains the Lambda amplitudes

    factor:
        (float, int) some scaling factor for RDM block

    amplitudes:
        (dict) Contains the CC amplitudes

    args, kargs:
        Used to resolve t_p amplitudes
    """
    t_1 = amplitudes["t_1"]
    l_1 = l_amplitudes["l_1"]
    occ = t_1.nbasis
    act = dm_out.nbasis

    to_ov = {"out": dm_out, "end4": occ, "begin5": occ}
    to_vo = {"out": dm_out, "begin4": occ, "end5": occ}
    ###2
    # a
    t_1.contract("ab,ab->ab", l_1, **to_ov, factor=-0.5 * factor)
    ###3
    # a
    t_1.contract("ab,ab->ba", l_1, **to_vo, factor=-0.5 * factor)
    #
    # lower RDM's:
    ### ii + jj + aa + bb
    # 1 i/j
    # b
    tmp = t_1.contract("ab,ab->a", l_1, out=None, factor=-0.5 * factor)
    # add ii/jj to [o,o] block
    dm_out.iadd(tmp, 1.0, 0, occ, 0, occ)
    dm_out.iadd_t(tmp, 1.0, 0, occ, 0, occ)
    # 2 a/b
    # b
    tmp = t_1.contract("ab,ab->b", l_1, out=None, factor=0.5 * factor)
    # add aa/bb to [o,v]/[v,o] block
    dm_out.iadd_t(tmp, 1.0, 0, occ, occ, act)
    dm_out.iadd(tmp, 1.0, occ, act, 0, occ)


def compute_2dm_lccsd_pQQp(
    dm_out, l_amplitudes, amplitudes, factor, *args, **kwargs
):
    """Computes specific block of N-RDM.

    **Arguments:**

    dm_out:
        (NIndex) the RDM stored in the cache

    l_amplitudes:
        (dict) Contains the Lambda amplitudes

    factor:
        (float, int) some scaling factor for RDM block

    amplitudes:
        (dict) Contains the CC amplitudes

    args, kwargs:
        Used to resolve t_p amplitudes
    """
    t_1 = amplitudes["t_1"]
    l_1 = l_amplitudes["l_1"]
    occ = t_1.nbasis
    act = dm_out.nbasis
    #
    # lower RDM's:
    # 1 i/j
    # b
    tmp = t_1.contract("ab,ab->a", l_1, out=None, factor=-0.5 * factor)
    # add ii/jj to [o,o] block
    dm_out.iadd(tmp, 1.0, 0, occ, 0, occ)
    dm_out.iadd_t(tmp, 1.0, 0, occ, 0, occ)
    # 2 a/b
    # b
    tmp = t_1.contract("ab,ab->b", l_1, out=None, factor=0.5 * factor)
    # add aa/bb to [o,v]/[v,o] block
    dm_out.iadd_t(tmp, 1.0, 0, occ, occ, act)
    dm_out.iadd(tmp, 1.0, occ, act, 0, occ)


def compute_2dm_lccsd_pQPq(
    dm_out, l_amplitudes, amplitudes, factor, *args, **kwargs
):
    """Computes specific block of N-RDM.

    **Arguments:**

    dm_out:
        (NIndex) the RDM stored in the cache

    l_amplitudes:
        (dict) Contains the Lambda amplitudes

    factor:
        (float, int) some scaling factor for RDM block

    amplitudes:
        (dict) Contains the CC amplitudes

    args, kwargs:
        Used to resolve t_p amplitudes
    """
    t_1 = amplitudes["t_1"]
    l_1 = l_amplitudes["l_1"]
    occ = t_1.nbasis
    act = dm_out.nbasis

    tmp_ov = t_1.new()
    # 3
    # a
    tmp_ov.iadd_mult(t_1, l_1, 0.5 * factor)
    # Add to [o,v] and [v,o] blocks
    dm_out.iadd_t(tmp_ov, 1.0, occ, act, 0, occ)
    dm_out.iadd(tmp_ov, 1.0, 0, occ, occ, act)


def compute_2dm_lccsd_qQQp(
    dm_out, l_amplitudes, amplitudes, factor, *args, **kwargs
):
    """Computes specific block of N-RDM.

    **Arguments:**

    dm_out:
        (NIndex) the RDM stored in the cache

    l_amplitudes:
        (dict) Contains the Lambda amplitudes

    factor:
        (float, int) some scaling factor for RDM block

    amplitudes:
        (dict) Contains the CC amplitudes

    args, kargs:
        Used to resolve t_p amplitudes
    """
    t_1 = amplitudes["t_1"]
    t_2 = amplitudes["t_2"]
    l_1 = l_amplitudes["l_1"]
    l_2 = l_amplitudes["l_2"]
    occ = t_1.nbasis

    to_oo = {"out": dm_out, "end4": occ, "end5": occ}
    to_ov = {"out": dm_out, "end6": occ, "begin7": occ}
    to_vo = {"out": dm_out, "begin6": occ, "end7": occ}
    ov = {"end0": occ, "begin1": occ, "factor": factor}
    # 3
    # a
    t_2.contract("abac,ac->ab", l_1, **to_ov, factor=-0.5 * factor)
    # 4
    l_2.contract("abcb,cb->ba", t_1, **to_vo, factor=0.5 * factor)
    #
    # lower RDM's:
    # ji +ja
    # 1 ji
    # a
    t_1.contract("ab,cb->ac", l_1, **to_oo, factor=-0.5 * factor)
    # 2 ja
    # a
    dm_out.iadd(t_1, **ov)
    # b tianf . lnf
    t_2.contract("abcd,cd->ab", l_1, **to_ov, factor=1.0 * factor)
    # c -tmaif . lmf
    t_2.contract("abcd,ad->cb", l_1, **to_ov, factor=-0.5 * factor)


def compute_2dm_lccsd_pQPp(
    dm_out, l_amplitudes, amplitudes, factor, *args, **kwargs
):
    """Computes specific block of N-RDM.

    **Arguments:**

    dm_out:
        (NIndex) the RDM stored in the cache

    l_amplitudes:
        (dict) Contains the Lambda amplitudes

    factor:
        (float, int) some scaling factor for RDM block

    amplitudes:
        (dict) Contains the CC amplitudes

    args, kwargs:
        Used to resolve t_p amplitudes
    """
    t_1 = amplitudes["t_1"]
    t_2 = amplitudes["t_2"]
    l_1 = l_amplitudes["l_1"]
    l_2 = l_amplitudes["l_2"]
    occ = t_1.nbasis
    act = dm_out.nbasis

    to_oo = {"out": dm_out, "end4": occ, "end5": occ}
    to_ov = {"out": dm_out, "end6": occ, "begin7": occ}
    to_vo = {"out": dm_out, "begin6": occ, "end7": occ}
    vo = {"begin0": occ, "end1": occ}
    tmp_vo = dm_out.copy(**vo)
    tmp_vo.clear()
    # 3
    l_2.contract("abac,ab->ca", t_1, **to_vo, factor=-0.5 * factor)
    # 4
    # a
    t_2.contract("abcb,cb->ab", l_1, **to_ov, factor=0.5 * factor)
    #
    # lower RDM's:
    # ji +bi
    # 1 ji
    # a
    t_1.contract("ab,cb->ac", l_1, **to_oo, factor=-0.5 * factor)
    # b
    # 2 bi
    # a
    tmp_vo.iadd_t(l_1, 0.5 * factor)
    dm_out.iadd(tmp_vo, 1.0, occ, act, 0, occ)
    # b
    l_2.contract("abcd,cd->ba", t_1, **to_vo, factor=0.5 * factor)


def compute_3dm_lccsd_qpPPpq(
    dm_out, l_amplitudes, amplitudes, factor, *args, **kwargs
):
    """Computes specific block of N-RDM.

    **Arguments:**

    dm_out:
        (NIndex) the RDM stored in the cache

    l_amplitudes:
        (dict) Contains the Lambda amplitudes

    factor:
        (float, int) some scaling factor for RDM block

    amplitudes:
        (dict) Contains the CC amplitudes

    args, kwargs:
        Used to resolve t_p amplitudes
    """
    t_1 = amplitudes["t_1"]
    l_1 = l_amplitudes["l_1"]
    occ = t_1.nbasis
    act = dm_out.nbasis

    to_vo = {"out": dm_out, "begin4": occ, "end5": occ}
    #
    # lower RDM's:
    # 1 ibbi
    # a
    t_1.contract("ab,ab->ba", l_1, **to_vo, factor=-0.5)
    # 3 bb
    tmp = t_1.contract("ab,ab->b", l_1, out=None, factor=0.5)
    # add to [v,o] block
    dm_out.iadd(tmp, factor, occ, act, 0, occ)
    # 8 jj
    # b
    tmp = t_1.contract("ab,ab->a", l_1, out=None, factor=-0.5)
    dm_out.iadd(tmp, factor, 0, occ, 0, occ)
    # 9 ii + II
    tmp = t_1.contract("ab,ab->a", l_1, out=None, factor=-1.0)
    dm_out.iadd_t(tmp, factor, 0, occ, 0, occ)


def compute_3dm_lccsd_qPQQPp(
    dm_out, l_amplitudes, amplitudes, factor, *args, **kwargs
):
    """Computes specific block of N-RDM.

    **Arguments:**

    dm_out:
        (NIndex) the RDM stored in the cache

    l_amplitudes:
        (dict) Contains the Lambda amplitudes

    factor:
        (float, int) some scaling factor for RDM block

    amplitudes:
        (dict) Contains the CC amplitudes

    args, kwargs:
        Used to resolve t_p amplitudes
    """
    t_1 = amplitudes["t_1"]
    t_2 = amplitudes["t_2"]
    l_1 = l_amplitudes["l_1"]
    l_2 = l_amplitudes["l_2"]
    occ = t_1.nbasis

    to_oo = {"out": dm_out, "end4": occ, "end5": occ}
    to_ov = {"out": dm_out, "end6": occ, "begin7": occ}
    to_vo = {"out": dm_out, "begin6": occ, "end7": occ}
    #
    # lower RDM's:
    # 1 bBBi
    l_2.contract("abcb,cb->ba", t_1, **to_vo, factor=0.5 * factor)
    # 2 jAAa
    # a
    t_2.contract("abcb,cb->ab", l_1, **to_ov, factor=0.5 * factor)
    # b lnane,je->naj, naj,na->aj
    # 5 ji
    # a
    t_1.contract("ab,cb->ac", l_1, **to_oo, factor=-0.5 * factor)


def compute_4dm_lccsd_pPqQQqPp(
    dm_out, l_amplitudes, amplitudes, factor, *args, **kwargs
):
    """Computes specific block of N-RDM.

    **Arguments:**

    dm_out:
        (NIndex) the RDM stored in the cache

    l_amplitudes:
        (dict) Contains the Lambda amplitudes

    factor:
        (float, int) some scaling factor for RDM block

    amplitudes:
        (dict) Contains the CC amplitudes

    args, kwargs:
        Used to resolve t_p amplitudes
    """
    t_1 = amplitudes["t_1"]
    l_1 = l_amplitudes["l_1"]
    occ = t_1.nbasis
    # 13 ii + II
    # a
    tmp = t_1.contract("ab,ab->a", l_1, out=None, factor=-1.0)
    dm_out.iadd_t(tmp, factor, 0, occ, 0, occ)
    # 14 jj + JJ
    # a
    #   tmp = t_1.contract("ab,ab->a", l_1, out=None, factor=-1.0)
    dm_out.iadd(tmp, factor, 0, occ, 0, occ)


###############################################################################
# Density Matrices pCCD-LCCD
###############################################################################


def compute_1dm_pccdlccd(
    select, dm_out, l_amplitudes, amplitudes, factor, *args, **kwargs
):
    """Computes specific block of N-RDM.

    **Arguments:**

    select:
        (str) the block to be calculated

    dm_out:
        (NIndex) the RDM stored in the cache

    l_amplitudes:
        (dict) Contains the Lambda amplitudes

    factor:
        (float, int) some scaling factor for RDM block

    amplitudes:
        (dict) Contains the CC amplitudes

    args, kwargs:
        Used to resolve t_p amplitudes
    """
    #
    # assign T_p to T_2
    #
    t_p = unmask("t_p", *args, **kwargs)
    set_seniority_0(amplitudes, t_p)
    #
    # Calculate LCCD RDM
    #
    compute_1dm_lccd(
        select, dm_out, l_amplitudes, amplitudes, factor, *args, **kwargs
    )
    #
    # remove T_p from T_2
    #
    set_seniority_0(amplitudes, 0.0)


def compute_2dm_pccdlccd(
    select, dm_out, l_amplitudes, amplitudes, factor, *args, **kwargs
):
    """Computes specific block of N-RDM.

    **Arguments:**

    select:
        (str) the block to be calculated

    dm_out:
        (NIndex) the RDM stored in the cache

    l_amplitudes:
        (dict) Contains the Lambda amplitudes

    factor:
        (float, int) some scaling factor for RDM block

    amplitudes:
        (dict) Contains the CC amplitudes

    args, kwargs:
        Used to resolve t_p amplitudes
    """
    #
    # assign T_p to T_2
    #
    t_p = unmask("t_p", *args, **kwargs)
    set_seniority_0(amplitudes, t_p)
    #
    # Calculate LCCD RDM
    #
    compute_2dm_lccd(
        select, dm_out, l_amplitudes, amplitudes, factor, *args, **kwargs
    )
    #
    # Calcualte remaining terms
    #
    if select == "qQPp":
        compute_2dm_pccdlccd_qQPp(
            dm_out, l_amplitudes, amplitudes, factor, *args, **kwargs
        )
    #
    # remove T_p from T_2
    #
    set_seniority_0(amplitudes, 0.0)


def compute_3dm_pccdlccd(
    select, dm_out, l_amplitudes, amplitudes, factor, *args, **kwargs
):
    """Computes specific block of N-RDM.

    **Arguments:**

    select:
        (str) the block to be calculated

    dm_out:
        (NIndex) the RDM stored in the cache

    l_amplitudes:
        (dict) Contains the Lambda amplitudes

    factor:
        (float, int) some scaling factor for RDM block

    amplitudes:
        (dict) Contains the CC amplitudes

    args, kwargs:
        Used to resolve t_p amplitudes
    """
    #
    # assign T_p to T_2
    #
    t_p = unmask("t_p", *args, **kwargs)
    set_seniority_0(amplitudes, t_p)
    #
    # Calculate LCCD RDM
    #
    compute_3dm_lccd(
        select, dm_out, l_amplitudes, amplitudes, factor, *args, **kwargs
    )
    #
    # remove T_p from T_2
    #
    set_seniority_0(amplitudes, 0.0)


def compute_4dm_pccdlccd(
    select, dm_out, l_amplitudes, amplitudes, factor, *args, **kwargs
):
    """Computes specific block of N-RDM.

    **Arguments:**

    select:
        (str) the block to be calculated

    dm_out:
        (NIndex) the RDM stored in the cache

    l_amplitudes:
        (dict) Contains the Lambda amplitudes

    factor:
        (float, int) some scaling factor for RDM block

    amplitudes:
        (dict) Contains the CC amplitudes

    args, kwargs:
        Used to resolve t_p amplitudes
    """
    #
    # assign T_p to T_2
    #
    t_p = unmask("t_p", *args, **kwargs)
    set_seniority_0(amplitudes, t_p)
    #
    # Calculate LCCD RDM
    #
    compute_4dm_lccd(
        select, dm_out, l_amplitudes, amplitudes, factor, *args, **kwargs
    )
    #
    # remove T_p from T_2
    #
    set_seniority_0(amplitudes, 0.0)


def compute_2dm_pccdlccd_qQPp(
    dm_out, l_amplitudes, amplitudes, factor, *args, **kwargs
):
    """Computes specific block of N-RDM.

    **Arguments:**

    dm_out:
        (NIndex) the RDM stored in the cache

    l_amplitudes:
        (dict) Contains the Lambda amplitudes

    factor:
        (float, int) some scaling factor for RDM block

    amplitudes:
        (dict) Contains the CC amplitudes

    args, kwargs:
        Used to resolve t_p amplitudes
    """
    t_2 = amplitudes["t_2"]
    l_2 = l_amplitudes["l_2"]
    t_p = unmask("t_p", *args, **kwargs)
    occ = t_2.nbasis

    tmp_ov = t_p.new()
    # 3
    # d
    tmp = t_2.contract("abcd,abcd->ab", l_2, out=None)
    tmp_ov.iadd_mult(t_p, tmp, 1.0)
    # e
    tmp = t_2.contract("abcd,abcd->ad", l_2, out=None)
    tmp_ov.iadd_mult(t_p, tmp, 1.0)
    # f
    tmp = t_2.contract("abcd,abcd->a", l_2, out=None)
    tmp_1 = t_p.contract("ab,a->ab", tmp, out=None, factor=-1.0)
    tmp_ov.iadd(tmp_1)
    # g
    tmp = l_2.contract("abcb,ab->ac", t_p, out=None)
    t_2.contract("abcb,ac->ab", tmp, tmp_ov, factor=-1.0)
    # h
    tmp = t_2.contract("abcd,abcd->b", l_2, out=None)
    tmp_1 = t_p.contract("ab,b->ab", tmp, out=None, factor=-1.0)
    tmp_ov.iadd(tmp_1)
    # i
    tmp = l_2.contract("abac,ab->bc", t_p, out=None)
    t_2.contract("abac,bc->ab", tmp, tmp_ov, factor=-1.0)
    # j
    tmp = t_2.contract("abcb,adcd->bd", l_2, out=None)
    tmp.contract("ab,cb->ca", t_p, tmp_ov, factor=0.5)
    # k
    tmp = t_2.contract("abac,dbdc->ad", l_2, out=None, factor=1.0)
    tmp.contract("ab,bc->ac", t_p, tmp_ov, factor=0.5)
    #
    # Combine all blocks and scale
    #
    options = {"factor": factor, "end0": occ, "begin1": occ}
    dm_out.iadd(tmp_ov, **options)


###############################################################################
# Density Matrices pCCD-LCCSD
###############################################################################


def compute_1dm_pccdlccsd(
    select, dm_out, l_amplitudes, amplitudes, factor, *args, **kwargs
):
    """Computes specific block of N-RDM.

    **Arguments:**

    select:
        (str) the block to be calculated

    dm_out:
        (NIndex) the RDM stored in the cache

    l_amplitudes:
        (dict) Contains the Lambda amplitudes

    factor:
        (float, int) some scaling factor for RDM block

    amplitudes:
        (dict) Contains the CC amplitudes

    args, kwargs:
        Used to resolve t_p amplitudes
    """
    #
    # assign T_p to T_2
    #
    t_p = unmask("t_p", *args, **kwargs)
    set_seniority_0(amplitudes, t_p)
    #
    # Calculate LCCSD RDM
    #
    compute_1dm_lccsd(
        select, dm_out, l_amplitudes, amplitudes, factor, *args, **kwargs
    )
    #
    # Calcualte remaining terms
    #
    if select == "pq":
        compute_1dm_pccdlccsd_pq(
            dm_out, l_amplitudes, amplitudes, factor, *args, **kwargs
        )
    #
    # remove T_p from T_2
    #
    set_seniority_0(amplitudes, 0.0)


def compute_2dm_pccdlccsd(
    select, dm_out, l_amplitudes, amplitudes, factor, *args, **kwargs
):
    """Computes specific block of N-RDM.

    **Arguments:**

    select:
        (str) the block to be calculated

    dm_out:
        (NIndex) the RDM stored in the cache

    l_amplitudes:
        (dict) Contains the Lambda amplitudes

    factor:
        (float, int) some scaling factor for RDM block

    amplitudes:
        (dict) Contains the CC amplitudes

    args, kargs:
        Used to resolve t_p amplitudes
    """
    #
    # assign T_p to T_2
    #
    t_p = unmask("t_p", *args, **kwargs)
    set_seniority_0(amplitudes, t_p)
    #
    # Calculate LCCSD RDM
    #
    compute_2dm_lccsd(
        select, dm_out, l_amplitudes, amplitudes, factor, *args, **kwargs
    )
    #
    # Calcualte remaining terms
    #
    if select in ["qQQp", "qQPq"]:
        compute_2dm_pccdlccsd_qQQp(
            dm_out, l_amplitudes, amplitudes, factor, *args, **kwargs
        )
    elif select in ["pQPp", "qPPp"]:
        compute_2dm_pccdlccsd_pQPp(
            dm_out, l_amplitudes, amplitudes, factor, *args, **kwargs
        )
    elif select in ["qQPp"]:
        compute_2dm_pccdlccsd_qQPp(
            dm_out, l_amplitudes, amplitudes, factor, *args, **kwargs
        )
    #
    # remove T_p from T_2
    #
    set_seniority_0(amplitudes, 0.0)


def compute_3dm_pccdlccsd(
    select, dm_out, l_amplitudes, amplitudes, factor, *args, **kwargs
):
    """Computes specific block of N-RDM.

    **Arguments:**

    select:
        (str) the block to be calculated

    dm_out:
        (NIndex) the RDM stored in the cache

    l_amplitudes:
        (dict) Contains the Lambda amplitudes

    factor:
        (float, int) some scaling factor for RDM block

    amplitudes:
        (dict) Contains the CC amplitudes

    args, kwargs:
        Used to resolve t_p amplitudes
    """
    #
    # assign T_p to T_2
    #
    t_p = unmask("t_p", *args, **kwargs)
    set_seniority_0(amplitudes, t_p)
    #
    # Calculate LCCSD RDM
    #
    compute_3dm_lccsd(
        select, dm_out, l_amplitudes, amplitudes, factor, *args, **kwargs
    )
    #
    # Calculate remaining terms
    #
    if select in ["qPQQPp"]:
        compute_3dm_pccdlccsd_qPQQPp(
            dm_out, l_amplitudes, amplitudes, factor, *args, **kwargs
        )
    #
    # remove T_p from T_2
    #
    set_seniority_0(amplitudes, 0.0)


def compute_4dm_pccdlccsd(
    select, dm_out, l_amplitudes, amplitudes, factor, *args, **kwargs
):
    """Computes specific block of N-RDM.

    **Arguments:**

    select:
        (str) the block to be calculated

    dm_out:
        (NIndex) the RDM stored in the cache

    l_amplitudes:
        (dict) Contains the Lambda amplitudes

    factor:
        (float, int) some scaling factor for RDM block

    amplitudes:
        (dict) Contains the CC amplitudes

    args, kwargs:
        Used to resolve t_p amplitudes
    """
    #
    # assign T_p to T_2
    #
    t_p = unmask("t_p", *args, **kwargs)
    set_seniority_0(amplitudes, t_p)
    #
    # Calculate LCCSD RDM
    #
    compute_4dm_lccsd(
        select, dm_out, l_amplitudes, amplitudes, factor, *args, **kwargs
    )
    #
    # remove T_p from T_2
    #
    set_seniority_0(amplitudes, 0.0)


def compute_1dm_pccdlccsd_pq(
    dm_out, l_amplitudes, amplitudes, factor, *args, **kwargs
):
    """Computes specific block of N-RDM.

    **Arguments:**

    dm_out:
        (NIndex) the RDM stored in the cache

    l_amplitudes:
        (dict) Contains the Lambda amplitudes

    factor:
        (float, int) some scaling factor for RDM block

    amplitudes:
        (dict) Contains the CC amplitudes

    args, kwargs:
        Used to resolve t_p amplitudes
    """
    t_1 = amplitudes["t_1"]
    t_2 = amplitudes["t_2"]
    l_2 = l_amplitudes["l_2"]
    t_p = unmask("t_p", *args, **kwargs)
    occ = t_2.nbasis
    #
    # Temporary output
    #
    tmp_ov = t_p.new()
    # 4d -lifmf . tma . cif -> iaf . cif
    tmp = l_2.contract("abcb,ce->aeb", t_1, out=None)
    tmp.contract("abc,ac->ab", t_p, tmp_ov, factor=-0.5)
    # 4e -lnena . tie . cna -> ian . cna
    tmp = l_2.contract("abac,eb->eca", t_1, out=None)
    tmp.contract("abc,cb->ab", t_p, tmp_ov, factor=-0.5)
    # 4f ljame . tme . cja -> ja . cja
    tmp = l_2.contract("abcd,cd->ab", t_1, out=None)
    tmp_ov.iadd_mult(t_p, tmp, 0.5)
    #
    # Combine all blocks and scale
    #
    options = {"factor": factor, "end0": occ, "begin1": occ}
    dm_out.iadd(tmp_ov, **options)


def compute_2dm_pccdlccsd_qQQp(
    dm_out, l_amplitudes, amplitudes, factor, *args, **kwargs
):
    """Computes specific block of N-RDM.

    **Arguments:**

    dm_out:
        (NIndex) the RDM stored in the cache

    l_amplitudes:
        (dict) Contains the Lambda amplitudes

    factor:
        (float, int) some scaling factor for RDM block

    amplitudes:
        (dict) Contains the CC amplitudes

    args, kwargs:
        Used to resolve t_p amplitudes
    """
    t_1 = amplitudes["t_1"]
    t_2 = amplitudes["t_2"]
    l_2 = l_amplitudes["l_2"]
    t_p = unmask("t_p", *args, **kwargs)
    occ = t_2.nbasis
    #
    # Temporary output
    #
    tmp_ov = t_p.new()
    # 3
    # b
    tmp = l_2.contract("abac,ac->ab", t_1, out=None)
    tmp_ov.iadd_mult(tmp, t_p, 0.5)
    # c
    tmp = l_2.contract("abcb,cd->abd", t_1, out=None)
    tmp.contract("abc,ab->ac", t_p, tmp_ov, factor=0.5)
    # d
    tmp = l_2.contract("abcd,ab->cd", t_1, out=None)
    tmp_ov.iadd_mult(tmp, t_p, -0.5, False)
    #
    # lower RDM's:
    # 2 ja
    # d -lifmf . tma . cif -> iaf . cif
    tmp = l_2.contract("abcb,ce->aeb", t_1, out=None)
    tmp.contract("abc,ac->ab", t_p, tmp_ov, factor=-0.5)
    # e -lnena . tie . cna -> ian . cna
    tmp = l_2.contract("abac,eb->eca", t_1, out=None)
    tmp.contract("abc,cb->ab", t_p, tmp_ov, factor=-0.5)
    # f ljame . tme . cja ->  ja . cja
    tmp = l_2.contract("abcd,cd->ab", t_1, out=None)
    tmp_ov.iadd_mult(tmp, t_p, 0.5)
    #
    # Combine all blocks and scale
    #
    options = {"factor": factor, "end0": occ, "begin1": occ}
    dm_out.iadd(tmp_ov, **options)


def compute_2dm_pccdlccsd_pQPp(
    dm_out, l_amplitudes, amplitudes, factor, *args, **kwargs
):
    """Computes specific block of N-RDM.

    **Arguments:**

    dm_out:
        (NIndex) the RDM stored in the cache

    l_amplitudes:
        (dict) Contains the Lambda amplitudes

    factor:
        (float, int) some scaling factor for RDM block

    amplitudes:
        (dict) Contains the CC amplitudes

    args, kwargs:
        Used to resolve t_p amplitudes
    """
    t_1 = amplitudes["t_1"]
    t_2 = amplitudes["t_2"]
    l_2 = l_amplitudes["l_2"]
    t_p = unmask("t_p", *args, **kwargs)
    occ = t_2.nbasis
    #
    # Temporary output
    #
    tmp_ov = t_p.new()
    # b lnane,je->naj, naj,na->aj
    tmp = l_2.contract("abac,dc->abd", t_1, out=None)
    tmp.contract("abc,ab->cb", t_p, tmp_ov, factor=-0.5)
    # c -ljama . tma . cif -> iaf . cif
    tmp = l_2.contract("abcb,cb->ab", t_1, out=None)
    tmp_ov.iadd_mult(tmp, t_p, -0.5, False)
    # d lmeja,me->ja
    tmp = l_2.contract("abcd,ab->cd", t_1, out=None)
    tmp_ov.iadd_mult(tmp, t_p, 0.5, False)
    #
    # Combine all blocks and scale
    #
    options = {"factor": factor, "end0": occ, "begin1": occ}
    dm_out.iadd(tmp_ov, **options)


def compute_2dm_pccdlccsd_qQPp(
    dm_out, l_amplitudes, amplitudes, factor, *args, **kwargs
):
    """Computes specific block of N-RDM.

    **Arguments:**

    dm_out:
        (NIndex) the RDM stored in the cache

    l_amplitudes:
        (dict) Contains the Lambda amplitudes

    factor:
        (float, int) some scaling factor for RDM block

    amplitudes:
        (dict) Contains the CC amplitudes

    args, kwargs:
        Used to resolve t_p amplitudes
    """
    t_1 = amplitudes["t_1"]
    t_2 = amplitudes["t_2"]
    l_1 = l_amplitudes["l_1"]
    l_2 = l_amplitudes["l_2"]
    t_p = unmask("t_p", *args, **kwargs)
    occ = t_2.nbasis
    #
    # Temporary output
    #
    tmp_ov = t_p.new()
    # 3
    # a
    f_ac = t_p.copy()
    f_ac.imul(l_1)
    f_ac.imul(t_1)
    tmp_ov.iadd(f_ac, 1.0)
    # b
    tmp = t_1.contract("ab,ab->a", l_1, out=None)
    tmp_1 = t_p.contract("ab,a->ab", tmp, factor=-1.0)
    tmp_ov.iadd(tmp_1)
    # c
    tmp = t_1.contract("ab,ab->b", l_1, out=None)
    tmp_1 = t_p.contract("ab,b->ab", tmp, out=None, factor=-1.0)
    tmp_ov.iadd(tmp_1)
    # d
    tmp = t_2.contract("abcd,abcd->ab", l_2, out=None)
    tmp_ov.iadd_mult(t_p, tmp, 1.0)
    # e
    tmp = t_2.contract("abcd,abcd->ad", l_2, out=None)
    tmp_ov.iadd_mult(t_p, tmp, 1.0)
    # f
    tmp = t_2.contract("abcd,abcd->a", l_2, out=None)
    tmp_1 = t_p.contract("ab,a->ab", tmp, out=None, factor=-1.0)
    tmp_ov.iadd(tmp_1)
    # g
    tmp = l_2.contract("abcb,ab->ac", t_p, out=None)
    t_2.contract("abcb,ac->ab", tmp, tmp_ov, factor=-1.0)
    # h
    tmp = t_2.contract("abcd,abcd->b", l_2, out=None)
    tmp_1 = t_p.contract("ab,b->ab", tmp, out=None, factor=-1.0)
    tmp_ov.iadd(tmp_1)
    # i
    tmp = l_2.contract("abac,ab->bc", t_p, out=None)
    t_2.contract("abac,bc->ab", tmp, tmp_ov, factor=-1.0)
    # j
    tmp = t_2.contract("abcb,adcd->bd", l_2, out=None)
    tmp.contract("ab,cb->ca", t_p, tmp_ov, factor=0.5)
    # k
    tmp = t_2.contract("abac,dbdc->ad", l_2, out=None)
    tmp.contract("ab,bc->ac", t_p, tmp_ov, factor=0.5)
    #
    # Combine all blocks and scale
    #
    options = {"factor": factor, "end0": occ, "begin1": occ}
    dm_out.iadd(tmp_ov, **options)


def compute_3dm_pccdlccsd_qPQQPp(
    dm_out, l_amplitudes, amplitudes, factor, *args, **kwargs
):
    """Computes specific block of N-RDM.

    **Arguments:**

    dm_out:
        (NIndex) the RDM stored in the cache

    l_amplitudes:
        (dict) Contains the Lambda amplitudes

    factor:
        (float, int) some scaling factor for RDM block

    amplitudes:
        (dict) Contains the CC amplitudes

    args, kwargs:
        Used to resolve t_p amplitudes
    """
    t_1 = amplitudes["t_1"]
    t_2 = amplitudes["t_2"]
    l_1 = l_amplitudes["l_1"]
    l_2 = l_amplitudes["l_2"]
    t_p = unmask("t_p", *args, **kwargs)
    occ = t_2.nbasis
    #
    # Temporary output
    #
    tmp_ov = t_p.new()
    # 1
    # a
    tmp_ov.iadd_mult(l_1, t_p, -0.5)
    # b
    tmp = l_2.contract("abcb,ab->cb", t_1, out=None)
    tmp_ov.iadd_mult(tmp, t_p, 0.5)
    # c
    tmp = l_2.contract("abac,ac->ab", t_1, out=None)
    tmp_ov.iadd_mult(tmp, t_p, 0.5)
    # d
    tmp = l_2.contract("abcd,cd->ab", t_1, out=None)
    tmp_ov.iadd_mult(tmp, t_p, -0.5)
    #
    # lower RDM's:
    # 2 jAAa
    # b lnane,je->naj, naj,na->aj
    tmp = l_2.contract("abac,dc->abd", t_1, out=None)
    tmp.contract("abc,ab->cb", t_p, tmp_ov, factor=-0.5)
    # c -ljama . tma . cif -> iaf . cif
    tmp = l_2.contract("abcb,cb->ab", t_1, out=None)
    tmp_ov.iadd_mult(tmp, t_p, -0.5)
    # d lmeja,me->ja
    tmp = l_2.contract("abcd,ab->cd", t_1, out=None)
    tmp_ov.iadd_mult(tmp, t_p, 0.5)
    #
    # Combine all blocks and scale
    #
    options = {"factor": factor, "end0": occ, "begin1": occ}
    dm_out.iadd(tmp_ov, **options)


###############################################################################
# Utility function for pCCD-based Density Matrices
###############################################################################


def set_seniority_0(amplitudes, value):
    """Overwrite seniority zero amplitudes of t_2 with some value.

    **Arguments:**

    amplitudes:
        (dict) containing t_2 amplitudes

    value:
        (float or array or FourIndex) used to substitute seniority zero amplitudes
    """
    t_2 = amplitudes["t_2"]
    occ = t_2.nbasis
    vir = t_2.nbasis1
    ind1, ind2 = np.indices((occ, vir))
    indices = [ind1, ind2, ind1, ind2]
    t_2.assign(value, indices)
