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

#include "emultipole.h"
#include "eri.h"
#include "external.h"
#include "external_charges.h"
#include "kin.h"
#include "nuclear.h"
#include "overlap.h"
#include "point_charges.h"

#ifdef PYBEST_ENABLE_PVP
#include "pvp.h"
#endif

#ifdef PYBEST_ENABLE_CHOLESKY
#include "cholesky_eri.h"
#endif

namespace py = pybind11;

PYBIND11_MODULE(pyints, m) {
  m.doc() =
      "pybind11 module PyInts to calculate various integrals using libint2 "
      "API)";  // optional module docstring

  m.def("compute_nuclear_repulsion_cpp", &compute_nuclear_repulsion,
        "A function to compute the potential energy due to nuclear-nuclear "
        "repulsion");
  m.def("compute_external_charges_cpp", &compute_external_charges,
        "A function to compute the potential energy due to the interaction "
        " between point charges");
  m.def("compute_nuclear_pc_cpp", &compute_nuclear_pc,
        "A function to compute the potential energy due to the interaction of"
        " the external point charges and the nuclei");
  m.def("compute_overlap_cpp", &compute_overlap,
        "A function to compute the AO overlap",
        py::return_value_policy::take_ownership);
  m.def("compute_kinetic_cpp", &compute_kinetic,
        "A function to compute the kinetic energy integrals in the AO basis",
        py::return_value_policy::take_ownership);
  m.def("compute_nuclear_cpp", &compute_nuclear,
        "A function to compute the electron-nuclei attraction integrals in the "
        "AO basis",
        py::return_value_policy::take_ownership);
  m.def(
      "compute_point_charges_cpp", &compute_point_charges,
      "A function that computes the interaction between external point charges "
      "and electrons",
      py::return_value_policy::take_ownership);
#ifdef PYBEST_ENABLE_PVP
  m.def("compute_pvp_cpp", &compute_pvp,
        "A function to compute the pVp integrals in the uncontracted AO basis",
        py::return_value_policy::take_ownership);
  m.def("compute_ppcp_cpp", &compute_ppcp,
        "A function to compute the pPCp integrals in the uncontracted AO basis",
        py::return_value_policy::take_ownership);
#endif
  m.def("compute_dipole_cpp", &compute_dipole,
        "A function to compute the dipole integrals in the AO basis",
        py::return_value_policy::take_ownership);
  m.def("compute_quadrupole_cpp", &compute_quadrupole,
        "A function to compute the quadrupole integrals in the AO basis",
        py::return_value_policy::take_ownership);
  m.def(
      "compute_eri_cpp", &compute_eri,
      "A function to compute the electron repulsion integrals in the AO basis",
      py::return_value_policy::take_ownership);
#ifdef PYBEST_ENABLE_CHOLESKY
  m.def("compute_cholesky_eri_cpp", &compute_cholesky_eri,
        "A function to cholesky decomposed compute the electron repulsion "
        "integrals in the AO basis",
        py::return_value_policy::take_ownership);
#endif
}
