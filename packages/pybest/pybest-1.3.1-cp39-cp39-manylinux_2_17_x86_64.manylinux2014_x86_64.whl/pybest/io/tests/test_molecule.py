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


import numpy as np

from pybest.io.iodata import IOData


def test_typecheck():
    m = IOData(coordinates=np.array([[1, 2, 3], [2, 3, 1]]))
    assert issubclass(m.coordinates.dtype.type, float)
    assert not hasattr(m, "atom")
    m = IOData(
        atom=np.array(["He", "Ne"]),
        coordinates=np.array([[1, 2, 3], [2, 3, 1]]),
    )
    m = IOData(
        atom=np.array(["He", "Ne"]),
        coordinates=np.array([[1, 2, 3], [2, 3, 1]]),
    )
    assert hasattr(m, "atom")
    assert issubclass(m.atom.dtype.type, object)
    del m.atom
    assert not hasattr(m, "atom")
