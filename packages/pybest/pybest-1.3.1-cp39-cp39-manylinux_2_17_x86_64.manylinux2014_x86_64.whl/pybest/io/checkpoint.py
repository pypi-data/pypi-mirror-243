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
"""Avoid recomputation of earlier results and reallocation of existing arrays

   In principle, the ``JustOnceClass`` and the ``Cache`` can be used
   independently, but in some cases it makes a lot of sense to combine them.
   See for example the density partitioning code in ``pybest.part``.
"""

from collections import UserDict

from pybest import filemanager
from pybest.exceptions import ArgumentError
from pybest.io.iodata import IOData


class CheckPoint(UserDict):
    """Base class for class performing checkpoints, that is, writing numerically
    useful data to disk. It stores all data in an IOData container and
    can dump this information to disk using PyBEST's internal format.
    """

    def __init__(self, data_dict=dict()):
        # Empty dataionary, will be passed to IOData container
        self._data = data_dict
        self._iodata = IOData()

    @property
    def data(self):
        """The dict from UserDict that contains all data dump to disk"""
        return self._data

    def clear(self):
        self._data = {}
        self._iodata = IOData()

    def update(self, key, value):
        """Can be used equivalent to __setitem__"""
        self._data.update({key: value})

    def to_file(self, filename):
        fname = filemanager.result_path(filename)
        if fname.suffix == ".h5":
            self._iodata = IOData(**self._data)
            self._iodata.to_file(fname)
        else:
            raise ArgumentError("Checkpoint can only dump to h5 format.")

    def from_file(self, filename):
        if filename.endswith(".h5"):
            return IOData.from_file(filename)
        else:
            raise ArgumentError("Checkpoint can only read from h5 format.")

    def __call__(self):
        """Set iodata to value, which must be a dataionary"""
        self._iodata = IOData(**self._data)
        return self._iodata
