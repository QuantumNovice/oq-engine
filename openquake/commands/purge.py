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
import os
import re
import getpass
from openquake.commonlib import sap, datastore
from openquake.engine.logs import dbcmd


def purge(calc_id):
    """
    Remove the given calculation. If calc_id is 0, remove all calculations.
    """
    user = getpass.getuser()
    if not calc_id:
        for fname in os.listdir(datastore.DATADIR):
            mo = re.match('calc_(\d+)\.hdf5', fname)
            if mo is not None:
                calc_id = int(mo.group(1))
                os.remove(os.path.join(datastore.DATADIR, fname))
                dbcmd('del_calc', calc_id, user)
                print('Removed %s' % fname)
    else:
        if calc_id < 0:
            calc_id = datastore.get_calc_ids()[calc_id]
        hdf5path = os.path.join(datastore.DATADIR, 'calc_%s.hdf5' % calc_id)
        os.remove(hdf5path)
        dbcmd('del_calc', calc_id, user)
        print('Removed %s' % hdf5path)


parser = sap.Parser(purge)
parser.arg('calc_id', 'calculation ID', type=int)
