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
"""Input and output routines

   All input routines begin with ``load_``. All output routines begin with
   ``dump_``.

   This package also contains a ``IOData`` class to facilitate reading from
   and writing to different file formats. It contains the methods ``from_file``
   and ``to_file`` that automatically determine the file format based on the
   prefix or extension of the filename.
"""


# define test runner
from pybest._pytesttester import PytestTester
from pybest.io.checkpoint import CheckPoint
from pybest.io.cube import dump_cube
from pybest.io.embedding import *
from pybest.io.external_charges import *
from pybest.io.internal import *
from pybest.io.iodata import IOData
from pybest.io.lockedh5 import *
from pybest.io.molden import *
from pybest.io.molekel import *
from pybest.io.molpro import dump_fcidump, load_fcidump
from pybest.io.xyz import *

test = PytestTester(__name__)
del PytestTester
