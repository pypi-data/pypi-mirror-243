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

#include "basis.h"

#include <math.h>
#include <stdlib.h>

#include <Eigen/Core>
#include <cmath>
#include <cstdlib>
#include <cstring>
#include <fstream>
#include <iomanip>
#include <iostream>
#include <stdexcept>
#include <string>

#include "libint_utils.h"

using std::abs;

/*
    Basis

*/

// Overload constructor:
Basis::Basis(const std::string& basisname, const std::string& molfile,
             const std::string& dirname)
    : basisname(basisname), molfile(molfile), dirname(dirname) {
  libint2::Shell::do_enforce_unit_normalization(false);

  // read coordinates and initialize atoms
  std::string xyzfilename = std::string(molfile);
  std::ifstream input_file(xyzfilename);
  atoms = libint2::read_dotxyz(input_file);

  // Change LIBINT_DATA_PATH to read in basis set from correct directory
  // dirname. This change is only locally and does not affect the global
  // enviromnent variable.
  std::string pybestdata = std::string(dirname);
  std::string mypath_ = "LIBINT_DATA_PATH=" + pybestdata;
  putenv(strdup(mypath_.c_str()));

  // Do not print stdout of libint
  // get underlying buffer
  std::streambuf* orig_buf = std::cout.rdbuf();
  std::cout.rdbuf(NULL);
  obs = libint2::BasisSet(basisname, atoms);
  // restore buffer
  std::cout.rdbuf(orig_buf);

  nbasis = obs.nbf();
  nshell = obs.size();
  ncenter = atoms.size();
  shell2atom = obs.shell2atom(atoms);
  for (std::size_t s = 0; s != obs.size(); ++s) {
    for (const auto& c : obs[s].contr) {
      auto factor = (!c.pure && c.l > 1) ? -1 : 1;
      shell_types.push_back(c.l * factor);
      for (auto n = 0ul; n < obs[s].alpha.size(); ++n) {
        // use normalization factor to get back to original coefficient
        double normalization_factor = get_renorm(c.l, s, n);
        contraction.push_back(c.coeff[n] / normalization_factor);
        alpha.push_back(obs[s].alpha[n]);
      }
    }
    nprim.push_back(obs[s].nprim());
  }
  for (auto a = 0ul; a < atoms.size(); ++a) {
    atomic_numbers.push_back(atoms[a].atomic_number);
    std::vector<double> xyz;
    xyz.push_back(atoms[a].x);
    xyz.push_back(atoms[a].y);
    xyz.push_back(atoms[a].z);
    coordinates.push_back(xyz);
  }
  libint2::finalize();  // do not use libint after this
}

Basis::Basis(const std::string& molfile, std::vector<long> nprims,
             std::vector<long> center, std::vector<int> l,
             std::vector<double> alphas, std::vector<double> contr)
    : basisname(""), molfile(molfile), dirname("") {
  // Do some standard test:
  if (nprims.size() != center.size())
    throw std::domain_error("Number of primitives and centers does not match.");
  if (nprims.size() != l.size())
    throw std::domain_error(
        "Number of primitives and shell types does not match.");
  if (std::any_of(nprims.begin(), nprims.end(),
                  [](std::size_t i) { return i == 0; }))
    throw std::domain_error("Number of primitives has to be larger than zero.");
  if (alphas.size() != contr.size())
    throw std::domain_error(
        "Number of exponents and contraction coefficients does not match.");
  std::size_t nprim_tot = 0;
  for (auto& n : nprims) nprim_tot += n;
  if (alphas.size() != nprim_tot)
    throw std::domain_error(
        "Number of exponents and primitives does not match.");
  // Start assigning basis set
  libint2::Shell::do_enforce_unit_normalization(false);

  // read coordinates and initialize atoms
  std::string xyzfilename = std::string(molfile);
  std::ifstream input_file(xyzfilename);
  atoms = libint2::read_dotxyz(input_file);

  std::vector<std::vector<libint2::Shell>> element_bases(118);
  std::size_t n = 0;
  for (std::size_t a = 0ul; a < atoms.size(); ++a) {
    auto Z = atoms[a].atomic_number;
    auto x = atoms[a].x;
    auto y = atoms[a].y;
    auto z = atoms[a].z;

    std::vector<libint2::Shell> shells;
    for (std::size_t a_ = 0ul; a_ < center.size(); ++a_) {
      if (atoms.size() <= std::size_t(center[a_]))
        throw std::domain_error("More centers than atoms specified.");
      if (a != std::size_t(center[a_])) continue;

      libint2::svector<double> contr_;
      libint2::svector<double> alpha_;
      for (auto s = 0; s != nprims[a_]; ++s) {
        contr_.emplace_back(contr[n]);
        alpha_.emplace_back(alphas[n]);
        n++;
      }
      auto pure = (l[a_] > 1) ? true : false;
      shells.push_back({
          std::move(alpha_),  // exponents of primitive Gaussians
          {{abs(l[a_]), pure, std::move(contr_)}},
          {{x, y, z}}  // origin coordinates
      });
    }
    element_bases[Z] = shells;
  }
  obs = libint2::BasisSet(atoms, element_bases);
  // set to pure to invoke init function of libint basis set
  // check if all l>1 are either cartesian or pure. Currently, we cannot
  // handle mixed basis sets. It is possible with libint, but not supported
  // here.
  bool cartesian = false;
  bool solid = false;
  int l_max = 0;
  for (auto& l_ : l) {
    if (l_ < 0) cartesian = true;
    if (l_ > 1) solid = true;
    l_max = (l_max < abs(l_)) ? abs(l_) : l_max;
  }
  if (l_max <= 1) cartesian = true;
  if (solid && cartesian)
    throw std::domain_error(
        "Cannot handle mixed cartesian and solid harminics");
  if (cartesian)
    obs.set_pure(false);
  else if (solid)
    obs.set_pure(true);
  else
    throw std::domain_error(
        "Don't know whether to use cartesians or solid harmonics.");
  pure2cart(0);
  pure2cart(1);
  nbasis = obs.nbf();
  nshell = obs.size();
  ncenter = atoms.size();
  shell2atom = obs.shell2atom(atoms);
  for (std::size_t s = 0; s != obs.size(); ++s) {
    for (const auto& c : obs[s].contr) {
      auto factor = (!c.pure && c.l > 1) ? -1 : 1;
      shell_types.push_back(c.l * factor);
      for (auto n = 0ul; n < obs[s].alpha.size(); ++n) {
        // use normalization factor to get back to original coefficient
        double normalization_factor = get_renorm(c.l, s, n);
        contraction.push_back(c.coeff[n] / normalization_factor);
        alpha.push_back(obs[s].alpha[n]);
      }
    }
    nprim.push_back(obs[s].nprim());
  }
  for (auto a = 0ul; a < atoms.size(); ++a) {
    atomic_numbers.push_back(atoms[a].atomic_number);
    std::vector<double> xyz;
    xyz.push_back(atoms[a].x);
    xyz.push_back(atoms[a].y);
    xyz.push_back(atoms[a].z);
    coordinates.push_back(xyz);
  }
}

Basis::Basis(std::vector<libint2::Atom> atoms_, std::vector<long> nprims,
             std::vector<long> center, std::vector<int> l,
             std::vector<double> alphas, std::vector<double> contr)
    : basisname(""), molfile(""), dirname("") {
  // Do some standard test:
  if (nprims.size() != center.size())
    throw std::domain_error("Number of primitives and centers does not match.");
  if (nprims.size() != l.size())
    throw std::domain_error(
        "Number of primitives and shell types does not match.");
  if (std::any_of(nprims.begin(), nprims.end(),
                  [](std::size_t i) { return i == 0; }))
    throw std::domain_error("Number of primitives has to be larger than zero.");
  if (alphas.size() != contr.size())
    throw std::domain_error(
        "Number of exponents and contraction coefficients does not match.");
  std::size_t nprim_tot = 0;
  for (auto& n : nprims) nprim_tot += n;
  if (alphas.size() != nprim_tot)
    throw std::domain_error(
        "Number of exponents and primitives does not match.");
  // Start assigning basis set
  libint2::Shell::do_enforce_unit_normalization(false);

  atoms = atoms_;

  std::vector<std::vector<libint2::Shell>> element_bases(118);
  std::size_t n = 0;
  for (std::size_t a = 0ul; a < atoms.size(); ++a) {
    auto Z = atoms[a].atomic_number;
    auto x = atoms[a].x;
    auto y = atoms[a].y;
    auto z = atoms[a].z;

    std::vector<libint2::Shell> shells;
    for (std::size_t a_ = 0ul; a_ < center.size(); ++a_) {
      if (atoms.size() <= std::size_t(center[a_]))
        throw std::domain_error("More centers than atoms specified.");
      if (a != std::size_t(center[a_])) continue;

      libint2::svector<double> contr_;
      libint2::svector<double> alpha_;
      for (auto s = 0; s != nprims[a_]; ++s) {
        contr_.emplace_back(contr[n]);
        alpha_.emplace_back(alphas[n]);
        n++;
      }
      auto pure = (l[a_] > 1) ? true : false;
      shells.push_back({
          std::move(alpha_),  // exponents of primitive Gaussians
          {{abs(l[a_]), pure, std::move(contr_)}},
          {{x, y, z}}  // origin coordinates
      });
    }
    element_bases[Z] = shells;
  }
  obs = libint2::BasisSet(atoms, element_bases);
  // set to pure to invoke init function of libint basis set
  // check if all l>1 are either cartesian or pure. Currently, we cannot
  // handle mixed basis sets. It is possible with libint, but not supported
  // here.
  bool cartesian = false;
  bool solid = false;
  int l_max = 0;
  for (auto& l_ : l) {
    if (l_ < 0) cartesian = true;
    if (l_ > 1) solid = true;
    l_max = (l_max < abs(l_)) ? abs(l_) : l_max;
  }
  if (l_max <= 1) cartesian = true;
  if (solid && cartesian)
    throw std::domain_error(
        "Cannot handle mixed cartesian and solid harminics");
  if (cartesian)
    obs.set_pure(false);
  else if (solid)
    obs.set_pure(true);
  else
    throw std::domain_error(
        "Don't know whether to use cartesians or solid harmonics.");
  pure2cart(0);
  pure2cart(1);
  nbasis = obs.nbf();
  nshell = obs.size();
  ncenter = atoms.size();
  shell2atom = obs.shell2atom(atoms);
  for (std::size_t s = 0; s != obs.size(); ++s) {
    for (const auto& c : obs[s].contr) {
      auto factor = (!c.pure && c.l > 1) ? -1 : 1;
      shell_types.push_back(c.l * factor);
      for (auto n = 0ul; n < obs[s].alpha.size(); ++n) {
        // use normalization factor to get back to original coefficient
        double normalization_factor = get_renorm(c.l, s, n);
        contraction.push_back(c.coeff[n] / normalization_factor);
        alpha.push_back(obs[s].alpha[n]);
      }
    }
    nprim.push_back(obs[s].nprim());
  }
  for (auto a = 0ul; a < atoms.size(); ++a) {
    atomic_numbers.push_back(atoms[a].atomic_number);
    std::vector<double> xyz;
    xyz.push_back(atoms[a].x);
    xyz.push_back(atoms[a].y);
    xyz.push_back(atoms[a].z);
    coordinates.push_back(xyz);
  }
}

/*
    Defintion of getters:
*/
const std::string& Basis::getBasisname() const { return basisname; }

const std::string& Basis::getMolfile() const { return molfile; }

const std::string& Basis::getDirname() const { return dirname; }

std::size_t Basis::getNBasis() { return nbasis; }

std::size_t Basis::getNShell() { return nshell; }

std::size_t Basis::getNCenter() { return ncenter; }

std::vector<long> Basis::getNPrim() { return nprim; }

std::vector<double> Basis::getAlpha() { return alpha; }

std::vector<double> Basis::getContraction() { return contraction; }

std::vector<long> Basis::getShell2atom() { return shell2atom; }

std::vector<int> Basis::getShellTypes() { return shell_types; }

std::vector<long> Basis::getAtomicNumbers() { return atomic_numbers; }

std::vector<std::vector<double>> Basis::getCoordinates() { return coordinates; }

/*
    Defintion of general functions:
*/
void Basis::pure2cart(int l) {
  for (const auto& shell : obs)
    for (const auto& contraction : shell.contr) {
      bool* solid = const_cast<bool*>(&contraction.pure);
      if (contraction.l == l) *solid = false;
    }
}

void Basis::cart2pure(int l) {
  for (const auto& shell : obs)
    for (const auto& contraction : shell.contr) {
      bool* solid = const_cast<bool*>(&contraction.pure);
      if (contraction.l == l) *solid = true;
    }
}

void Basis::print_basis_info() {
  libint2::Shell::do_enforce_unit_normalization(false);
  std::cout << "  Reading basis set information from file: " << basisname
            << std::endl;
  std::cout << "  Number of contracted basis functions:    " << nbasis
            << std::endl;
  std::cout << "  Maximum orbital angular momentum:        " << obs.max_l()
            << std::endl;

  for (auto a = 0ul; a < atoms.size(); ++a) {
    auto Z = atoms[a].atomic_number;
    auto x = atoms[a].x;
    auto y = atoms[a].y;
    auto z = atoms[a].z;

    std::cout << " Index:  " << a << '\t' << " Charge: " << Z << '\t'
              << " Center: " << std::fixed << std::setprecision(9) << x << '\t'
              << y << '\t' << z << std::endl;
    for (std::size_t s = 0; s != obs.size(); ++s) {
      auto x_ = obs[s].O[0];
      auto y_ = obs[s].O[1];
      auto z_ = obs[s].O[2];
      if (x != x_ || y != y_ || z != z_) continue;
      std::cout << " " << obs[s].contr[0].l << std::endl;
      for (const auto& c : obs[s].contr) {
        for (auto n = 0ul; n < obs[s].alpha.size(); ++n) {
          // use normalization factor to get back to original coefficient
          double normalization_factor = get_renorm(c.l, s, n);
          std::cout << " " << std::setw(18) << std::right << obs[s].alpha[n]
                    << '\t' << std::setw(16) << std::right
                    << c.coeff[n] / normalization_factor << std::endl;
        }
      }
    }
  }
}

void Basis::dump_molden(const char* filename,
                        const py::EigenDRef<Eigen::MatrixXd> coeffs,
                        const py::EigenDRef<Eigen::MatrixXd> occs,
                        const py::EigenDRef<Eigen::MatrixXd> energies,
                        const std::vector<bool>& spin, double eps) {
  libint2::Shell::do_enforce_unit_normalization(false);
  libint2::molden::Export molden(atoms, obs, coeffs, occs, energies,
                                 std::vector<std::string>(), spin, eps);
  molden.write(std::string(filename));
}

/**
 * Evaluate orbital (MO) on grid and dump to file in .cube format.
 *
 * For given grid points `grid_x`, `grid_y`, and `grid_z`, the
 * the orbital function is evaluated and the final result appended
 * to the file `filename`. This routine does not print any headers.
 * The orbital function is evaluated in its cartesian representation,
 * while the MO coefficients `coeffs` are assumed to be given for
 * solid harmonics (PyBEST only supports pure functions).
 * The order of functions in the basis set instance and MO coefficients
 * has to be the same (by construction), otherwise the routine will
 * break.
 *
 * @param filename Filename where data will be appended.
 * @param coeffs AO/MO expansion coefficients for ONE MO.
 * @param grid_x Grid points along x axis.
 * @param grid_y Grid points along y axis.
 * @param grid_z Grid points along z axis.
 */
void Basis::dump_cube_orbital(const char* filename,
                              const py::EigenDRef<Eigen::VectorXd> coeffs,
                              const py::EigenDRef<Eigen::VectorXd> grid_x,
                              const py::EigenDRef<Eigen::VectorXd> grid_y,
                              const py::EigenDRef<Eigen::VectorXd> grid_z) {
  libint2::Shell::do_enforce_unit_normalization(false);

  std::string filename_ = filename;
  std::ofstream os(filename_, std::ios_base::app);
  os.precision(6);
  // loop over all grid points
  for (int i_x = 0; i_x < grid_x.rows(); ++i_x) {
    auto x = grid_x(i_x);
    for (int i_y = 0; i_y < grid_y.rows(); ++i_y) {
      auto y = grid_y(i_y);
      // introduce counter to decide on linebreak (for each 6 grid points)
      for (int i_z = 0; i_z < grid_z.rows(); ++i_z) {
        auto z = grid_z(i_z);
        // compute value of selected orbital (MO) at point (x,y,z)
        double cube_val = 0.0;
        // loop over basis set, that is, the AOs
        // we need to 2 variables in the loop:
        // 1) for the basis instance (used by libint2) ``s``
        // 2) for the AO/MO coefficients ``mu``
        // This is C++17 standard and does not work with libint if we use
        // intel oneAPI to build Basis. Thus, we go back to C++11 standard
        // for (auto [s, mu] = std::tuple{0, 0};
        //     s != obs.size() && mu != coeffs.size(); ++s, ++mu) {
        for (std::size_t s = 0, mu = 0; s != obs.size() && mu != coeffs.size();
             ++s, ++mu) {
          // Get center of AO
          auto x_ao = obs[s].O[0];
          auto y_ao = obs[s].O[1];
          auto z_ao = obs[s].O[2];
          // Contribution of each AO at grid point (x,y,z)
          double cube_val_ao = 0.0;
          // loop over CGO (each AO can be a linear combination of primitives)
          for (const auto& c : obs[s].contr) {
            auto l_max = ((c.l + 1) * (c.l + 2)) / 2;
            auto l_max_pure = 2 * c.l + 1;
            for (auto n = 0ul; n < obs[s].alpha.size(); ++n) {
              auto shell_exp_l = shell_exp[c.l];
              // store results for cartesian and pure functions
              std::vector<double> cart(l_max, 0.0);
              std::vector<double> pure(2 * c.l + 1, 0.0);
              // loop over all cartesian functions of a specific shell with c.l
              for (auto l = 0; l < l_max; ++l) {
                auto l_xyz = shell_exp_l[l];
                // r^l exp(-alpha r^2) * N
                auto r2 =
                    pow(x - x_ao, 2) + pow(y - y_ao, 2) + pow(z - z_ao, 2);
                // assign value at point (x,y,z) of primitive to temporary
                // cartesian vector
                cart[l] = pow(x - x_ao, l_xyz[0]) * pow(y - y_ao, l_xyz[1]) *
                          pow(z - z_ao, l_xyz[2]) * exp(-obs[s].alpha[n] * r2);
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
                  cube_val_ao += cart[l] * c.coeff[n] * coeffs[mu + l];
                }
              } else {
                // transform back to pure solid harmonics using libint's
                // tform_cols function (transforms only a column vector for
                // shell c.l)
                libint2::solidharmonics::tform_cols(1, c.l, &cart[0], &pure[0]);
                // loop over all MOs in pure form/solid harmonics
                // the order of m_l functions is the same in pure and coeffs
                for (std::size_t l = 0; l < pure.size(); ++l) {
                  cube_val_ao += pure[l] * c.coeff[n] * coeffs[mu + l];
                }
              }
              pure.clear();
              cart.clear();
            }
            // adjust counter over MOs: move counter to last index of current
            // shell c.l
            mu += l_max_pure - 1;
          }
          // Assign each CGO/AO contribution to grid point
          cube_val += cube_val_ao;
        }
        if (i_z % 6 == 0 && i_z > 0) os << std::endl;
        // print value of cube
        os << "  " << std::scientific << std::setw(13) << cube_val;
      }  // for z
      os << std::endl;
    }  // for y
  }    // for x
}

void Basis::print_atomic_info() {
  std::cout << "Index \t Charge    \t   x [au]   \t   y [au]   \t   z [au]"
            << std::endl;
  for (auto a = 0ul; a < atoms.size(); ++a) {
    auto Z = atoms[a].atomic_number;
    auto x = atoms[a].x;
    auto y = atoms[a].y;
    auto z = atoms[a].z;

    std::cout << a << "  \t  " << Z << "\t \t" << std::right << std::fixed
              << std::setw(12) << std::setprecision(8) << x << '\t'
              << std::right << std::fixed << std::setw(12) << y << '\t'
              << std::right << std::fixed << std::setw(12) << z << std::endl;
  }
}

std::size_t Basis::get_shell_size(int shell_type) {
  return (shell_type >= 0)
             ? (2 * shell_type + 1)
             : ((abs(shell_type) + 1) * (abs(shell_type) + 2) / 2);
}

std::size_t Basis::get_nbasis_in_shell(std::size_t s) { return obs[s].size(); }

void Basis::set_dummy_atom(int i) {
  atoms[i].atomic_number = 0.0;
  atomic_numbers[i] = 0.0;
}

double Basis::get_renorm(std::size_t l, std::size_t s, std::size_t n) {
  // The following lines are taken from libint's renorm function
  // Note, this only works if
  // libint2::Shell::do_enforce_unit_normalization(false); is set.
  using libint2::math::df_Kminus1;
  using std::pow;
  const auto sqrt_Pi_cubed = double{5.56832799683170784528481798212};
  const auto two_alpha = 2 * obs[s].alpha[n];
  const auto two_alpha_to_am32 = pow(two_alpha, l + 1) * sqrt(two_alpha);
  const auto normalization_factor =
      sqrt(pow(2, l) * two_alpha_to_am32 / (sqrt_Pi_cubed * df_Kminus1[2 * l]));
  return normalization_factor;
}

double Basis::get_renorm(std::size_t l, std::size_t s, std::size_t na,
                         std::vector<std::size_t> n) {
  // The following lines are taken from libint's renorm function
  // Note, this only works if
  // libint2::Shell::do_enforce_unit_normalization(false); is set.
  using libint2::math::df_Kminus1;
  using std::pow;
  const auto sqrt_Pi_cubed = double{5.56832799683170784528481798212};
  const auto two_alpha = 2 * obs[s].alpha[na];
  const auto two_alpha_to_am32 = two_alpha * sqrt(two_alpha);
  const auto normalization_factor =
      sqrt(pow(2 * two_alpha, n[0] + n[1] + n[2]) * two_alpha_to_am32 /
           (sqrt_Pi_cubed * df_Kminus1[2 * n[0]] * df_Kminus1[2 * n[1]] *
            df_Kminus1[2 * n[2]]));
  return normalization_factor;
}

void Basis::renormalize_contr(int l, std::vector<std::size_t> n,
                              double factor) {
  libint2::Shell::do_enforce_unit_normalization(false);
  // loop over all basis functions
  for (std::size_t s = 0; s != obs.size(); ++s) {
    for (auto& c : obs[s].contr) {
      if (c.l != l) continue;
      for (auto na = 0ul; na < obs[s].alpha.size(); ++na) {
        // use normalization factor to get back to original coefficient
        double normalization_factor = get_renorm(c.l, s, na, n) * factor;
        libint2::svector<libint2::Shell::real_t>& coefficient_new =
            const_cast<libint2::svector<libint2::Shell::real_t>&>(c.coeff);
        coefficient_new[na] = c.coeff[na] / normalization_factor;
      }
    }
  }
}

Basis from_coordinates(std::vector<long> atomic_numbers,
                       std::vector<std::vector<double>> coordinates,
                       std::vector<long> primitives,
                       std::vector<long> shell2atom,
                       std::vector<int> shell_types, std::vector<double> alphas,
                       std::vector<double> contraction

) {
  libint2::Shell::do_enforce_unit_normalization(false);
  std::vector<libint2::Atom> atoms;
  // assign to libint2::Atoms
  for (auto a = 0ul; a < atomic_numbers.size(); ++a) {
    libint2::Atom atom;
    atom.atomic_number = atomic_numbers[a];
    atom.x = coordinates[a][0];
    atom.y = coordinates[a][1];
    atom.z = coordinates[a][2];

    atoms.push_back(atom);
  }

  return Basis(atoms, primitives, shell2atom, shell_types, alphas, contraction);
}
