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
# 2020-07-01: use pathlib.Path to dump/load files
# 2020-07-01: new prepare_ghost function
# 2020-07-01: updated to PyBEST standard, including naming convention
# 2022-07-01: introduced `.pc` and `.emb` file extentions (P. Tecmer)

"""Input/output dispatcher for different file formats

   The ``IOData.from_file`` and ``IOData.to_file`` methods read/write data
   from/to a file. The format is deduced from the prefix or extension of the
   filename.
"""

import pathlib

import h5py as h5
import numpy as np

from pybest.exceptions import ArgumentError, MatrixShapeError, UnknownOption


class ArrayTypeCheckDescriptor:
    """
    A class perfoming np.ndarray attribute checks
    """

    def __init__(
        self,
        name,
        ndim=None,
        shape=None,
        dtype=None,
        matching=None,
        default=None,
    ):
        """
        Decorator to perform type checking an np.ndarray attributes

        **Arguments:**

        name
             Name of the attribute (without leading underscores).

        **Optional arguments:**

        ndim
             The number of dimensions of the array.

        shape
             The shape of the array. Use -1 for dimensions where the shape is
             not fixed a priori.

        dtype
             The datatype of the array.

        matching
             A list of names of other attributes that must have consistent
             shapes. This argument requires that the shape is speciefied.
             All dimensions for which the shape tuple equals -1 are must be
             the same in this attribute and the matching attributes.

        default
             The name of another (type-checke) attribute to return as default
             when this attribute is not set
        """
        if matching is not None and shape is None:
            raise ArgumentError(
                "The matching argument requires the shape to be " "specified."
            )
        self._name = name
        self._ndim = ndim
        self._shape = shape
        if dtype is None:
            self._dtype = None
        else:
            self._dtype = np.dtype(dtype)
        self._matching = matching
        self._default = default
        self.__doc__ = "A type-checked attribute"

    def __get__(self, obj, dtype=None):
        if obj is None:
            return self
        if self._default is not None and not hasattr(obj, f"_{self._name}"):
            setattr(
                obj,
                "_" + self._name,
                (getattr(obj, f"_{self._default}").astype(self._dtype)),
            )
        return getattr(obj, f"_{self._name}")

    def __set__(self, obj, value):
        # try casting to proper dtype:
        value = np.array(value, dtype=self._dtype, copy=False)
        # if not isinstance(value, np.ndarray):
        #    raise TypeError('Attribute \'%s\' of \'%s\' must be a numpy '
        #                    'array.' % (self._name, type(obj)))
        if self._ndim is not None and value.ndim != self._ndim:
            raise MatrixShapeError(
                f"Attribute '{self._name}' of '{type(obj)}' must be a numpy"
                f" array with {self._ndim} dimension(s)."
            )
        if self._shape is not None:
            for i, shape in enumerate(self._shape):
                if shape >= 0 and shape != value.shape[i]:
                    raise MatrixShapeError(
                        f"Attribute '{self._name}' of '{type(obj)}' must be a "
                        f"numpy array with {shape} elements in "
                        f"dimension {i}."
                    )
        if self._dtype is not None:
            if not issubclass(value.dtype.type, self._dtype.type):
                raise MatrixShapeError(
                    f"Attribute '{self._name}' of '{type(obj)}' must be a "
                    f"numpy array with dtype '{self._dtype.type}'."
                )
        if self._matching is not None:
            for othername in self._matching:
                other = getattr(obj, f"_{othername}", None)
                if other is not None:
                    for i, shape in enumerate(self._shape):
                        if shape == -1 and other.shape[i] != value.shape[i]:
                            raise MatrixShapeError(
                                f"Shape[{i}] of attribute '{self._name}' of "
                                f"'{type(obj)}' in is incompatible with "
                                f"that of '{othername}'."
                            )
        setattr(obj, f"_{self._name}", value)

    def __delete__(self, obj):
        delattr(obj, f"_{self._name}")


class IOData:
    """A container class for data loaded from (or to be written to) a file.

    In principle, the constructor accepts any keyword argument, which is
    stored as an attribute. All attributes are optional. Attributes can be
    set and removed after the IOData instance is constructed. The following
    attributes are supported by at least one of the io formats:

    **Type checked array attributes (if present):**

    coordinates
         A (N, 3) float array with Cartesian coordinates of the atoms.

    **Unspecified type (duck typing):**

    e_tot
         The total energy (electronic+nn)

    e_hf
         The total Hartree-Fock energy (electronic+nn)

    e_ref
         The energy of the reference determinant (electronic+nn)

    e_corr
         The correlation energy with respect to the reference determinant

    e_method
         The total energy of method (electronic+nn)

    e_core
         The core energy

    e_kin
         The kinetic energy

    e_na
         The nuclear repulsion energy

    e_x
         The exchange energy

    orb_a
         The alpha-spin orbitals (coefficients, occupation numbers, and energies).

    orb_b
         The beta-spin orbitals (coefficients, occupation numbers, and energies).

    mos
         A list (int) of MO indices (used for dumping of cube files)

    t_1
         The singles amplitudes

    t_p
         The pair amplitudes

    t_2
         The doubles amplitudes

    kin
         The kinetic energy integrals

    na
         The nucleus-electron attraction integrals

    pvp
         The pVp integrals

    nuc
         The nuclear-nuclear repulsion integrals

    one
         All one-electron integrals

    eri
         The electron repulsion integrals

    dm_1 (optionally with a suffix that specifies the type)
         The spin-free one-particle reduced density matrix

    dm_2 (optionally with a suffix that specifies the type)
         The spin-free two-particle reduced density matrix

    lf
         A LinalgFactory instance

    ms2
         The spin multiplicity

    mulliken_charges
         Mulliken AIM charges

    nelec
         The number of electrons

    niter_wfn
         The number of iterations for convergence of wfn

    niter_orb
         The number of iterations for convergence of orbitals

    gobasis
         An instance of the PyBasis class

    olp
         The overlap integrals

    one_mo
         All one-electron integrals in the molecular-orbital basis

    permutation
         The permutation applied to the basis functions

    signs
         The sign changes applied to the basis functions

    title
         A suitable name for the data

    two_mo
         Two-electron integrals in the molecular-orbital basis
    """

    def __init__(self, **kwargs):
        for key, value in kwargs.items():
            setattr(self, key, value)

    # only perform type checking on minimal attributes
    atom = ArrayTypeCheckDescriptor("atom", 1, (-1,), str, ["coordinates"])
    coordinates = ArrayTypeCheckDescriptor(
        "coordinates", 2, (-1, 3), float, ["atom"]
    )

    @property
    def natom(self):
        """The number of atoms"""
        if hasattr(self, "atom"):
            return len(self.atom)
        if hasattr(self, "coordinates"):
            return len(self.coordinates)
        return 0

    @classmethod
    def from_file(cls, *filenames, **kwargs):
        """Load data from a file.

        **Arguments:**

        filename1, filename2, ...
             The files to load data from. When multiple files are given, data
             from the first file is overwritten by data from the second, etc.
             When one file contains sign and permutation changes for the
             orbital basis, these changes will be applied to data from all
             other files.

        **Optional arguments:**

        lf
             A LinalgFactory instance. DenseLinalgFactory is used as default.

        This routine uses the extension or prefix of the filename to
        determine the file format. It returns a dictionary with data loaded
        from the file.

        For each file format, a specialized function is called that returns a
        dictionary with data from the file.
        """
        result = {}

        lf = kwargs.pop("lf", None)
        if lf is None:
            from pybest.linalg import DenseLinalgFactory

            lf = DenseLinalgFactory()
        if len(kwargs) > 0:
            raise UnknownOption(f"Keyword argument(s) not supported: {kwargs}")

        for filename in filenames:
            # cast pathlib.Paths back to str for compatibility
            if isinstance(filename, str):
                filename = pathlib.Path(filename)
            elif not isinstance(filename, pathlib.Path):
                raise TypeError(
                    f"Do not know how to handle type {type(filename)}"
                )

            if isinstance(filename, h5.Group) or filename.suffix == ".h5":
                from pybest.io.internal import load_h5

                result.update(load_h5(filename))
            elif filename.suffix == ".xyz":
                from pybest.io.xyz import load_xyz

                result.update(load_xyz(filename))
            elif filename.suffix == ".pc":
                from pybest.io.external_charges import load_charges

                result.update(load_charges(filename))
            elif filename.suffix == ".emb":
                from pybest.io.embedding import load_embedding

                result.update(load_embedding(filename))
            elif filename.suffix == ".mkl":
                from pybest.io.molekel import load_mkl

                result.update(load_mkl(filename, lf))
            elif ".molden" in filename.suffixes:
                from pybest.io.molden import load_molden

                result.update(load_molden(filename))
            elif "FCIDUMP" in pathlib.PurePath(filename).name:
                from pybest.io.molpro import load_fcidump

                result.update(load_fcidump(filename, lf))
            else:
                raise UnknownOption(
                    f"Unknown file format for reading: {filename}"
                )

        # Apply changes in orbital order and sign conventions
        if "permutation" in result:
            for value in result.values():
                from pybest.linalg.base import LinalgObject

                if isinstance(value, LinalgObject):
                    value.permute_basis(result["permutation"])
            del result["permutation"]
        if "signs" in result:
            for value in result.values():
                from pybest.linalg.base import LinalgObject

                if isinstance(value, LinalgObject):
                    value.change_basis_signs(result["signs"])
            del result["signs"]

        return cls(**result)

    @classmethod
    def from_str(cls, geo_str):
        """A plain xyz reader

        **Arguments:**

        geo_str
            A string with the xyz geometry data
        """
        from pybest.io.xyz import load_xyz_plain

        results = load_xyz_plain(geo_str)
        return cls(**results)

    def to_file(self, filename):
        """Write data to a file

        **Arguments:**

        filename
             The file to write the data to

        This routine uses the extension or prefix of the filename to determine
        the file format. For each file format, a specialized function is
        called that does the real work.
        """
        if isinstance(filename, str):
            filename = pathlib.Path(filename)
        elif not isinstance(filename, pathlib.Path):
            raise TypeError(f"Do not know how to handle type {type(filename)}")

        if isinstance(filename, h5.Group) or filename.suffix == ".h5":
            data = vars(self).copy()
            # get rid of leading underscores
            for key in data.keys():
                if key[0] == "_":
                    data[key[1:]] = data[key]
                    del data[key]
            from pybest.io.internal import dump_h5

            dump_h5(filename, data)
        elif filename.suffix == ".xyz":
            from pybest.io.xyz import dump_xyz

            dump_xyz(filename, self)
        elif ".molden" in filename.suffixes:
            from pybest.io.molden import dump_molden

            dump_molden(str(filename.resolve()), self)
        elif "FCIDUMP" in pathlib.PurePath(filename).name:
            from pybest.io.molpro import dump_fcidump

            dump_fcidump(filename, self)
        elif ".cube" in filename.suffixes:
            from pybest.io.cube import dump_cube

            dump_cube(filename, self)
        else:
            raise UnknownOption(f"Unknown file format for writing: {filename}")

    def copy(self):
        """Return a shallow copy"""
        kwargs = vars(self).copy()
        # get rid of leading underscores
        for key in kwargs.keys():
            if key[0] == "_":
                kwargs[key[1:]] = kwargs[key]
                del kwargs[key]
        return self.__class__(**kwargs)

    @classmethod
    def prepare_ghosts(cls, *filenames):
        """Returns dummy atoms list for each of the monomers (A or B).
        Expects the following files:
            mon_a.xyz
            mon_b.xyz
            dimer.xyz
        Where the following naming convention is assumed:
        mon_a: <dimer_name>a.xyz
        mon_b: <dimer_name>b.xyz

        Arguments:
            filenames {[str or pathlib.Path]} -- geometry files

        Returns:
            [type] -- [description]
        """
        #
        # ANCIENT VODO-MAGIC BEWARE
        #
        unique_ghost_elements = []
        element_maps = []

        # creates element maps for monA,monB and whole complex
        for filename in filenames:
            # AB dimer goes last
            temporary_map = []
            with open(filename, "r", encoding="utf-8") as input_geometry:
                for _ in range(2):  # skipping first two lines of .xyz
                    next(input_geometry)
                for row in input_geometry:
                    if len(row.split()) > 3:
                        temporary_map.append(row.split()[0])
            element_maps.append(temporary_map)

        # list outs all ghost elements defined
        for map_index in range(len(element_maps))[:-1]:
            for element_index in range(len(element_maps[-1])):
                if (
                    element_maps[map_index][element_index]
                    != element_maps[-1][element_index]
                ):
                    # gets all diffrences from AB complex
                    unique_ghost_elements.append(
                        element_maps[-1][element_index]
                    )

        # gets uniques
        unique_ghost_elements = list(set(unique_ghost_elements))

        # sets map for new ghost names
        # like X0, X1 etc. for all unique ghost atoms
        new_names_map = [
            "X" + str(i) for i in range(len(unique_ghost_elements))
        ]

        # updates ghost names; element_maps[-1] list of DIMER atom names (no ghosts)
        for index_outer, element_map in enumerate(element_maps[:-1]):
            # element_map - list of atoms names in monA and monB
            for index_inner, element in enumerate(element_map):
                # if atom name in monA is not the same as correspoding in DIMER,
                if element != element_maps[-1][index_inner]:
                    element_maps[index_outer][index_inner] = new_names_map[
                        unique_ghost_elements.index(
                            element_maps[-1][index_inner]
                        )
                    ]

        ghost_mon_a = [
            idx
            for idx, name in enumerate(element_maps[0])
            if name in new_names_map
        ]
        ghost_mon_b = [
            idx
            for idx, name in enumerate(element_maps[1])
            if name in new_names_map
        ]
        return ghost_mon_a, ghost_mon_b
