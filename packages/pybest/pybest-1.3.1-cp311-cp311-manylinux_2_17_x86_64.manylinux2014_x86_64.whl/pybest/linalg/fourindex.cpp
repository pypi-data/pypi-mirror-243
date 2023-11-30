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

#include <math.h>

#include <cstring>
#include <vector>

#ifdef _OPENMP
#include <omp.h>
#else
#define omp_get_thread_num() 0
#define omp_get_num_threads() 1
#define omp_get_max_threads() 1
#endif

#include "fourindex.h"

void apply_four_index_transform_cpp_chol(
    py::array_t<double, py::array::c_style | py::array::forcecast> inp1,
    py::array_t<double, py::array::c_style | py::array::forcecast> inp2,
    py::array_t<double, py::array::c_style | py::array::forcecast> &out) {
  // Check if number of dimensions of np.ndarray is correct, if not, raise
  // ValueError
  out.mutable_unchecked<3>();
  // Create buffer pointer to input and output
  py::buffer_info bufinp1 = inp1.request();
  py::buffer_info bufinp2 = inp2.request();
  py::buffer_info bufout = out.request();
  double *ptrinp1 = (double *)bufinp1.ptr;
  double *ptrinp2 = (double *)bufinp2.ptr;
  double *ptrout = (double *)bufout.ptr;
  // Get dimensions and check for consistencies
  long nvec = inp1.shape(0);
  long nbasis = inp1.shape(1);

  if (inp1.shape(1) != nbasis || inp1.shape(2) != nbasis)
    throw std::runtime_error(
        "Number of dimensions of input1 arguments does not match");
  if (inp2.shape(0) != nbasis || inp2.shape(1) != nbasis)
    throw std::runtime_error(
        "Number of dimensions of input2 arguments does not match");
  if (out.shape(0) != nvec || out.shape(1) != nbasis || out.shape(2) != nbasis)
    throw std::runtime_error(
        "Number of dimensions of output arguments does not match");
    //  int ompth = omp_get_num_threads(); //Number of OMP threads for the for
    //  loop int mklth = 1; //Number of MKL threads for the mkl calls
    // This nested parallelism might not be the fastest; need to check
    //  #if defined(BLAS_MKL)
    //      if (1 < mkl_domain_get_max_threads(MKL_DOMAIN_BLAS)){
    //          #if defined(_OPENMP)
    //              ompth = omp_get_num_threads()/2; //Number of OMP threads for
    //              the for loop mklth = 2; //Number of MKL threads for the mkl
    //              calls mkl_set_dynamic(false); omp_set_nested(true);
    //              omp_set_max_active_levels(2);
    //          #endif
    //      }
    //  #endif
#if defined(_OPENMP)
#pragma omp parallel
    // #pragma omp parallel num_threads(ompth)
#endif
  {
#if defined(_OPENMP)
#pragma omp for
#endif
    for (long x = 0; x < nvec; ++x) {
      //      #if defined(BLAS_MKL)
      //          if (1 < mkl_domain_get_max_threads(MKL_DOMAIN_BLAS)){
      //              #if defined(_OPENMP)
      //                  mkl_set_num_threads_local(mklth);
      //              #endif
      //          }
      //      #endif
      for (long p = 0; p < nbasis; ++p) {
        std::vector<double> *vxpn = new std::vector<double>;
        // to prevent resizing
        vxpn->reserve(nbasis);
        for (long n = 0; n < nbasis; ++n) {
          double res =
              cblas_ddot(nbasis, &(ptrinp1)[n * nbasis + x * nbasis * nbasis],
                         1, &(ptrinp2)[p], nbasis);
          vxpn->push_back(res);
        }
        for (long q = 0; q < nbasis; ++q) {
          double res =
              cblas_ddot(nbasis, &(*vxpn)[0], 1, &(ptrinp2)[q], nbasis);
          ptrout[(x * nbasis + p) * nbasis + q] = res;
        }
        delete vxpn;
      }
    }
  }
  //  #if defined(BLAS_MKL)
  //      if (1 < mkl_domain_get_max_threads(MKL_DOMAIN_BLAS)){
  //          #if defined(_OPENMP)
  //              mkl_set_dynamic(true);
  //          #endif
  //      }
  //  #endif
}

void apply_four_index_transform_cpp(
    py::array_t<double, py::array::c_style | py::array::forcecast> inp1,
    py::array_t<double, py::array::c_style | py::array::forcecast> inp2,
    py::array_t<double, py::array::c_style | py::array::forcecast> &out) {
  /**Do four-index transformation.

         Perform four-index transformation using 2 consecutive quarter
     transformation

         four-index transformation of the 2-elctron integrals using two
     consecutive quarter transformation. This routine employs the standard 1)
     supermatrix symmetry and 2) overlap symmetry according to the
     implementation of Saunders and van Lenthe in Mol. Phys., 48, 923 (1983)
     which has the best scaling if N_MO < N_AO. The implementation is done for
     N_MO = N_AO, but can be easily extended for the general case where N_MO <=
     N_AO. For N_MO = N_AO, the scaling is 25*N^5/24.

         These are the following steps using Dirac's notation for the
         2-electron integrals:
         0) Two-electron integrals in AO-basis need to be scaled by a factor of
            (1/2)^(delta_pq+delta_rs+delta_pq,rs)
         1) contract (pr,qs) -> [pr,qi] for cases where p>=q and r>=s for all
     rs>=pq 2) contract [pr,qi] -> [pj,qi] for all i,j 3) account for symmetry:
     (pi,qj) = [pj,qi]+[pi,qj] 4) contract (pi,qj) -> [pi,kj] as in 1) 5)
     contract [pi,kj] -> [li,kj] as in 2) 6) account for symmetry: [ki,lj] =
     [li,kj]+[ki,lj] 7) account for supermatrix symmetry: (ki,lj) =
     [ki,lj]+[ik,jl]
      **/

  // Check if number of dimensions of np.ndarray is correct, if not, raise
  // ValueError
  out.mutable_unchecked<4>();
  // Create buffer pointer to input and output
  py::buffer_info bufinp1 = inp1.request();
  py::buffer_info bufinp2 = inp2.request();
  py::buffer_info bufout = out.request();
  double *ptrinp1 = (double *)bufinp1.ptr;
  double *ptrinp2 = (double *)bufinp2.ptr;
  double *ptrout = (double *)bufout.ptr;
  // Get dimensions and check for consistencies
  long nbasis = inp1.shape(1);

  if (inp1.shape(0) != nbasis || inp1.shape(1) != nbasis ||
      inp1.shape(2) != nbasis || inp1.shape(3) != nbasis)
    throw std::runtime_error(
        "Number of dimensions of input1 arguments does not match");
  if (inp2.shape(0) != nbasis || inp2.shape(1) != nbasis)
    throw std::runtime_error(
        "Number of dimensions of input2 arguments does not match");
  if (out.shape(0) != nbasis || out.shape(1) != nbasis ||
      out.shape(2) != nbasis || out.shape(3) != nbasis)
    throw std::runtime_error(
        "Number of dimensions of output arguments does not match");

  // allocate memory
  double *i_pqri;
  i_pqri = new double[nbasis * nbasis * nbasis * nbasis];
  std::memset(i_pqri, 0, sizeof(double) * nbasis * nbasis * nbasis * nbasis);
  double *aos;
  aos = new double[nbasis * nbasis * nbasis * nbasis];

  // scale integrals:
  for (long p = 0; p < nbasis; p++) {
    for (long q = 0; q < nbasis; q++) {
      for (long r = 0; r < nbasis; r++) {
        for (long s = 0; s < nbasis; s++) {
          long factor = 0;
          if (p == q) {
            factor += 1;
          }
          if (r == s) {
            factor += 1;
          }
          if (p == r) {
            if (q == s) {
              factor += 1;
            }
          } else if (p == s) {
            if (q == r) {
              factor += 1;
            }
          }
          aos[p * nbasis * nbasis * nbasis + q * nbasis * nbasis + r * nbasis +
              s] = ptrinp1[p * nbasis * nbasis * nbasis + r * nbasis * nbasis +
                           q * nbasis + s] /
                   (pow(2, factor));
        }
      }
    }
  }
  // first quarter transformation: pr,qs -> pj,qi
  for (long p = 0; p < nbasis; p++) {
    for (long q = 0; q < (p + 1); q++) {
      for (long r = p; r < nbasis; r++) {
        // Note that there is a type in the original work for the upper bound of
        // the summation over s
        long end = r;
        if (r == p) {
          end = q;
        }
        for (long s = 0; s < (end + 1); s++) {
          for (long i = 0; i < nbasis; i++) {
            i_pqri[p * nbasis * nbasis * nbasis + q * nbasis * nbasis +
                   r * nbasis + i] +=
                aos[p * nbasis * nbasis * nbasis + q * nbasis * nbasis +
                    r * nbasis + s] *
                ptrinp2[s * nbasis + i];
          }
        }
      }
    }
  }

  delete[] aos;
  aos = NULL;

  for (long p = 0; p < nbasis; p++) {
    for (long q = 0; q < (p + 1); q++) {
      for (long r = p; r < nbasis; r++) {
        for (long j = 0; j < nbasis; j++) {
          for (long i = 0; i < nbasis; i++) {
            ptrout[p * nbasis * nbasis * nbasis + q * nbasis * nbasis +
                   j * nbasis + i] +=
                ptrinp2[r * nbasis + j] *
                i_pqri[p * nbasis * nbasis * nbasis + q * nbasis * nbasis +
                       r * nbasis + i];
          }
        }
      }
    }
  }
  delete[] i_pqri;
  i_pqri = NULL;
  double *t_pqji;
  t_pqji = new double[nbasis * nbasis * nbasis * nbasis];
  std::memset(t_pqji, 0, sizeof(double) * nbasis * nbasis * nbasis * nbasis);

  for (long p = 0; p < nbasis; p++) {
    for (long q = 0; q < (p + 1); q++) {
      for (long i = 0; i < nbasis; i++) {
        for (long j = 0; j < (i + 1); j++) {
          t_pqji[p * nbasis * nbasis * nbasis + q * nbasis * nbasis +
                 i * nbasis + j] =
              (ptrout[p * nbasis * nbasis * nbasis + q * nbasis * nbasis +
                      i * nbasis + j] +
               ptrout[p * nbasis * nbasis * nbasis + q * nbasis * nbasis +
                      j * nbasis + i]);
        }
      }
    }
  }

  double *i_pqri2;
  i_pqri2 = new double[nbasis * nbasis * nbasis * nbasis];
  std::memset(i_pqri2, 0, sizeof(double) * nbasis * nbasis * nbasis * nbasis);
  std::memset(ptrout, 0, sizeof(double) * nbasis * nbasis * nbasis * nbasis);
  // second quarter transformation: pj,qi -> lj,ki
  for (long p = 0; p < nbasis; p++) {
    for (long q = 0; q < (p + 1); q++) {
      for (long k = 0; k < nbasis; k++) {
        for (long i = 0; i < nbasis; i++) {
          for (long j = 0; j < (i + 1); j++) {
            i_pqri2[p * nbasis * nbasis * nbasis + k * nbasis * nbasis +
                    i * nbasis + j] +=
                ptrinp2[q * nbasis + k] *
                t_pqji[p * nbasis * nbasis * nbasis + q * nbasis * nbasis +
                       i * nbasis + j];
          }
        }
      }
    }
  }

  delete[] t_pqji;
  t_pqji = NULL;

  for (long p = 0; p < nbasis; p++) {
    for (long l = 0; l < nbasis; l++) {
      for (long k = 0; k < nbasis; k++) {
        for (long i = 0; i < nbasis; i++) {
          for (long j = 0; j < (i + 1); j++) {
            ptrout[l * nbasis * nbasis * nbasis + k * nbasis * nbasis +
                   i * nbasis + j] +=
                ptrinp2[p * nbasis + l] *
                i_pqri2[p * nbasis * nbasis * nbasis + k * nbasis * nbasis +
                        i * nbasis + j];
          }
        }
      }
    }
  }
  delete[] i_pqri2;
  i_pqri2 = NULL;
  double *t_pqji2;
  t_pqji2 = new double[nbasis * nbasis * nbasis * nbasis];
  std::memset(t_pqji2, 0, sizeof(double) * nbasis * nbasis * nbasis * nbasis);

  // account again for overlap symmetry:
  for (long k = 0; k < nbasis; k++) {
    for (long l = 0; l < (k + 1); l++) {
      for (long i = 0; i < nbasis; i++) {
        for (long j = 0; j < (i + 1); j++) {
          t_pqji2[k * nbasis * nbasis * nbasis + l * nbasis * nbasis +
                  i * nbasis + j] =
              ptrout[l * nbasis * nbasis * nbasis + k * nbasis * nbasis +
                     i * nbasis + j] +
              ptrout[k * nbasis * nbasis * nbasis + l * nbasis * nbasis +
                     i * nbasis + j];
        }
      }
    }
  }
  long ji = 0;
  // form final transformed integrals: account for supermatrix symmetry
  for (long i = 0; i < nbasis; i++) {
    for (long j = 0; j < (i + 1); j++) {
      ji += 1;
      long lk = 0;
      for (long k = 0; k < nbasis; k++) {
        for (long l = 0; l < (k + 1); l++) {
          lk += 1;
          if (lk <= ji) {
            ptrout[l * nbasis * nbasis * nbasis + j * nbasis * nbasis +
                   k * nbasis + i] =
                t_pqji2[k * nbasis * nbasis * nbasis + l * nbasis * nbasis +
                        i * nbasis + j] +
                t_pqji2[i * nbasis * nbasis * nbasis + j * nbasis * nbasis +
                        k * nbasis + l];
            ptrout[l * nbasis * nbasis * nbasis + i * nbasis * nbasis +
                   k * nbasis + j] =
                ptrout[l * nbasis * nbasis * nbasis + j * nbasis * nbasis +
                       k * nbasis + i];
            ptrout[k * nbasis * nbasis * nbasis + j * nbasis * nbasis +
                   l * nbasis + i] =
                ptrout[l * nbasis * nbasis * nbasis + j * nbasis * nbasis +
                       k * nbasis + i];
            ptrout[k * nbasis * nbasis * nbasis + i * nbasis * nbasis +
                   l * nbasis + j] =
                ptrout[l * nbasis * nbasis * nbasis + j * nbasis * nbasis +
                       k * nbasis + i];
            ptrout[i * nbasis * nbasis * nbasis + k * nbasis * nbasis +
                   j * nbasis + l] =
                ptrout[l * nbasis * nbasis * nbasis + j * nbasis * nbasis +
                       k * nbasis + i];
            ptrout[i * nbasis * nbasis * nbasis + l * nbasis * nbasis +
                   j * nbasis + k] =
                ptrout[l * nbasis * nbasis * nbasis + j * nbasis * nbasis +
                       k * nbasis + i];
            ptrout[j * nbasis * nbasis * nbasis + k * nbasis * nbasis +
                   i * nbasis + l] =
                ptrout[l * nbasis * nbasis * nbasis + j * nbasis * nbasis +
                       k * nbasis + i];
            ptrout[j * nbasis * nbasis * nbasis + l * nbasis * nbasis +
                   i * nbasis + k] =
                ptrout[l * nbasis * nbasis * nbasis + j * nbasis * nbasis +
                       k * nbasis + i];
          }
        }
      }
    }
  }
  delete[] t_pqji2;
  t_pqji2 = NULL;
}
