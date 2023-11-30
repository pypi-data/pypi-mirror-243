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

#include "static_embedding.h"

#include <stdlib.h>

#include <Eigen/Core>
#include <cmath>
#include <cstdlib>
#include <cstring>
#include <iomanip>
#include <iostream>
#include <stdexcept>
#include <string>

using std::abs;

/*
    StaticEmbedding

*/

// Overload constructor:
StaticEmbedding::StaticEmbedding(std::vector<double> charges_,
                                 std::vector<double> x, std::vector<double> y,
                                 std::vector<double> z, std::vector<double> wi)
    : chargefile("") {
  for (auto& c : charges_) {
    charges.push_back(c);
  }
  for (auto& w : wi) {
    weights.push_back(w);
  }
  for (auto a = 0ul; a < charges.size(); ++a) {
    double xa = x[a];
    double ya = y[a];
    double za = z[a];
    coordinates.push_back({xa, ya, za});
  }
}

std::vector<std::pair<double, std::array<double, 3>>>
// The get_charge_pairs allows us to access Libint
// engine for computing integrals over charges
StaticEmbedding::get_charge_pairs() {
  std::vector<std::pair<double, std::array<double, 3>>> potential;

  // We read in the xyz coordinated of charges multiplied by weights
  for (auto a = 0ul; a < charges.size(); ++a) {
    auto charge = charges[a] * weights[a];
    auto x = coordinates[a][0];
    auto y = coordinates[a][1];
    auto z = coordinates[a][2];
    std::pair<double, std::array<double, 3>> element(charge, {x, y, z});
    potential.push_back(element);
  }
  return potential;
}

/*
 * Evaluate a static embedding potential taken from a .emb file.
 */

// We calculate the static embedding potential according to
// Gomes et al, PCCP, 10, 5353-5362 (2008)
// Specifically, we evaluate the following expression
// v_ij \approx sum_k ( w_k * v_emb(r_k) * [Phi_i(r_k)Phi_j(r_k)0])
// Later on, the matrix representation of embedding potential is
// added to the one-electron Fock matrix

void StaticEmbedding::compute_static_embedding(
    Basis* basis0, Basis* basis1,
    py::array_t<double, py::array::c_style | py::array::forcecast>& out) {
  libint2::Shell::do_enforce_unit_normalization(false);

  // Create buffer pointer to output
  py::buffer_info bufout = out.request();
  double* ptrout = (double*)bufout.ptr;

  auto obs0 = basis0->obs;
  auto obs1 = basis1->obs;

  auto shell2bf0 = obs0.shell2bf();  // maps shell index to basis function index
  auto shell2bf1 = obs1.shell2bf();  // maps shell index to basis function index
                                     // shell2bf[0] = index of the first basis
                                     // function in shell 0 shell2bf[1] = index
                                     // of the first basis function in shell 1
                                     // ...
  // loop over all grid points
  for (int i = 0; i < charges.size(); ++i) {
    auto x = coordinates[i][0];
    auto y = coordinates[i][1];
    auto z = coordinates[i][2];
    auto charge = charges[i];
    auto weight = weights[i];
    // compute value of selected orbital (MO) at point (x,y,z)
    // loop over basis set, that is, the AOs
    // we need to 2 variables in the loop:
    // 1) for the basis instance (used by libint2) ``s``
    // 2) for the AO/MO coefficients ``mu``
    std::vector<double> phi_i;
    std::vector<double> phi_j;
    std::vector<double> cart;
    std::vector<double> pure;
    std::vector<double> cart1;
    std::vector<double> pure1;
    for (auto s = 0; s != obs0.size(); ++s) {
      // Get center of AO
      auto x_ao = obs0[s].O[0];
      auto y_ao = obs0[s].O[1];
      auto z_ao = obs0[s].O[2];
      // Contribution of each AO at grid point (x,y,z)
      const auto& c_i = obs0[s].contr;
      phi_i.resize(2 * c_i[0].l + 1, 0.0);
      // loop over CGO (each AO can be a linear combination of primitives)
      for (const auto& c : obs0[s].contr) {
        auto l_max = ((c.l + 1) * (c.l + 2)) / 2;
        for (auto n = 0ul; n < obs0[s].alpha.size(); ++n) {
          auto shell_exp_l = shell_exp[c.l];
          // store results for cartesian and pure functions
          cart.resize(l_max, 0.0);
          pure.resize(2 * c.l + 1, 0.0);
          // loop over all cartesian functions of a specific shell with c.l
          for (auto l = 0; l < l_max; ++l) {
            auto l_xyz = shell_exp_l[l];
            // r^l exp(-alpha r^2) * N
            auto r2 = pow(x - x_ao, 2) + pow(y - y_ao, 2) + pow(z - z_ao, 2);
            // assign value at point (x,y,z) of primitive to temporary
            // cartesian vector
            cart[l] = pow(x - x_ao, l_xyz[0]) * pow(y - y_ao, l_xyz[1]) *
                      pow(z - z_ao, l_xyz[2]) * exp(-obs0[s].alpha[n] * r2);
          }
          // transform cartesian back to solid harmonics
          // NOTE: we do not transform (s or) p functions as we use the
          // order (x,y,z)/(+1,-1,0) for p functions; all higher l functions
          // need to be transformed
          if (c.l <= 1) {
            // assign and multiply with MO coefficient coeffs and
            // contraction coefficient (properly normalized) c.coeff[n] of
            // n-th primitive
            for (auto l = 0; l < l_max; ++l) {
              phi_i[l] += cart[l] * c.coeff[n];
            }
          } else {
            // transform back to pure solid harmonics using libint's
            // tform_cols function (transforms only a column vector for
            // shell c.l)
            libint2::solidharmonics::tform_cols(1, c.l, &cart[0], &pure[0]);
            // loop over all MOs in pure form/solid harmonics
            // the order of m_l functions is the same in pure and coeffs
            for (std::size_t l = 0; l < pure.size(); ++l) {
              phi_i[l] += pure[l] * c.coeff[n];
            }
          }
          pure.clear();
          cart.clear();
        }
      }
      for (auto s1 = 0; s1 != obs1.size(); ++s1) {
        // Get center of AO
        auto x_ao1 = obs1[s1].O[0];
        auto y_ao1 = obs1[s1].O[1];
        auto z_ao1 = obs1[s1].O[2];
        // Contribution of each AO at grid point (x,y,z)
        const auto& c_j = obs1[s1].contr;
        phi_j.resize(2 * c_j[0].l + 1, 0.0);
        // loop over CGO (each AO can be a linear combination of primitives)
        for (const auto& c : obs1[s1].contr) {
          auto l_max = ((c.l + 1) * (c.l + 2)) / 2;
          for (auto n = 0ul; n < obs1[s1].alpha.size(); ++n) {
            auto shell_exp_l = shell_exp[c.l];
            // store results for cartesian and pure functions
            cart1.resize(l_max, 0.0);
            pure1.resize(2 * c.l + 1, 0.0);
            // loop over all cartesian functions of a specific shell with c.l
            for (auto l = 0; l < l_max; ++l) {
              auto l_xyz = shell_exp_l[l];
              // r^l exp(-alpha r^2) * N
              auto r2 =
                  pow(x - x_ao1, 2) + pow(y - y_ao1, 2) + pow(z - z_ao1, 2);
              // assign value at point (x,y,z) of primitive to temporary
              // cartesian vector
              cart1[l] = pow(x - x_ao1, l_xyz[0]) * pow(y - y_ao1, l_xyz[1]) *
                         pow(z - z_ao1, l_xyz[2]) *
                         exp(-obs1[s1].alpha[n] * r2);
            }
            // transform cartesian back to solid harmonics
            // NOTE: we do not transform (s or) p functions as we use the
            // order (x,y,z)/(+1,-1,0) for p functions; all higher l functions
            // need to be transformed
            if (c.l <= 1) {
              // assign and multiply with MO coefficient coeffs and
              // contraction coefficient (properly normalized) c.coeff[n] of
              // n-th primitive
              for (auto l = 0; l < l_max; ++l) {
                phi_j[l] += cart1[l] * c.coeff[n];
              }
            } else {
              // transform back to pure solid harmonics using libint's
              // tform_cols function (transforms only a column vector for
              // shell c.l)
              libint2::solidharmonics::tform_cols(1, c.l, &cart1[0], &pure1[0]);
              // loop over all MOs in pure form/solid harmonics
              // the order of m_l functions is the same in pure and coeffs
              for (std::size_t l = 0; l < pure1.size(); ++l) {
                phi_j[l] += pure1[l] * c.coeff[n];
              }
            }
            pure1.clear();
            cart1.clear();
          }
        }
        auto bf0 = shell2bf0[s];    // first basis function in first shell
        auto n0 = obs0[s].size();   // number of basis functions in first shell
        auto bf1 = shell2bf1[s1];   // first basis function in second shell
        auto n1 = obs1[s1].size();  // number of basis functions in second shell

        // integrals are packed into ints_shellset in row-major (C) form
        // this iterates over integrals in this order
        for (size_t f0 = 0; f0 != n0; ++f0)
          for (size_t f1 = 0; f1 != n1; ++f1) {
            ptrout[(bf0 + f0) * obs1.nbf() + (bf1 + f1)] +=
                charge * weight * phi_i[f0] * phi_j[f1];
          }
        phi_j.clear();
      }
      phi_i.clear();
    }
  }  // for x, y, z, charge, weight line
}
