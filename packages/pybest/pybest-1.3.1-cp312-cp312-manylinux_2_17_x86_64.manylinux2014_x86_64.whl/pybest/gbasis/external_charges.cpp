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

// #define DEBUG

#include "external_charges.h"

#include <stdlib.h>

#include <array>
#include <cmath>
#include <cstdlib>
#include <cstring>
#include <iomanip>
#include <iostream>
#include <stdexcept>
#include <string>
#include <vector>

using std::abs;

/*
    ExternalCharges

*/

// Overload constructor:
ExternalCharges::ExternalCharges(std::vector<double> charges_,
                                 std::vector<double> x, std::vector<double> y,
                                 std::vector<double> z)
    : chargefile("") {
  for (auto& c : charges_) {
    charges.push_back(c);
  }
  for (auto a = 0ul; a < charges.size(); ++a) {
    double xa = x[a];
    double ya = y[a];
    double za = z[a];
    coordinates.push_back({xa, ya, za});
  }
}
// Returns a vector that contains a pair of the charge value and a vector of
// (x,y,z) coordinates in each element.
// Needed for Libint to assign charges to point-charge-like potentials
std::vector<std::pair<double, std::array<double, 3>>>
ExternalCharges::get_charge_pairs() {
  std::vector<std::pair<double, std::array<double, 3>>> potential;

  for (auto a = 0ul; a < charges.size(); ++a) {
    auto charge = charges[a];
    auto x = coordinates[a][0];
    auto y = coordinates[a][1];
    auto z = coordinates[a][2];
    // assigning point charges at (x,y,z) position required for
    // libint's v_engine to generate a point-charge potential.
    std::pair<double, std::array<double, 3>> element(charge, {x, y, z});
    potential.push_back(element);
  }
  return potential;
}
