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
#include "pvp.h"

#include "libint_utils.h"

typedef struct {
  long x;
  long y;
  long z;
} shell_index;

const static shell_index s[] = {
    {0, 0, 0},
};

const static shell_index p[] = {
    {1, 0, 0},
    {0, 1, 0},
    {0, 0, 1},
};

const static shell_index d[] = {
    {2, 0, 0}, {1, 1, 0}, {1, 0, 1}, {0, 2, 0}, {0, 1, 1}, {0, 0, 2},
};

const static shell_index f[] = {
    {3, 0, 0}, {2, 1, 0}, {2, 0, 1}, {1, 2, 0}, {1, 1, 1},
    {1, 0, 2}, {0, 3, 0}, {0, 2, 1}, {0, 1, 2}, {0, 0, 3},
};

const static shell_index g[] = {
    {4, 0, 0}, {3, 1, 0}, {3, 0, 1}, {2, 2, 0}, {2, 1, 1},
    {2, 0, 2}, {1, 3, 0}, {1, 2, 1}, {1, 1, 2}, {1, 0, 3},
    {0, 4, 0}, {0, 3, 1}, {0, 2, 2}, {0, 1, 3}, {0, 0, 4},
};

const static shell_index h[] = {
    {5, 0, 0}, {4, 1, 0}, {4, 0, 1}, {3, 2, 0}, {3, 1, 1}, {3, 0, 2}, {2, 3, 0},
    {2, 2, 1}, {2, 1, 2}, {2, 0, 3}, {1, 4, 0}, {1, 3, 1}, {1, 2, 2}, {1, 1, 3},
    {1, 0, 4}, {0, 5, 0}, {0, 4, 1}, {0, 3, 2}, {0, 2, 3}, {0, 1, 4}, {0, 0, 5},
};

const static shell_index i[] = {
    {6, 0, 0}, {5, 1, 0}, {5, 0, 1}, {4, 2, 0}, {4, 1, 1}, {4, 0, 2}, {3, 3, 0},
    {3, 2, 1}, {3, 1, 2}, {3, 0, 3}, {2, 4, 0}, {2, 3, 1}, {2, 2, 2}, {2, 1, 3},
    {2, 0, 4}, {1, 5, 0}, {1, 4, 1}, {1, 3, 2}, {1, 2, 3}, {1, 1, 4}, {1, 0, 5},
    {0, 6, 0}, {0, 5, 1}, {0, 4, 2}, {0, 3, 3}, {0, 2, 4}, {0, 1, 5}, {0, 0, 6},
};

const static shell_index k[] = {
    {7, 0, 0}, {6, 1, 0}, {6, 0, 1}, {5, 2, 0}, {5, 1, 1}, {5, 0, 2},
    {4, 3, 0}, {4, 2, 1}, {4, 1, 2}, {4, 0, 3}, {3, 4, 0}, {3, 3, 1},
    {3, 2, 2}, {3, 1, 3}, {3, 0, 4}, {2, 5, 0}, {2, 4, 1}, {2, 3, 2},
    {2, 2, 3}, {2, 1, 4}, {2, 0, 5}, {1, 6, 0}, {1, 5, 1}, {1, 4, 2},
    {1, 3, 3}, {1, 2, 4}, {1, 1, 5}, {1, 0, 6}, {0, 7, 0}, {0, 6, 1},
    {0, 5, 2}, {0, 4, 3}, {0, 3, 4}, {0, 2, 5}, {0, 1, 6}, {0, 0, 7},
};

typedef struct {
  long size;
  const shell_index* el;
} shell_struct;

const static shell_struct shell[8] = {{1, s},  {3, p},  {6, d},  {10, f},
                                      {15, g}, {21, h}, {28, i}, {36, k}};

// permute from solid harmonics to cartesian (y,z,x) -> (x,y,z)
const static size_t permute_psh[3] = {1, 2, 0};

long check_term_xyz(size_t xyz, size_t f, const shell_index* shelli) {
  if (xyz == 0)
    return shelli->x;
  else if (xyz == 1)
    return shelli->y;
  else if (xyz == 2)
    return shelli->z;
  else
    throw std::domain_error("xyz has to be in the interval [0,2]");
}

long get_subshell_index(size_t xyz, int shift, const shell_index* shelli,
                        const shell_index* shelli_,
                        const shell_struct* shells) {
  long x_ = shelli->x;
  long y_ = shelli->y;
  long z_ = shelli->z;
  if (xyz == 0)
    x_ += shift;
  else if (xyz == 1)
    y_ += shift;
  else if (xyz == 2)
    z_ += shift;

  for (long i = 0; i < shells->size; ++i) {
    if (shelli_->x == x_ && shelli_->y == y_ && shelli_->z == z_) return i;
    shelli_++;
  }
  return -1;
}

/**
 * Resolve the composite index for a two-dimensional array.
 * For p-shells, we have to permute the indices back to cartesian ordering.
 *
 * @param bfs0 Pointer to array transforming shell to basis function basis0
 * (uncontracted solid harmonics).
 * @param bfs1 Pointer to array transforming shell to basis function basis1
 * (uncontracted solid harmonics).
 * @param f0 Iteration index over ns0.
 * @param f1 Iteration index over ns1.
 * @param ns0 Pointer to an array containing the number of uncontracted basis
 * function (basis0) per shell.
 * @param ns1 Pointer to an array containing the number of uncontracted basis
 * function (basis1) per shell.
 * @param s0 Iteration index over uncontracted cartesian basis functions
 * (basis0).
 * @param s1 Iteration index over uncontracted cartesian basis functions
 * (basis1).
 * @param uobs1_s The uncontracted basis set in solid harmonics.
 */
long permute_p_shell(const size_t* bfs0, const size_t* bfs1, const size_t f0,
                     const size_t f1, const size_t* ns0, const size_t* ns1,
                     const size_t s0, const size_t s1,
                     libint2::BasisSet uobs1_s) {
  auto inds = (bfs0[s0] + f0) * uobs1_s.nbf() + (bfs1[s1] + f1);
  if (ns0[s0] == 3) {
    if (ns1[s1] == 3) {
      inds = (bfs0[s0] + permute_psh[f0]) * uobs1_s.nbf() +
             (bfs1[s1] + permute_psh[f1]);
    } else {
      inds = (bfs0[s0] + permute_psh[f0]) * uobs1_s.nbf() + (bfs1[s1] + f1);
    }
  } else {
    if (ns1[s1] == 3) {
      inds = (bfs0[s0] + f0) * uobs1_s.nbf() + (bfs1[s1] + permute_psh[f1]);
    }
  }
  return inds;
}

void compute_pvp(
    Basis* basis0, Basis* basis1,
    py::array_t<double, py::array::c_style | py::array::forcecast>& out,
    bool uncontract) {
  // Do not rescale contraction coefficients to ensure unit normalization of all
  // solid harmonics Gaussians and the axis-aligned (xl, yl, zl) Cartesian
  // Gaussians
  libint2::Shell::do_enforce_unit_normalization(false);

  libint2::initialize();  // safe to use libint now

  if (uncontract != true)
    throw std::invalid_argument(
        "pVp integrals can only be calculated for an uncontracted basis");
  // uncontract basis:
  auto uobs0 = uncontract_basis_set(basis0);
  auto uobs1 = uncontract_basis_set(basis1);
  auto uobs0_s = uncontract_basis_set(basis0);
  auto uobs1_s = uncontract_basis_set(basis1);
  // set all to solid harmonics to do the transformation properly
  uobs0_s.set_pure(true);
  uobs1_s.set_pure(true);
  // Create buffer pointer to output
  py::buffer_info bufout = out.request();
  double* ptrout = (double*)bufout.ptr;

  auto max_nprim = std::max(basis0->obs.max_nprim(), basis1->obs.max_nprim());
  auto max_l = std::max(basis0->obs.max_l(), basis1->obs.max_l());
  libint2::Engine v_engine(
      libint2::Operator::nuclear,  // will compute overlap ints
      max_nprim,  // max # of primitives in shells this engine will accept
      max_l + 1   // max angular momentum of shells this engine will accept
  );
  v_engine.set_params(make_point_charges(basis0->atoms));
  v_engine.set_params(make_point_charges(basis1->atoms));

  // maps shell index to basis function index
  auto shell2bf0 =
      uobs0.shell2bf();  // maps shell index to basis function index
  auto shell2bf1 =
      uobs1.shell2bf();  // maps shell index to basis function index

  const auto& buf_vec =
      v_engine.results();  // will point to computed shell sets
                           // const auto& is very important!

  // Dummy loop to get information about indices in solid harmonics
  auto shell2bf0_s = uobs0_s.shell2bf();
  size_t* bfs0 = new size_t[uobs0_s.size()]();
  size_t* ns0 = new size_t[uobs0_s.size()]();
  for (size_t s0 = 0; s0 != uobs0_s.size(); ++s0) {
    bfs0[s0] = shell2bf0_s[s0];
    ns0[s0] = uobs0_s[s0].size();
  }
  auto shell2bf1_s = uobs1_s.shell2bf();
  size_t* bfs1 = new size_t[uobs1_s.size()]();
  size_t* ns1 = new size_t[uobs1_s.size()]();
  for (size_t s1 = 0; s1 != uobs1_s.size(); ++s1) {
    bfs1[s1] = shell2bf1_s[s1];
    ns1[s1] = uobs1_s[s1].size();
  }

  // derivative information on pVp integrals
  int subtract[4][4] = {{-1, -1}, {1, -1}, {-1, 1}, {1, 1}};

  // <-->, <+->, <-+>, <++>
  for (int iter = 0; iter < 4; ++iter) {
    // Loop over all shells
    for (size_t s0 = 0; s0 != uobs0.size(); ++s0) {
      // create a temporary copy of the contraction coefficients that we need to
      // modify
      int* contr0l = const_cast<int*>(&uobs0[s0].contr[0].l);
      auto n0 = uobs0[s0].size();  // number of basis functions in first shell
      auto l0 = uobs0[s0].contr[0].l;
      auto a0 = uobs0[s0].alpha[0];
      // Get Shell structure information:
      const shell_struct* shell0 = &shell[l0];
      const shell_index* shell0_i;
      shell0_i = shell0->el;

      if (iter == 0 || iter == 2)
        if (uobs0[s0].contr[0].l == 0) continue;
      *contr0l += subtract[iter][0];
      auto l0_ = uobs0[s0].contr[0].l;
      for (size_t s1 = 0; s1 != uobs1.size(); ++s1) {
        const long ncart = ((max_l + 2) * (max_l + 3)) / 2;
        const long nsolid = 2 * max_l + 1;
        // Temporary work arrays
        double* cart_ = new double[ncart * ncart]{0.0};
        // create a temporary copy of the contraction coefficients that we need
        // to modify
        int* contr1l = const_cast<int*>(&uobs1[s1].contr[0].l);
        if (iter == 0 || iter == 1)
          if (uobs1[s1].contr[0].l == 0) continue;
        auto n1 =
            uobs1[s1].size();  // number of basis functions in second shell
        auto l1 = uobs1[s1].contr[0].l;
        auto a1 = uobs1[s1].alpha[0];
        *contr1l += subtract[iter][1];
        auto n1_ = uobs1[s1].size();
        auto l1_ = uobs1[s1].contr[0].l;

        // Get Shell structure information:
        const shell_struct* shell1 = &shell[l1];
        const shell_index* shell1_i;

        v_engine.compute(uobs0[s0], uobs1[s1]);

        auto ints_shellset = buf_vec[0];  // location of the computed integrals
        if (ints_shellset == nullptr)
          continue;  // nullptr returned if the entire shell-set was screened
                     // out

        // reset first shell
        shell0_i = shell0->el;
        for (size_t f0 = 0; f0 != n0; ++f0) {
          // reset second shell
          shell1_i = shell1->el;
          for (size_t f1 = 0; f1 != n1; ++f1) {
            // Loop over x, y, z
            for (auto xyz = 0; xyz < 3; ++xyz) {
              if (subtract[iter][0] == -1)
                if (!check_term_xyz(xyz, f0, shell0_i)) continue;
              if (subtract[iter][1] == -1)
                if (!check_term_xyz(xyz, f1, shell1_i)) continue;

              // get index of shell derivative
              const shell_struct* shell0_ = &shell[l0_];
              const shell_index* shell0_i_;
              shell0_i_ = shell0_->el;
              long index0_ = get_subshell_index(xyz, subtract[iter][0],
                                                shell0_i, shell0_i_, shell0_);

              const shell_struct* shell1_ = &shell[l1_];
              const shell_index* shell1_i_;
              shell1_i_ = shell1_->el;
              long index1_ = get_subshell_index(xyz, subtract[iter][1],
                                                shell1_i, shell1_i_, shell1_);

              if (index0_ < 0 || index1_ < 0)
                throw std::domain_error("Invalid index!");

              double factor = 1.0;
              if (subtract[iter][0] == 1)
                factor *= -2.0 * a0;
              else
                factor *= check_term_xyz(xyz, f0, shell0_i);
              if (subtract[iter][1] == 1)
                factor *= -2.0 * a1;
              else
                factor *= check_term_xyz(xyz, f1, shell1_i);

              // Loop over new second shell
              cart_[f0 * n1 + f1] +=
                  ints_shellset[index0_ * n1_ + index1_] * factor;
            }
            shell1_i++;
          }  // end for f2
          shell0_i++;
        }  // end for f1
        // Transform back to real solid harmonics using libints tfrom function
        // Temporary work arrays
        double* solid_ = new double[nsolid * nsolid]{0.0};
        // do the actual transformation
        libint2::solidharmonics::tform(
            uobs0_s[s0].contr[0], uobs1_s[s1].contr[0], &cart_[0], &solid_[0]);
        delete[] cart_;
        // Assign to output array
        for (size_t f0 = 0; f0 != ns0[s0]; ++f0) {
          for (size_t f1 = 0; f1 != ns1[s1]; ++f1) {
            // We have to permute p functions as tform transforms them into
            // solid harmonics as well.
            auto inds =
                permute_p_shell(bfs0, bfs1, f0, f1, ns0, ns1, s0, s1, uobs1_s);
            ptrout[inds] += solid_[f0 * ns1[s1] + f1];
          }
        }
        delete[] solid_;
        // reset l quantum number to calculate next basis set element
        *contr1l -= subtract[iter][1];
      }  // end for s2
      // reset l quantum number to calculate next basis set element
      *contr0l -= subtract[iter][0];
    }
  }
  libint2::finalize();  // do not use libint after this
}

void compute_ppcp(
    Basis* basis0, Basis* basis1, ExternalCharges* charges,
    py::array_t<double, py::array::c_style | py::array::forcecast>& out,
    bool uncontract) {
  // Do not rescale contraction coefficients to ensure unit normalization of all
  // solid harmonics Gaussians and the axis-aligned (xl, yl, zl) Cartesian
  // Gaussians
  libint2::Shell::do_enforce_unit_normalization(false);

  libint2::initialize();  // safe to use libint now

  if (uncontract != true)
    throw std::invalid_argument(
        "pPCp integrals can only be calculated for an uncontracted basis");
  // uncontract basis:
  auto uobs0 = uncontract_basis_set(basis0);
  auto uobs1 = uncontract_basis_set(basis1);
  auto uobs0_s = uncontract_basis_set(basis0);
  auto uobs1_s = uncontract_basis_set(basis1);
  // set all to solid harmonics to do the transformation properly
  uobs0_s.set_pure(true);
  uobs1_s.set_pure(true);
  // Create buffer pointer to output
  py::buffer_info bufout = out.request();
  double* ptrout = (double*)bufout.ptr;

  auto max_nprim = std::max(basis0->obs.max_nprim(), basis1->obs.max_nprim());
  auto max_l = std::max(basis0->obs.max_l(), basis1->obs.max_l());
  libint2::Engine v_engine(
      libint2::Operator::nuclear,  // will compute overlap ints
      max_nprim,  // max # of primitives in shells this engine will accept
      max_l + 1   // max angular momentum of shells this engine will accept
  );
  auto charges_ = charges->get_charge_pairs();
  v_engine.set_params(charges_);

  // maps shell index to basis function index
  auto shell2bf0 =
      uobs0.shell2bf();  // maps shell index to basis function index
  auto shell2bf1 =
      uobs1.shell2bf();  // maps shell index to basis function index

  const auto& buf_vec =
      v_engine.results();  // will point to computed shell sets
                           // const auto& is very important!

  // Dummy loop to get information about indices in solid harmonics
  auto shell2bf0_s = uobs0_s.shell2bf();
  size_t* bfs0 = new size_t[uobs0_s.size()]();
  size_t* ns0 = new size_t[uobs0_s.size()]();
  for (size_t s0 = 0; s0 != uobs0_s.size(); ++s0) {
    bfs0[s0] = shell2bf0_s[s0];
    ns0[s0] = uobs0_s[s0].size();
  }
  auto shell2bf1_s = uobs1_s.shell2bf();
  size_t* bfs1 = new size_t[uobs1_s.size()]();
  size_t* ns1 = new size_t[uobs1_s.size()]();
  for (size_t s1 = 0; s1 != uobs1_s.size(); ++s1) {
    bfs1[s1] = shell2bf1_s[s1];
    ns1[s1] = uobs1_s[s1].size();
  }

  // derivative information on pcpp integrals
  int subtract[4][4] = {{-1, -1}, {1, -1}, {-1, 1}, {1, 1}};

  // <-->, <+->, <-+>, <++>
  for (int iter = 0; iter < 4; ++iter) {
    // Loop over all shells
    for (size_t s0 = 0; s0 != uobs0.size(); ++s0) {
      // create a temporary copy of the contraction coefficients that we need to
      // modify
      int* contr0l = const_cast<int*>(&uobs0[s0].contr[0].l);
      auto n0 = uobs0[s0].size();  // number of basis functions in first shell
      auto l0 = uobs0[s0].contr[0].l;
      auto a0 = uobs0[s0].alpha[0];
      // Get Shell structure information:
      const shell_struct* shell0 = &shell[l0];
      const shell_index* shell0_i;
      shell0_i = shell0->el;

      if (iter == 0 || iter == 2)
        if (uobs0[s0].contr[0].l == 0) continue;
      *contr0l += subtract[iter][0];
      auto l0_ = uobs0[s0].contr[0].l;
      for (size_t s1 = 0; s1 != uobs1.size(); ++s1) {
        const long ncart = ((max_l + 2) * (max_l + 3)) / 2;
        const long nsolid = 2 * max_l + 1;
        // Temporary work arrays
        double* cart_ = new double[ncart * ncart]{0.0};
        // create a temporary copy of the contraction coefficients that we need
        // to modify
        int* contr1l = const_cast<int*>(&uobs1[s1].contr[0].l);
        if (iter == 0 || iter == 1)
          if (uobs1[s1].contr[0].l == 0) continue;
        auto n1 =
            uobs1[s1].size();  // number of basis functions in second shell
        auto l1 = uobs1[s1].contr[0].l;
        auto a1 = uobs1[s1].alpha[0];
        *contr1l += subtract[iter][1];
        auto n1_ = uobs1[s1].size();
        auto l1_ = uobs1[s1].contr[0].l;

        // Get Shell structure information:
        const shell_struct* shell1 = &shell[l1];
        const shell_index* shell1_i;

        v_engine.compute(uobs0[s0], uobs1[s1]);

        auto ints_shellset = buf_vec[0];  // location of the computed integrals
        if (ints_shellset == nullptr)
          continue;  // nullptr returned if the entire shell-set was screened
                     // out

        // reset first shell
        shell0_i = shell0->el;
        for (size_t f0 = 0; f0 != n0; ++f0) {
          // reset second shell
          shell1_i = shell1->el;
          for (size_t f1 = 0; f1 != n1; ++f1) {
            // Loop over x, y, z
            for (auto xyz = 0; xyz < 3; ++xyz) {
              if (subtract[iter][0] == -1)
                if (!check_term_xyz(xyz, f0, shell0_i)) continue;
              if (subtract[iter][1] == -1)
                if (!check_term_xyz(xyz, f1, shell1_i)) continue;

              // get index of shell derivative
              const shell_struct* shell0_ = &shell[l0_];
              const shell_index* shell0_i_;
              shell0_i_ = shell0_->el;
              long index0_ = get_subshell_index(xyz, subtract[iter][0],
                                                shell0_i, shell0_i_, shell0_);

              const shell_struct* shell1_ = &shell[l1_];
              const shell_index* shell1_i_;
              shell1_i_ = shell1_->el;
              long index1_ = get_subshell_index(xyz, subtract[iter][1],
                                                shell1_i, shell1_i_, shell1_);

              if (index0_ < 0 || index1_ < 0)
                throw std::domain_error("Invalid index!");

              double factor = 1.0;
              if (subtract[iter][0] == 1)
                factor *= -2.0 * a0;
              else
                factor *= check_term_xyz(xyz, f0, shell0_i);
              if (subtract[iter][1] == 1)
                factor *= -2.0 * a1;
              else
                factor *= check_term_xyz(xyz, f1, shell1_i);

              // Loop over new second shell
              cart_[f0 * n1 + f1] +=
                  ints_shellset[index0_ * n1_ + index1_] * factor;
            }
            shell1_i++;
          }  // end for f2
          shell0_i++;
        }  // end for f1
        // Transform back to real solid harmonics using libints tfrom function
        // Temporary work arrays
        double* solid_ = new double[nsolid * nsolid]{0.0};
        // do the actual transformation
        libint2::solidharmonics::tform(
            uobs0_s[s0].contr[0], uobs1_s[s1].contr[0], &cart_[0], &solid_[0]);
        delete[] cart_;
        // Assign to output array
        for (size_t f0 = 0; f0 != ns0[s0]; ++f0) {
          for (size_t f1 = 0; f1 != ns1[s1]; ++f1) {
            // We have to permute p functions as tform transforms them into
            // solid harmonics as well.
            auto inds =
                permute_p_shell(bfs0, bfs1, f0, f1, ns0, ns1, s0, s1, uobs1_s);
            ptrout[inds] += solid_[f0 * ns1[s1] + f1];
          }
        }
        delete[] solid_;
        // reset l quantum number to calculate next basis set element
        *contr1l -= subtract[iter][1];
      }  // end for s2
      // reset l quantum number to calculate next basis set element
      *contr0l -= subtract[iter][0];
    }
  }
  libint2::finalize();  // do not use libint after this
}
