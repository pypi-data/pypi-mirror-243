# -*- coding: utf-8 -*-

""" Module summary description.

More detailed description.
"""
import os

import country_converter as coco
import pandas as pd
import world_bank_data as wb
from country_list import country_list
from pandas import Series, read_csv

from covid import DATA_DIR

FRANCE_ADMIN = read_csv(os.path.join(DATA_DIR, "france_departement_pop.csv"))[["CODDEP", "DEP", "PTOT"]]

CIA_WIKI_POP = Series(index=["Taiwan", "Western Sahara", "Aland Islands", "Anguilla",
                             "Bonaire, Saint Eustatius and Saba", "Christmas Island",
                             "Cocos (Keeling) Islands", "Cook Islands", "Eritrea",
                             "Falkland Islands", "French Guiana", "Guadeloupe", "Guernsey",
                             "Jersey", "Martinique", "Mayotte", "Montserrat", "Niue",
                             "Norfolk Island", "Pitcairn", "Reunion", "St. Barths",
                             "St. Helena", "St. Pierre and Miquelon", "Svalbard and Jan Mayen Islands",
                             "Tokelau", "Vatican", "Wallis and Futuna Islands"],
                      data=[23508428, 652271, 29838, 18090, 25019, 2205, 596, 8574, 6081196,
                            3198, 268700, 390253, 67052, 101073, 372594, 256518, 5373, 2000,
                            1748, 50, 853659, 7122, 4577, 5347, 2926, 1647, 799, 15854])

WORLD_BANK_DATA = wb.get_series('SP.POP.TOTL', mrv=1, simplify_index=True)["Afghanistan"::]
WORLD_POPULATION = pd.concat([WORLD_BANK_DATA, CIA_WIKI_POP])
WORLD_POPULATION_BY_ISO3 = {key: pop for key, pop in zip(coco.convert(list(WORLD_POPULATION.index),
                                                                      to="ISO3"),
                                                         WORLD_POPULATION)}

COUNTRY_LIST_EN = [country[1] for country in country_list.countries_for_language("en")]

# Lockdown dates at national level
# lockdown_tracker_file = os.path.join(tempfile.gettempdir(), "lockdown_tracker.csv")
# urlretrieve("https://raw.githubusercontent.com/AuraVisionLabs/covid19-lockdown-tracker/master/wiki_lockdown_dates.csv",
#             lockdown_tracker_file)
# COUNTRY_LOCKDOWN_TRACKER = read_csv(lockdown_tracker_file, index_col=0)
# COUNTRY_LOCKDOWN_TRACKER = COUNTRY_LOCKDOWN_TRACKER[COUNTRY_LOCKDOWN_TRACKER["Level"] == "National"]
