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
# Some functions have been taken from `Horton 2.0.0`.
# However, this file has been updated and debugged. Compatibility with Horton is NOT
# guaranteed.
# Its current version contains updates from the PyBEST developer team.
#
# Detailed changes (see also CHANGELOG):
# 2020-07-01: update to new python features, including f-strings, exception class
# 2020-07-01: new functions: check_gobasis, get_com, unmask_orb, unmask

"""Utility functions"""

from collections import Counter
from contextlib import contextmanager

import numpy as np

from pybest.exceptions import ArgumentError, GOBasisError
from pybest.periodic import periodic

__all__ = [
    "check_gobasis",
    "check_type",
    "check_options",
    "check_lf",
    "doc_inherit",
    "fda_1order",
    "fda_2order",
    "get_com",
    "unmask_orb",
    "unmask",
    "numpy_seed",
]


def check_gobasis(gobasis=None):
    """Check a GO Basis specification

    **Arguments:**

    gobasis
         A PyBasis instance.

    **Optional arguments:**

    **Returns:**
    """
    #
    # Determine PyBasis:
    #
    if gobasis is not None:
        atom = np.array(gobasis.atom)
        natom = len(atom)
        shell = gobasis.shell2atom
        coord = np.array(gobasis.coordinates)
    else:
        raise GOBasisError("No PyBasis instance given.")

    #
    # Check coordinates:
    #
    if coord.shape != (natom, 3):
        raise GOBasisError("Coordinates corrupted.")
    if not issubclass(coord.dtype.type, np.floating):
        raise GOBasisError("Coordinates have wrong type.")

    #
    # Check atoms:
    #
    if not issubclass(atom.dtype.type, np.integer):
        raise GOBasisError("Atoms have wrong type.")

    #
    # Check basis set:
    #

    if len(Counter(shell).keys()) != natom:
        raise GOBasisError(
            "Basis set incomplete. Pleases check if basis set file is correct."
        )
    if gobasis.ncenter != natom:
        raise GOBasisError(
            "Number of atom centers. Does not agree with number of atoms"
        )
    if len(gobasis.alpha) != len(gobasis.contraction):
        raise GOBasisError(
            "Number of contractions and exponents does not agree."
        )
    if sum(gobasis.nprim) != len(gobasis.contraction):
        raise GOBasisError(
            "Number of contractions does not agree with number of primitives."
        )


def check_type(name, instance, *Classes):
    """Check type of argument with given name against list of types

    **Arguments:**

    name
         The name of the argument being checked.

    instance
         The object being checked.

    Classes
         A list of allowed types.
    """
    if len(Classes) == 0:
        raise TypeError(
            "Type checking with an empty list of classes. This is a simple bug!"
        )
    match = False
    for Class in Classes:
        if isinstance(instance, Class):
            match = True
            break
    if not match:
        classes_parts = ["'", Classes[0].__name__, "'"]
        for Class in Classes[1:-1]:
            classes_parts.extend([", ``", Class.__name__, "'"])
        if len(Classes) > 1:
            classes_parts.extend([" or '", Classes[-1].__name__, "'"])
        raise TypeError(
            f"The argument '{name}' must be an instance of {''.join(classes_parts)}. "
            f"Got a '{instance.__class__.__name__}' instance instead."
        )


def check_options(name, select, *options):
    """Check if a select is in the list of options. If not raise ValueError

    **Arguments:**

    name
         The name of the argument.

    select
         The value of the argument.

    options
         A list of allowed options.
    """
    if select not in options:
        formatted = ", ".join([f"'{option}'" for option in options])
        raise ValueError(f"The argument '{name}' must be one of: {formatted}")


def check_lf(lf, operand):
    """Check if operand and lf belong to the same factory.
    Only 4-index quantities are supported.
    All lower-dimensional quantities are always Dense and
    work with both factories.

    **Arguments:**

    lf
         An instance of LinalgFactory.

    operand
         The operand to be checked.

    """
    from pybest.linalg import DenseFourIndex, DenseLinalgFactory
    from pybest.linalg.cholesky import CholeskyFourIndex, CholeskyLinalgFactory

    check_type(lf, lf, CholeskyLinalgFactory, DenseLinalgFactory)
    check_type(operand, operand, CholeskyFourIndex, DenseFourIndex)

    # Note: CholeskyLinalgFactory inherits from DenseLinalgFactory. Checking for
    # DenseLinalgFactory will allways be True
    if isinstance(lf, CholeskyLinalgFactory) != isinstance(
        operand, CholeskyFourIndex
    ):
        raise ArgumentError(
            f"LinalgFactory {type(lf)} and operand {type(operand)} are of different type."
        )


def doc_inherit(base_class):
    """Docstring inheriting method descriptor

    doc_inherit decorator

    Usage:

    .. code-block:: python

         class Foo(object):
             def foo(self):
                 "Frobber"
                 pass

         class Bar(Foo):
             @doc_inherit(Foo)
             def foo(self):
                 pass

    Now, ``Bar.foo.__doc__ == Bar().foo.__doc__ == Foo.foo.__doc__ ==
    "Frobber"``
    """

    def decorator(method):
        overridden = getattr(base_class, method.__name__, None)
        if overridden is None:
            raise NameError(f"Can't find method '{overridden}' in base class.")
        method.__doc__ = overridden.__doc__
        return method

    return decorator


def get_com(mol):
    """Calculate Center of Mass with respect to atomic numbers

    mol
        An IOData istance containing information about the molecule OR
        a PyBasis instance
    """
    summass = 0.0
    com = np.zeros((3), float)
    # Only need this for IOData container
    numbers = np.array([periodic[i].number for i in mol.atom])
    for key, i in zip(numbers, range(len(numbers))):
        mass = periodic[key].number
        summass += mass
        # Convert to np array in case of list
        com += mass * np.array(mol.coordinates[i])
    com /= summass
    return com


def unmask_orb(*args, **kwargs):
    """Check arguments and return orbitals as a list [alpha,beta].
    If not present, empty list is returned.
    If orbitals are contained in several arguments, the orbitals
    are returned in the following order: kwargs > args > IOData.
    """
    from pybest.io.iodata import IOData
    from pybest.linalg.base import Orbital

    orb = []
    #
    # first kwargs
    #
    orb_a = kwargs.get("orb_a", None)
    orb_b = kwargs.get("orb_b", None)
    if orb_a:
        orb.insert(0, orb_a)
    if orb_b:
        orb.append(orb_b)
    #
    # args > IOData
    #
    if not orb:
        orb_data = []
        orb_args = []
        for arg in args:
            if isinstance(arg, Orbital):
                orb_args.append(arg)
            elif isinstance(arg, IOData):
                if hasattr(arg, "orb_a"):
                    orb_data.insert(0, arg.orb_a)
                if hasattr(arg, "orb_b"):
                    orb_data.append(arg.orb_b)
            else:
                continue
        #
        # decide on orbs according to args > IOData.
        # Both alpha and beta orbitals are passed in args or IOData.
        # Mixing is not allowed!
        #
        if orb_args:
            return orb_args
        elif orb_data:
            return orb_data
    return orb


def unmask(label, *args, **kwargs):
    """Check arguments and return some arbitrary data with the label 'label'.
    If not present, None is returned.
    If data with given label is contained in several arguments, it is
    returned in the following order: kwargs > args > IOData.
    """
    from pybest.io.iodata import IOData

    data = kwargs.get(label, None)
    if data is None:
        for arg in args:
            if not isinstance(arg, IOData) and hasattr(arg, "label"):
                if arg.label == label:
                    return arg
            if isinstance(arg, IOData) and hasattr(arg, label):
                data = getattr(arg, label)
    return data


def fda_1order(fun, fun_deriv, x, dxs, threshold=1e-5):
    """Check the analytical gradient of `fun_deriv` using finite differece approximation

    Arguments:

    fun
         The function whose derivatives must be to be tested

    fun_deriv
         The implementation of the analytical derivatives

    x
         The argument for the reference point.

    dxs
         A list with small relative changes to x

    threshold
         The threshold

    For every displacement in ``dxs``, the following computation is repeated:

    1) D1 = 'fun(x+dx) - fun(x)' is computed.
    2) D2 = '0.5 (fun_deriv(x+dx) + fun_deriv(x)) . dx' is computed.

    For each case, |D1 - D2| should be smaller than the threshold.
    """

    dn1s = []
    dn2s = []
    dnds = []
    f0 = fun(x)
    grad0 = fun_deriv(x)
    for dx in dxs:
        f1 = fun(x + dx)
        grad1 = fun_deriv(x + dx)
        grad = 0.5 * (grad0 + grad1)
        d1 = f1 - f0
        if hasattr(d1, "__iter__"):
            norm = np.linalg.norm
        else:
            norm = abs
        d2 = np.dot(grad, dx)

        dn1s.append(norm(d1))
        dn2s.append(norm(d2))
        dnds.append(norm(d1 - d2))
    dn1s = np.array(dn1s)
    dn2s = np.array(dn2s)
    dnds = np.array(dnds)

    mask = dnds > threshold
    if (mask).all():
        raise AssertionError(
            f"The first order approximation for the difference is too wrong. "
            f"The allowed threshold is {threshold}.\n"
            f"First order approximation to differences:\n {*dn1s[mask],}\n"
            f"Analytic derivative:\n {*dn2s[mask],}\n"
            f"Absolute errors:\n {*dnds[mask],}"
        )


def fda_2order(fun, fun_deriv, x, dxs, threshold=1e-5):
    """Check the analytical hessian of `fun_deriv` using finite differece approximation

    Arguments:

    fun
         The function whose derivatives must be to be tested

    fun_deriv
         The implementation of the analytical derivatives

    x
         The argument for the reference point.

    dxs
         A list with small relative changes to x

    threshold
         The threshold

    For every displacement in ``dxs``, the following computation is repeated:

    1) D1 = 'fun(x+dx) - 2 fun(x) + fun(x-dx)' is computed.
    2) D2 = '0.25 dx . (fun_deriv(x+dx) + 2 fun_deriv(x) + fun_deriv(x-dz)) . dx' is
       computed.

    For each case, |D1 - D2|, should be smaller than the threshold.
    """
    dn1s = []
    dn2s = []
    dnds = []
    f0 = fun(x)
    grad0 = fun_deriv(x)
    for dx in dxs:
        f1 = fun(x + dx)
        f2 = fun(x - dx)
        grad1 = fun_deriv(x + dx)
        grad2 = fun_deriv(x - dx)
        grad = (grad1 + 2.0 * grad0 + grad2) * 0.25
        d1 = f1 - 2.0 * f0 + f2
        if hasattr(d1, "__iter__"):
            norm = np.linalg.norm
        else:
            norm = abs
        d2_ = np.dot(grad, dx)
        d2 = np.dot(dx, d2_)

        dn1s.append(norm(d1))
        dn2s.append(norm(d2))
        dnds.append(norm(d1 - d2))
    dn1s = np.array(dn1s)
    dn2s = np.array(dn2s)
    dnds = np.array(dnds)

    mask = dnds > threshold
    if (mask).all():
        raise AssertionError(
            f"The first order approximation for the difference is too wrong. "
            f"The allowed threshold is {threshold}.\n"
            f"First order approximation to differences:\n {*dn1s[mask],}\n"
            f"Analytic derivative:\n {*dn2s[mask],}\n"
            f"Absolute errors:\n {*dnds[mask],}"
        )


@contextmanager
def numpy_seed(seed=1):
    """Temporarily set NumPy's random seed to a given number.

    Parameters
    ----------
    seed : int
           The seed for NumPy's random number generator.
    """
    state = np.random.get_state()
    np.random.seed(seed)
    yield None
    np.random.set_state(state)
