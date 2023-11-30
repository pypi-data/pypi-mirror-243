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

// UPDATELIBDOCTITLE: Auxiliary functions

#ifndef PyBEST_GBASIS_EMULTIPOLE_H
#define PyBEST_GBASIS_EMULTIPOLE_H

#include <pybind11/numpy.h>
#include <pybind11/pybind11.h>

#include <chrono>
#include <cmath>
#include <fstream>
#include <iomanip>
#include <iostream>
#include <sstream>
#include <vector>

#include "basis.h"
namespace py = pybind11;

// Libint Gaussian integrals library
#include <libint2.hpp>
#if !LIBINT2_CONSTEXPR_STATICS
#include <libint2/statics_definition.h>
#endif

#if LIBINT2_REALTYPE != double
#error LibInt must be compiled with REALTYPE=double.
#endif

#if LIBINT2_SUPPORT_ERI == 0
#error LibInt must be compiled with support for electron repulsion integrals.
#endif

#ifndef LIBINT2_MAX_AM
#define LIBINT2_MAX_AM LIBINT2_MAX_AM_ERI
#endif
#if LIBINT2_MAX_AM < MAX_SHELL_TYPE
#error LibInt must be compiled with an angular momentum limit of at least MAX_SHELL_TYPE.
#endif

// Auxiliary functions for Gaussian integrals
void compute_dipole(
    Basis *basis0, Basis *basis1,
    py::array_t<double, py::array::c_style | py::array::forcecast> &olp,
    py::array_t<double, py::array::c_style | py::array::forcecast> &mux,
    py::array_t<double, py::array::c_style | py::array::forcecast> &muy,
    py::array_t<double, py::array::c_style | py::array::forcecast> &muz,
    double x, double y, double z);
void compute_quadrupole(
    Basis *basis0, Basis *basis1,
    py::array_t<double, py::array::c_style | py::array::forcecast> &olp,
    py::array_t<double, py::array::c_style | py::array::forcecast> &mux,
    py::array_t<double, py::array::c_style | py::array::forcecast> &muy,
    py::array_t<double, py::array::c_style | py::array::forcecast> &muz,
    py::array_t<double, py::array::c_style | py::array::forcecast> &muxx,
    py::array_t<double, py::array::c_style | py::array::forcecast> &muxy,
    py::array_t<double, py::array::c_style | py::array::forcecast> &muxz,
    py::array_t<double, py::array::c_style | py::array::forcecast> &muyy,
    py::array_t<double, py::array::c_style | py::array::forcecast> &muyz,
    py::array_t<double, py::array::c_style | py::array::forcecast> &muzz,
    double x, double y, double z);

#endif
