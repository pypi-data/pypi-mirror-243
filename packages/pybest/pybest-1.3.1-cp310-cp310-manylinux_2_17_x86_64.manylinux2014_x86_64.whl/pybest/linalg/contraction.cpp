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
#ifdef _OPENMP
#include <omp.h>
#else
#define omp_get_thread_num() 0
#define omp_get_num_threads() 1
#define omp_get_max_threads() 1
#endif
#include <cmath>
#include <cstddef>
#include <cstring>
#include <iostream>
#include <stdexcept>
#include <vector>

#include "contraction.h"

void contract_two_to_two_abcd_cb_ad_blas(
    py::array_t<double, py::array::c_style | py::array::forcecast> inp1,
    py::array_t<double, py::array::c_style | py::array::forcecast> inp2,
    py::array_t<double, py::array::c_style | py::array::forcecast> two,
    py::array_t<double, py::array::c_style | py::array::forcecast> &out,
    double factor, bool clear, long b0, long e0, long b1, long e1, long b2,
    long e2, long b3, long e3, long b4, long e4, long b5, long e5, bool t) {
  // Check if number of dimensions of np.ndarray is correct, if not, raise
  // ValueError
  out.mutable_unchecked<2>();
  // Create buffer pointer to input and output
  py::buffer_info bufinp1 = inp1.request();
  py::buffer_info bufinp2 = inp2.request();
  py::buffer_info buftwo = two.request();
  py::buffer_info bufout = out.request();
  double *ptrinp1 = (double *)bufinp1.ptr;
  double *ptrinp2 = (double *)bufinp2.ptr;
  double *ptrtwo = (double *)buftwo.ptr;
  double *ptrout = (double *)bufout.ptr;
  // dimensions
  long nvec = inp1.shape(0);
  long nbasis = inp1.shape(1);
  long nbasis2 = two.shape(1);
  int ntota = e0 - b0;
  int ntotb = e1 - b1;
  int ntotc = e2 - b2;
  int ntotd = e3 - b3;
  // Get dimensions and check for consistencies
  if ((e4 - b4) != ntotc || (e5 - b5) != ntotb)
    throw std::runtime_error(
        "Number of dimensions of input and output arguments does not match");
  if (t) {
    if (ntotd != inp2.shape(0) || inp1.shape(0) != inp2.shape(1) ||
        ntotb != inp2.shape(2))
      throw std::runtime_error(
          "Number of dimensions of transposed input arguments does not match");
  } else {
    if (inp1.shape(0) != inp2.shape(0) || inp1.shape(1) != inp2.shape(1) ||
        inp1.shape(2) != inp2.shape(2))
      throw std::runtime_error(
          "Number of dimensions of input arguments does not match");
  }
  if (out.shape(0) != ntota || out.shape(1) != ntotd)
    throw std::runtime_error(
        "Number of dimensions of output arguments does not match");
  if (clear) {
    memset(ptrout, 0, sizeof(double) * ntota * ntotd);
  }
#if defined(BLAS_MKL)
  if (1 < mkl_domain_get_max_threads(MKL_DOMAIN_BLAS)) {
#if defined(_OPENMP)
    omp_set_num_threads(1);
    mkl_set_dynamic(0);
    omp_set_max_active_levels(2);
#endif
  }
#endif
#if defined(_OPENMP)
#pragma omp parallel
#endif
  {
#if defined(_OPENMP)
#pragma omp for
#endif
    for (int a = b0; a < e0; ++a) {
      int len = nvec * ntotb;
      std::vector<double> *vaxb = new std::vector<double>;
      // to prevent resizing
      vaxb->reserve(len);
      for (int x = 0; x < nvec; ++x) {
        for (int b = b5; b < e5; ++b) {
          // Use blas to do the vector-vector multiplication
          // xac,cb -> va[xb]
          double res = cblas_ddot(
              ntotc, &(ptrinp1)[x * nbasis * nbasis + a * nbasis + b2], 1,
              &(ptrtwo)[b4 * nbasis2 + b], nbasis2);
          vaxb->push_back(res);
        }
      }
      for (int d = b3; d < e3; ++d) {
        // vaxb,xbd -> ad
        double res = 0.0;
        if (t) {
          res += cblas_ddot(nvec * ntotb, &(*vaxb)[0], 1,
                            &(ptrinp2)[(d - b3) * nvec * ntotb], 1);
        } else {
          res += cblas_ddot(nvec * ntotb, &(*vaxb)[0], 1,
                            &(ptrinp2)[b1 * nbasis + d], nbasis);
        }
        int indexout = ((a - b0) * ntotd + (d - b3));
        ptrout[indexout] += res * factor;
      }
      delete vaxb;
    }
  }
#if defined(BLAS_MKL)
  if (1 < mkl_domain_get_max_threads(MKL_DOMAIN_BLAS)) {
#if defined(_OPENMP)
    mkl_set_dynamic(true);
#endif
  }
#endif
}

void contract_four_to_four_abcd_efbd_aecf_blas(
    py::array_t<double, py::array::c_style | py::array::forcecast> inp1,
    py::array_t<double, py::array::c_style | py::array::forcecast> inp2,
    py::array_t<double, py::array::c_style | py::array::forcecast> four,
    py::array_t<double, py::array::c_style | py::array::forcecast> &out,
    double factor, bool clear, long b0, long e0, long b1, long e1, long b2,
    long e2, long b3, long e3) {
  // Check if number of dimensions of np.ndarray is correct, if not, raise
  // ValueError
  out.mutable_unchecked<4>();
  // Create buffer pointer to input and output
  py::buffer_info bufinp1 = inp1.request();
  py::buffer_info bufinp2 = inp2.request();
  py::buffer_info buffour = four.request();
  py::buffer_info bufout = out.request();
  double *ptrinp1 = (double *)bufinp1.ptr;
  double *ptrinp2 = (double *)bufinp2.ptr;
  double *ptrfour = (double *)buffour.ptr;
  double *ptrout = (double *)bufout.ptr;

  // dimensions
  long nvec = inp1.shape(0);
  long ntot = inp1.shape(1);
  long nbasis0 = four.shape(0);
  long nbasis1 = four.shape(2);
  // Check for consistencies
  if (inp1.shape(0) != inp2.shape(0) || inp1.shape(1) != inp2.shape(1) ||
      inp1.shape(2) != inp2.shape(2) || inp2.shape(1) != inp2.shape(2))
    throw std::runtime_error(
        "Number of dimensions of input arguments does not match");
  if (out.shape(0) != nbasis0 || out.shape(2) != nbasis0 ||
      out.shape(1) != (e0 - b0) || out.shape(3) != (e1 - b1))
    throw std::runtime_error(
        "Number of dimensions of output arguments does not match");
  if (four.shape(2) != (e2 - b2) || four.shape(3) != (e3 - b3))
    throw std::runtime_error(
        "Number of dimensions of four-index arguments does not match");
  if (nbasis1 != (e0 - b0) || nbasis1 != (e1 - b1))
    throw std::runtime_error("Number of dimensions of slice does not match");
  if (clear) {
    memset(ptrout, 0, sizeof(double) * nbasis1 * nbasis1 * nbasis0 * nbasis0);
  }
#if defined(BLAS_MKL)
  if (1 < mkl_domain_get_max_threads(MKL_DOMAIN_BLAS)) {
#if defined(_OPENMP)
    omp_set_num_threads(1);
    mkl_set_dynamic(0);
#endif
  }
#endif
#if defined(_OPENMP)
#pragma omp parallel
#endif
  {
#if defined(_OPENMP)
#pragma omp for
#endif
    for (int a = b0; a < e0; a++) {    // e
      for (int b = b1; b < e1; b++) {  // f
        std::vector<double> *vabcd = new std::vector<double>;
        // to prevent resizing
        vabcd->reserve(nbasis1 * nbasis1);
        for (int c = b2; c < e2; c++) {    // b
          for (int d = b3; d < e3; d++) {  // d
            // Use blas to do the vector-vector multiplication
            // xac,xbd -> vabcd  (xeb, xfd -> ebfd)
            double res = cblas_ddot(nvec, &(ptrinp1)[c + a * ntot], ntot * ntot,
                                    &(ptrinp2)[d + b * ntot], ntot * ntot);
            vabcd->push_back(res);
          }
        }
        for (int i = 0; i < nbasis0; i++) {
          for (int j = 0; j < nbasis0; j++) {
            int aa = a - b0;
            int bb = b - b1;
            // xabij
            double res = cblas_ddot(nbasis1 * nbasis1, &(*vabcd)[0], 1,
                                    &(ptrfour)[i * nbasis0 * nbasis1 * nbasis1 +
                                               j * nbasis1 * nbasis1],
                                    1);
            int indexout = (((i * nbasis1 + aa) * nbasis0 + j) * nbasis1 + bb);
            ptrout[indexout] += res * factor;
          }
        }
        delete vabcd;
      }
    }
  }
}

void contract_four_to_four_abcd_efbd_aecf(
    py::array_t<double, py::array::c_style | py::array::forcecast> inp1,
    py::array_t<double, py::array::c_style | py::array::forcecast> inp2,
    py::array_t<double, py::array::c_style | py::array::forcecast> four,
    py::array_t<double, py::array::c_style | py::array::forcecast> &out,
    double factor, bool clear, long b0, long e0, long b1, long e1, long b2,
    long e2, long b3, long e3) {
  // Check if number of dimensions of np.ndarray is correct, if not, raise
  // ValueError
  out.mutable_unchecked<4>();
  // Create buffer pointer to input and output
  py::buffer_info bufinp1 = inp1.request();
  py::buffer_info bufinp2 = inp2.request();
  py::buffer_info buffour = four.request();
  py::buffer_info bufout = out.request();
  double *ptrinp1 = (double *)bufinp1.ptr;
  double *ptrinp2 = (double *)bufinp2.ptr;
  double *ptrfour = (double *)buffour.ptr;
  double *ptrout = (double *)bufout.ptr;
  // dimensions
  long nvec = inp1.shape(0);
  long ntot = inp1.shape(1);
  long nbasis0 = four.shape(0);
  long nbasis1 = four.shape(1);
  // Check for consistencies
  if (inp1.shape(0) != inp2.shape(0) || inp1.shape(1) != inp2.shape(1) ||
      inp1.shape(2) != inp2.shape(2))
    throw std::runtime_error(
        "Number of dimensions of input arguments does not match");
  if (out.shape(0) != nbasis0 || out.shape(2) != nbasis0 ||
      out.shape(1) != nbasis1 || out.shape(3) != nbasis1)
    throw std::runtime_error(
        "Number of dimensions of output arguments does not match");
  if (four.shape(2) != nbasis0 || four.shape(3) != nbasis1)
    throw std::runtime_error(
        "Number of dimensions of four-index arguments does not match");
  if (nbasis1 != (e0 - b0) || nbasis1 != (e1 - b1) || nbasis0 != (e2 - b2) ||
      nbasis1 != (e3 - b3))
    throw std::runtime_error("Number of dimensions of slice does not match");
  if (clear) {
    memset(ptrout, 0, sizeof(double) * nbasis1 * nbasis1 * nbasis0 * nbasis0);
  }
  long a, b, c, d, aa, bb, cc, dd, ind1, ind2, indexout, ind4, x, i, j;
  double xiajd;
  long dim = nbasis0 * nbasis1 * nbasis0 * nbasis1;
  std::vector<double *> local(omp_get_max_threads());
#if defined(_OPENMP)
#pragma omp parallel private(a, b, c, d, aa, bb, cc, dd, ind1, ind2, ind4, \
                             indexout, x, i, j, xiajd)
#endif
  {
    int np = omp_get_num_threads();
    std::vector<double> localout(dim);
    local[omp_get_thread_num()] = localout.data();
#if defined(_OPENMP)
#pragma omp for
#endif
    for (x = 0; x < nvec; x++) {
      for (i = 0; i < nbasis0; i++) {
        for (a = b0; a < e0; a++) {
          aa = a - b0;
          for (j = 0; j < nbasis0; j++) {
            for (d = b3; d < e3; d++) {
              dd = d - b3;
              xiajd = 0.0;
              for (c = b2; c < e2; c++) {
                cc = c - b2;
                ind1 = (x * ntot + a) * ntot + c;
                ind4 = ((i * nbasis1 + cc) * nbasis0 + j) * nbasis1 + dd;
                xiajd += ptrinp1[ind1] * ptrfour[ind4];
              }
              for (b = b1; b < e1; b++) {
                bb = b - b1;
                ind2 = (x * ntot + b) * ntot + d;
                indexout = (((i * nbasis1 + aa) * nbasis0 + j) * nbasis1 + bb);
                localout[indexout] += xiajd * ptrinp2[ind2] * factor;
              }
            }
          }
        }
      }
    }
    // aggregate local copies into global array
#if defined(_OPENMP)
#pragma omp for
#endif
    for (int k = 0; k < dim; ++k)
      for (int p = 0; p < np; ++p) ptrout[k] += local[p][k];
  }
}
