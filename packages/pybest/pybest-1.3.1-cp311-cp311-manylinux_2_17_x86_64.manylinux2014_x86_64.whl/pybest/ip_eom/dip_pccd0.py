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
"""Double Ionization Potential Equation of Motion Coupled Cluster implementations
   for a pCCD reference function and 0 unpaired electrons (S_z=0.0 components)

   Variables used in this module:
    :ncore:     number of frozen core orbitals
                (abbreviated as nc)
    :nocc:      number of occupied orbitals in the principle configuration
    :nacto:     number of active occupied orbitals in the principle configuration
                (abbreviated as no)
    :nvirt:     number of virtual orbitals in the principle configuration
    :nactv:     number of active virtual orbitals in the principle configuration
                (abbreviated as nv)
    :nbasis:    total number of basis functions
    :nact:      total number of active orbitals (nacto+nactv)
                (abbreviated as na)
    :e_dip:     the energy correction for IP
    :civ_dip:   the CI amplitudes from a given EOM model
    :rij:       2 holes operator
    :rijkc:     3 holes 1 particle operator (same spin)
    :rijKC:     3 holes 1 particle operator (opposite spin)
    :cia:       the pCCD pair amplitudes (T_p)

   Indexing convention:
    :i,j,k,..: occupied orbitals of principle configuration
    :a,b,c,..: virtual orbitals of principle configuration
    :p,q,r,..: general indices (occupied, virtual)

   Abbreviations used (if not mentioned in doc-strings; all ERI are in
   physicists' notation):
    :<pq||rs>: <pq|rs>-<pq|sr>
    :2h:    2 holes (also used as index _2)
    :3h:    3 holes (also used as indes _3)
    :aa:    same-spin component
    :ab:    opposite-spin component
"""

from pybest.auxmat import get_fock_matrix
from pybest.ip_eom.dip_base import RDIPCC0
from pybest.log import timer


class RDIPpCCD0(RDIPCC0):
    """
    Restricted Double Ionization Potential Equation of Motion Coupled Cluster
    class restricted to Double IP for a pCCD reference function and 0 unpaired
    electrons (S_z=0.0 components)

    This class defines only the function that are unique for the DIP-pCCD model
    with 0 unpaired electron:

        * set_hamiltonian (calculates effective Hamiltonian -- at most O(o2v2))
        * compute_h_diag (pre-conditioner used by Davidson)
        * build_subspace_hamiltonian (subspace to be diagonalized)
    """

    long_name = "Double Ionization Potential Equation of Motion pair Coupled Cluster Doubles"
    acronym = "DIP-EOM-pCCD"
    reference = "pCCD"
    order = "DIP"
    alpha = 0

    @timer.with_section("Hdiag DIPpCCD0")
    def compute_h_diag(self, *args):
        """Diagonal approximation to Hamiltonian for Sz=0.0"""
        cia = self.checkpoint["t_p"]
        h_diag = self.lf.create_one_index(self.dimension, label="h_diag")
        #
        # Get effective Hamiltonian terms
        #
        no = self.occ_model.nacto[0]
        x1im = self.from_cache("x1im")
        goooo = self.from_cache("goooo")
        #
        # intermediates
        #
        x1im_diag = x1im.copy_diagonal()
        gij = goooo.contract("abab->ab", out=None)
        goovv = self.from_cache("goovv")
        gjjdd = goovv.contract("aabb->ab", out=None)
        if self.dump_cache:
            self.cache.dump("goovv")
        #
        # H_iJ,iJ
        #
        h_iJ = self.lf.create_two_index(no, no)
        #
        # x1im(i,i)
        #
        h_iJ.iadd_expand_one_to_two("a->ab", x1im_diag)
        h_iJ.iadd_expand_one_to_two("b->ab", x1im_diag)
        #
        # <ij|ij> + <ii|dd> cid dij
        #
        h_iJ.iadd(gij)
        tmp = gjjdd.contract("ab,ab->a", cia, out=None)
        h_iJ.iadd_diagonal(tmp)
        #
        # assign using mask
        #
        h_diag.assign(h_iJ.ravel(), end0=no * no)
        #
        # H_iJkc,iJkc and H_iJKC,iJKC
        #
        if self.nhole > 2:
            self.get_3_hole_terms_h_diag(h_diag)
        return h_diag

    def get_3_hole_terms_h_diag(self, h_diag):
        """Determine all contributions containing three hole operators for
        the spin-dependent representation:
            * H_iJkc,iJkc
            * H_iJKC,iJKC

        **Arguments:**

        h_diag:
            The diagonal elements of the Hamiltonian
        """
        cia = self.checkpoint["t_p"]
        #
        # Get effective Hamiltonian terms
        #
        no, nv = self.occ_model.nacto[0], self.occ_model.nactv[0]
        x1im = self.from_cache("x1im")
        goooo = self.from_cache("goooo")
        x1cd = self.from_cache("x1cd")
        xjkmN = self.from_cache("xjkmN")
        #
        # intermediates
        #
        lij = goooo.contract("abab->ab", out=None)
        goooo.contract("abba->ab", lij, factor=-1.0)
        x1im_diag = x1im.copy_diagonal()
        x1cd_diag = x1cd.copy_diagonal()
        xkcmd = self.from_cache("xkcmd")
        xkckc = xkcmd.contract("abab->ab", out=None)
        if self.dump_cache:
            self.cache.dump("xkcmd")
        xjkjK = xjkmN.contract("abab->ab", out=None)
        xjcmD = self.from_cache("xjcmD")
        xjcjC = xjcmD.contract("abab->ab", out=None)
        if self.dump_cache:
            self.cache.dump("xjcmD")
        goovv = self.from_cache("goovv")
        gjjdd = goovv.contract("aabb->ab", out=None)
        if self.dump_cache:
            self.cache.dump("goovv")
        #
        # get ranges
        #
        end_2h = no * no
        end_3h = end_2h + no * (no - 1) // 2 * no * nv
        #
        # H_iJkc,iJkc
        #
        H_iJkc = self.denself.create_four_index(no, no, no, nv)
        #
        # x1im(k,k)
        #
        H_iJkc.iadd_expand_one_to_four("2", x1im_diag, factor=1.0)
        #
        # 0.5 x1im(j,j)
        #
        H_iJkc.iadd_expand_one_to_four("1", x1im_diag, factor=0.5)
        #
        # 0.5 x1cd(c,c)
        #
        H_iJkc.iadd_expand_one_to_four("3", x1cd_diag, factor=0.5)
        #
        # xkcmd(k,c,k,c)
        #
        H_iJkc.iadd_expand_two_to_four("cd->abcd", xkckc, factor=1.0)
        #
        # 0.5 xjcmD(j,c,j,c)
        #
        H_iJkc.iadd_expand_two_to_four("bd->abcd", xjcjC, factor=0.5)
        #
        # xjkmN(j,k,j,k)
        #
        H_iJkc.iadd_expand_two_to_four("bc->abcd", xjkjK, factor=1.0)
        #
        # 0.25 lij(i,k)
        #
        H_iJkc.iadd_expand_two_to_four("ac->abcd", lij, factor=0.25)
        #
        # -gjjcc cjc djk
        #
        gjjdd_ = gjjdd.copy()
        gjjdd_.imul(cia)
        # jc -> jjc
        tmp3 = self.lf.create_three_index(no, no, nv)
        tmp3.iadd_expand_two_to_three("ab->aab", gjjdd_)
        H_iJkc.iadd_expand_three_to_four("0", tmp3, factor=-1.0)
        #
        # Pki (ijkc)
        #
        H_iJkc.iadd_transpose((2, 1, 0, 3))
        #
        # assign using mask
        #
        h_diag.assign(
            H_iJkc, begin0=end_2h, end0=end_3h, ind1=self.get_mask(True)
        )
        #
        # H_iJKC,iJKC
        #
        H_iJkc.clear()
        #
        # x1im(k,k)
        #
        H_iJkc.iadd_expand_one_to_four("2", x1im_diag, factor=1.0)
        #
        # 0.5 x1im(i,i)
        #
        H_iJkc.iadd_expand_one_to_four("0", x1im_diag, factor=0.5)
        #
        # 0.5 x1cd(c,c)
        #
        H_iJkc.iadd_expand_one_to_four("3", x1cd_diag, factor=0.5)
        #
        # xkcmd(k,c,k,c)
        #
        H_iJkc.iadd_expand_two_to_four("cd->abcd", xkckc, factor=1.0)
        #
        # 0.5 xjcmD(i,c,i,c)
        #
        H_iJkc.iadd_expand_two_to_four("ad->abcd", xjcjC, factor=0.5)
        #
        # xjkmN(i,k,i,k)
        #
        H_iJkc.iadd_expand_two_to_four("ac->abcd", xjkjK, factor=1.0)
        #
        # 0.25 lij(j,k)
        #
        H_iJkc.iadd_expand_two_to_four("bc->abcd", lij, factor=0.25)
        #
        # -giicc cic dik
        #
        H_iJkc.iadd_expand_three_to_four("1", tmp3, factor=-1.0)
        #
        # Permutation (kj)
        #
        H_iJkc.iadd_transpose((0, 2, 1, 3), factor=1.0)
        #
        # assign using mask
        #
        h_diag.assign(H_iJkc, begin0=end_3h, ind1=self.get_mask(False))

    @timer.with_section("SubH DIPpCCD0")
    def build_subspace_hamiltonian(self, b_vector, h_diag, *args):

        """
        Used by the Davidson module to construct subspace Hamiltonian for S_z=0.0

        **Arguments:**

        b_vector:
            (OneIndex object) contains current approximation to CI coefficients

        h_diag:
            Diagonal Hamiltonian elements required in davidson module (not used
            here)

        args:
            Set of arguments passed by the Davidson module (not used here)
        """
        cia = self.checkpoint["t_p"]
        #
        # Get effective Hamiltonian terms
        # we load only arrays of a maximum size of o3v, everything bigger than
        # o2v2 is dumped/loaded to/from disk if self.dump_cache = True
        #
        no = self.occ_model.nacto[0]
        x1im = self.from_cache("x1im")
        goooo = self.from_cache("goooo")
        #
        # Final index of 2 hole terms
        #
        end_2h = no * no
        #
        # Calculate sigma vector = (H.b_vector)
        #
        # sigma/b_vector for 2 holes
        # output
        s_2 = self.lf.create_two_index(no, no)
        to_s_2 = {"out": s_2, "select": self.tco, "clear": False}
        sigma = self.lf.create_one_index(self.dimension)
        # input, assign R_iJ
        b_2 = self.lf.create_two_index(no, no)
        b_2.assign(b_vector, end2=end_2h)
        #
        # R_iJ
        #
        # (1) x1im(i,m) rmJ / rim x1im(j,m)
        #
        x1im.contract("ab,bc->ac", b_2, **to_s_2)
        b_2.contract("ab,cb->ac", x1im, **to_s_2)
        #
        # (2) <ij|mn> rmN + <mn|dd> rmN cid dij
        #
        goooo.contract("abcd,cd->ab", b_2, **to_s_2)
        # (cid, d) -> i
        goovv = self.from_cache("goovv")
        tmpd = goovv.contract("abcc,ab->c", b_2, out=None)
        if self.dump_cache:
            self.cache.dump("goovv")
        tmp = cia.contract("ab,b->a", tmpd, out=None)
        s_2.iadd_diagonal(tmp)
        del tmp, tmpd
        #
        # R_iJkc/R_iJKC including coupling terms
        #
        if self.nhole > 2:
            self.get_3_hole_terms(b_2, b_vector, s_2, sigma)
        #
        # Assign to sigma vector
        #
        sigma.assign(s_2.ravel(), end0=end_2h)
        return sigma

    def get_3_hole_terms(self, b_2, b_vector, s_2, sigma):
        """Determine all contributions containing three hole operators for
        the spin-dependent representation:
            * coupling terms to R_iJ
            * R_iJkc
            * R_iJKC

        **Arguments:**

        b_2, b_vector:
            b vectors used in Davidson diagonalization

        s_2, sigma:
            sigma vectors used in Davidson diagonalization
        """
        #
        # Get effective Hamiltonian terms
        #
        no, nv = self.occ_model.nacto[0], self.occ_model.nactv[0]
        #
        # Calculate sigma vector = (H.b_vector)_kc
        # sigma/b_vector for 3 holes
        # output
        s_3 = self.denself.create_four_index(no, no, no, nv)
        # input
        b_3aa = self.denself.create_four_index(no, no, no, nv)
        b_3ab = self.denself.create_four_index(no, no, no, nv)
        #
        # Final indices of 2 and 3 hole operator blocks
        #
        end_2h = no * no
        end_3h = end_2h + no * no * (no - 1) // 2 * nv
        #
        # assign R_iJkc
        #
        mask = self.get_index_of_mask(True)
        b_3aa.assign(b_vector, ind=mask, begin4=end_2h, end4=end_3h)
        # account for symmetry (ik)
        b_3aa.iadd_transpose((2, 1, 0, 3), factor=-1.0)
        #
        # assign R_iJKC
        #
        mask = self.get_index_of_mask(False)
        b_3ab.assign(b_vector, ind=mask, begin4=end_3h)
        # account for symmetry (JK)
        b_3ab.iadd_transpose((0, 2, 1, 3), factor=-1.0)
        #
        # Get coupling terms to R_iJ
        #
        self.get_3_hole_r_iJ_terms(b_3aa, b_3ab, s_2)
        #
        # R_iJkc
        #
        self.get_3_hole_r_3ss_terms(b_2, b_3aa, b_3ab, s_3)
        # Assign to sigma vector using mask
        sigma.assign(s_3, begin0=end_2h, end0=end_3h, ind1=self.get_mask(True))
        #
        # R_iJKC
        #
        self.get_3_hole_r_3os_terms(b_2, b_3aa, b_3ab, s_3)
        # Assign to sigma vector using mask
        sigma.assign(s_3, begin0=end_3h, ind1=self.get_mask(False))

    def get_3_hole_r_iJ_terms(self, b_3aa, b_3ab, s_2):
        """Determine all contributions containing two particle operators:
            * coupling terms to R_iJ

        **Arguments:**

        b_3aa, b_3ab:
            b vectors of different R operators used in Davidson diagonalization

        s_2:
            sigma vector corresponding to R_iJ used in Davidson diagonalization
        """
        to_s_2 = {"out": s_2, "select": self.tco, "clear": False}
        #
        # Get effective Hamiltonian terms
        #
        fock = self.from_cache("fock")
        gooov = self.from_cache("gooov")
        #
        # get ranges
        #
        ov4 = self.get_range("ov", start=4)
        #
        # (3) fmd riJmd + fmd riJMD
        #
        b_3aa.contract("abcd,cd->ab", fock, **to_s_2, **ov4)
        b_3ab.contract("abcd,cd->ab", fock, **to_s_2, **ov4)
        #
        # (4) -0.5<nm||jd> riNMD -0.5<nm||id> rnJmd -<nm|jd> riNmd - <nm|id> rnJMD
        #
        gooov.contract("abcd,eabd->ec", b_3ab, **to_s_2, factor=-0.5)
        gooov.contract("abcd,ebad->ec", b_3ab, **to_s_2, factor=0.5)
        gooov.contract("abcd,aebd->ce", b_3aa, **to_s_2, factor=-0.5)
        gooov.contract("abcd,bead->ce", b_3aa, **to_s_2, factor=0.5)
        gooov.contract("abcd,eabd->ec", b_3aa, **to_s_2, factor=-1.0)
        gooov.contract("abcd,aebd->ce", b_3ab, **to_s_2, factor=-1.0)

    def get_3_hole_r_3ss_terms(self, b_2, b_3aa, b_3ab, s_3):
        """Determine all contributions containing two particle operators:
            * R_iJkc

        **Arguments:**

        b_3aa, b_3ab:
            b vectors of different R operators used in Davidson diagonalization

        s_3:
            sigma vector corresponding to R_iJkc used in Davidson diagonalization
        """
        cia = self.checkpoint["t_p"]
        s_3.clear()
        to_s_3 = {"out": s_3, "select": self.tco, "clear": False}
        tco = {"select": self.tco}
        #
        # Get effective Hamiltonian terms
        # we load only arrays of a maximum size of o3v, everything bigger than
        # o2v2 is dumped/loaded to/from disk if self.dump_cache = True
        #
        no, nv = self.occ_model.nacto[0], self.occ_model.nactv[0]
        x1im = self.from_cache("x1im")
        goooo = self.from_cache("goooo")
        x1cd = self.from_cache("x1cd")
        gooov = self.from_cache("gooov")
        xjkcm = self.from_cache("xjkcm")
        xikcm = self.from_cache("xikcm")
        xjkmN = self.from_cache("xjkmN")
        # All terms with P(ik)
        # (1) xjkcm riM + xikcm rmJ
        #
        xjkcm.contract("abcd,ed->eabc", b_2, **to_s_3)
        xikcm.contract("abcd,de->aebc", b_2, **to_s_3)
        #
        # (3) x1im(k,m) riJmc + 0.5 x1im(j,m) riMkc
        #
        b_3aa.contract("abcd,ec->abed", x1im, **to_s_3)
        b_3aa.contract("abcd,eb->aecd", x1im, **to_s_3, factor=0.5)
        #
        # (4) 0.5 x1cd(c,d) riJkd
        #
        b_3aa.contract("abcd,ed->abce", x1cd, **to_s_3, factor=0.5)
        #
        # (5) xkcmd riJmd + xkcMD riJMD + 0.5 xjcmD riMkd
        #
        xkcmd = self.from_cache("xkcmd")
        b_3aa.contract("abcd,efcd->abef", xkcmd, **to_s_3)
        if self.dump_cache:
            self.cache.dump("xkcmd")
        xkcMD = self.from_cache("xkcMD")
        b_3ab.contract("abcd,efcd->abef", xkcMD, **to_s_3)
        if self.dump_cache:
            self.cache.dump("xkcMD")
        xjcmD = self.from_cache("xjcmD")
        b_3aa.contract("abcd,efbd->aecf", xjcmD, **to_s_3, factor=0.5)
        if self.dump_cache:
            self.cache.dump("xjcmD")
        #
        # (6) xjkmN riMnc + 0.25 <ik||mn> rmJnc
        #
        b_3aa.contract("abcd,efbc->aefd", xjkmN, **to_s_3)
        goooo.contract("abcd,cedf->aebf", b_3aa, **to_s_3, factor=0.25)
        goooo.contract("abcd,cedf->beaf", b_3aa, **to_s_3, factor=-0.25)
        #
        # djk terms
        #
        tmpic = self.lf.create_two_index(no, nv)
        tmpijc = self.lf.create_three_index(no, no, nv)
        #
        # (2) <ml|ic> rmL cjc djk -> (ic, cjc) -> (ijc)
        #
        gooov.contract("abcd,ab->cd", b_2, tmpic, select=self.tco)
        #
        # (9) -0.5<nm||cd> riNMD cjc dkj -> (ic, cjc) -> (ijc)
        #     -   <nm| cd> riNmd cjc dkj -> (ic, cjc) -> (ijc)
        #
        goovv = self.from_cache("goovv")
        b_3ab.contract("abcd,bced->ae", goovv, tmpic, factor=-0.5, **tco)
        b_3ab.contract("abcd,bcde->ae", goovv, tmpic, factor=0.5, **tco)
        b_3aa.contract("abcd,bced->ae", goovv, tmpic, factor=-1.0, **tco)
        if self.dump_cache:
            self.cache.dump("goovv")
        #
        # tmpic cjc -> (ijc)
        #
        tmpic.contract("ac,bc->abc", cia, tmpijc)
        del tmpic
        #
        # Expand indices
        #
        s_3.iadd_expand_three_to_four("abc->abbc", tmpijc)
        #
        # Permutation P(ki)
        #
        s_3.iadd_transpose((2, 1, 0, 3), factor=-1.0)

    def get_3_hole_r_3os_terms(self, b_2, b_3aa, b_3ab, s_3):
        """Determine all contributions containing two particle operators:
            * R_iJKC

        **Arguments:**

        b_3aa, b_3ab:
            b vectors of different R operators used in Davidson diagonalization

        s_3:
            sigma vector corresponding to R_iJKC used in Davidson diagonalization
        """
        cia = self.checkpoint["t_p"]
        s_3.clear()
        to_s_3 = {"out": s_3, "select": self.tco, "clear": False}
        tco = {"select": self.tco}
        #
        # Get effective Hamiltonian terms
        #
        no, nv = self.occ_model.nacto[0], self.occ_model.nactv[0]
        x1im = self.from_cache("x1im")
        goooo = self.from_cache("goooo")
        x1cd = self.from_cache("x1cd")
        gooov = self.from_cache("gooov")
        xjkcm = self.from_cache("xjkcm")
        xikcm = self.from_cache("xikcm")
        xjkmN = self.from_cache("xjkmN")
        # All terms with P(jk)
        # (1) xjkcm(ikcm) rmJ + xikcm(jkcm) rim
        #
        xjkcm.contract("abcd,de->aebc", b_2, **to_s_3)
        xikcm.contract("abcd,ed->eabc", b_2, **to_s_3)
        #
        # (3) x1im(k,m) riJMC + 0.5 x1im(i,m) rmJCK
        #
        b_3ab.contract("abcd,ec->abed", x1im, **to_s_3)
        b_3ab.contract("abcd,ea->ebcd", x1im, **to_s_3, factor=0.5)
        #
        # (4) 0.5 x1cd(c,d) riJKD
        #
        b_3ab.contract("abcd,ed->abce", x1cd, **to_s_3, factor=0.5)
        #
        # (5) xkcmd riJMD + xkcMD riJmd + 0.5 xjcmD(icmd) rmJKD
        #
        xkcmd = self.from_cache("xkcmd")
        b_3ab.contract("abcd,efcd->abef", xkcmd, **to_s_3)
        if self.dump_cache:
            self.cache.dump("xkcmd")
        xkcMD = self.from_cache("xkcMD")
        b_3aa.contract("abcd,efcd->abef", xkcMD, **to_s_3)
        if self.dump_cache:
            self.cache.dump("xkcMD")
        xjcmD = self.from_cache("xjcmD")
        b_3ab.contract("abcd,efad->ebcf", xjcmD, **to_s_3, factor=0.5)
        if self.dump_cache:
            self.cache.dump("xjcmD")
        #
        # (6) xjkmN(ikmn) rmJNC + 0.25 <jk||mn> riMNC
        #
        b_3ab.contract("abcd,efac->ebfd", xjkmN, **to_s_3)
        goooo.contract("abcd,ecdf->eabf", b_3ab, **to_s_3, factor=0.25)
        goooo.contract("abcd,edcf->eabf", b_3ab, **to_s_3, factor=-0.25)
        #
        # dik terms
        #
        tmpic = self.lf.create_two_index(no, nv)
        tmpijc = self.lf.create_three_index(no, no, nv)
        #
        # (2) <ml|jc> rlM cic dik -> (jc, cic) -> (ijc)
        #
        gooov.contract("abcd,ba->cd", b_2, tmpic, **tco)
        #
        # (9) -0.5<nm||cd> rnJmd cic dik -> (jc, cic) -> (ijc)
        #     -   <nm| cd> rnJMD cic dik -> (jc, cic) -> (ijc)
        #
        goovv = self.from_cache("goovv")
        b_3aa.contract("abcd,aced->be", goovv, tmpic, factor=-0.5, **tco)
        b_3aa.contract("abcd,acde->be", goovv, tmpic, factor=0.5, **tco)
        b_3ab.contract("abcd,aced->be", goovv, tmpic, factor=-1.0, **tco)
        if self.dump_cache:
            self.cache.dump("goovv")
        #
        # tmpic(jc) cic -> (ijc)
        #
        cia.contract("ac,bc->abc", tmpic, tmpijc)
        #
        # Expand indices
        #
        s_3.iadd_expand_three_to_four("abc->abac", tmpijc)
        #
        # Permutation P(kj)
        #
        s_3.iadd_transpose((0, 2, 1, 3), factor=-1.0)

    @timer.with_section("SetH DIPpCCD0")
    def set_hamiltonian(self, mo1, mo2):
        """Derive all effective Hamiltonian terms. Like
        fock_pq/f:     mo1_pq + sum_m(2<pm|qm> - <pm|mq>)

        **Arguments:**

        mo1, mo2
             one- and two-electron integrals.
        """
        cia = self.checkpoint["t_p"]
        #
        # get ranges
        #
        no, nv, na = (
            self.occ_model.nacto[0],
            self.occ_model.nactv[0],
            self.occ_model.nact[0],
        )
        oooo = self.get_range("oooo")
        oovv = self.get_range("oovv")
        #
        # Inactive Fock matrix
        #
        fock = self.init_cache("fock", na, na)
        get_fock_matrix(fock, mo1, mo2, no)
        #
        # goovv (used also for other contractions below)
        #
        goovv = self.init_cache("goovv", no, no, nv, nv)
        mo2.contract(
            "abcd->abcd",
            out=goovv,
            factor=1.0,
            clear=True,
            **oovv,
            select="einsum",
        )
        #
        # x1im
        #
        x1im = self.init_cache("x1im", no, no)
        # -fim
        x1im.iadd(fock, -1.0, end2=no, end3=no)
        # -<im|ee> cie
        goovv.contract("abcc,ac->ab", cia, x1im, factor=-1.0)
        if self.dump_cache:
            self.cache.dump("goovv")
        #
        # goooo
        #
        goooo = self.init_cache("goooo", no, no, no, no)
        mo2.contract(
            "abcd->abcd",
            out=goooo,
            factor=1.0,
            clear=True,
            **oooo,
            select="einsum",
        )
        #
        # 3 hole terms
        #
        if self.nhole > 2:
            self.set_hamiltonian_3_hole(fock, goooo, mo2)
        #
        # Clean up
        #
        mo1.__del__()
        mo2.__del__()

    def set_hamiltonian_3_hole(self, fock, goooo, mo2):
        """Derive all effective Hamiltonian terms for 3 hole operators

        **Arguments:**

        fock, mo2
            fock matrix and two-electron integrals.
        """
        cia = self.checkpoint["t_p"]
        #
        # get ranges
        #
        no, nv = self.occ_model.nacto[0], self.occ_model.nactv[0]
        vo2 = self.get_range("vo", start=2)
        ooov = self.get_range("ooov")
        oovv = self.get_range("oovv")
        ovov = self.get_range("ovov")
        ovvo = self.get_range("ovvo")
        vovv = self.get_range("vovv")
        #
        # x1cd
        #
        x1cd = self.init_cache("x1cd", nv, nv)
        # fcd
        x1cd.iadd(fock, 1.0, begin2=no, begin3=no)
        # -<kk|cd> ckc
        tmp = mo2.contract("aabc->abc", out=None, **oovv)
        tmp.contract("abc,ab->bc", cia, x1cd, factor=-1.0)
        del tmp
        #
        # gooov
        #
        gooov = self.init_cache("gooov", no, no, no, nv)
        mo2.contract(
            "abcd->abcd",
            out=gooov,
            factor=1.0,
            clear=True,
            **ooov,
            select="einsum",
        )
        #
        # xjkcm
        #
        xjkcm = self.init_cache("xjkcm", no, no, nv, no)
        # -<jk|mc>
        mo2.contract(
            "abcd->abdc",
            out=xjkcm,
            factor=-1.0,
            clear=True,
            **ooov,
            select="einsum",
        )
        # -<mk||jc> ckc
        gooov.contract("abcd,bd->cbda", cia, xjkcm, factor=-1.0)
        gooov.contract("abcd,ad->cadb", cia, xjkcm, factor=1.0)
        # <jm|kc> cjc
        gooov.contract("abcd,ad->acdb", cia, xjkcm)
        # -fcm ckc dkj
        tmp = cia.contract("ab,bc->abc", fock, out=None, factor=-1.0, **vo2)
        # -<cm|dd> ckd dkj
        mo2.contract("abcc,dc->dab", cia, tmp, factor=-1.0, **vovv)
        xjkcm.iadd_expand_three_to_four("abc->aabc", tmp)
        #
        # xkcmd
        #
        xkcmd = self.init_cache("xkcmd", no, nv, no, nv)
        # <kd||cm>
        mo2.contract(
            "abcd->acdb",
            out=xkcmd,
            factor=1.0,
            clear=True,
            **ovvo,
            select="einsum",
        )
        mo2.contract(
            "abcd->adcb",
            out=xkcmd,
            factor=-1.0,
            **ovov,
            select="einsum",
        )
        # <kd|cm> ckc
        mo2.contract("abcd,ac->acdb", cia, xkcmd, **ovvo)
        if self.dump_cache:
            self.cache.dump("xkcmd")
        #
        # xkcMD
        #
        xkcMD = self.init_cache("xkcMD", no, nv, no, nv)
        # <kd|cm>
        mo2.contract(
            "abcd->acdb",
            out=xkcMD,
            factor=1.0,
            clear=True,
            **ovvo,
            select="einsum",
        )
        # <km||cd> ckc
        mo2.contract("abcd,ac->acbd", cia, xkcMD, **oovv)
        mo2.contract("abcd,ad->adbc", cia, xkcMD, factor=-1.0, **oovv)
        if self.dump_cache:
            self.cache.dump("xkcMD")
        #
        # xjcmD
        #
        xjcmD = self.init_cache("xjcmD", no, nv, no, nv)
        govov = self.denself.create_four_index(no, nv, no, nv)
        mo2.contract(
            "abcd->abcd",
            out=govov,
            factor=1.0,
            clear=True,
            **ovov,
            select="einsum",
        )
        # -<jc|md>
        xjcmD.iadd(govov, factor=-1.0)
        del govov
        # <jm|dc> cjc
        mo2.contract("abcd,ad->adbc", cia, xjcmD, **oovv)
        if self.dump_cache:
            self.cache.dump("xjcmD")
        #
        # xjkmN
        #
        xjkmN = self.init_cache("xjkmN", no, no, no, no)
        # <jk|mn>
        xjkmN.iadd(goooo, factor=1.0)
        # -<mn|dd> ckd dkj (kmn)
        tmp = mo2.contract("abcc,dc->dab", cia, out=None, **oovv)
        xjkmN.iadd_expand_three_to_four("abc->aabc", tmp)
        del tmp
        #
        # xikcm
        #
        xikcm = self.init_cache("xikcm", no, no, nv, no)
        # -0.5<ik||mc>
        gooov.contract(
            "abcd->abdc", out=xikcm, factor=-0.5, clear=True, select="einsum"
        )
        gooov.contract("abcd->badc", out=xikcm, factor=0.5, select="einsum")
        # -<mk|ic> ckc
        gooov.contract("abcd,bd->cbda", cia, xikcm, factor=-1.0)
