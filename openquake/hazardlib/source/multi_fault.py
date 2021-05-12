# The Hazard Library
# Copyright (C) 2012-2021 GEM Foundation
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as
# published by the Free Software Foundation, either version 3 of the
# License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
"""
Module :mod:`openquake.hazardlib.source.multi_fault`
defines :class:`MultiFaultSource`.
"""

import numpy as np
from typing import Union
from openquake.hazardlib.source.rupture import (
    NonParametricProbabilisticRupture)
from openquake.hazardlib.source.non_parametric import (
    NonParametricSeismicSource as NP)
from openquake.hazardlib.geo.surface.multi import MultiSurface
from openquake.hazardlib.source.base import BaseSeismicSource

F32 = np.float32


class FaultSection(object):
    """
    A class to define a fault section, that is the geometry definition of a
    portion of a fault.

    :param sec_id:
        A unique identifier
    :param surface:
        An instance of
        :class:`openquake.hazardlib.geo.surface.base.BaseSurface` which
        describes the 3D geometry of a part of a fault system.
    """
    def __init__(self, sec_id: str, surface):
        self.sec_id = sec_id
        self.surface = surface


class MultiFaultSource(BaseSeismicSource):
    """
    The multi-fault source is a source typology specifiically support the
    calculation of hazard using fault models with segments participating to
    multiple ruptures.

    :param source_id:
        A unique identifier for the source
    :param name:
        The name of the fault
    :param tectonic_region_type:
        A string that defines the TRT of the fault source
    :param sections:
        A list of :class:`openquake.hazardlib.source.multi_fault.FaultSection`
        instances. The cardinality of this list is N.
    :param rupture_idxs:
        A list of lists. Each element contains the IDs of the sections
        participating to a rupture. The cardinality of this list is N.
    :param occurrence_probs:
        A list with cardinality N with instances of the class
        :class:`openquake.hazardlib.pmf.PMF`. Each element specifies the
        occurrence of 0, 1 ... occurrences of a rupture in the investigation
        time.
    :param magnitudes:
        An iterable with cardinality N containing the magnitudes of the
        ruptures
    :param rakes:
        An iterable with cardinality N containing the rake of each
        rupture
    """
    code = b'F'
    MODIFICATIONS = {}

    def __init__(self, source_id: str, name: str, tectonic_region_type: str,
                 sections: list, rupture_idxs: list,
                 occurrence_probs: Union[list, np.ndarray],
                 magnitudes: list, rakes: list):
        self.sections = sections
        self.rupture_idxs = rupture_idxs
        self.poes = occurrence_probs
        self.mags = magnitudes
        self.rakes = rakes
        self.trt = tectonic_region_type
        super().__init__(source_id, name, tectonic_region_type)
        self.create_inverted_index()

    def create_inverted_index(self):
        """
        Creates an inverted index structure, i.e. a dictionary sec_id->index
        """
        self.invx = {}
        for i, sec in enumerate(self.sections):
            self.invx[sec.sec_id] = i

    def iter_ruptures(self, fromidx=0, untilidx=None, **kwargs):
        """
        An iterator for the ruptures.

        :param fromidx: start
        :param untilidx: stop
        """
        # Create inverted index
        if 'invx' not in self.__dict__:
            self.create_inverted_index()

        # Iter ruptures
        untilidx = len(self.mags) if untilidx is None else untilidx
        for i in range(fromidx, untilidx):
            idxs = self.rupture_idxs[i]
            if len(idxs) < 2:
                sfc = self.sections[self.invx[idxs[0]]].surface
            else:
                s = self.sections
                sfc = MultiSurface([s[self.invx[j]].surface for j in idxs])
            rake = self.rakes[i]
            hypo = self.sections[self.invx[idxs[0]]].surface.get_middle_point()
            pmf = self.poes[i]
            yield NonParametricProbabilisticRupture(self.mags[i], rake,
                                                    self.trt, hypo, sfc, pmf)

    def count_ruptures(self):
        return len(self.mags)

    def get_min_max_mag(self):
        return np.min(self.mags), np.max(self.mags)

    def get_one_rupture(self, ses_seed, rupture_mutex):
        raise NotImplementedError

    @property
    def data(self):  # compatibility with NonParametricSeismicSource
        for sec in self.sections:
            yield sec, None

    polygon = NP.polygon
    wkt = NP.wkt
