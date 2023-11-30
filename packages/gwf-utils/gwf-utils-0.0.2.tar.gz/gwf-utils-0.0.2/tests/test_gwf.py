#!/usr/bin/env python
# -*- coding: utf-8 -*-
# vim: nu:ai:ts=4:sw=4

#
#  Copyright (C) 2023 Joseph Areeda <joseph.areeda@ligo.org>
#
#  This program is free software: you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation, either version 3 of the License, or
#  (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
"""
High level tests of Gwf class
"""

__author__ = 'joseph areeda'
__email__ = 'joseph.areeda@ligo.org'

from pathlib import Path

import pytest

from gwf_utils.Gwf import Gwf

infile = Path("../testdata/L-L1_llhoft-1384353755-1.gwf")


def test_one():
    gwf = Gwf(path=infile)
    chan_list = gwf.get_channel_list()
    assert chan_list is not None
    assert len(chan_list) > 1
    data = gwf.get_frvect_data(chan_list[0])
    assert data['dx'] > 0
    assert len(data['dtype_str']) > 0
    assert data["data_rate"] > 0
