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

// UPDATELIBDOCTITLE: Low-level routines for ``CholeskyLinalgFactory``

#ifndef PyBEST_MATRIX_CONTRACTION_H
#define PyBEST_MATRIX_CONTRACTION_H

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

void contract_two_to_two_abcd_cb_ad_blas(
    py::array_t<double, py::array::c_style | py::array::forcecast> inp1,
    py::array_t<double, py::array::c_style | py::array::forcecast> inp2,
    py::array_t<double, py::array::c_style | py::array::forcecast> two,
    py::array_t<double, py::array::c_style | py::array::forcecast> &out,
    double factor, bool clear, long b0, long e0, long b1, long e1, long b2,
    long e2, long b3, long e3, long b4, long e4, long b5, long e5, bool t);

void contract_four_to_four_abcd_efbd_aecf(
    py::array_t<double, py::array::c_style | py::array::forcecast> inp1,
    py::array_t<double, py::array::c_style | py::array::forcecast> inp2,
    py::array_t<double, py::array::c_style | py::array::forcecast> four,
    py::array_t<double, py::array::c_style | py::array::forcecast> &out,
    double factor, bool clear, long b0, long e0, long b1, long e1, long b2,
    long e2, long b3, long e3);

void contract_four_to_four_abcd_efbd_aecf_blas(
    py::array_t<double, py::array::c_style | py::array::forcecast> inp1,
    py::array_t<double, py::array::c_style | py::array::forcecast> inp2,
    py::array_t<double, py::array::c_style | py::array::forcecast> four,
    py::array_t<double, py::array::c_style | py::array::forcecast> &out,
    double factor, bool clear, long b0, long e0, long b1, long e1, long b2,
    long e2, long b3, long e3);
#endif
