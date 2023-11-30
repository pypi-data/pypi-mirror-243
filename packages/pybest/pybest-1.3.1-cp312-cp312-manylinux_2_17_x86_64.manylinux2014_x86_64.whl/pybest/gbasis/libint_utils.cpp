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
#include "libint_utils.h"

#include <cassert>

size_t get_tot_nbasis(const std::vector<libint2::Shell>& shells) {
  size_t n = 0;
  for (const auto& shell : shells) n += shell.size();
  return n;
}

libint2::BasisSet uncontract_basis_set(Basis* basis) {
  libint2::Shell::do_enforce_unit_normalization(false);
  libint2::BasisSet obsu;
  std::vector<std::vector<libint2::Shell>> element_bases(120);

  for (auto a = 0ul; a < basis->atoms.size(); ++a) {
    auto Z = basis->atoms[a].atomic_number;
    auto x = basis->atoms[a].x;
    auto y = basis->atoms[a].y;
    auto z = basis->atoms[a].z;

    std::vector<libint2::Shell> shells;
    for (size_t s = 0; s != basis->obs.size(); ++s) {
      auto x_ = basis->obs[s].O[0];
      auto y_ = basis->obs[s].O[1];
      auto z_ = basis->obs[s].O[2];
      if (x != x_ || y != y_ || z != z_) continue;
      if (s > 0) {
        if (basis->obs[s].alpha == basis->obs[s - 1].alpha) continue;
      }
      for (auto n = 0ul; n < basis->obs[s].alpha.size(); ++n) {
        for (const auto& c : basis->obs[s].contr) {
          shells.push_back({
              {basis->obs[s].alpha[n]},  // exponents of primitive Gaussians
              {{c.l, false, {1.0L}}},
              {{x, y, z}}  // origin coordinates
          });
        }
      }
    }
    element_bases[Z] = shells;
  }
  obsu = libint2::BasisSet(basis->atoms, element_bases);
  // There is no init() in the constructor, so we use the init() in the
  // set_pure functions. Here, nothing happens as all basis functions are
  // cartesians by constructions.
  obsu.set_pure(false);
  return obsu;
}

size_t get_nubf(Basis* basis, bool solid) {
  libint2::Shell::do_enforce_unit_normalization(false);
  libint2::initialize();  // safe to use libint now
  std::vector<libint2::Shell> shells;

  for (size_t s = 0; s != basis->obs.size(); ++s) {
    if (s > 0) {
      if (basis->obs[s].alpha == basis->obs[s - 1].alpha) continue;
    }
    for (size_t n = 0; n < basis->obs[s].alpha.size(); ++n) {
      for (const auto& c : basis->obs[s].contr) {
        shells.push_back({
            {basis->obs[s].alpha[n]},  // exponents of primitive Gaussians
            {{c.l, solid, {1.0L}}},
            {{basis->obs[s].O[0], basis->obs[s].O[1],
              basis->obs[s].O[2]}}  // origin coordinates
        });
      }
    }
  }

  size_t nbasis = get_tot_nbasis(shells);
  libint2::finalize();  // do not use libint after this
  return nbasis;
}

void get_solid_tform_u2c(
    Basis* basis,
    py::array_t<double, py::array::c_style | py::array::forcecast>& out,
    size_t ncbf, size_t nubf) {
  libint2::Shell::do_enforce_unit_normalization(false);
  libint2::initialize();  // safe to use libint now

  // Create buffer pointer to output
  py::buffer_info bufout = out.request();
  double* ptrout = (double*)bufout.ptr;
  // col and row indices for transformation matrix
  auto row = 0ul;
  auto col = 0ul;
  for (size_t s = 0ul; s != basis->obs.size(); ++s) {
    for (const auto& c : basis->obs[s].contr) {
      for (int nl = 0ul; nl < (2 * c.l + 1); ++nl) {
        // introduce temporary indices for reset
        auto col_ = col;
        for (auto n = 0ul; n < basis->obs[s].alpha.size(); ++n) {
          // reset if segmented (both contracted and uncontracted indices):
          if (s > 0)
            if (basis->obs[s].alpha == basis->obs[s - 1].alpha && n == 0) {
              // for contracted, move back for all components of a shell
              col -= (basis->obs[s].alpha.size() * (2 * c.l + 1));
            }
          // assign matrix element. We have to rescale the coefficients
          // as libint renormalizes the contraction coefficients internally.
          // Thus, we have to devide by the renormalized contraction coefficient
          // of the uncontracted basis to obtain the original contraction
          // coefficient of the input basis set. Otherwise, we renormalize
          // twice:
          double normalization_factor = basis->get_renorm(c.l, s, n);
          ptrout[row * nubf + col] = c.coeff[n] / normalization_factor;

          // move to next element
          // for c/uc transformation matrix move to next element of shell l
          col += (2 * c.l + 1);
        }
        // reset col for next row if l > 0:
        if (c.l > 0 and nl != (2 * c.l))
          col = col_ + 1;
        else if (c.l > 0 and nl == (2 * c.l))
          col = col - 2 * c.l;
        row += 1;
      }
    }
  }
  libint2::finalize();  // do not use libint after this
}
