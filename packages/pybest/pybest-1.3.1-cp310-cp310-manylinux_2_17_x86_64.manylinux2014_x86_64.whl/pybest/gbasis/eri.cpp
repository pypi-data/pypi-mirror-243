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
#include "eri.h"

// libint2 stores eri as (ij|kl), while pybest uses <ik|jl>. In the libint
// interface the basis sets are indexed as follows (01|23), while in pybest
// we use <02|13>. Thus, the basis sets in the functional defintion are
// changed to agree with the pybest order.
void compute_eri(
    Basis *basis0, Basis *basis2, Basis *basis1, Basis *basis3,
    py::array_t<double, py::array::c_style | py::array::forcecast> &out,
    bool symmetry) {
  // Check if number of dimensions of np.ndarray is correct, if not, raise
  // ValueError
  out.mutable_unchecked<4>();
  // Do not rescale contraction coefficients to ensure unit normalization of all
  // solid harmonics Gaussians and the axis-aligned (xl, yl, zl) Cartesian
  // Gaussians
  libint2::Shell::do_enforce_unit_normalization(false);

  libint2::initialize();  // safe to use libint now

  auto max_nprim = std::max(basis0->obs.max_nprim(), basis1->obs.max_nprim());
  max_nprim = std::max(max_nprim, basis2->obs.max_nprim());
  max_nprim = std::max(max_nprim, basis3->obs.max_nprim());
  auto max_l = std::max(basis0->obs.max_l(), basis1->obs.max_l());
  max_l = std::max(max_l, basis2->obs.max_l());
  max_l = std::max(max_l, basis3->obs.max_l());
  libint2::Engine c_engine(
      libint2::Operator::coulomb,  // will compute overlap ints
      max_nprim,  // max # of primitives in shells this engine will accept
      max_l       // max angular momentum of shells this engine will accept
  );

  auto shell2bf0 =
      basis0->obs.shell2bf();  // maps shell index to basis function index
  auto shell2bf1 =
      basis1->obs.shell2bf();  // maps shell index to basis function index
  auto shell2bf2 =
      basis2->obs.shell2bf();  // maps shell index to basis function index
  auto shell2bf3 =
      basis3->obs.shell2bf();  // maps shell index to basis function index
                               // shell2bf[0] = index of the first basis
                               // function in shell 0 shell2bf[1] = index of the
                               // first basis function in shell 1
                               // ...
  const auto &buf_vec =
      c_engine.results();  // will point to computed shell sets
                           // const auto& is very important!

  // Create buffer pointer to output
  py::buffer_info bufout = out.request();
  double *ptrout = (double *)bufout.ptr;

  // Loop over all shells
  auto end0 = basis0->obs.size();
  auto end1 = basis1->obs.size();
  auto end2 = basis2->obs.size();
  auto end3 = basis3->obs.size();
  for (size_t s0 = 0; s0 != end0; ++s0) {
    if (symmetry) end1 = s0 + 1;
    for (size_t s1 = 0; s1 != end1; ++s1) {
      for (size_t s2 = 0; s2 != end2; ++s2) {
        if (symmetry) end3 = s2 + 1;
        for (size_t s3 = 0; s3 != end3; ++s3) {
          if (((s0 * (s0 + 1) / 2 + s1) >= (s2 * (s2 + 1) / 2 + s3)) ||
              !symmetry) {
            c_engine.compute(basis0->obs[s0], basis1->obs[s1], basis2->obs[s2],
                             basis3->obs[s3]);
            auto ints_shellset =
                buf_vec[0];  // location of the computed integrals
            if (ints_shellset == nullptr)
              continue;  // nullptr returned if the entire shell-set was
                         // screened out

            auto bf0 = shell2bf0[s0];  // first basis function in first shell
            auto n0 = basis0->obs[s0]
                          .size();  // number of basis functions in first shell
            auto bf1 = shell2bf1[s1];  // first basis function in first shell
            auto n1 = basis1->obs[s1]
                          .size();  // number of basis functions in first shell
            auto bf2 = shell2bf2[s2];  // first basis function in second shell
            auto n2 = basis2->obs[s2]
                          .size();  // number of basis functions in second shell
            auto bf3 = shell2bf3[s3];  // first basis function in second shell
            auto n3 = basis3->obs[s3]
                          .size();  // number of basis functions in second shell

            // integrals are packed into ints_shellset in row-major (C) form
            // this iterates over integrals in this order
            for (size_t f0 = 0; f0 != n0; ++f0)
              for (size_t f1 = 0; f1 != n1; ++f1)
                for (size_t f2 = 0; f2 != n2; ++f2)
                  for (size_t f3 = 0; f3 != n3; ++f3) {
                    auto index0 = (((bf0 + f0) * basis2->obs.nbf() + bf2 + f2) *
                                       basis1->obs.nbf() +
                                   bf1 + f1) *
                                      basis3->obs.nbf() +
                                  bf3 + f3;
                    // output[(((bf0+f0)*basis2->obs.nbf()+bf2+f2)*basis1->obs.nbf()+bf1+f1)*basis3->obs.nbf()+bf3+f3]
                    // = ints_shellset[((f0*n1+f1)*n2+f2)*n3+f3];
                    auto val =
                        ints_shellset[((f0 * n1 + f1) * n2 + f2) * n3 + f3];
                    ptrout[index0] = val;
                    if (symmetry) {
                      auto index1 =
                          (((bf1 + f1) * basis2->obs.nbf() + bf2 + f2) *
                               basis0->obs.nbf() +
                           bf0 + f0) *
                              basis3->obs.nbf() +
                          bf3 + f3;
                      auto index2 =
                          (((bf0 + f0) * basis3->obs.nbf() + bf3 + f3) *
                               basis1->obs.nbf() +
                           bf1 + f1) *
                              basis2->obs.nbf() +
                          bf2 + f2;
                      auto index3 =
                          (((bf1 + f1) * basis3->obs.nbf() + bf3 + f3) *
                               basis0->obs.nbf() +
                           bf0 + f0) *
                              basis2->obs.nbf() +
                          bf2 + f2;
                      auto index4 =
                          (((bf2 + f2) * basis0->obs.nbf() + bf0 + f0) *
                               basis3->obs.nbf() +
                           bf3 + f3) *
                              basis1->obs.nbf() +
                          bf1 + f1;
                      auto index5 =
                          (((bf3 + f3) * basis0->obs.nbf() + bf0 + f0) *
                               basis2->obs.nbf() +
                           bf2 + f2) *
                              basis1->obs.nbf() +
                          bf1 + f1;
                      auto index6 =
                          (((bf2 + f2) * basis1->obs.nbf() + bf1 + f1) *
                               basis3->obs.nbf() +
                           bf3 + f3) *
                              basis0->obs.nbf() +
                          bf0 + f0;
                      auto index7 =
                          (((bf3 + f3) * basis1->obs.nbf() + bf1 + f1) *
                               basis2->obs.nbf() +
                           bf2 + f2) *
                              basis0->obs.nbf() +
                          bf0 + f0;
                      ptrout[index1] = val;
                      ptrout[index2] = val;
                      ptrout[index3] = val;
                      ptrout[index4] = val;
                      ptrout[index5] = val;
                      ptrout[index6] = val;
                      ptrout[index7] = val;
                    }
                  }
          }
        }
      }
    }
  }
  libint2::finalize();  // do not use libint after this
}
