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
#include "nuclear.h"

#include "libint_utils.h"

void compute_nuclear(
    Basis* basis0, Basis* basis1,
    py::array_t<double, py::array::c_style | py::array::forcecast>& out,
    bool uncontract) {
  // Do not rescale contraction coefficients to ensure unit normalization of all
  // solid harmonics Gaussians and the axis-aligned (xl, yl, zl) Cartesian
  // Gaussians
  libint2::Shell::do_enforce_unit_normalization(false);

  libint2::initialize();  // safe to use libint now

  auto uobs0 = basis0->obs;
  auto uobs1 = basis1->obs;
  if (uncontract == true) {
    uobs0 = uncontract_basis_set(basis0);
    uobs0.set_pure(true);
    uobs1 = uncontract_basis_set(basis1);
    uobs1.set_pure(true);
    // reset p shell back to cartesian so that we can dump molden output
    for (auto& shell : uobs0)
      for (auto& contraction : shell.contr) {
        if (contraction.l == 1) {
          bool* solid = const_cast<bool*>(&contraction.pure);
          *solid = false;
        }
        if (contraction.l == 0) {
          bool* solid = const_cast<bool*>(&contraction.pure);
          *solid = false;
        }
      }
    for (auto& shell : uobs1)
      for (auto& contraction : shell.contr) {
        if (contraction.l == 1) {
          bool* solid = const_cast<bool*>(&contraction.pure);
          *solid = false;
        }
        if (contraction.l == 0) {
          bool* solid = const_cast<bool*>(&contraction.pure);
          *solid = false;
        }
      }
  }
  // Create buffer pointer to output
  py::buffer_info bufout = out.request();
  double* ptrout = (double*)bufout.ptr;

  auto max_nprim = std::max(basis0->obs.max_nprim(), basis1->obs.max_nprim());
  auto max_l = std::max(basis0->obs.max_l(), basis1->obs.max_l());
  libint2::Engine v_engine(
      libint2::Operator::nuclear,  // will compute overlap ints
      max_nprim,  // max # of primitives in shells this engine will accept
      max_l       // max angular momentum of shells this engine will accept
  );
  v_engine.set_params(make_point_charges(basis0->atoms));
  v_engine.set_params(make_point_charges(basis1->atoms));

  auto shell2bf0 =
      uobs0.shell2bf();  // maps shell index to basis function index
  auto shell2bf1 =
      uobs1.shell2bf();  // maps shell index to basis function index
                         // shell2bf[0] = index of the first basis function in
                         // shell 0 shell2bf[1] = index of the first basis
                         // function in shell 1
                         // ...
  const auto& buf_vec =
      v_engine.results();  // will point to computed shell sets
                           // const auto& is very important!

  // Loop over all shells
  for (size_t s0 = 0; s0 != uobs0.size(); ++s0) {
    for (size_t s1 = 0; s1 != uobs1.size(); ++s1) {
      v_engine.compute(uobs0[s0], uobs1[s1]);
      auto ints_shellset = buf_vec[0];  // location of the computed integrals
      if (ints_shellset == nullptr)
        continue;  // nullptr returned if the entire shell-set was screened out

      auto bf0 = shell2bf0[s0];    // first basis function in first shell
      auto n0 = uobs0[s0].size();  // number of basis functions in first shell
      auto bf1 = shell2bf1[s1];    // first basis function in second shell
      auto n1 = uobs1[s1].size();  // number of basis functions in second shell

      // integrals are packed into ints_shellset in row-major (C) form
      // this iterates over integrals in this order
      for (size_t f0 = 0; f0 != n0; ++f0)
        for (size_t f1 = 0; f1 != n1; ++f1) {
          ptrout[(bf0 + f0) * uobs1.nbf() + (bf1 + f1)] =
              ints_shellset[f0 * n1 + f1];
        }
    }
  }
  libint2::finalize();  // do not use libint after this
}
