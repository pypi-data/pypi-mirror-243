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
#include "emultipole.h"

void compute_dipole(
    Basis *basis0, Basis *basis1,
    py::array_t<double, py::array::c_style | py::array::forcecast> &olp,
    py::array_t<double, py::array::c_style | py::array::forcecast> &mux,
    py::array_t<double, py::array::c_style | py::array::forcecast> &muy,
    py::array_t<double, py::array::c_style | py::array::forcecast> &muz,
    double x, double y, double z) {
  // Do not rescale contraction coefficients to ensure unit normalization of all
  // solid harmonics Gaussians and the axis-aligned (xl, yl, zl) Cartesian
  // Gaussians
  libint2::Shell::do_enforce_unit_normalization(false);

  libint2::initialize();  // safe to use libint now

  auto max_nprim = std::max(basis0->obs.max_nprim(), basis1->obs.max_nprim());
  auto max_l = std::max(basis0->obs.max_l(), basis1->obs.max_l());
  libint2::Engine mu_engine(
      libint2::Operator::emultipole1,
      max_nprim,  // max # of primitives in shells this engine will accept
      max_l       // max angular momentum of shells this engine will accept
  );
  mu_engine.set_params(std::array<double, 3>{x, y, z});

  auto shell2bf0 =
      basis0->obs.shell2bf();  // maps shell index to basis function index
  auto shell2bf1 =
      basis1->obs.shell2bf();  // maps shell index to basis function index
                               // shell2bf[0] = index of the first basis
                               // function in shell 0 shell2bf[1] = index of the
                               // first basis function in shell 1
                               // ...
  const auto &buf_vec =
      mu_engine.results();  // will point to computed shell sets
                            // const auto& is very important!

  // Create buffer pointer to outputs
  py::buffer_info bufolp = olp.request();
  py::buffer_info bufmux = mux.request();
  py::buffer_info bufmuy = muy.request();
  py::buffer_info bufmuz = muz.request();
  double *ptrolp = (double *)bufolp.ptr;
  double *ptrmux = (double *)bufmux.ptr;
  double *ptrmuy = (double *)bufmuy.ptr;
  double *ptrmuz = (double *)bufmuz.ptr;
  // Loop over all shells
  for (size_t s0 = 0; s0 != basis0->obs.size(); ++s0) {
    for (size_t s1 = 0; s1 != basis1->obs.size(); ++s1) {
      mu_engine.compute(basis0->obs[s0], basis1->obs[s1]);
      auto ints_shellset = buf_vec[0];  // location of the computed integrals
      if (ints_shellset == nullptr)
        continue;  // nullptr returned if the entire shell-set was screened out

      auto bf0 = shell2bf0[s0];  // first basis function in second shell
      auto n0 =
          basis0->obs[s0].size();  // number of basis functions in second shell
      auto bf1 = shell2bf1[s1];    // first basis function in first shell
      auto n1 =
          basis1->obs[s1].size();  // number of basis functions in first shell

      auto s_shellset = buf_vec[0];  // skipped nullptr check for simplicity
      auto mux_shellset = buf_vec[1];
      auto muy_shellset = buf_vec[2];
      auto muz_shellset = buf_vec[3];
      // integrals are packed into ints_shellset in row-major (C) form
      // this iterates over integrals in this order
      for (size_t f0 = 0; f0 != n0; ++f0)
        for (size_t f1 = 0; f1 != n1; ++f1) {
          ptrolp[(bf0 + f0) * basis1->obs.nbf() + (bf1 + f1)] =
              s_shellset[f0 * n1 + f1];
          ptrmux[(bf0 + f0) * basis1->obs.nbf() + (bf1 + f1)] =
              mux_shellset[f0 * n1 + f1];
          ptrmuy[(bf0 + f0) * basis1->obs.nbf() + (bf1 + f1)] =
              muy_shellset[f0 * n1 + f1];
          ptrmuz[(bf0 + f0) * basis1->obs.nbf() + (bf1 + f1)] =
              muz_shellset[f0 * n1 + f1];
        }
    }
  }
  libint2::finalize();  // do not use libint after this
}

void compute_quadrupole(
    Basis *basis0, Basis *basis1,
    py::array_t<double, py::array::c_style | py::array::forcecast> &olp,
    py::array_t<double, py::array::c_style | py::array::forcecast> &mux,
    py::array_t<double, py::array::c_style | py::array::forcecast> &muy,
    py::array_t<double, py::array::c_style | py::array::forcecast> &muz,
    py::array_t<double, py::array::c_style | py::array::forcecast> &muxx,
    py::array_t<double, py::array::c_style | py::array::forcecast> &muxy,
    py::array_t<double, py::array::c_style | py::array::forcecast> &muxz,
    py::array_t<double, py::array::c_style | py::array::forcecast> &muyy,
    py::array_t<double, py::array::c_style | py::array::forcecast> &muyz,
    py::array_t<double, py::array::c_style | py::array::forcecast> &muzz,
    double x, double y, double z) {
  // Do not rescale contraction coefficients to ensure unit normalization of all
  // solid harmonics Gaussians and the axis-aligned (xl, yl, zl) Cartesian
  // Gaussians
  libint2::Shell::do_enforce_unit_normalization(false);

  libint2::initialize();  // safe to use libint now

  auto max_nprim = std::max(basis0->obs.max_nprim(), basis1->obs.max_nprim());
  auto max_l = std::max(basis0->obs.max_l(), basis1->obs.max_l());
  libint2::Engine mu_engine(
      libint2::Operator::emultipole2,
      max_nprim,  // max # of primitives in shells this engine will accept
      max_l       // max angular momentum of shells this engine will accept
  );
  mu_engine.set_params(std::array<double, 3>{x, y, z});

  auto shell2bf0 =
      basis0->obs.shell2bf();  // maps shell index to basis function index
  auto shell2bf1 =
      basis1->obs.shell2bf();  // maps shell index to basis function index
                               // shell2bf[0] = index of the first basis
                               // function in shell 0 shell2bf[1] = index of the
                               // first basis function in shell 1
                               // ...
  const auto &buf_vec =
      mu_engine.results();  // will point to computed shell sets
                            // const auto& is very important!

  // Create buffer pointer to outputs
  py::buffer_info bufolp = olp.request();
  py::buffer_info bufmux = mux.request();
  py::buffer_info bufmuy = muy.request();
  py::buffer_info bufmuz = muz.request();
  py::buffer_info bufmuxx = muxx.request();
  py::buffer_info bufmuxy = muxy.request();
  py::buffer_info bufmuxz = muxz.request();
  py::buffer_info bufmuyy = muyy.request();
  py::buffer_info bufmuyz = muyz.request();
  py::buffer_info bufmuzz = muzz.request();
  double *ptrolp = (double *)bufolp.ptr;
  double *ptrmux = (double *)bufmux.ptr;
  double *ptrmuy = (double *)bufmuy.ptr;
  double *ptrmuz = (double *)bufmuz.ptr;
  double *ptrmuxx = (double *)bufmuxx.ptr;
  double *ptrmuxy = (double *)bufmuxy.ptr;
  double *ptrmuxz = (double *)bufmuxz.ptr;
  double *ptrmuyy = (double *)bufmuyy.ptr;
  double *ptrmuyz = (double *)bufmuyz.ptr;
  double *ptrmuzz = (double *)bufmuzz.ptr;
  // Loop over all shells
  for (size_t s0 = 0; s0 != basis0->obs.size(); ++s0) {
    for (size_t s1 = 0; s1 != basis1->obs.size(); ++s1) {
      mu_engine.compute(basis0->obs[s0], basis1->obs[s1]);
      auto ints_shellset = buf_vec[0];  // location of the computed integrals
      if (ints_shellset == nullptr)
        continue;  // nullptr returned if the entire shell-set was screened out

      auto bf0 = shell2bf0[s0];  // first basis function in second shell
      auto n0 =
          basis0->obs[s0].size();  // number of basis functions in second shell
      auto bf1 = shell2bf1[s1];    // first basis function in first shell
      auto n1 =
          basis1->obs[s1].size();  // number of basis functions in first shell

      auto s_shellset = buf_vec[0];  // skipped nullptr check for simplicity
      auto mux_shellset = buf_vec[1];
      auto muy_shellset = buf_vec[2];
      auto muz_shellset = buf_vec[3];
      auto muxx_shellset = buf_vec[4];
      auto muxy_shellset = buf_vec[5];
      auto muxz_shellset = buf_vec[6];
      auto muyy_shellset = buf_vec[7];
      auto muyz_shellset = buf_vec[8];
      auto muzz_shellset = buf_vec[9];
      // integrals are packed into ints_shellset in row-major (C) form
      // this iterates over integrals in this order
      for (size_t f0 = 0; f0 != n0; ++f0)
        for (size_t f1 = 0; f1 != n1; ++f1) {
          ptrolp[(bf0 + f0) * basis1->obs.nbf() + (bf1 + f1)] =
              s_shellset[f0 * n1 + f1];
          ptrmux[(bf0 + f0) * basis1->obs.nbf() + (bf1 + f1)] =
              mux_shellset[f0 * n1 + f1];
          ptrmuy[(bf0 + f0) * basis1->obs.nbf() + (bf1 + f1)] =
              muy_shellset[f0 * n1 + f1];
          ptrmuz[(bf0 + f0) * basis1->obs.nbf() + (bf1 + f1)] =
              muz_shellset[f0 * n1 + f1];
          ptrmuxx[(bf0 + f0) * basis1->obs.nbf() + (bf1 + f1)] =
              muxx_shellset[f0 * n1 + f1];
          ptrmuxy[(bf0 + f0) * basis1->obs.nbf() + (bf1 + f1)] =
              muxy_shellset[f0 * n1 + f1];
          ptrmuxz[(bf0 + f0) * basis1->obs.nbf() + (bf1 + f1)] =
              muxz_shellset[f0 * n1 + f1];
          ptrmuyy[(bf0 + f0) * basis1->obs.nbf() + (bf1 + f1)] =
              muyy_shellset[f0 * n1 + f1];
          ptrmuyz[(bf0 + f0) * basis1->obs.nbf() + (bf1 + f1)] =
              muyz_shellset[f0 * n1 + f1];
          ptrmuzz[(bf0 + f0) * basis1->obs.nbf() + (bf1 + f1)] =
              muzz_shellset[f0 * n1 + f1];
        }
    }
  }
  libint2::finalize();  // do not use libint after this
}
