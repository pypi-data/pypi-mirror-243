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


from pathlib import Path


def in_pybest_source_root():
    """Test if the current directory is the PyBEST source tree root"""
    # Check for some files and directories that must be present (for functions
    # that use this check).
    if not Path("setup.py").is_file():
        return False
    if not Path("src").is_dir():
        return False
    if not Path("scripts").is_dir():
        return False
    if not Path("README").is_file():
        return False
    with open("README") as f:
        if (
            next(f)
            != "PyBEST: *Py*thonic *B*lack-box *E*lectronic *S*tructure *T*ool.\n"
        ):
            return False
    return True
