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
#
# This file has been rewritten by Maximilian Kriebel.
#
# Detailed changes (see also CHANGELOG):
# 2020-07-01: Update to PyBEST standard, including naming convention
# 2020-07-01: Introduce general tensor contraction engine used for all NIndex objects
# 2022-09/10: dense.py split into files for each class in subfolder dense
# 2022-09/10: [slice] and [tco] replaced with [contract]

"""Base classes"""


import abc
import uuid

import numpy as np

from pybest import filemanager
from pybest.exceptions import ArgumentError, UnknownOption
from pybest.linalg.contract import (
    cholesky_td_routine,
    get_outshape,
    parse_contract_input,
    parse_subscripts,
    slice_output,
    td_helper,
)
from pybest.linalg.gpu_contract import (
    PYBEST_CUPY_AVAIL,
    cupy_helper,
    cupy_optimized,
)
from pybest.log import log
from pybest.utils import check_type

try:
    from opt_einsum import contract as oe_contract
except ImportError:
    log.warn("The opt_einsum module has not been detected.")
    oe_contract = np.einsum


class LinalgFactory(abc.ABC):
    """A collection of compatible matrix and linear algebra routines.

    This is just an abstract base class that serves as a template for
    specific implementations.
    """

    def __init__(self, default_nbasis=None):
        """
        **Optional arguments:**

        default_nbasis
             The default basis size when constructing new
             operators/expansions.
        """
        self.default_nbasis = default_nbasis

    @classmethod
    def from_hdf5(cls, grp):
        """Construct an instance from data previously stored in an h5py.Group.

        **Arguments:**

        grp
             An h5py.Group object.
        """
        default_nbasis = grp.attrs.get("default_nbasis")
        return cls(default_nbasis)

    def to_hdf5(self, grp):
        """Write a LinalgFactory to an HDF5 group

        **Argument:**

        grp
             A h5py.Group instance to write to.
        """
        grp.attrs["class"] = self.__class__.__name__
        if self.default_nbasis is not None:
            grp.attrs["default_nbasis"] = self.default_nbasis

    @property
    def default_nbasis(self):
        """The default number of basis functions"""
        return self._default_nbasis

    @default_nbasis.setter
    def default_nbasis(self, nbasis):
        """Set default number of basis functions"""
        self._default_nbasis = nbasis

    @abc.abstractmethod
    def create_one_index(self, nbasis=None, label=""):
        """Create a new instance of OneIndex"""

    @abc.abstractmethod
    def create_orbital(self, nbasis=None, nfn=None):
        """Create a new instance of Orbital

        **Arguments:**

        nbasis
            (int) The number of basis functions.

        nfn
            (int) The number of (molecular) orbitals.
        """

    @abc.abstractmethod
    def create_two_index(self, nbasis=None, nbasis1=None, label=""):
        """Create a new instance of TwoIndex"""

    @abc.abstractmethod
    def create_three_index(
        self, nbasis=None, nbasis1=None, nbasis2=None, label=""
    ):
        """Create a new instance of ThreeIndex"""

    @abc.abstractmethod
    def create_four_index(
        self, nbasis=None, nbasis1=None, nbasis2=None, nbasis3=None, label=""
    ):
        """Create a new instance of FourIndex"""


class LinalgObject(abc.ABC):
    """A base class for NIndex objects."""

    @property
    @abc.abstractmethod
    def array(self):
        """Linalg objects store all data in array"""

    @property
    @abc.abstractmethod
    def array2(self):
        """Cholesky Linalg objects store all data in array and array2"""

    @property
    @abc.abstractmethod
    def arrays(self):
        """List of all linalg array objects"""

    @property
    @abc.abstractmethod
    def label(self):
        """The label of a linalg object"""

    @abc.abstractmethod
    def __eq__(self, other):
        """Check if two objects are equal"""

    @abc.abstractmethod
    def __del__(self):
        """Explicitly delete all arrays"""

    @classmethod
    @abc.abstractmethod
    def from_hdf5(cls, grp):
        """Read from h5 file."""

    @abc.abstractmethod
    def to_hdf5(self, grp):
        """Write to h5 file."""

    @abc.abstractmethod
    def new(self):
        """Return a new NIndex object with the same nbasis"""

    def __clear__(self):
        """Part of the API specified in pybest.cache"""
        self.clear()

    @abc.abstractmethod
    def clear(self):
        """Reset all elements to zero."""

    @abc.abstractmethod
    def replace_array(self, value):
        """Replace array elements. No copy is generated, only a new reference."""


class Orbital(LinalgObject):
    """Base class for Orbital objects."""

    @property
    def array(self):
        """Linalg objects store all data in array. Will be overwritten by
        DenseNIndex objects.
        Those are not needed for Orbital class. The current class structure
        requires them to be defined.
        """

    @property
    def array2(self):
        """Cholesky Linalg objects store all data in array and array2. Will be
        overwritten by CholeskyFourIndex.
        Those are not needed for Orbital class. The current class structure
        requires them to be defined.
        """

    @property
    def arrays(self):
        """List of all linalg array objects. Will be overwritten by Dense and
        CholeskyIndex objects.
        Those are not needed for Orbital class. The current class structure
        requires them to be defined.
        """

    @property
    def label(self):
        """The label of a linalg/orbital object. It is not needed for the
        Orbital class. However, the current class structure requires it to be
        defined.
        """

    @abc.abstractmethod
    def check_normalization(self, overlap, eps=1e-4):
        """Check normalization of orbitals."""

    @abc.abstractmethod
    def error_eigen(self, fock, overlap):
        """Compute the error of the orbitals with respect to the eigenproblem"""


class NIndexObject(LinalgObject):
    """A base class for NIndex objects."""

    @property
    def array(self):
        """Linalg objects store all data in array. Will be overwritten by
        DenseNIndex objects."""

    @property
    def array2(self):
        """Cholesky Linalg objects store all data in array and array2. Will be
        overwritten by CholeskyFourIndex."""

    @property
    def arrays(self):
        """List of all linalg array objects. Will be overwritten by Dense and
        CholeskyIndex objects."""

    @property
    def label(self):
        """The label of a linalg object"""

    @abc.abstractmethod
    def iscale(self, factor):
        """In-place multiplication with a scalar."""

    @property
    @abc.abstractmethod
    def shape(self):
        """Return shape of array."""

    @property
    def ndim(self):
        """The number of axes in the N-index object."""
        return len(self.shape)

    def fix_ends(self, *ends):
        """Return the last index of each dimension of array."""
        shape = self.shape
        if len(shape) != len(ends):
            raise ArgumentError(
                "The argument 'ends' must have the same length as 'self.shape'."
            )
        return tuple(ends[i] or shape[i] for i in range(len(shape)))

    def dump_array(self, label, filename=None):
        """Dump some NIndexObject to disk and delete all array instances.
        NIndexObject will be dump to ``temp_dir`` specified in ``filemanager``
        (globally defined)

        **Arguments:**

        label
            (str) The label used to store the attribute in the IOData container

        **Optional Arguments:**

        filename
            (str) The filename of the checkpoint file. Has to end with ``.h5``
        """
        # import outside toplevel to prevent circular import
        from pybest.io.iodata import IOData

        # Generate some unique internal label if not present or empty
        if not self.label:
            self.label = str(uuid.uuid4())
        # Use the pybest.io interface to write the checkpoint file
        filename = filename or f"checkpoint_{self.label}.h5"
        # Use the pybest.io interface to write the checkpoint file
        if not label:
            raise ArgumentError(f"Improper label chosen: {label}.")
        data = IOData(**{f"{label}": self})
        # Some tmp dir
        filename = filemanager.temp_path(f"{filename}")
        data.to_file(filename)
        # Delete array explicitly
        self.__del__()

    def load_array(self, label, filename=None):
        """Read some NIndexObject from disk and replace all array instances.
        NIndexObject will be read from ``temp_dir`` specified in ``filemanager``
        (globally defined)

        **Arguments:**

        label
            (str) The label used to store the attribute in the IOData container

        **Optional Arguments:**

        filename
            (str) The filename of the checkpoint file. Has to end with ``.h5``
        """
        # import outside toplevel to prevent circular import
        from pybest.io.iodata import IOData

        # Use the pybest.io interface to read the checkpoint file
        filename = filename or f"checkpoint_{self.label}.h5"
        # Some tmp dir
        filename = filemanager.temp_path(filename)
        # check if file exists
        if not filename.exists():
            raise FileNotFoundError(
                f"Cannot find checkpoint file while loading array from {filename}"
            )
        # get data stored using IOData attribute `label`
        data = IOData.from_file(filename)
        if not hasattr(data, label):
            raise ArgumentError(f"Cannot find label {label}")
        data = getattr(data, label)
        self.replace_array(data)

    def contract(self, *args, **kwargs):
        """General NIndex contraction function

            NIndex = CholeskyFourIndex or DenseNIndex
            where N = One, Two, Three, Four

        *** Arguments ***

        * self : NIndex
              This is the first operand.

        * subscript : string
              Specifies the subscripts for summation as comma separated list
              of subscript labels, for example: 'abcd,efcd->abfe'.

        * operands : DenseNIndex
              These are the other arrays for the operation. If out keyword is
              not specified and the result of operation is not scalar value,
              the last operand is treated as out.

        *** Keyword arguments ***

        * out : DenseNIndex
              The product of operation is added to out.

        * factor : float
              The product of operation is multiplied by factor before it is
              added to out.

        * clear : boolean
               The out is cleared before the product of operation is added to
               out if clear is set to True.

        * select : string
               Specifies the contraction algorithm: One of:
               - 'opt_einsum' - opt_einsum.contract
               - 'einsum' - numpy.einsum function,
               - 'td' - operations with utilization of numpy.tensordot function,
               - 'cupy' - operations using the cupy library,
               - None - first tries 'cupy' (very fast but
                 only supported for a set of contractions), then 'td' routine.
                 In case of failure, it performs the 'einsum' operation.
               'td' is usually much faster, but it can result in increased
               memory usage and it is available only for specific cases.

        * optimize : {False, True, 'optimal'}
               Specifies contraction path for operation if select is set to
               'einsum'. For details, see numpy.einsum_path.

        * begin0, end0, begin1, ... :
               The lower and upper bounds for summation.
        """
        subscripts = args[0]
        factor = kwargs.get("factor", 1.0)
        select = kwargs.get("select", None)
        clear = kwargs.get("clear", False)
        opt = kwargs.get("optimize", "optimal")
        out = kwargs.get("out", None)
        save_memory = kwargs.get("save_memory", False)

        # Check if out is scalar
        scripts, outscript = parse_subscripts(subscripts)
        is_out_scalar = outscript in ("", "...")

        # If keyword out is None, use last argument as out. Determine operands.
        if (len(args) == len(scripts) + 1) and (out is None):
            operands = [self] + list(args[1:-1])
            out = args[-1]
            arr = out.array
        else:
            operands = [self] + list(args[1:])

        # Slice arrays of operands and create a list with operands (ndarrays)
        subs_, operands_ = parse_contract_input(subscripts, operands, kwargs)
        args_ = [subs_] + operands_

        # Create output array if not given
        if (not is_out_scalar) and (out is None):
            from pybest.linalg import DenseLinalgFactory

            shape = get_outshape(subs_, operands_)
            out = DenseLinalgFactory.allocate_check_output(None, shape)

        # Clear out is required and reference to its _array attribute.
        if out is not None:
            if clear:
                out.clear()
            arr = out.array

        # 1. The product of operation is a scalar.
        if is_out_scalar:
            if out is not None:
                raise ArgumentError(
                    "Output operand should not be specified if the contraction"
                    " result is scalar."
                )
            if select == "td":
                return factor * td_helper(*args_)
            if select == "opt_einsum":
                return factor * oe_contract(*args_, optimize=opt)
            if select == "einsum":
                return factor * np.einsum(*args_, optimize=opt)
            if select == "cupy":
                if PYBEST_CUPY_AVAIL:
                    try:
                        return factor * cupy_helper(*args_, **kwargs)
                    except MemoryError:
                        return factor * td_helper(*args_)
                else:
                    select = None
            if select is None:
                try:
                    x = factor * td_helper(*args_)
                except ArgumentError:
                    x = factor * np.einsum(*args_, optimize=opt)
                return x
            raise UnknownOption(
                f"Unrecognized keyword: select = {select}.\n"
                "Do you mean one of: 'cupy', 'td', 'opt_einsum' or 'einsum'?\n"
            )

        # 2. The product of operation is DenseNIndexObject.
        slice_ = slice_output(subscripts, kwargs)

        if select == "td" and len(self.arrays) == 2:
            try:
                args_td = [subscripts, operands_, arr, factor, save_memory]
                cholesky_td_routine(*args_td)
            except (NotImplementedError, ValueError):
                try:
                    arr[:] += factor * td_helper(*args_)
                except ArgumentError:
                    raise ArgumentError(
                        f"{subscripts} cannot be done with select='td'."
                    ) from None

        elif select == "td":
            arr[slice_] += factor * td_helper(*args_)

        elif select == "opt_einsum":
            arr[slice_] += factor * oe_contract(*args_, optimize=opt)

        elif select == "einsum":
            arr[slice_] += factor * np.einsum(*args_, optimize=opt)

        elif select == "cupy":
            if PYBEST_CUPY_AVAIL:
                try:
                    args_cupy = args_ + [arr]
                    arr[slice_] += factor * cupy_helper(*args_cupy, **kwargs)
                except MemoryError:
                    if log.do_high:
                        log.warn("Not enough Video memory.")
                        log.warn("Defaulting to numpy.tensordot.")
                    try:
                        if len(self.arrays) == 2:
                            try:
                                args_td = [
                                    subscripts,
                                    operands_,
                                    arr,
                                    factor,
                                    save_memory,
                                ]
                                cholesky_td_routine(*args_td)
                            except NotImplementedError:
                                arr[slice_] += factor * td_helper(*args_)
                        else:
                            arr[slice_] += factor * td_helper(*args_)
                    except ArgumentError:
                        arr[slice_] += factor * np.einsum(*args_, optimize=opt)
            else:
                arr[slice_] += factor * td_helper(*args_)

        elif select is None:
            if args_[0] in cupy_optimized and PYBEST_CUPY_AVAIL:
                args_ = args_ + [arr]
                arr[slice_] += factor * cupy_helper(*args_, **kwargs)
            else:
                try:
                    if len(self.arrays) == 2:
                        try:
                            args_td = [
                                subscripts,
                                operands_,
                                arr,
                                factor,
                                save_memory,
                            ]
                            cholesky_td_routine(*args_td)
                        except NotImplementedError:
                            arr[slice_] += factor * td_helper(*args_)
                    else:
                        arr[slice_] += factor * td_helper(*args_)
                except ArgumentError:
                    arr[slice_] += factor * oe_contract(*args_, optimize=opt)

        else:
            raise UnknownOption(
                f"Unrecognized keyword: select = {select}.\n"
                "Do you mean one of: 'cupy', 'td', 'opt_einsum' or 'einsum'?\n"
            )

        return out

    def get_max_values(self, limit=20, absolute=True):
        """Returns list of tuples with maximal values and their indices."""

        values = list(
            (index, val) for index, val in np.ndenumerate(self.array)
        )
        sortkey = {True: lambda x: abs(x[1]), False: lambda x: x[1]}
        values.sort(key=sortkey[absolute], reverse=True)

        if len(values) > limit:
            values = values[:limit]

        return values


class OneIndex(NIndexObject):
    """Base class for OneIndex objects."""

    @abc.abstractmethod
    def copy(self):
        """Create a copy of TwoIndex object."""

    @abc.abstractmethod
    def get_element(self, i):
        """Return element i of array"""

    @abc.abstractmethod
    def set_element(self, i, value):
        """Set element i of array"""


class TwoIndex(NIndexObject):
    """Base class for TwoIndex objects."""

    @abc.abstractmethod
    def copy(self):
        """Create a copy of TwoIndex object."""

    @abc.abstractmethod
    def get_element(self, i, j):
        """Return element i,j of array."""

    @abc.abstractmethod
    def set_element(self, i, j, value, symmetry=2):
        """Set element i,j of array."""


class ThreeIndex(NIndexObject):
    """Base class for ThreeIndex objects."""

    @abc.abstractmethod
    def copy(self):
        """Create a copy of TwoIndex object."""

    @abc.abstractmethod
    def get_element(self, i, j, k):
        """Return element i,j,k of array."""

    @abc.abstractmethod
    def set_element(self, i, j, k, value):
        """Set element i,j,k of array."""


class FourIndex(NIndexObject):
    """Base class for FourIndex objects."""

    @abc.abstractmethod
    def copy(
        self,
        begin0=0,
        end0=None,
        begin1=0,
        end1=None,
        begin2=0,
        end2=None,
        begin3=0,
        end3=None,
    ):
        """Create a copy of FourIndex object."""

    @abc.abstractmethod
    def get_element(self, i, j, k, l):
        """Return element i,j,k,l of array."""

    @abc.abstractmethod
    def set_element(self, i, j, k, l, value, symmetry=8):
        """Set element i,j,k,l of array."""


def parse_four_index_transform_exps(exp0, exp1, exp2, exp3, Class):
    """Parse the optional arguments exp1, exp2 and exp3.

    **Arguments:**

    exp0, exp1, exp2, exp3
         Four sets of orbitals for the mo transformation. Some may be None
         but only the following not None combinations are allowed:

         * ``(exp0,)``: maintain eight-fold symmetry (if any)
         * ``(exp0, exp1)``: maintain four-fold symmetry (if any)
         * ``(exp0, exp2)``: maintain two-fold symmetry (if any)
         * ``(exp0, exp1, exp2, exp3)``: break all symmetry

    Class
         The expected class of the exps objects.


    **Returns:** exp0, exp1, exp2, exp3. (All not None)
    """
    # Four supported situations
    if exp1 is None and exp2 is None and exp3 is None:
        # maintains eight-fold symmetry
        exp1 = exp0
        exp2 = exp0
        exp3 = exp0
    elif exp2 is None and exp3 is None:
        # maintains four-fold symmetry
        exp2 = exp0
        exp3 = exp1
    elif exp1 is None and exp3 is None:
        # maintains two-fold symmetry
        exp1 = exp0
        exp3 = exp2
    elif exp1 is None or exp2 is None or exp3 is None:
        # the only other allowed case is no symmetry.
        raise ArgumentError(
            "It is not clear how to interpret the optional arguments exp1, exp2 and exp3."
        )
    check_type("exp0", exp0, Class)
    check_type("exp1", exp1, Class)
    check_type("exp2", exp2, Class)
    check_type("exp3", exp3, Class)
    return exp0, exp1, exp2, exp3
