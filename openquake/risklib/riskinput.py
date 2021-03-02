# -*- coding: utf-8 -*-
# vim: tabstop=4 shiftwidth=4 softtabstop=4
#
# Copyright (C) 2015-2021 GEM Foundation
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

import numpy
from openquake.baselib import hdf5
from openquake.baselib.general import group_array, AccumDict

U32 = numpy.uint32
F32 = numpy.float32


def get_assets_by_taxo(assets):
    """
    :param assets: an array of assets
    :returns: assets_by_taxo with attributes eps and idxs
    """
    assets_by_taxo = AccumDict(group_array(assets, 'taxonomy'))
    assets_by_taxo.assets = assets
    assets_by_taxo.idxs = numpy.argsort(numpy.concatenate([
        a['ordinal'] for a in assets_by_taxo.values()]))
    return assets_by_taxo


def get_output_gmf(crmodel, assets_by_taxo, haz, epsgetter):
    """
    :param assets_by_taxo: a dictionary taxonomy index -> assets on a site
    :param haz: a DataFrame of GMVs on that site
    :param rlzi: if given, a realization index
    :returns: an ArrayWrapper loss_type -> array of shape (A, ...)
    """
    primary = crmodel.primary_imtls
    alias = {imt: 'gmv_%d' % i for i, imt in enumerate(primary)}
    # the order in which the gmfs are stored is random since it depends
    # on which hazard task ends first; here we reorder
    # the gmfs by event ID; this is convenient in
    # general and mandatory for the case of
    # VulnerabilityFunctionWithPMF, otherwise the
    # sample method would receive the means in random
    # order and produce random results even if the
    # seed is set correctly; very tricky indeed! (MS)
    haz = haz.sort_values('eid')
    for m, imt in enumerate(primary):
        col = f'gmv_{m}'
        if col not in haz.columns:
            haz[col] = numpy.zeros(len(haz))  # ZeroGetter
    eids = haz.eid.to_numpy()
    dic = dict(eids=eids, assets=assets_by_taxo.assets,
               loss_types=crmodel.loss_types, haz=haz, rlzs=haz.rlz.to_numpy())
    items = []
    for taxonomy, assets_ in assets_by_taxo.items():
        epsilons = epsgetter.get(assets_) if epsgetter else ()
        items.append((taxonomy, assets_, epsilons))
    for lt in crmodel.loss_types:
        losses = []
        for taxonomy, assets_, epsilons in items:
            arrays = []
            rmodels, weights = crmodel.get_rmodels_weights(lt, taxonomy)
            for rm in rmodels:
                imt = rm.imt_by_lt[lt]
                col = alias.get(imt, imt)
                arrays.append(rm(lt, assets_, haz, col, epsilons))
            res = arrays[0] if len(arrays) == 1 else numpy.average(
                arrays, weights=weights, axis=0)
            losses.append(res)
        arr = numpy.concatenate(losses)  # losses per each taxonomy
        dic[lt] = arr[assets_by_taxo.idxs]  # reordered by ordinal
    return hdf5.ArrayWrapper((), dic)


def get_output_pc(crmodel, assets_by_taxo, haz, epsgetter, rlzi):
    """
    :param assets_by_taxo: a dictionary taxonomy index -> assets on a site
    :param haz: an ArrayWrapper of ProbabilityCurves on that site
    :param rlzi: if given, a realization index
    :returns: an ArrayWrapper loss_type -> array of shape (A, ...)
    """
    primary = crmodel.primary_imtls
    alias = {imt: 'gmv_%d' % i for i, imt in enumerate(primary)}
    data = {f'gmv_{m}': haz.array[crmodel.imtls(imt), 0]
            for m, imt in enumerate(primary)}
    dic = dict(assets=assets_by_taxo.assets,
               loss_types=crmodel.loss_types, haz=haz, rlzi=rlzi)
    for lt in crmodel.loss_types:
        ls = []
        for taxonomy, assets_ in assets_by_taxo.items():
            arrays = []
            rmodels, weights = crmodel.get_rmodels_weights(lt, taxonomy)
            for rm in rmodels:
                imt = rm.imt_by_lt[lt]
                col = alias.get(imt, imt)
                arrays.append(rm(lt, assets_, data, col))
            res = arrays[0] if len(arrays) == 1 else numpy.average(
                arrays, weights=weights, axis=0)
            ls.append(res)
        arr = numpy.concatenate(ls)
        dic[lt] = arr[assets_by_taxo.idxs] if len(arr) else arr
    return hdf5.ArrayWrapper((), dic)


class RiskInput(object):
    """
    Contains all the assets and hazard values associated to a given
    imt and site.

    :param hazard_getter:
        a callable returning the hazard data for a given realization
    :param assets_by_site:
        array of assets, one per site
    """
    def __init__(self, hazard_getter, assets):
        self.hazard_getter = hazard_getter
        self.assets = assets
        self.weight = len(assets)
        aids = []
        for asset in self.assets:
            aids.append(asset['ordinal'])
        self.aids = numpy.array(aids, numpy.uint32)

    def gen_outputs(self, crmodel, monitor, epsgetter=None, haz=None):
        """
        Group the assets per taxonomy and compute the outputs by using the
        underlying riskmodels. Yield one output per realization.

        :param crmodel: a CompositeRiskModel instance
        :param monitor: a monitor object used to measure the performance
        """
        self.monitor = monitor
        hazard_getter = self.hazard_getter
        if haz is None:
            with monitor('getting hazard', measuremem=False):
                haz = hazard_getter.get_hazard()
        with monitor('computing risk', measuremem=False):
            # this approach is slow for event_based_risk since a lot of
            # small arrays are passed (one per realization) instead of
            # a long array with all realizations; ebrisk does the right
            # thing since it calls get_output directly
            assets_by_taxo = get_assets_by_taxo(self.assets)
            if hasattr(haz, 'groupby'):  # DataFrame
                yield get_output_gmf(crmodel, assets_by_taxo, haz, epsgetter)
            else:  # list of probability curves
                for rlz, pc in enumerate(haz):
                    yield get_output_pc(
                        crmodel, assets_by_taxo, pc, epsgetter, rlz)

    def __repr__(self):
        [sid] = self.hazard_getter.sids
        return '<%s sid=%s, %d asset(s)>' % (
            self.__class__.__name__, sid, len(self.aids))


class EpsilonGetter(object):
    """
    An object ``EpsilonGetter(master_seed, asset_correlation, E)``
    has a method ``.get(assets)`` which returns a matrix of (A, E)
    normally distributed random numbers, being A the number of assets.
    If the ``asset_correlation`` is 1 the numbers are the same for
    all assets of the same taxonomy.

    >>> epsgetter = EpsilonGetter(
    ...     master_seed=42, asset_correlation=1, tot_events=5)
    >>> assets = numpy.array([(0, 1), (1, 1), (2, 2)],
    ...     [('ordinal', int), ('taxonomy', int)])
    >>> epsgetter.get(assets)
    array([[ 0.79422116, -1.6106067 , -0.76643026, -0.4143733 ,  0.5967326 ],
           [ 0.79422116, -1.6106067 , -0.76643026, -0.4143733 ,  0.5967326 ],
           [ 2.0044227 , -0.7924013 ,  1.2191101 ,  1.3231088 ,  1.1357217 ]],
          dtype=float32)
    """
    def __init__(self, master_seed, asset_correlation, tot_events):
        self.master_seed = master_seed
        self.asset_correlation = asset_correlation
        self.tot_events = tot_events

    def gen_rng(self, assets):
        for a, asset in enumerate(assets):
            idx = int(asset['taxonomy'] if self.asset_correlation
                      else asset['ordinal'])
            philox = numpy.random.Philox(
                self.master_seed * self.tot_events + idx)
            yield numpy.random.Generator(philox)

    def get(self, assets):
        """
        :param assets: array of assets
        :returns: an array of shape (num_assets, tot_events) and dtype float32
        """
        epsilons = numpy.zeros((len(assets), self.tot_events), F32)
        for a, rng in enumerate(self.gen_rng(assets)):
            epsilons[a] = rng.normal(size=self.tot_events)
        return epsilons


def str2rsi(key):
    """
    Convert a string of the form 'rlz-XXXX/sid-YYYY/ZZZ'
    into a triple (XXXX, YYYY, ZZZ)
    """
    rlzi, sid, imt = key.split('/')
    return int(rlzi[4:]), int(sid[4:]), imt


def rsi2str(rlzi, sid, imt):
    """
    Convert a triple (XXXX, YYYY, ZZZ) into a string of the form
    'rlz-XXXX/sid-YYYY/ZZZ'
    """
    return 'rlz-%04d/sid-%04d/%s' % (rlzi, sid, imt)
