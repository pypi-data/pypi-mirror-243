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

import warnings

from pybest import context
from pybest.gbasis.gobasis import compute_nuclear_repulsion, get_gobasis

ref = 9.138880475737013


def test_nucnuc():
    fn = context.get_fn("test/h2o_ccdz.xyz")
    obs = get_gobasis("cc-pvdz", fn, print_basis=False)

    nucnuc = compute_nuclear_repulsion(obs)

    error = abs(nucnuc - ref)
    failure = error > 1e-10

    # FIXME: This should be simplified when we have a way to tell which libint
    # version wer are using.
    if failure and error < 1e-9:
        warnings.warn(
            "Most likely, you are using an older version of the libint2 "
            "library. This version of PyBEST requires libint v2.7.2+"
        )
    elif not failure:
        # everything works fine
        assert not failure
    # if errors are not below 1e-9, raise test failure
    assert error < 1e-9
