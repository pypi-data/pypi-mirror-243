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
"""Gaussian orbital basis set module."""

# pylint: skip-file

from pathlib import Path, PurePath

import numpy as np

from pybest import filemanager
from pybest.context import context
from pybest.exceptions import GOBasisError
from pybest.io.embedding import load_embedding
from pybest.io.external_charges import load_charges
from pybest.io.iodata import IOData
from pybest.io.xyz import dump_xyz, load_xyz
from pybest.linalg import CholeskyLinalgFactory, DenseLinalgFactory
from pybest.log import log, timer
from pybest.utils import check_gobasis, check_type

# pybind11 classes
from . import Basis

__all__ = [
    "get_gobasis",
    "compute_nuclear_repulsion",
    "compute_overlap",
    "compute_kinetic",
    "compute_nuclear",
    "compute_dipole",
    "compute_quadrupole",
    "compute_pvp",
    "compute_eri",
    "compute_cholesky_eri",
    "get_tform_u2c",
]

try:
    from pybest.gbasis.pyints import (
        compute_cholesky_eri_cpp as cholesky_backend,
    )

    PYBEST_CHOLESKY_ENABLED = 1
except ImportError:
    PYBEST_CHOLESKY_ENABLED = 0

try:

    PYBEST_PVP_ENABLED = 1
except ImportError:
    PYBEST_PVP_ENABLED = 0

#
# Basis set reader
#


@timer.with_section("ReadBasisSet")
def get_gobasis(
    basisname: str,
    coords,
    active_fragment=None,
    dummy=None,
    element_map=None,
    print_basis=True,
) -> Basis:
    """Read basis set for molecular coordinates. If active_fragment and dummy are specified,
    the function will consider only the active fragment (active_fragment) and introduce
    ghost atoms (dummy).

    **Arguments:**

    basisname
        The name of the basis set

    coords
        filename containing the xyz coordinates or an IOData instance.


    **Optional arguments:**

    active_fragment
        Active fragment. A list containing the indices of all active atoms

    dummy
        Dummy atoms. A list containing the indices of all dummy atoms (same
        basis set as atom, but setting a charge of 0).

    element_map
        Different basis sets for different atoms. A dictionary containing
        the element names as keys and the basis set string as basis set
        information.

    print_basis
         If True (default), the information about the basis set is printed.
    """

    log.cite("the use of the Libint library", "valeev2019")

    #
    # Auxiliary functions
    #

    def dump_xyz_libint(fname, mol, unit_angstrom=False, fragment=None):
        #
        # Temporary file stored in filemanager.temp_dir
        #
        filename = filemanager.temp_path(f"{Path(fname).stem}.xyz")
        #
        # dump xyz coordinates of active fragment
        #
        dump_xyz(filename, mol, unit_angstrom=unit_angstrom, fragment=fragment)
        #
        # overwrite filename info
        #
        return filename

    def get_dir_path(basisname):
        dir_path = None
        # Check if augmented basis; PyBEST stores the full basis
        basisname_old = basisname
        if "aug-" in basisname:
            basisname = basisname.replace("aug-", "aug")
        if "*" in basisname:
            basisname = basisname.replace("*", "star")
        if context.check_fn(f"basis/{basisname.lower()}.g94"):
            dir_path = (
                Path(context.get_fn(f"basis/{basisname.lower()}.g94"))
                .resolve()
                .parent
            )
            basisname = basisname.lower()
        elif Path(basisname_old).exists():
            if "aug-" in basisname_old:
                raise GOBasisError(
                    "User-defined basis set cannot start with 'aug-'. Please rename "
                    "your basis set."
                )
            dir_path = Path(basisname_old).resolve().parent
            basisname = PurePath(basisname_old).stem
        else:
            raise GOBasisError(
                f"Basis set file {basisname}/{basisname_old} not found. "
                "Please check if file is present."
            )
        return dir_path, basisname

    def print_basis_info():
        if print_basis:
            if log.do_medium:
                log.hline("#")
                if active_fragment is None:
                    log("Printing basis for whole molecule:")
                else:
                    s = (
                        "["
                        + ",".join([f"{s_}" for s_ in active_fragment])
                        + "]"
                    )
                    log(f"Printing basis for active fragment {s}")
                basis.print_basis_info()
                log.hline("~")

    def print_active_fragmet_info():
        if active_fragment is not None:
            if log.do_medium:
                log.hline("#")
                log("Creating active fragment of supramolecule.")
                log.hline("-")
                basis.print_atomic_info()
                log.hline("-")

    def create_dummy_atoms():
        if dummy is not None:
            if not isinstance(dummy, list):
                raise GOBasisError("Dummy indices have to be a list")
            if not all(idx >= 0 for idx in dummy):
                raise GOBasisError(
                    f"Dummy indices have to be greater or equal 0. Got {dummy} instead."
                    f"Dummy indices have to be greater or equal {0}. Got negative instead."
                )
            #
            # account for shift due to active fragments:
            #
            shift = 0
            if active_fragment is not None:
                shift = min(active_fragment)
            for idx in dummy:
                if idx > basis.ncenter:
                    raise GOBasisError(
                        f"Dummy index {idx+1} larger than number of "
                        f"atoms {basis.ncenter}."
                    )
                basis.set_dummy_atoms(idx - shift)
            if log.do_medium:
                log.hline("#")
                log(
                    "Introducing dummy atoms. Coordinates [bohr] contain new charges:"
                )
                log.hline("-")
                basis.print_atomic_info()
                log.hline("-")

    #
    # Check coordinates: filename or IOData container; convert to pathlib.Path
    #
    coordfile = coords
    check_type("coordfile", coordfile, str, IOData)
    #
    # If np.ndarray, convert to .xyz format to read in coordinates using API
    #
    if isinstance(coordfile, IOData):
        #
        # Check if xyz file is present
        #
        if hasattr(coordfile, "filename"):
            coordfile = Path(coordfile.filename)
        else:
            #
            # If not, create xyz file
            # Dump coordinates for libint2 interface
            #
            coordfile = dump_xyz_libint("tmp_mol.xyz", coordfile)
    else:
        coordfile = Path(coordfile)
    #
    # Check for active fragments and decompose total molecules according to it
    #
    if active_fragment is not None:
        if not isinstance(active_fragment, list):
            raise GOBasisError("active_fragment has to be a list")
        #
        # Check if dummy atom is in active_fragment, otherwise raise error
        #
        if not all(idx >= 0 for idx in active_fragment):
            raise GOBasisError(
                f"Active indices have to be greater or equal 0. Got {active_fragment} instead."
                f"Active indices have to be greater or equal {0}. Got negative instead."
            )
        if dummy is not None:
            for idx in dummy:
                if idx not in active_fragment:
                    raise GOBasisError(
                        f"Dummy atom {idx} has to be in active_fragment"
                    )
        #
        # Create active fragment and save it to disk in filemanager.temp_dir
        # Read all coordinates in angstrom
        #
        data = load_xyz(coordfile, unit_angstrom=True)
        mol = IOData(coordinates=data["coordinates"], atom=data["atom"])
        #
        # overwrite filename info
        #
        coordfile = dump_xyz_libint(
            coordfile, mol, unit_angstrom=True, fragment=active_fragment
        )
    #
    # Check if basis set file is available
    #
    dir_path, basisname = get_dir_path(basisname)
    #
    # Read in basis (pass str to c++ routine)
    #
    basis = Basis(basisname, str(coordfile.resolve()), str(dir_path.resolve()))
    #
    # Print basis set information
    #
    print_basis_info()
    #
    # Print some info if fragments are present
    #
    print_active_fragmet_info()
    #
    # Create dummy atoms
    #
    create_dummy_atoms()
    #
    # Check basis set for consistencies
    #
    check_gobasis(basis)

    return basis


#
# Get external point charges
#


@timer.with_section("ReadPointCharges")
def get_charges(filename):
    """Get point charges from some .pc file.
    The structure of the .pc file is assumed to be similar to the .xyz file.
    Specifically:
        - the first line is the number of point charges in the file [int]
        - the second line is reserved for comments [str]
        - the following lines (each line for point charge) are composed of
        four columns:
            - first three columns are the xyz coordinates in Angstroms [float]
            - the 4-th column is the charge in a.u. [float]

    **Arguments:**

    filename
        filename containing the point charges (IOData instance : str)

    """
    from pybest.gbasis.pycharges import ExternalCharges

    # Get external charges from a .pc file
    data = load_charges(filename)
    charges = data["charges"]
    coords = data["coordinates"]
    x, y, z = coords[:, 0], coords[:, 1], coords[:, 2]
    return ExternalCharges(charges, x, y, z)


#
# Get static embedding potential
#


@timer.with_section("ReadEmbPotential")
def get_embedding(filename):
    """Get embedding potential from *.emb file.
    The structure of the .emb file is assumed to be similar to the .xyz file.
    Specifically:
        - the first line is the number of points in the file [int]
        - the second line is reserved for comments [str]
        - the following lines (each line for point charge) are composed of
        five columns:
            * the 1-st column contains charges [float]
            * the 2-nd, 3-rd, and 4-th columns include the xyz coordinates
            in Angstroms [float]
            * the 5-th column contains the wights [float]

    **Arguments:**

    filename
        filename containing the embedding potential (IOData instance : str)
    """

    from pybest.gbasis.pyembedding import StaticEmbedding

    log.cite(
        "the static embedding potential",
        "gomes2008embedding",
        "chakraborty2023",
    )

    # Get embedding potential from .emb file)
    data = load_embedding(filename)
    charges = data["charges"]
    coords = data["coordinates"]
    weights = data["weights"]
    x_coord, y_coord, z_coord = coords[:, 0], coords[:, 1], coords[:, 2]
    return StaticEmbedding(charges, x_coord, y_coord, z_coord, weights)


#
# External potentials
#


@timer.with_section("IntsNucNuc")
def compute_nuclear_repulsion(basis0, basis1=None):
    """Compute the nuclear repulsion energy

    **Arguments:**

    basis0, basis1
         A Basis instance

    **Returns:** A number (float)
    """
    from pybest.gbasis.pyints import compute_nuclear_repulsion_cpp as compute

    if basis1 is None:
        basis1 = basis0
    return compute(basis0, basis1)


@timer.with_section("IntsChargesNuc")
def compute_nuclear_pc(basis0, charges):
    """Compute the interaction of external charges with nuclear potential

    **Arguments:**

    basis0
         A Basis instance

    charges
         An ExternalCharges instance

    **Returns:** A number (float)
    """
    from pybest.gbasis.pyints import compute_nuclear_pc_cpp as compute_pc

    external = compute_pc(basis0, charges)
    return external


#
# 1- and 2-body integrals
#


@timer.with_section("IntsOlp")
def compute_overlap(basis0, basis1=None, uncontract=False):
    """Compute the overlap integrals in a Gaussian orbital basis

    **Arguments:**

    basis0, basis1
         A Basis instance

    **Returns:** ``TwoIndex`` object
    """
    from pybest.gbasis.pybasis import get_nubf
    from pybest.gbasis.pyints import compute_overlap_cpp as compute

    if basis1 is None:
        basis1 = basis0
    nbasis0 = basis0.nbasis
    nbasis1 = basis1.nbasis
    if uncontract:
        nbasis0 = get_nubf(basis0, True)
        nbasis1 = get_nubf(basis1, True)
    lf = DenseLinalgFactory(max(nbasis0, nbasis1))
    out = lf.create_two_index(nbasis0, nbasis1, "olp")
    # call the low-level routine
    compute(basis0, basis1, out.array, uncontract)
    # done
    return out


@timer.with_section("IntsKin")
def compute_kinetic(basis0, basis1=None, uncontract=False):
    """Compute the overlap integrals in a Gaussian orbital basis

    **Arguments:**

    basis0, basis1
         A Basis instance

    **Returns:** ``TwoIndex`` object
    """
    from pybest.gbasis.pybasis import get_nubf
    from pybest.gbasis.pyints import compute_kinetic_cpp as compute

    if basis1 is None:
        basis1 = basis0
    nbasis0 = basis0.nbasis
    nbasis1 = basis1.nbasis
    if uncontract:
        nbasis0 = get_nubf(basis0, True)
        nbasis1 = get_nubf(basis1, True)
    lf = DenseLinalgFactory(max(nbasis0, nbasis1))
    out = lf.create_two_index(nbasis0, nbasis1, "kin")
    # call the low-level routine
    compute(basis0, basis1, out.array, uncontract)
    # done
    return out


@timer.with_section("IntsNuc")
def compute_nuclear(basis0, basis1=None, uncontract=False):
    """Compute the overlap integrals in a Gaussian orbital basis

    **Arguments:**

    basis0, basis1
         A Basis instance

    **Returns:** ``TwoIndex`` object
    """
    from pybest.gbasis.pybasis import get_nubf
    from pybest.gbasis.pyints import compute_nuclear_cpp as compute

    if basis1 is None:
        basis1 = basis0
    nbasis0 = basis0.nbasis
    nbasis1 = basis1.nbasis
    if uncontract:
        nbasis0 = get_nubf(basis0, True)
        nbasis1 = get_nubf(basis1, True)
    lf = DenseLinalgFactory(max(nbasis0, nbasis1))
    out = lf.create_two_index(nbasis0, nbasis1, "ne")
    # call the low-level routine
    compute(basis0, basis1, out.array, uncontract)
    # done
    return out


@timer.with_section("IntsPointCharges")
def compute_point_charges(basis0, charges, basis1=None, uncontract=False):
    """Compute the interaction of point charges with electrons

    **Arguments:**

    basis0, basis1
         A Basis instance

    charges
        An External Charges instance

    uncontract
        Uncontracted basis is needed for DKH

    **Returns:** ``TwoIndex`` object
    """
    from pybest.gbasis.pybasis import get_nubf
    from pybest.gbasis.pyints import compute_point_charges_cpp as compute

    if basis1 is None:
        basis1 = basis0
    nbasis0 = basis0.nbasis
    nbasis1 = basis1.nbasis
    if uncontract:
        nbasis0 = get_nubf(basis0, True)
        nbasis1 = get_nubf(basis1, True)
    lf = DenseLinalgFactory(max(nbasis0, nbasis1))
    out = lf.create_two_index(nbasis0, nbasis1, "pc")
    # call the low-level routine
    compute(basis0, basis1, charges, out.array, uncontract)
    # done
    return out


@timer.with_section("IntsStaticEmbedding")
def compute_static_embedding(basis0, embedding, basis1=None, uncontract=False):
    """Compute the static embedding

    **Arguments:**

    basis0, basis1
         A Basis instance

    embedding
         An StaticEmbedding instance

    uncontract
        Uncontracted basis is needed for DKH

    **Returns:** ``TwoIndex`` object
    """
    from pybest.gbasis.pybasis import get_nubf

    if basis1 is None:
        basis1 = basis0
    nbasis0 = basis0.nbasis
    nbasis1 = basis1.nbasis
    if uncontract:
        nbasis0 = get_nubf(basis0, True)
        nbasis1 = get_nubf(basis1, True)
    lf = DenseLinalgFactory(max(nbasis0, nbasis1))
    out = lf.create_two_index(nbasis0, nbasis1, "emb")
    # call the low-level routine
    embedding.compute_static_embedding_cpp(basis0, basis1, out.array)
    # done
    return out


@timer.with_section("IntsDipole")
def compute_dipole(basis0, basis1=None, x=0.0, y=0.0, z=0.0):
    """Compute the dipole integrals in a Gaussian orbital basis

    **Arguments:**

    basis0, basis1
         A Basis instance

    **Returns:** ``TwoIndex`` object
    """
    from pybest.gbasis.pyints import compute_dipole_cpp as compute

    if basis1 is None:
        basis1 = basis0
    nbasis0 = basis0.nbasis
    nbasis1 = basis1.nbasis
    lf = DenseLinalgFactory(max(nbasis0, nbasis1))
    olp = lf.create_two_index(nbasis0, nbasis1, label="olp")
    mu_x = lf.create_two_index(nbasis0, nbasis1, label="mu_x")
    mu_y = lf.create_two_index(nbasis0, nbasis1, label="mu_y")
    mu_z = lf.create_two_index(nbasis0, nbasis1, label="mu_z")
    # call the low-level routine
    compute(
        basis0, basis1, olp.array, mu_x.array, mu_y.array, mu_z.array, x, y, z
    )

    # done
    return olp, mu_x, mu_y, mu_z, {"origin_coord": [x, y, z]}


@timer.with_section("IntsQuadrupole")
def compute_quadrupole(basis0, basis1=None, x=0.0, y=0.0, z=0.0):
    """Compute the overlap integrals in a Gaussian orbital basis

    **Arguments:**

    basis0, basis1
         A Basis instance

    **Returns:** ``TwoIndex`` object
    """
    from pybest.gbasis.pyints import compute_quadrupole_cpp as compute

    if basis1 is None:
        basis1 = basis0
    nbasis0 = basis0.nbasis
    nbasis1 = basis1.nbasis
    lf = DenseLinalgFactory(max(nbasis0, nbasis1))

    olp = lf.create_two_index(nbasis0, nbasis1, label="olp")
    mu_x = lf.create_two_index(nbasis0, nbasis1, label="mu_x")
    mu_y = lf.create_two_index(nbasis0, nbasis1, label="mu_y")
    mu_z = lf.create_two_index(nbasis0, nbasis1, label="mu_z")
    mu_xx = lf.create_two_index(nbasis0, nbasis1, label="mu_xx")
    mu_xy = lf.create_two_index(nbasis0, nbasis1, label="mu_xy")
    mu_xz = lf.create_two_index(nbasis0, nbasis1, label="mu_xz")
    mu_yy = lf.create_two_index(nbasis0, nbasis1, label="mu_yy")
    mu_yz = lf.create_two_index(nbasis0, nbasis1, label="mu_yz")
    mu_zz = lf.create_two_index(nbasis0, nbasis1, label="mu_zz")
    # call the low-level routine
    compute(
        basis0,
        basis1,
        olp.array,
        mu_x.array,
        mu_y.array,
        mu_z.array,
        mu_xx.array,
        mu_xy.array,
        mu_xz.array,
        mu_yy.array,
        mu_yz.array,
        mu_zz.array,
        x,
        y,
        z,
    )
    # done
    return (
        olp,
        mu_x,
        mu_y,
        mu_z,
        mu_xx,
        mu_xy,
        mu_xz,
        mu_yy,
        mu_yz,
        mu_zz,
    )


@timer.with_section("IntsPVP")
def compute_pvp(basis0, basis1=None, uncontract=True):
    """Compute the overlap integrals in a Gaussian orbital basis

    **Arguments:**

    basis0, basis1
         A Basis instance

    **Returns:** ``TwoIndex`` object
    """
    try:
        from pybest.gbasis.pyints import compute_pvp_cpp as compute
    # NOTE: apparently pybind11's ImportError class is not subclass of Python's ImportError
    except Exception as excepts:
        log.warn("pVp integrals not supported yet.")
        raise excepts
    from pybest.gbasis.pybasis import get_nubf

    if basis1 is None:
        basis1 = basis0
    nbasis0 = basis0.nbasis
    nbasis1 = basis1.nbasis
    if uncontract:
        nbasis0 = get_nubf(basis0, True)
        nbasis1 = get_nubf(basis1, True)
    lf = DenseLinalgFactory(max(nbasis0, nbasis1))
    out = lf.create_two_index(nbasis0, nbasis1, "pvp")
    # call the low-level routine
    compute(basis0, basis1, out.array, uncontract)
    # done
    return out


@timer.with_section("IntsPPCP")
def compute_ppcp(basis0, charges, basis1=None, uncontract=True):
    """Compute the pPCp integrals to correct for picture changes
    when using, for instance, the DKH Hamiltonian.

    **Arguments:**

    basis0, basis1
         A Basis instance

    **Returns:** ``TwoIndex`` object
    """
    try:
        from pybest.gbasis.pyints import compute_ppcp_cpp as compute
    # NOTE: apparently pybind11's ImportError class is not subclass of Python's ImportError
    except Exception as missing_module:
        log.warn("pPCp integrals not supported yet.")
        raise missing_module
    from pybest.gbasis.pybasis import get_nubf

    if basis1 is None:
        basis1 = basis0
    nbasis0 = basis0.nbasis
    nbasis1 = basis1.nbasis
    if uncontract:
        nbasis0 = get_nubf(basis0, True)
        nbasis1 = get_nubf(basis1, True)
    lf = DenseLinalgFactory(max(nbasis0, nbasis1))
    out = lf.create_two_index(nbasis0, nbasis1, "ppcp")
    # call the low-level routine
    compute(basis0, basis1, charges, out.array, uncontract)
    # done
    return out


@timer.with_section("IntsERI")
def compute_eri(basis0, basis1=None, basis2=None, basis3=None, symmetry=True):
    """Compute the overlap integrals in a Gaussian orbital basis

    **Arguments:**

    basis0, basis1
         A Basis instance

    **Returns:** ``TwoIndex`` object
    """
    from pybest.gbasis.pyints import compute_eri_cpp as compute

    if basis1 is None:
        basis1 = basis0
    if basis2 is None:
        basis2 = basis0
    if basis3 is None:
        basis3 = basis0
    nbasis0 = basis0.nbasis
    nbasis1 = basis1.nbasis
    nbasis2 = basis2.nbasis
    nbasis3 = basis3.nbasis
    if symmetry:
        log("Computing only symmetry-unique elements of ERI.")
    else:
        log("Computing all elements of ERI.")
    lf = DenseLinalgFactory(max(nbasis0, nbasis1, nbasis2, nbasis3))
    out = lf.create_four_index(nbasis0, nbasis1, nbasis2, nbasis3, "eri")
    # call the low-level routine
    compute(basis0, basis1, basis2, basis3, out.array, symmetry)
    # done
    return out


@timer.with_section("IntsCD-ERI")
def compute_cholesky_eri(
    basis0, basis1=None, symmetry=True, threshold=1e-3, prealloc=15
):
    """Compute the cholesky decomposed ERI in a Gaussian orbital basis

     **Arguments:**

     basis0, basis1
         A Basis instance

     threshold float
         accuracy threshold for cd-eri algorithm

     prealloc int
         controlls pre-allocation size of output tensor.

         total size is Naux x Nbf x Nbf,
         prealloc controlls size of Naux as:
         Naux = prealloc * Nbf.

         For thresholds below 1e-6 prealloc=10 is reasonable.
         If pre-allocation size won't be sufficient,
         additional memory allocations and data movement might
         occur, degrading the performance.


    **Returns:** ``CholeskyFourIndex`` object
    """
    if not PYBEST_CHOLESKY_ENABLED:
        log.warn(
            "Cholesky-decomposition ERI are not available. Build libchol and "
            "re-run build --enable-cholesky=1"
        )
        raise RuntimeError(
            "Cholesky decomposition of ERI was not enabled during compilation!"
        )

    log.warn(f"basis1:{basis1} option is not active in cd-eri module")
    log.warn(f"symmetry:{symmetry} option is not active in cd-eri module")
    nbasis0 = basis0.nbasis

    if log.do_medium:
        log.hline("~")
        log("Computing cholesky decomposed ERI:")
        log(f"NBASIS:        {nbasis0}")
        log(f"CD_THRESH:     {threshold}")
        log(f"CD_BETA:       {prealloc}")
        log("computing ...")

    # call the low-level routine
    cd_eri = cholesky_backend(basis0, threshold, prealloc)
    nvec = int(cd_eri.size / (nbasis0 * nbasis0))

    # fold to 3-idx tensor
    cd_eri_npy = cd_eri.reshape(nvec, nbasis0, nbasis0)

    # compute some statistics
    cd_eri_nbytes = cd_eri_npy.nbytes
    cd_eri_mib = cd_eri_nbytes / (float(1024) ** 2)
    cd_eri_sparsity = 1.0 - np.count_nonzero(cd_eri_npy) / float(
        cd_eri_npy.size
    )

    if log.do_medium:
        log("\t finished!")
        log(f"CD_ERI_SHAPE:    {(nvec, nbasis0, nbasis0)}")
        log(f"CD_ERI_SIZE:     {cd_eri_npy.size}")
        log(f"CD_ERI_BYTES:    {cd_eri_nbytes} ({cd_eri_mib:.2f} MiB)")
        log(f"CD_ERI_SPARSITY: {100 * cd_eri_sparsity:.2f} %")
        log.hline("~")

    lf = CholeskyLinalgFactory()
    out = lf.create_four_index(
        nbasis=nbasis0,
        nvec=nvec,
        array=cd_eri_npy,
        array2=cd_eri_npy,
        copy=False,
        label="cd-eri",
    )
    return out


#
# Basis set transformation uncontracted<->contracted
#


def get_tform_u2c(basis):
    """Transform intergrals from an uncontracted to a contracted basis set

    **Arguments:**

    basis
         FIXME

    **Returns:** ``TwoIndex`` object
    """
    from pybest.gbasis.pybasis import get_nubf, get_solid_tform_u2c

    nub = get_nubf(basis, True)
    # prepare the output array
    lf = DenseLinalgFactory(basis.nbasis)
    output = lf.create_two_index(basis.nbasis, nub)
    # call the low-level routine
    get_solid_tform_u2c(basis, output.array, basis.nbasis, nub)
    # done
    return output
