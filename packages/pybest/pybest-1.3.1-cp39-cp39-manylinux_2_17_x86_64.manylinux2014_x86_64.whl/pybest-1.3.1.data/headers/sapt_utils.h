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

#ifndef PYBEST_SAPT_UTILS_H
#define PYBEST_SAPT_UTILS_H

#include <pybind11/numpy.h>
#include <pybind11/pybind11.h>

namespace py = pybind11;

typedef py::array_t<double, py::array::c_style | py::array::forcecast>
    SAPT_NPY_ARRAY;

void get_sapt_amplitudes(SAPT_NPY_ARRAY t_rsab_npy, SAPT_NPY_ARRAY t_ra_npy,
                         SAPT_NPY_ARRAY t_sb_npy, SAPT_NPY_ARRAY en_occ_a_npy,
                         SAPT_NPY_ARRAY en_virt_a_npy,
                         SAPT_NPY_ARRAY en_occ_b_npy,
                         SAPT_NPY_ARRAY en_virt_b_npy, std::size_t nocc_a,
                         std::size_t nocc_b, std::size_t nvirt_a,
                         std::size_t nvirt_b);

#endif
