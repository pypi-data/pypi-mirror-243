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

#include "contraction.h"

namespace py = pybind11;

PYBIND11_MODULE(pycontract, m) {
  m.doc() =
      "pybind11 module PyContract to construct contracted Cholesky object)";  // optional module docstring

  // functions
  m.def("contract_two_to_two_abcd_cb_ad_blas",
        &contract_two_to_two_abcd_cb_ad_blas, "Perform contraction abcd,cb->ad",
        py::return_value_policy::take_ownership);
  m.def("contract_four_to_four_abcd_efbd_aecf",
        &contract_four_to_four_abcd_efbd_aecf,
        "Perform contraction abcd,efbd->aecf",
        py::return_value_policy::take_ownership);
  m.def("contract_four_to_four_abcd_efbd_aecf_blas",
        &contract_four_to_four_abcd_efbd_aecf_blas,
        "Perform contraction abcd,efbd->aecf using blas",
        py::return_value_policy::take_ownership);
}
