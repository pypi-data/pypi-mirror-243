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

#include "external_charges.h"

namespace py = pybind11;

PYBIND11_MODULE(pycharges, m) {
  // optional module dosctring
  m.doc() =
      "pybind11 module PyCharges to read external charges (x, y, z, "
      "and v) from a file)";

  // ExternalCharges class
  py::class_<ExternalCharges> externalcharges(m, "ExternalCharges");
  externalcharges
      .def(py::init<std::vector<double>, std::vector<double>,
                    std::vector<double>, std::vector<double>>())
      .def(py::init<const ExternalCharges &>())
      .def_readwrite("charges", &ExternalCharges::charges, "charge values")
      .def_readwrite("coordinates", &ExternalCharges::coordinates);
}
