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
"""The main PyBEST Package"""


__version__ = "1.3.1"

import atexit

# intialize exceptions first
from .exceptions import *  # isort:skip

# then initialize global FileManager
from .file_manager import FileManager  # isort:skip

filemanager = FileManager("pybest-results", "pybest-temp")
# If keep_temp is set to False, delete all temp dirs after exit
atexit.register(filemanager.clean_up_temporary_directory)

# stolen from NumPy
from pybest._pytesttester import PytestTester

from .auxmat import *
from .cache import Cache, JustOnceClass, just_once
from .cc import *
from .ci import *
from .constants import *
from .context import *
from .corrections import *
from .ee_eom import *
from .featuredlists import *
from .gbasis import *
from .geminals import *
from .helperclass import *
from .io import *
from .ip_eom import *
from .linalg import *
from .localization import *
from .log import *
from .modelhamiltonians import *
from .occ_model import *
from .orbital_entanglement import *
from .orbital_utils import *
from .part import *
from .periodic import *
from .pt import *
from .sapt import *
from .scf import *
from .solvers import *
from .steplength import *
from .units import *
from .utils import *
from .wrappers import *

test = PytestTester(__name__)
del PytestTester
