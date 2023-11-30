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
#include <pybind11/pybind11.h>
#include <pybind11/stl.h>

#include "fourindex.h"

namespace py = pybind11;

PYBIND11_MODULE(pytransform, m) {
  m.doc() =
      "pybind11 module PyTransform to perform 4-index transformation)";  // optional
                                                                         // module
                                                                         // docstring

  // functions
  m.def("apply_four_index_transform_cpp", &apply_four_index_transform_cpp,
        "Perform 4-index transform of dense object",
        py::return_value_policy::take_ownership);
  m.def("apply_four_index_transform_cpp_chol",
        &apply_four_index_transform_cpp_chol,
        "Perform 4-index transform of Cholesky object",
        py::return_value_policy::take_ownership);
}
