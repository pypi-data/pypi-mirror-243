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

#include "basis.h"
#include "libint_utils.h"

namespace py = pybind11;

PYBIND11_MODULE(pybasis, m) {
  // optional module dosctring
  m.doc() = "pybind11 module PyBasis to read AO basis sets using libint2 API)";

  // Utility functions
  m.def("get_nubf", &get_nubf, "Return number of uncontracted basis functions");
  m.def("get_solid_tform_u2c", &get_solid_tform_u2c,
        "Return the transformation matrix uncontracted<-->contracted",
        py::return_value_policy::take_ownership);
  // used as a constructor from python-side
  m.def("from_coordinates", &from_coordinates,
        "Read basis set from coordinates");

  // Basis set class
  py::class_<Basis> basis(m, "Basis");
  basis
      .def(py::init<const std::string &, const std::string &,
                    const std::string &>())
      .def(py::init<const std::string &, std::vector<long>, std::vector<long>,
                    std::vector<int>, std::vector<double>,
                    std::vector<double>>())
      .def(py::init<const Basis &>())
      .def("print_basis_info", &Basis::print_basis_info)
      .def("print_atomic_info", &Basis::print_atomic_info)
      .def("renormalize_contr", &Basis::renormalize_contr)
      .def("get_nbasis_in_shell", &Basis::get_nbasis_in_shell)
      .def("set_dummy_atoms", &Basis::set_dummy_atom)
      .def("dump_molden", &Basis::dump_molden)
      .def("dump_cube_orbital", &Basis::dump_cube_orbital)
      // FIXME: test for negative values
      .def("get_shell_size", &Basis::get_shell_size)
      .def("get_renorm_pure",
           (double (Basis::*)(std::size_t, std::size_t, std::size_t)) &
               Basis::get_renorm,
           "Get renormalization constant for solid harmonics")
      .def("get_renorm_cart",
           (double (Basis::*)(std::size_t, std::size_t, std::size_t,
                              std::vector<std::size_t>)) &
               Basis::get_renorm,
           "Get renormalization constant for cartesians")
      // getters; we do not want them to be writable from python
      .def_property("basisname", &Basis::getBasisname, nullptr,
                    "Get the name of the AO basis set (if specified)")
      .def_property("molfile", &Basis::getMolfile, nullptr,
                    "Get the name of the coordinate xyz file (if present)")
      .def_property("basisdir", &Basis::getDirname, nullptr,
                    "Get the directory of basis set library (if present)")
      // define read-writable attributes
      .def_readwrite("nbasis", &Basis::nbasis,
                     "the total number of basis functions")
      .def_readwrite("ncenter", &Basis::ncenter,
                     "the total number of atomic centers")
      .def_readwrite("nshell", &Basis::nshell, "the total number of shells")
      .def_readwrite("nprim", &Basis::nprim,
                     "the number of primitives per contraction")
      .def_readwrite("alpha", &Basis::alpha, "the exponents for each primitive")
      .def_readwrite("contraction", &Basis::contraction,
                     "the contraction coefficients for each primitive")
      .def_readwrite("shell2atom", &Basis::shell2atom, "the shell to atom list")
      .def_readwrite("shell_types", &Basis::shell_types,
                     "the shell type per contraction")
      .def_readwrite("atom", &Basis::atomic_numbers,
                     "the atomic numbers of each atom")
      .def_readwrite("coordinates", &Basis::coordinates, "Get the coordinates");
}
