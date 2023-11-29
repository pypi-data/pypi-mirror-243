# -*- coding: utf-8 -*-

""" Module summary description.

More detailed description.
"""

__author__ = 'Benjamin Pillot, Louis Gostiaux'
__copyright__ = 'Copyright 2020, Benjamin Pillot, Louis Gostiaux'
__version__ = '1.3'

import logging
import os

from pandas import read_csv

logging.getLogger().setLevel(logging.ERROR)

covid_dir = os.path.dirname(os.path.realpath(__file__))
DATA_DIR = os.path.join(covid_dir, "data")

RESOURCE_URL = read_csv(os.path.join(DATA_DIR, "resource_url.csv"), index_col=0)

# COVID_FRANCE = os.path.join(tempfile.gettempdir(), "covid_france.csv")

# COUNTRY_A3_MATCH = read_csv(os.path.join(data_dir, "country_a3_match.csv"), index_col=0,
#                             skipinitialspace=True)["Country A3"]

# France data
# urlretrieve("https://www.data.gouv.fr/fr/datasets/r/63352e38-d353-4b54-bfd1-f1b3ee1cabd7", COVID_FRANCE)

# urlretrieve("https://github.com/datasets/geo-countries/raw/master/data/countries.geojson", COUNTRIES_GEOJSON)
