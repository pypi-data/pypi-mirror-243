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

#ifndef PyBEST_MATRIX_FOURINDEX_H
#define PyBEST_MATRIX_FOURINDEX_H

// Include the CBLAS headers
#ifdef BLAS_MKL
#include <mkl.h>
#endif
#ifdef BLAS_OTHER
#if __has_include(<cblas.h>)
extern "C" {
#include <cblas.h>
}
#else
extern "C" {
#include <cblas_openblas.h>
}
#endif
#endif

#include <pybind11/numpy.h>
#include <pybind11/pybind11.h>
namespace py = pybind11;

void apply_four_index_transform_cpp(
    py::array_t<double, py::array::c_style | py::array::forcecast> inp1,
    py::array_t<double, py::array::c_style | py::array::forcecast> inp2,
    py::array_t<double, py::array::c_style | py::array::forcecast> &out);

void apply_four_index_transform_cpp_chol(
    py::array_t<double, py::array::c_style | py::array::forcecast> inp1,
    py::array_t<double, py::array::c_style | py::array::forcecast> inp2,
    py::array_t<double, py::array::c_style | py::array::forcecast> &out);

#endif
