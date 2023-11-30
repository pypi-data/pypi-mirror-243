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
#include "cholesky_eri.h"

// this is just minimal wrapper unpacking PYBEST's PyBasis to libint2::BasisSet
// which is default
py::array_t<double, py::array::c_style | py::array::forcecast>
compute_cholesky_eri(Basis *basis0, double cd_threshold, size_t cd_beta) {
#ifndef LIBCHOL_AVAILABLE
  throw std::runtime_error("PyBest was not compiled against libchol module!");
#endif

  // NOTE: This will make a copy
  // auto cd_eri = chol::compute_cholesky_decomposition(basis0->obs, threshold);
  // return py::array(cd_eri.size(), cd_eri.data());

  // NOTE: This will not make a copy, but dunno if Python's GC can deallocate
  // that see:
  // https://github.com/pybind/pybind11/issues/1042#issuecomment-325941022
  auto v = new std::vector<double>(
      chol::compute_cholesky_decomposition(basis0->obs, cd_threshold, cd_beta));
  auto capsule = py::capsule(
      v, [](void *v) { delete reinterpret_cast<std::vector<double> *>(v); });
  return py::array(v->size(), v->data(), capsule);
}
