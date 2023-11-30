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
#include "external.h"

// compute the nuclear repulsion energy
double compute_nuclear_repulsion(Basis* basis0, Basis* basis1) {
  auto enuc = 0.0;
  for (size_t i = 0; i < basis0->atoms.size(); i++)
    for (size_t j = 0; j < basis1->atoms.size(); j++) {
      // get distances
      auto xij = basis0->atoms[i].x - basis1->atoms[j].x;
      auto yij = basis0->atoms[i].y - basis1->atoms[j].y;
      auto zij = basis0->atoms[i].z - basis1->atoms[j].z;
      auto r2 = xij * xij + yij * yij + zij * zij;
      auto r = sqrt(r2);
      if (r != 0.0)
        enuc +=
            basis0->atoms[i].atomic_number * basis1->atoms[j].atomic_number / r;
    }
  return enuc / 2.0;
}
// compute the interaction between external charges
// currently not used, but might be needed later on
double compute_external_charges(ExternalCharges* ext_charges) {
  auto enuc = 0.0;
  for (size_t j = 0; j < ext_charges->charges.size(); j++) {
    for (size_t i = 0; i < ext_charges->charges.size(); i++) {
      // get distances
      auto xij =
          ext_charges->coordinates[i][0] - ext_charges->coordinates[j][0];
      auto yij =
          ext_charges->coordinates[i][1] - ext_charges->coordinates[j][1];
      auto zij =
          ext_charges->coordinates[i][2] - ext_charges->coordinates[j][2];
      auto r2 = xij * xij + yij * yij + zij * zij;
      auto r = sqrt(r2);
      if (r != 0.0)
        enuc += ext_charges->charges[i] * ext_charges->charges[j] / r;
    }
  }
  return enuc / 2.0;
}
// compute the interaction between the nuclei and external charges
double compute_nuclear_pc(Basis* basis0, ExternalCharges* ext_charges) {
  auto enuc = 0.0;
  for (size_t j = 0; j < ext_charges->charges.size(); j++) {
    for (size_t i = 0; i < basis0->atoms.size(); i++) {
      // get distances
      auto xij = basis0->atoms[i].x - ext_charges->coordinates[j][0];
      auto yij = basis0->atoms[i].y - ext_charges->coordinates[j][1];
      auto zij = basis0->atoms[i].z - ext_charges->coordinates[j][2];
      auto r2 = xij * xij + yij * yij + zij * zij;
      auto r = sqrt(r2);
      if (r != 0.0)
        enuc += basis0->atoms[i].atomic_number * ext_charges->charges[j] / r;
    }
  }
  return enuc;
}
