# -*- coding: utf-8 -*-
# PyBEST: Pythonic Black-box Electronic Structure Tool
# Copyright (C) 2016-- The PyBEST Development Team
#
# This file is part of PyBEST.
#
# PyBEST is free software; you can redistribute it and/or
# modify it under the terms of the GNU General Public License
# as published by the Free Software Foundation; either version 3
# of the License, or (at your option) any later version.
#
# PyBEST is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, see <http://www.gnu.org/licenses/>
# --

# Detailed changelog:
#
# This implementation has been taken from `Horton 2.0.0`.
# However, this file has been updated and debugged. Compatibility with Horton is NOT
# guaranteed.
# Its current version contains updates from the PyBEST developer team.
#
# Detailed changes:
# 2020-07-01: Create PyBEST basis set instance
# 2020-07-01: Update to PyBEST standard, including filemanager
# 2020-07-01: Update to new python features: f-strings, pathlib

"""Molekel wavefunction input file format"""


import pathlib

import numpy as np

from pybest import filemanager
from pybest.gbasis.gobasis_helper import shell_str2int
from pybest.gbasis.pybasis import Basis
from pybest.io.iodata import IOData
from pybest.io.molden import (
    _fix_molden_from_buggy_codes,
    _get_molden_permutation,
)
from pybest.io.xyz import dump_xyz
from pybest.periodic import periodic
from pybest.units import angstrom

__all__ = ["load_mkl"]


def load_mkl(filename, lf):
    """Load data from a Molekel file.

    **Arguments:**

    filename
         The filename of the mkl file.

    lf
         A LinalgFactory instance.

    **Returns** a dictionary with: ``coordinates``, ``numbers``, ``obasis``,
    ``orb_a``. It may also contain: ``orb_b``, ``signs``.
    """

    def helper_dump_xyz_for_libint(fname, mol):

        #
        # Temporary file stored in {filemanager.temp_dir}
        #
        filename = filemanager.temp_path(f"{pathlib.Path(fname).stem}.xyz")
        #
        # dump xyz coordinates of active fragment
        #
        dump_xyz(filename, mol, unit_angstrom=False)
        #
        # overwrite filename info
        #
        return filename

    def helper_char_mult(f):
        return [int(word) for word in f.readline().split()]

    def helper_coordinates(f):
        """Load element numbers and coordinates"""
        atoms = []
        coordinates = []
        while True:
            line = f.readline()
            if len(line) == 0 or line.strip() == "$END":
                break
            words = line.split()
            atoms.append(periodic[words[0]].symbol.ljust(2))
            coordinates.append(
                [float(words[1]), float(words[2]), float(words[3])]
            )
        atoms = np.array(atoms, object)
        coordinates = np.array(coordinates) * angstrom
        mol = IOData(**{"coordinates": coordinates, "atom": atoms})
        #
        # If not, create xyz file
        # Dump coordinates for libint2 interface
        #
        coordfile = helper_dump_xyz_for_libint("tmp_mol.xyz", mol)
        return coordfile, mol

        numbers = []
        coordinates = []
        while True:
            line = f.readline()
            if len(line) == 0 or line.strip() == "$END":
                break
            words = line.split()
            numbers.append(int(words[0]))
            coordinates.append(
                [float(words[1]), float(words[2]), float(words[3])]
            )
        numbers = np.array(numbers, int)
        coordinates = np.array(coordinates) * angstrom
        return numbers, coordinates

    def helper_obasis(f, coordfile):
        shell_types = []
        shell_map = []
        nprims = []
        alphas = []
        con_coeffs = []

        center_counter = 0
        in_shell = False
        nprim = None
        while True:
            line = f.readline()
            lstrip = line.strip()
            if len(line) == 0 or lstrip == "$END":
                break
            if len(lstrip) == 0:
                continue
            if lstrip == "$$":
                center_counter += 1
                in_shell = False
            else:
                words = line.split()
                if len(words) == 2:
                    assert in_shell
                    alpha = float(words[0])
                    alphas.append(alpha)
                    con_coeffs.append(float(words[1]))
                    nprim += 1
                else:
                    if nprim is not None:
                        nprims.append(nprim)
                    shell_map.append(center_counter)
                    # always assume pure basis functions
                    shell_type = shell_str2int(words[1], pure=True)[0]
                    shell_types.append(shell_type)
                    in_shell = True
                    nprim = 0
        if nprim is not None:
            nprims.append(nprim)

        shell_map = np.array(shell_map)
        nprims = np.array(nprims)
        shell_types = np.array(shell_types)
        alphas = np.array(alphas)
        con_coeffs = np.array(con_coeffs)

        gobasis = Basis(
            str(coordfile.resolve()),
            nprims,
            shell_map,
            shell_types,
            alphas,
            con_coeffs,
        )

        return gobasis

    def helper_coeffs(f, nbasis):
        coeffs = []
        energies = []

        in_orb = 0
        while True:
            line = f.readline()
            lstrip = line.strip()
            if len(line) == 0 or lstrip == "$END":
                break
            if in_orb == 0:
                # read a1g line
                words = lstrip.split()
                ncol = len(words)
                assert ncol > 0
                for word in words:
                    assert word == "a1g"
                cols = [np.zeros((nbasis, 1), float) for icol in range(ncol)]
                in_orb = 1
            elif in_orb == 1:
                # read energies
                words = lstrip.split()
                assert len(words) == ncol
                for word in words:
                    energies.append(float(word))
                in_orb = 2
                ibasis = 0
            elif in_orb == 2:
                # read expansion coefficients
                words = lstrip.split()
                assert len(words) == ncol
                for icol in range(ncol):
                    cols[icol][ibasis] = float(words[icol])
                ibasis += 1
                if ibasis == nbasis:
                    in_orb = 0
                    coeffs.extend(cols)

        return np.hstack(coeffs), np.array(energies)

    def helper_occ(f):
        occs = []
        while True:
            line = f.readline()
            lstrip = line.strip()
            if len(line) == 0 or lstrip == "$END":
                break
            for word in lstrip.split():
                occs.append(float(word))
        return np.array(occs)

    charge = None
    spinmult = None
    numbers = None
    coordfile = None
    obasis = None
    coeff_alpha = None
    ener_alpha = None
    occ_alpha = None
    coeff_beta = None
    ener_beta = None
    occ_beta = None
    with open(filename) as f:
        while True:
            line = f.readline()
            if len(line) == 0:
                break
            line = line.strip()
            if line == "$CHAR_MULT":
                charge, spinmult = helper_char_mult(f)
            elif line == "$COORD":
                coordfile, mol = helper_coordinates(f)
            elif line == "$BASIS":
                obasis = helper_obasis(f, coordfile)
            elif line == "$COEFF_ALPHA":
                coeff_alpha, ener_alpha = helper_coeffs(f, obasis.nbasis)
            elif line == "$OCC_ALPHA":
                occ_alpha = helper_occ(f)
            elif line == "$COEFF_BETA":
                coeff_beta, ener_beta = helper_coeffs(f, obasis.nbasis)
            elif line == "$OCC_BETA":
                occ_beta = helper_occ(f)

    if charge is None:
        raise IOError("Charge and multiplicity not found in mkl file.")
    if coordfile is None:
        raise IOError("Coordinates not found in mkl file.")
    if obasis is None:
        raise IOError("Orbital basis not found in mkl file.")
    if coeff_alpha is None:
        raise IOError("Alpha orbitals not found in mkl file.")
    if occ_alpha is None:
        raise IOError("Alpha occupation numbers not found in mkl file.")

    lf.default_nbasis = obasis.nbasis
    numbers = np.array([periodic[i].number for i in mol.atom])
    nelec = numbers.sum() - charge
    if coeff_beta is None:
        assert nelec % 2 == 0
        assert abs(occ_alpha.sum() - nelec) < 1e-7
        orba = lf.create_orbital(obasis.nbasis, coeff_alpha.shape[1])
        orba.coeffs[:] = coeff_alpha
        orba.energies[:] = ener_alpha
        orba.occupations[:] = occ_alpha / 2
        orbb = None
    else:
        if occ_beta is None:
            raise IOError(
                "Beta occupation numbers not found in mkl file while beta orbitals were present."
            )
        nalpha = int(np.round(occ_alpha.sum()))
        nbeta = int(np.round(occ_beta.sum()))
        assert nelec == nalpha + nbeta
        assert coeff_alpha.shape == coeff_beta.shape
        assert ener_alpha.shape == ener_beta.shape
        assert occ_alpha.shape == occ_beta.shape
        orba = lf.create_orbital(obasis.nbasis, coeff_alpha.shape[1])
        orba.coeffs[:] = coeff_alpha
        orba.energies[:] = ener_alpha
        orba.occupations[:] = occ_alpha
        orbb = lf.create_orbital(obasis.nbasis, coeff_beta.shape[1])
        orbb.coeffs[:] = coeff_beta
        orbb.energies[:] = ener_beta
        orbb.occupations[:] = occ_beta

    permutation = _get_molden_permutation(obasis)
    # bring back to standard ordering in PyBEST
    orba.permute_basis(permutation)
    result = {
        "coordinates": mol.coordinates,
        "orb_a": orba,
        "lf": lf,
        "atom": mol.atom,
        "gobasis": obasis,
    }
    if orbb is not None:
        orbb.permute_basis(permutation)
        result["orb_b"] = orbb
    _fix_molden_from_buggy_codes(result, filename)
    return result
