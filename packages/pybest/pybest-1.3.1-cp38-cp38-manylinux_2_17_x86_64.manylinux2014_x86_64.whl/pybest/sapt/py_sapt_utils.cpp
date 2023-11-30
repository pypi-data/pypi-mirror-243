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

#include "sapt_utils.h"

namespace py = pybind11;

PYBIND11_MODULE(pysapt, m) {
  m.doc() = "pybind11 module PySapt exposing some c++ routines for sapt";

  // Utility functions
  m.def("get_amplitudes", &get_sapt_amplitudes,
        "Returns SAPT uncoupled restricted theory denominators used in "
        "amplitudes");
}
