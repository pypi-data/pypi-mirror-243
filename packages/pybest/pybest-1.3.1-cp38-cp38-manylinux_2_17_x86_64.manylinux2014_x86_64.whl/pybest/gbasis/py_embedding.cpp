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

#include "static_embedding.h"

namespace py = pybind11;

PYBIND11_MODULE(pyembedding, m) {
  // optional module dosctring
  m.doc() =
      "pybind11 module PyStaticEmbedding to read static embedding (x, y, z, "
      "wi, and v) from file)";

  // StaticEmbedding class
  py::class_<StaticEmbedding> staticembedding(m, "StaticEmbedding");
  staticembedding
      .def(py::init<std::vector<double>, std::vector<double>,
                    std::vector<double>, std::vector<double>,
                    std::vector<double>>())
      .def(py::init<const StaticEmbedding &>())
      .def("compute_static_embedding_cpp",
           &StaticEmbedding::compute_static_embedding,
           "A function to calculate static"
           "embedding taken from an external file",
           py::return_value_policy::take_ownership);
}
