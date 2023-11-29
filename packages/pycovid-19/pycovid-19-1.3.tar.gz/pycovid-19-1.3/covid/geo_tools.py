# -*- coding: utf-8 -*-

""" Everything related to geographic entities and
corresponding processes comes here.

More detailed description.
"""
import tempfile
from abc import abstractmethod
from urllib.request import urlretrieve

from fuzzywuzzy import process, fuzz
from geopandas import GeoDataFrame

import country_converter as coco
import numpy as np
import pandas as pd

from covid import RESOURCE_URL
from covid.resources import WORLD_POPULATION_BY_ISO3, COUNTRY_LIST_EN, FRANCE_ADMIN
from covid.utilities import str_to_list, lazyproperty


class GeographicRegion:
    """ GeographicRegion class

    Use geographic entities as objects in whole package
    """
    _score_cutoff = 80

    def __init__(self, raw_name):
        """ Constructor

        :param raw_name:
        """
        self.raw_name = list(str_to_list(raw_name))

    def __iter__(self):
        return self.name.__iter__()

    def __len__(self):
        return len(self.raw_name)

    @lazyproperty
    @abstractmethod
    def name(self):
        pass


class CountryCollection(GeographicRegion):
    """ CountryCollection instance

    Gather collection of country names and populations
    """

    def _convert(self, to):
        """ Convert list of raw names to standard names

        :param to:
        :return: list of valid names (None in place of no valid names)
        """
        with_not_founds = str_to_list(coco.convert(self.raw_name, to=to))
        without_not_founds = [raw_name if name == "not found" else name for raw_name, name in
                              zip(self.raw_name, with_not_founds)]

        fuzzy_edit_fix = [process.extractOne(raw_name, COUNTRY_LIST_EN, score_cutoff=self._score_cutoff,
                                             scorer=fuzz.token_set_ratio) if name == "not found" else raw_name
                          for name, raw_name in zip(with_not_founds, without_not_founds)]

        return [fix[0] if fix and name == "not found" else fix for fix, name in zip(fuzzy_edit_fix, with_not_founds)]

    @lazyproperty
    def population(self):
        return [WORLD_POPULATION_BY_ISO3[iso3] if iso3 in WORLD_POPULATION_BY_ISO3.keys() else np.nan
                for iso3 in self._convert(to="ISO3")]

    @lazyproperty
    def iso3(self):
        return self._convert(to='ISO3')

    @lazyproperty
    def name(self):
        return self._convert(to="name_short")


class Geometry:
    """ Geometry class

    """
    gdf = None
    file = tempfile.mkstemp(suffix=".json")[1]

    def __init__(self, url_region_name, geographic_region_class, region_name_column_label="name"):
        self.url = RESOURCE_URL.loc[url_region_name, "geometry"]
        self.geographic_region_class = geographic_region_class
        self.region_name_column_label = region_name_column_label

    def build(self):
        if self.gdf is None:
            urlretrieve(self.url, self.file)
            self.gdf = GeoDataFrame.from_file(self.file)
            self.gdf.index = self.geographic_region_class(self.gdf[self.region_name_column_label]).name
            self.gdf["region"] = self.gdf.index


class RegionCollection(GeographicRegion):
    """ Region collection within a country based on pandas dataframe

    """
    data_frame = None
    region_name_column = None
    region_code_column = None
    population_column = None

    def __init__(self, collection, by="name"):
        self.id = by
        super().__init__(collection)

    def _convert(self, region_column):
        standard = [process.extractOne(raw_name, self.data_frame[region_column], score_cutoff=self._score_cutoff,
                                       scorer=fuzz.token_set_ratio) for raw_name in self.raw_name]
        return [std[0] if std else std for std in standard]

    @lazyproperty
    def population(self):
        if self.population_column:
            if self.id == "name":
                return list(pd.merge(pd.Series(data=self.name, name=self.region_name_column), self.data_frame,
                                     on=self.region_name_column)[self.population_column])
            else:
                return list(pd.merge(pd.Series(data=self.code, name=self.region_code_column), self.data_frame,
                                     on=self.region_code_column)[self.population_column])

    @lazyproperty
    def name(self):
        if self.id == "name":
            return self._convert(self.region_name_column)
        else:
            std_code = pd.Series(data=self.code, name=self.region_code_column)
            return list(pd.merge(std_code, self.data_frame, on=self.region_code_column)[self.region_name_column])

    @lazyproperty
    def code(self):
        if self.id == "code":
            return self._convert(self.region_code_column)
        else:
            std_name = pd.Series(data=self.name, name=self.region_name_column)
            return list(pd.merge(std_name, self.data_frame, on=self.region_name_column)[self.region_code_column])


WORLD_GEOMETRY = Geometry("world", CountryCollection)


class France(RegionCollection):
    data_frame = FRANCE_ADMIN
    region_name_column = "DEP"
    region_code_column = "CODDEP"
    population_column = "PTOT"
#
#
# FRANCE_GEOMETRY = Geometry("France", RegionCollection, "code")
