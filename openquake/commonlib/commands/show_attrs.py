# -*- coding: utf-8 -*-
# vim: tabstop=4 shiftwidth=4 softtabstop=4
#
# Copyright (C) 2015-2016 GEM Foundation
#
# OpenQuake is free software: you can redistribute it and/or modify it
# under the terms of the GNU Affero General Public License as published
# by the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# OpenQuake is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with OpenQuake. If not, see <http://www.gnu.org/licenses/>.

from __future__ import print_function
from openquake.commonlib import sap, datastore


def show_attrs(key, calc_id=-1):
    """
    Show the attributes of a HDF5 dataset in the datastore

    :param key: key of the datastore
    :param calc_id: numeric calculation ID (default last calculation)
    """
    ds = datastore.read(calc_id)
    try:
        attrs = ds.hdf5[key].attrs
    except KeyError:
        print('%r is not in %s' % (key, ds))
        return
    if len(attrs) == 0:
        print('%s has no attributes' % key)
    for name, value in attrs.items():
        print(name, value)

parser = sap.Parser(show_attrs)
parser.arg('key', 'key of the datastore')
parser.arg('calc_id', 'calculation ID', type=int)
