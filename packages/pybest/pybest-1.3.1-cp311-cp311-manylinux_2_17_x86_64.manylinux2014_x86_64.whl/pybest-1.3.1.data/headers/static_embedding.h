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

#ifndef PyBEST_STATIC_EMBEDDING_H
#define PyBEST_STATIC_EMBEDDING_H

#include <pybind11/eigen.h>
#include <pybind11/pybind11.h>

#include "basis.h"
namespace py = pybind11;

#include <vector>

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

class StaticEmbedding {
 public:
  const std::string chargefile;
  std::size_t ncharges;
  std::vector<double> charges;
  std::vector<std::vector<double>> coordinates;
  std::vector<double> weights;
  // constructors
  StaticEmbedding(std::vector<double> charges, std::vector<double> x,
                  std::vector<double> y, std::vector<double> z,
                  std::vector<double> wi);
  StaticEmbedding(const StaticEmbedding& rhs) = default;
  // destructor
  ~StaticEmbedding() = default;

  // Functions to create charge-coordinate pairs
  std::vector<std::pair<double, std::array<double, 3>>> get_charge_pairs();
  // Function to calculate embedding potential
  void compute_static_embedding(
      Basis* basis0, Basis* basis1,
      py::array_t<double, py::array::c_style | py::array::forcecast>& out);
};

#endif
