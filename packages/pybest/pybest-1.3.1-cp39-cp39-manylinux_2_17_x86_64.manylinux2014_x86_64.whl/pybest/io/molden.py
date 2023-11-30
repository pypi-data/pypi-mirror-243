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
# 2020-07-01: Update to PyBEST standard, including order of basis function, filemanager
# 2020-07-01: Use libint's dump to molden feature
# 2020-07-01: Update to new python features: f-strings, pathlib

"""Molden wavefunction input file format"""

# TODO: Rewrite load_molden to reduce complexity

import pathlib

import numpy as np

from pybest import filemanager
from pybest.exceptions import ArgumentError, ConsistencyError
from pybest.gbasis.gobasis_helper import shell_str2int

# pybind11 class
from pybest.gbasis.pybasis import Basis
from pybest.io.iodata import IOData
from pybest.linalg import DenseLinalgFactory
from pybest.log import log
from pybest.periodic import periodic
from pybest.units import angstrom

__all__ = ["load_molden", "dump_molden"]


def _get_molden_permutation(obasis, reverse=False):
    # Reorder the Cartesian basis functions to obtain the PyBEST standard ordering.
    # Molden assumes the following ordering:
    # 5D: D 0, D+1, D-1, D+2, D-2
    # 6D: xx, yy, zz, xy, xz, yz
    # 7F: F 0, F+1, F-1, F+2, F-2, F+3, F-3
    # 10F: xxx, yyy, zzz, xyy, xxy, xxz, xzz, yzz, yyz, xyz
    # 9G: G 0, G+1, G-1, G+2, G-2, G+3, G-3, G+4, G-4
    # 15G: xxxx yyyy zzzz xxxy xxxz xyyy yyyz xzzz yzzz xxyy xxzz yyzz xxyz xyyz xyzz
    permutation_rules = {
        # solid harmonics
        2: np.array([4, 2, 0, 1, 3]),
        3: np.array([6, 4, 2, 0, 1, 3, 5]),
        4: np.array([8, 6, 4, 2, 0, 1, 3, 5, 7]),
        # cartesians
        -2: np.array([0, 3, 4, 1, 5, 2]),
        -3: np.array([0, 4, 5, 3, 9, 6, 1, 8, 7, 2]),
        -4: np.array([0, 3, 4, 9, 12, 10, 5, 13, 14, 7, 1, 6, 11, 8, 2]),
    }
    permutation = []
    for shell_type in obasis.shell_types:
        rule = permutation_rules.get(shell_type)
        if reverse and rule is not None:
            reverse_rule = np.zeros(len(rule), int)
            for i, j in enumerate(rule):
                reverse_rule[j] = i
            rule = reverse_rule
        if rule is None:
            rule = np.arange(obasis.get_shell_size(shell_type))
        permutation.extend(rule + len(permutation))
    return np.array(permutation, dtype=int)


def load_molden(filename):
    """Load data from a molden input file.

    **Arguments:**

    filename
         The filename of the molden input file.

    **Returns:** a dictionary with: ``coordinates``, ``numbers``, ``obasis``,
    ``orb_a``, ``signs``. It may also contain: ``title``, ``orb_b``.
    """

    def helper_dump_xyz_for_libint(fname, mol):
        from pybest.io.xyz import dump_xyz

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

    def helper_coordinates(f, cunit):
        """Load element numbers and coordinates"""
        atoms = []
        coordinates = []
        while True:
            last_pos = f.tell()
            line = f.readline()
            if len(line) == 0:
                break
            words = line.split()
            if len(words) != 6:
                # Go back to previous line and stop
                f.seek(last_pos)
                break
            atoms.append(periodic[words[2]].symbol.ljust(2))
            coordinates.append(
                [float(words[3]), float(words[4]), float(words[5])]
            )
        atoms = np.array(atoms, object)
        coordinates = np.array(coordinates) * cunit
        mol = IOData(**{"coordinates": coordinates, "atom": atoms})
        #
        # If not, create xyz file
        # Dump coordinates for libint2 interface
        #
        coordfile = helper_dump_xyz_for_libint("tmp_mol.xyz", mol)
        return coordfile, mol

    def helper_obasis(f, coordfile, pure):
        """Load the orbital basis"""
        shell_types = []
        shell_map = []
        nprims = []
        alphas = []
        con_coeffs = []

        icenter = 0
        in_atom = False
        in_shell = False
        while True:
            last_pos = f.tell()
            line = f.readline()
            if len(line) == 0:
                break
            words = line.split()
            if len(words) == 0:
                in_atom = False
                in_shell = False
            elif len(words) == 2 and not in_atom:
                icenter = int(words[0]) - 1
                in_atom = True
                in_shell = False
            elif len(words) == 3:
                in_shell = True
                shell_map.append(icenter)
                shell_label = words[0].lower()
                shell_type = shell_str2int(
                    shell_label, pure.get(shell_label, False)
                )[0]
                shell_types.append(shell_type)
                nprims.append(int(words[1]))
            elif len(words) == 2 and in_atom:
                assert in_shell
                alpha = float(words[0].replace("D", "E"))
                alphas.append(alpha)
                con_coeff = float(words[1].replace("D", "E"))
                con_coeffs.append(con_coeff)
            else:
                # done, go back one line
                f.seek(last_pos)
                break
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
        """Load the orbital coefficients"""
        coeff_alpha = []
        ener_alpha = []
        occ_alpha = []
        coeff_beta = []
        ener_beta = []
        occ_beta = []

        new_orb = True
        while True:
            line = f.readline()
            if len(line) == 0 or "[" in line:
                break
            # prepare array with orbital coefficients
            if "=" in line:
                if "Ene=" in line:
                    energy = float(line.split("=")[1])
                elif "Spin=" in line:
                    spin = line.split("=")[1].strip()
                elif "Occup=" in line:
                    occ = float(line.split()[1])
                new_orb = True
            else:
                words = line.split()
                # First column corresponds to orbital index
                # Note that zeros might not be stored in the .molden file
                # Thus, to prevent an error, we read in each index explicitly
                # reset by 1 to account for python indexing
                icoeff = int(words[0]) - 1
                if icoeff >= nbasis:
                    raise IOError(
                        "Too many expansions coefficients in one orbital in molden file."
                    )
                if new_orb:
                    # store col, energy and occ
                    col = np.zeros((nbasis, 1))
                    if spin.lower() == "alpha":
                        coeff_alpha.append(col)
                        ener_alpha.append(energy)
                        occ_alpha.append(occ)
                    else:
                        coeff_beta.append(col)
                        ener_beta.append(energy)
                        occ_beta.append(occ)
                    new_orb = False
                col[icoeff] = float(words[1])

        coeff_alpha = np.hstack(coeff_alpha)
        ener_alpha = np.array(ener_alpha)
        occ_alpha = np.array(occ_alpha)
        if len(coeff_beta) == 0:
            coeff_beta = None
            ener_beta = None
            occ_beta = None
        else:
            coeff_beta = np.hstack(coeff_beta)
            ener_beta = np.array(ener_beta)
            occ_beta = np.array(occ_beta)
        return (
            (coeff_alpha, ener_alpha, occ_alpha),
            (coeff_beta, ener_beta, occ_beta),
        )

    # First pass: scan the file for pure/cartesian modifiers.
    # Unfortunately, some program put this information _AFTER_ the basis
    # set specification.
    pure = {"d": False, "f": False, "g": False}
    with open(filename, encoding="utf8") as f:
        for line in f:
            line = line.lower()
            if line.startswith("[5d]") or line.startswith("[5d7f]"):
                pure["d"] = True
                pure["f"] = True
            elif line.lower().startswith("[7f]"):
                pure["f"] = True
            elif line.lower().startswith("[5d10f]"):
                pure["d"] = True
                pure["f"] = False
            elif line.lower().startswith("[9g]"):
                pure["g"] = True

    # Second pass: read all the other info.
    coordfile = None
    obasis = None
    coeff_alpha = None
    ener_alpha = None
    occ_alpha = None
    coeff_beta = None
    ener_beta = None
    occ_beta = None
    title = None
    mol = None
    with open(filename, encoding="utf8") as f:
        line = f.readline()
        if line != "[Molden Format]\n":
            raise IOError("Molden header not found")
        while True:
            line = f.readline()
            if len(line) == 0:
                break
            line = line.strip()
            if line == "[Title]":
                title = f.readline().strip()
            elif line.startswith("[Atoms]"):
                if "au" in line.lower():
                    cunit = 1
                elif "angs" in line.lower():
                    cunit = angstrom
                coordfile, mol = helper_coordinates(f, cunit)
            elif line == "[GTO]":
                if coordfile is None:
                    raise IOError(
                        "Coordinates not found in molden input file."
                    )
                obasis = helper_obasis(f, coordfile, pure)
            elif line == "[STO]":
                raise NotImplementedError(
                    "Slater-type orbitals are not supported in PyBEST."
                )
            elif line == "[MO]":
                data_alpha, data_beta = helper_coeffs(f, obasis.nbasis)
                coeff_alpha, ener_alpha, occ_alpha = data_alpha
                coeff_beta, ener_beta, occ_beta = data_beta

    if coordfile is None:
        raise IOError("Coordinates not found in molden input file.")
    if obasis is None:
        raise IOError("Orbital basis not found in molden input file.")
    if coeff_alpha is None:
        raise IOError("Alpha orbitals not found in molden input file.")

    lf = DenseLinalgFactory(obasis.nbasis)
    if coeff_beta is None:
        orba = lf.create_orbital(obasis.nbasis, coeff_alpha.shape[1])
        orba.coeffs[:] = coeff_alpha
        orba.energies[:] = ener_alpha
        orba.occupations[:] = occ_alpha / 2
        orbb = None
    else:
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
    if title is not None:
        result["title"] = title
    if orbb is not None:
        orbb.permute_basis(permutation)
        result["orb_b"] = orbb

    _fix_molden_from_buggy_codes(result, filename)

    return result


def _is_normalized_properly(obasis, orba, orbb, signs=None, threshold=1e-4):
    """Test the normalization of the occupied and virtual orbitals

    **Arguments:**

    obasis
         An instance of the PyBasis class.

    orba
         The alpha orbitals.

    orbb
         The beta orbitals (may be None).

    **Optional arguments:**

    signs
         Changes in sign conventions.

    threshold
         When the maximal error on the norm is large than the threshold,
         the function returns False. True is returned otherwise.
    """
    from pybest.gbasis.gobasis import compute_overlap

    # Set default value for signs
    if signs is None:
        signs = np.ones(obasis.nbasis, int)
    # Compute the overlap matrix.
    olp = compute_overlap(obasis)
    # Compute the norm of each occupied and virtual orbital. Keep track of
    # the largest deviation from unity
    error_max = 0.0
    for iorb in range(orba.nfn):
        vec = orba.coeffs[:, iorb] * signs
        norm = olp.inner(vec, vec)
        error_max = max(error_max, abs(norm - 1))
    if orbb is not None:
        for iorb in range(orbb.nfn):
            vec = orbb.coeffs[:, iorb] * signs
            norm = olp.inner(vec, vec)
            error_max = max(error_max, abs(norm - 1))
    # final judgement
    return error_max <= threshold


def _get_orca_signs(obasis):
    """Return an array with sign corrections for orbitals read from ORCA.

    **Arguments:**

    obasis
         An instance of GOBasis.
    """
    sign_rules = {
        4: [-1, -1, 1, 1, 1, 1, 1, -1, -1],
        3: [-1, 1, 1, 1, 1, 1, -1],
        2: [1, 1, 1, 1, 1],
        0: [1],
        1: [1, 1, 1],
    }
    signs = []
    for shell_type in obasis.shell_types:
        if shell_type in sign_rules:
            signs.extend(sign_rules[shell_type])
        else:
            signs.extend([1] * obasis.get_shell_size(shell_type))
    return np.array(signs, dtype=int)


def _get_molpro_factors(obasis):
    """Return an array with scalint corrections for orbitals read from molpro.

    **Arguments:**

    obasis
         An instance of GOBasis.
    """
    factor_rules = {
        0: [1],
        1: [1, 1, 1],
        -2: [1, np.sqrt(3), np.sqrt(3), 1, np.sqrt(3), 1],
        -3: [
            1,
            np.sqrt(5),
            np.sqrt(5),
            np.sqrt(5),
            np.sqrt(15),
            np.sqrt(5),
            1,
            np.sqrt(5),
            np.sqrt(5),
            1,
        ],
        # There are some problems with g functions as they have a different normalization.
        # Due to numerical problems, we cannot use 37/3 as scaling factor...
        -4: [
            1,
            np.sqrt(7),
            np.sqrt(7),
            np.sqrt(35 / 3 + 0.666666666666667),
            np.sqrt(35),
            np.sqrt(35 / 3 + 0.666666666666667),
            np.sqrt(7),
            np.sqrt(35),
            np.sqrt(35),
            np.sqrt(7),
            1,
            np.sqrt(7),
            np.sqrt(35 / 3 + 0.666666666666667),
            np.sqrt(7),
            1,
        ],
    }
    factors = []
    for shell_type in obasis.shell_types:
        if shell_type in factor_rules:
            factors.extend(factor_rules[shell_type])
        else:
            factors.extend([1] * obasis.get_shell_size(shell_type))
    return np.array(factors, dtype=float)


def _get_fixed_con_coeffs(obasis, mode):
    """Return corrected contraction coefficients, assuming they came from an
    ORCA/PSI4 molden/mkl file.

    **Arguments:**

    obasis
         An instance of GOBasis.

    mode
         A string, either 'orca' or 'psi4'
    """
    assert mode in ["orca", "psi4"]
    factor = 1.0
    obasis.renormalize_contr(0, np.array([0, 0, 0]), factor)
    obasis.renormalize_contr(1, np.array([1, 0, 0]), factor)
    if mode == "psi4":
        factor = 1 / np.sqrt(3)
    obasis.renormalize_contr(2, np.array([1, 1, 0]), factor)
    if mode == "psi4":
        factor = 1 / np.sqrt(15)
    obasis.renormalize_contr(3, np.array([1, 1, 1]), factor)
    if mode == "psi4":
        factor = 1 / np.sqrt(105)
    obasis.renormalize_contr(4, np.array([2, 1, 1]), factor)


def _get_fixed_mo_coeffs(obasis, mode, result):
    """Return corrected contraction coefficients, assuming they came from an
    ORCA/PSI4 molden/mkl file.

    **Arguments:**

    obasis
         An instance of GOBasis.

    mode
         A string, either 'orca' or 'psi4'
    """
    assert mode in ["molpro"]
    factors = _get_molpro_factors(obasis)
    result["orb_a"].iscale_basis(factors)
    if result.get("orb_b") is not None:
        result["orb_b"].iscale_basis(factors)


def _fix_molden_from_buggy_codes(result, filename):
    """Detect errors in the data loaded from a molden/mkl/... file and correct.

    **Argument:**

    result
         A dictionary with the data loaded in the ``load_molden`` function.

    This function can recognize erroneous files created by PSI4 and ORCA. The
    data in the obasis and signs fields will be updated accordingly.
    """
    obasis = result["gobasis"]
    # make working copy
    obasis_ = Basis(obasis)
    #
    # First, check current normalization
    #
    if _is_normalized_properly(obasis_, result["orb_a"], result.get("orb_b")):
        # The file is good. No need to change data.
        return
    if log.do_medium:
        log.hline("~")
        log("Detected incorrect normalization of orbitals loaded from a file.")
    #
    # Second, consider ORCA molden files
    #
    orca_signs = _get_orca_signs(obasis_)
    _get_fixed_con_coeffs(obasis_, "orca")
    if _is_normalized_properly(
        obasis_, result["orb_a"], result.get("orb_b"), orca_signs
    ):
        if log.do_medium:
            log("Detected typical ORCA errors in file. Fixing them...")
            log.hline("~")
        result["signs"] = orca_signs
        result["gobasis"] = obasis_
        return
    #
    # Third, consider PSI4 molden files
    #
    # make working copy
    obasis_ = Basis(obasis)
    # Try to fix it as if it was a file generated by PSI4.
    _get_fixed_con_coeffs(obasis_, "psi4")
    if _is_normalized_properly(obasis_, result["orb_a"], result.get("orb_b")):
        if log.do_medium:
            log("Detected typical PSI4 errors in file. Fixing them...")
            log.hline("~")
        result["gobasis"] = obasis_
        return
    #
    # Fourth, consider MOLPRO molden files
    #
    _get_fixed_mo_coeffs(obasis, "molpro", result)
    if _is_normalized_properly(obasis, result["orb_a"], result.get("orb_b")):
        if log.do_medium:
            log("Detected typical MOLPRO errors in file. Fixing them...")
            log.hline("~")
        return

    raise IOError(
        f"Could not correct the data read from {filename}. The molden or "
        "molekel file you are trying to load contains errors."
    )


def dump_molden(filename, data, threshold=0.0):
    """Write data to a file in the molden input format.

    **Arguments:**

    filename
         The filename of the molden input file, which is an output file for
         this routine.

    data
         An IOData instance. Must contain ``orb_a``.
         May contain ``orb_b``.
    """
    # check where basis set is stored
    if hasattr(data, "occ_model") and isinstance(
        data.occ_model.factory, Basis
    ):
        # NOTE: trip the wire, when gobasis definition different
        if hasattr(data, "gobasis"):
            if data.occ_model.factory != data.gobasis:
                raise ConsistencyError(
                    "Different basis sets stored in IOData (occ_model vs gobasis). "
                )

        gobasis = data.occ_model.factory
    elif hasattr(data, "gobasis"):
        gobasis = data.gobasis
    else:
        raise ArgumentError("Basis set not found!")

    if hasattr(data, "orb_b"):
        spina = np.ones((data.orb_a.nbasis,), dtype=bool)
        spinb = np.zeros((data.orb_a.nbasis,), dtype=bool)
        orbs = np.hstack((data.orb_a.coeffs, data.orb_b.coeffs))
        occs = np.hstack((data.orb_a.occupations, data.orb_b.occupations))
        energies = np.hstack((data.orb_a.energies, data.orb_b.energies))
        spin = np.hstack((spina, spinb))
        gobasis.dump_molden(filename, orbs, occs, energies, spin, threshold)
    else:
        spin = np.ones((data.orb_a.nbasis,), dtype=bool)
        gobasis.dump_molden(
            filename,
            data.orb_a.coeffs,
            data.orb_a.occupations * 2.0,
            data.orb_a.energies,
            spin,
            threshold,
        )
