// PyBEST: Pythonic Black-box Electronic Structure Tool
// Copyright (C) 2016-- The PyBEST Development Team
//
// This file is part of PyBEST.
//
// PyBEST is free software; you can redistribute it and/or
// modify it under the terms of the GNU General Public License
// as published by the Free Software Foundation; either version 3
// of the License, or (at your option) any later version.
//
// PyBEST is distributed in the hope that it will be useful,
// but WITHOUT ANY WARRANTY; without even the implied warranty of
// MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
// GNU General Public License for more details.
//
// You should have received a copy of the GNU General Public License
// along with this program; if not, see <http://www.gnu.org/licenses/>
// --

#include "sapt_utils.h"

void get_sapt_amplitudes(SAPT_NPY_ARRAY t_rsab_npy, SAPT_NPY_ARRAY t_ra_npy,
                         SAPT_NPY_ARRAY t_sb_npy, SAPT_NPY_ARRAY en_occ_a_npy,
                         SAPT_NPY_ARRAY en_virt_a_npy,
                         SAPT_NPY_ARRAY en_occ_b_npy,
                         SAPT_NPY_ARRAY en_virt_b_npy, std::size_t nocc_a,
                         std::size_t nocc_b, std::size_t nvirt_a,
                         std::size_t nvirt_b) {
  // pybind11 boilerplate
  py::buffer_info t_rsab_buff = t_rsab_npy.request();
  py::buffer_info t_ra_buff = t_ra_npy.request();
  py::buffer_info t_sb_buff = t_sb_npy.request();
  py::buffer_info en_occ_a_buff = en_occ_a_npy.request();
  py::buffer_info en_virt_a_buff = en_virt_a_npy.request();
  py::buffer_info en_occ_b_buff = en_occ_b_npy.request();
  py::buffer_info en_virt_b_buff = en_virt_b_npy.request();
  double *t_rsab = (double *)t_rsab_buff.ptr;
  double *t_ra = (double *)t_ra_buff.ptr;
  double *t_sb = (double *)t_sb_buff.ptr;
  double *en_occ_a = (double *)en_occ_a_buff.ptr;
  double *en_virt_a = (double *)en_virt_a_buff.ptr;
  double *en_occ_b = (double *)en_occ_b_buff.ptr;
  double *en_virt_b = (double *)en_virt_b_buff.ptr;

  double tmp_1 = 0, tmp_2 = 0;
  // TODO: change occupy idx to be most-outer one, requires reordering of the
  // tensors.
  for (std::size_t r = 0; r < nvirt_a; r++) {
    for (std::size_t a = 0; a < nocc_a; a++) {
      tmp_1 = en_occ_a[a] - en_virt_a[r];
      // T1 - mon a induction denominator
      t_ra[r * nocc_a + a] = 1.0 / tmp_1;
      for (std::size_t s = 0; s < nvirt_b; s++) {
        for (std::size_t b = 0; b < nocc_b; b++) {
          tmp_2 = en_occ_b[b] - en_virt_b[s] + tmp_1;
          // T2 - ABAB dispersion denominator
          t_rsab[((r * nvirt_b + s) * nocc_a + a) * nocc_b + b] = 1.0 / tmp_2;
        }
      }
    }
  }
  for (std::size_t s = 0; s < nvirt_b; s++) {
    for (std::size_t b = 0; b < nocc_b; b++) {
      tmp_2 = en_occ_b[b] - en_virt_b[s];
      // T1 - mon b induction denominator
      t_sb[s * nocc_b + b] = 1.0 / tmp_2;
    }
  }
}
