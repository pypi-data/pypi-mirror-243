# -*- coding: utf-8 -*-

""" Module summary description.

More detailed description.
"""
import tempfile
from abc import abstractmethod
from urllib.request import urlretrieve

from fuzzywuzzy import fuzz, process
import pandas as pd
import numpy as np

from covid import RESOURCE_URL
from covid.exceptions import CovidMatcherError
from covid.geo_tools import CountryCollection

JOHN_HOPKINS_WORLD_COLUMN_DROP = ["Province/State", "Country/Region", "Lat", "Long"]
PREVALENCE_RATIO = 100000


def retrieve_cases(covid_matcher, regions, normalized, cumulative=True):
    """ Get cases for given country

    :param covid_matcher: CovidMatcher instance
    :param regions: GeographicRegion collection
    :param normalized:
    :param cumulative: (boolean) if True return cumulative cases, daily otherwise
    :return:
    """
    if regions == "all":
        return covid_matcher.get_all(normalized, cumulative)
    else:
        return covid_matcher.get_cases(regions, normalized, cumulative)


class CovidMatcher:
    """ CovidMatcher class

    Match covid database for given region
    """
    # Case time series
    cumulative_cases = None
    daily_cases = None

    regions = None

    valid_case_type = ["deaths", "confirmed", "recovered"]

    # Path to temp file and URL
    file = tempfile.mkstemp(suffix=".csv")[1]

    # Prevalence ratio
    prevalence_ratio = PREVALENCE_RATIO

    def __init__(self, case_type, region_name):
        self.case_type = process.extractOne(case_type, self.valid_case_type, scorer=fuzz.partial_token_set_ratio)[0]
        self.region_name = region_name

    @abstractmethod
    def _build_database(self, *args, **kwargs):
        pass

    def build_database(self, *args, **kwargs):
        """ Build database

        :param args:
        :param kwargs:
        :return:
        """
        # Import file and read it
        urlretrieve(RESOURCE_URL.loc[self.region_name, self.case_type], self.file)
        self.cumulative_cases = pd.read_csv(self.file, keep_default_na=False)

        # Call specific child method to build database
        self._build_database(*args, **kwargs)

        # Store regions, index as DatetimeIndex and daily cases
        self.cumulative_cases.index = pd.DatetimeIndex(self.cumulative_cases.index)
        self.daily_cases = self.cumulative_cases.diff()

    def get_all(self, normalized, cumulative, *args, **kwargs):
        """ Get sum of all cases in database

        :param normalized: (boolean), if True return prevalence, absolute cases otherwise
        :param cumulative: (boolean) if True, return cumulative cases, daily otherwise
        :return:
        """
        if cumulative:
            cases = self.cumulative_cases.sum(axis=1)
        else:
            cases = self.daily_cases.sum(axis=1)

        if normalized:
            return cases * self.prevalence_ratio / np.sum(self.regions.population)
        else:
            return cases

    def get_cases(self, region, normalized, cumulative, *args, **kwargs):
        """ Get covid absolute data according to case type

        :param region: GeographicRegion collection instance
        :param normalized: (boolean) if True, return normalized data
        :param cumulative: (boolean) if True return cumulative cases, daily otherwise
        :return: dict of time series for each country
        """
        if cumulative:
            cases = self.cumulative_cases
        else:
            cases = self.daily_cases

        if normalized:
            return {name: cases.loc[:, name] * self.prevalence_ratio / pop
                    for name, pop in zip(region.name, region.population)}
        else:
            return {name: cases.loc[:, name] for name in region.name}

    def get_map_of_cases(self, date, normalized, cumulative, *args, **kwargs):
        """ Get spatial repartition of cases at a date

        :param date:
        :param normalized: boolean
        :param cumulative: boolean, if True get cumulative cases, daily otherwise
        :return: DataFrame with two columns {'region' and 'cases'}
        """
        if cumulative:
            cases = self.cumulative_cases
        else:
            cases = self.daily_cases

        try:
            if normalized:
                return pd.DataFrame.from_dict(
                    dict(region=cases.keys(),
                         cases=cases.loc[date] * self.prevalence_ratio / self.regions.population))
            else:
                return pd.DataFrame.from_dict(dict(region=cases.keys(), cases=cases.loc[date]))
        except KeyError:
            raise CovidMatcherError(f"'{date}' is not a valid date format or is outside the time range")

    def last_date(self):
        return self.cumulative_cases.index[-1]


class WorldCovidMatcher(CovidMatcher):
    """ WorldCovidMatcher class

    Match Covid-19 data in the world
    """

    def __init__(self, case_type):

        super().__init__(case_type, "world")

    def _build_database(self):
        """ Build database with respect to case type

        :return:
        """
        provinces = CountryCollection(self.cumulative_cases["Province/State"])
        countries = CountryCollection(self.cumulative_cases["Country/Region"])
        self.cumulative_cases.index = [province if province else country for province, country in
                                       zip(provinces.name, countries.name)]
        self.cumulative_cases = self.cumulative_cases.drop(columns=JOHN_HOPKINS_WORLD_COLUMN_DROP)
        self.cumulative_cases = self.cumulative_cases.groupby(self.cumulative_cases.index).agg("sum").transpose()
        self.regions = CountryCollection(self.cumulative_cases.keys())


class CountryCovidMatcher(CovidMatcher):
    """ Match Covid-19 cases in given country

    """
    region_name_column = None
    region_code_column = None

    def _build_database(self, *args, **kwargs):
        pass


# class CountryCovidMatcher(CovidMatcher):
#     """ CountryCovidMatcher class
#
#     Match Covid-19 data in a given country
#     """
#     geographic_region_class = None
#     data_frame = None
#     csv_sep = None
#
#     # DataFrame colum labels
#     region_column_label = None
#     date_column_label = None
#     sex_column_label = None
#     death_column_label = None
#     confirmed_column_label = None
#     recovered_column_label = None
#     hospitalization_column_label = None
#     reanimation_column_label = None
#
#     def _build_database(self, case_type, *args, **kwargs):
#         urlretrieve(self.url.loc[self.region_name, "all"], self.file)
#         self.data_frame = pd.read_csv(self.file, sep=self.csv_sep, keep_default_na=False)
#
#         sub_regions = self.geographic_region_class(self.data_frame[self.region_column_label])
