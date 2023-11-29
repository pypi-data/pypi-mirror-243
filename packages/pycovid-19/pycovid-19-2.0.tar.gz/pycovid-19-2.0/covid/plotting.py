# -*- coding: utf-8 -*-

""" Module summary description.

More detailed description.
"""
import folium
from pandas.plotting import register_matplotlib_converters
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import plotly.graph_objects as go
from plotly.subplots import make_subplots

from covid.database import retrieve_cases, PREVALENCE_RATIO, WorldCovidMatcher
from covid.exceptions import OffsetError
from covid.geo_tools import CountryCollection, WORLD_GEOMETRY
from covid.utilities import check_string

register_matplotlib_converters()


FOLIUM_COLOR = {'deaths': 'red', 'confirmed': 'orange', 'recovered': 'green'}
CASE_TYPE_LONG = {'deaths': 'deaths', 'confirmed': 'confirmed cases', 'recovered': 'recovered cases'}
SUBPLOT_NB_COLS = 2
HOVERFORMAT_NORMALIZED = '.1f'
TICKFORMAT_NORMALIZED = '.1f'
HOVERFORMAT_ABSOLUTE = '.0f'
TICKFORMAT_ABSOLUTE = '.1s'


# TODO: create animated gif for world and country maps (using Pillow ?)


def _get_subplot_axes(countries, case_type, use_plotly):

    ncols = min(len(countries), SUBPLOT_NB_COLS)
    nrows = max(int(np.ceil(len(countries) / SUBPLOT_NB_COLS)), 1)

    if use_plotly:
        fig = make_subplots(rows=nrows, cols=ncols, subplot_titles=[country for country in countries])
        axes = None
    else:
        fig, axes = plt.subplots(nrows, ncols)
        if isinstance(axes, np.ndarray):
            axes = axes.flatten()
        else:
            axes = [axes]

    return fig, axes


def _get_doubling_cases(cases, doubling_factor):
    non_zero_cases = cases[cases > 0]
    non_zero_cases[:] = non_zero_cases.iloc[0] * (2 ** (1 / doubling_factor)) ** np.arange(non_zero_cases.size)
    return non_zero_cases


class CovidMap:
    """ CovidMap class

    """

    def __init__(self, covid_matcher, geometry):
        """ Build covid map

        :param covid_matcher:
        :param geometry:
        """
        self.covid_matcher = covid_matcher
        self.geometry = geometry

    def build(self):
        """ Build object (matcher and geometry)

        :return:
        """
        self.covid_matcher.build_database()
        self.geometry.build()

    def get_layer(self, date, normalized, cumulative):
        """ Return layer map as a GeoDataFrame

        :param date:
        :param normalized:
        :param cumulative:
        :return: GeoDataFrame
        """
        gdf = self.covid_matcher.get_map_of_cases(date, normalized, cumulative)
        gdf = self.geometry.gdf.merge(gdf, on="region")
        gdf["latitude"] = gdf.centroid.y
        gdf["longitude"] = gdf.centroid.x

        return gdf


class WorldCovidMap(CovidMap):

    def __init__(self, case_type):
        super().__init__(WorldCovidMatcher(case_type), WORLD_GEOMETRY)


def get_folium_map(covid_map, date, normalized, cumulative, zoom_start):
    """ Retrieve folium map of Covid cases

    :param covid_map:
    :param date:
    :param normalized:
    :param cumulative:
    :param zoom_start: starting zoom on Folium map
    :return:
    """
    covid_map.build()
    if date is None:
        date = covid_map.covid_matcher.last_date()
    else:
        date = pd.to_datetime(date)

    layer = covid_map.get_layer(date, normalized, cumulative)

    if cumulative:
        case_desc = "cumulative"
    else:
        case_desc = "daily"

    if normalized:
        title = f"Prevalence ({case_desc} {CASE_TYPE_LONG[covid_map.covid_matcher.case_type]})"
    else:
        title = f"Number of {case_desc} {CASE_TYPE_LONG[covid_map.covid_matcher.case_type]}"

    folium_map = folium.Map(location=[layer["latitude"].mean(), layer["longitude"].mean()], zoom_start=zoom_start)
    title_html = f'''<h3 align="center" style="font-size:20px"><b>{title} ({date.strftime('%Y-%m-%d')})</b></h3>'''
    folium_map.get_root().html.add_child(folium.Element(title_html))

    if normalized:
        choropleth = folium.Choropleth(
            geo_data=layer,
            data=layer,
            columns=['region', 'cases'],
            key_on='feature.properties.region',
            fill_color='YlGn',
            fill_opacity=0.7,
            line_opacity=0.2,
            bins=list(layer["cases"].quantile([0, 0.15, 0.3, 0.6, 0.8, 0.9, 0.95, 0.97, 0.99, 1])),
            legend_name=f'Prevalence (per {PREVALENCE_RATIO:,})',
            highlight=True,
            line_color='black').add_to(folium_map)

        folium.GeoJsonTooltip(
            fields=["region", "cases"],
            aliases=["Region:", f"Prevalence (per {PREVALENCE_RATIO:,}):"],
            localize=True,
            sticky=False,
            labels=True).add_to(choropleth.geojson)

    else:
        max_cases = layer["cases"].max()
        color = FOLIUM_COLOR[covid_map.covid_matcher.case_type]
        for _, row in layer.iterrows():
            if row["cases"] > 0:
                folium.CircleMarker(
                    location=[row["latitude"], row["longitude"]],
                    radius=25 * np.sqrt(row["cases"] / max_cases),
                    tooltip=folium.Tooltip(f'{row["region"]}<br>'
                                           f'{CASE_TYPE_LONG[covid_map.covid_matcher.case_type].capitalize()}: '
                                           f'{row["cases"]:,}'),
                    fill=True,
                    color=color,
                    fill_color=color).add_to(folium_map)

    return folium_map


def get_world_map(case_type, date=None, normalized=False, cumulative=True):
    """ Get Folium world map

    :param case_type:
    :param date: datetime string
    :param normalized: if True, normalized cases by country's population
    :param cumulative: if True, return cumulative cases, daily otherwise
    :return:
    """
    return get_folium_map(WorldCovidMap(case_type), date, normalized, cumulative, zoom_start=2)


def plot_cases(covid_matcher, regions, doubling_factor, cumulative, normalized, min_prevalence, use_plotly):
    """ Plot cases for a given region

    :param covid_matcher:
    :param regions:
    :param doubling_factor:
    :param cumulative:
    :param normalized:
    :param min_prevalence:
    :param use_plotly:
    :return:
    """

    covid_matcher.build_database()
    fig, axes = _get_subplot_axes(regions, covid_matcher.case_type, use_plotly)
    covid_cases = retrieve_cases(covid_matcher, regions, normalized, cumulative)

    if normalized:
        ylabel = f"Prevalence (per {PREVALENCE_RATIO:,})"
        legend_name = "Prevalence"
        hoverformat = HOVERFORMAT_NORMALIZED
        tickformat = TICKFORMAT_NORMALIZED
    else:
        ylabel = f"Number of {CASE_TYPE_LONG[covid_matcher.case_type]}"
        legend_name = f"{CASE_TYPE_LONG[covid_matcher.case_type].capitalize()}"
        hoverformat = HOVERFORMAT_ABSOLUTE
        tickformat = TICKFORMAT_ABSOLUTE

    if cumulative:
        legend = [f"Situation where {CASE_TYPE_LONG[covid_matcher.case_type]} double every %.f days"
                  % doubling_factor, f"COVID-19 {CASE_TYPE_LONG[covid_matcher.case_type]}"]
        title = f"COVID-19 {CASE_TYPE_LONG[covid_matcher.case_type]} vs. situations where " \
                f"{CASE_TYPE_LONG[covid_matcher.case_type]} double every {doubling_factor} days"
    else:
        legend = [f"Daily increase of COVID-19 {CASE_TYPE_LONG[covid_matcher.case_type]}"]
        title = f"Daily increase of COVID-19 {CASE_TYPE_LONG[covid_matcher.case_type]}"

    for ax_id, (country, cases) in enumerate(covid_cases.items()):

        cases = cases[cases >= min_prevalence]
        doubling_cases = _get_doubling_cases(cases, doubling_factor)

        if use_plotly:
            row = ax_id // SUBPLOT_NB_COLS + 1
            col = SUBPLOT_NB_COLS - ((ax_id + 1) % SUBPLOT_NB_COLS)
            if cumulative:
                fig.add_trace(go.Scatter(x=cases.index, y=cases, mode="lines", legendgroup="group2",
                                         name=legend_name, line=dict(color="crimson")), row=row, col=col)
                fig.add_trace(go.Scatter(x=doubling_cases.index, y=doubling_cases, mode="lines", legendgroup="group1",
                                         name=f"Every {doubling_factor} days", line=dict(color="royalblue")),
                              row=row, col=col)
                fig.update_yaxes(title_text=ylabel, hoverformat=hoverformat, tickformat=tickformat, type='log',
                                 row=row, col=col)
            else:
                fig.add_trace(go.Bar(x=cases.index, y=cases, legendgroup="group",
                                     name="Daily increase"), row=row, col=col)
                fig.update_yaxes(title_text=ylabel, hoverformat=hoverformat, tickformat=tickformat, row=row, col=col)

        else:

            if cumulative:
                for case in [doubling_cases, cases]:
                    axes[ax_id].plot(case)
                axes[ax_id].set_yscale("log")
            else:
                axes[ax_id].bar(cases)

            axes[ax_id].set_ylabel(ylabel)
            axes[ax_id].set_title(country)
            axes[ax_id].legend(legend)

            # format the ticks
            day_of_month = mdates.DayLocator(interval=max(int(cases.size / 4), 1))
            axes[ax_id].xaxis.set_major_locator(day_of_month)

    if not use_plotly:
        plt.subplots_adjust(hspace=0.35)
    else:
        fig.update_layout(title_text=title, hovermode="x unified", showlegend=False,
                          height=max(len(regions) // SUBPLOT_NB_COLS * 300, 600))
        fig.show()


def plot_country_cases(countries, case_type, doubling_factor=4, cumulative=True, normalized=False, min_prevalence=0,
                       use_plotly=True):
    """ Plot Covid-19 countrycases

    :param countries: list of valid country names
    :param case_type: {'deaths', 'confirmed [cases]', 'recovered [cases]'}
    :param doubling_factor: pace (number of days) at which theoretical cases double
    :param cumulative: if True, show cumulative cases, daily increase otherwise
    :param normalized: if True, show prevalence, absolute number of cases otherwise
    :param min_prevalence: minimum prevalence for plotting cases (per-thousand or absolute)
    :param use_plotly: if True, use plotly for plots
    :return:
    """
    return plot_cases(WorldCovidMatcher(case_type), CountryCollection(countries), doubling_factor,
                      cumulative, normalized, min_prevalence, use_plotly)


def plot_pace(covid_matcher, regions, normalized, cumulative, plot_type, do_offset, offset_value,
              min_prevalence, use_plotly):

    covid_matcher.build_database()
    covid_cases = retrieve_cases(covid_matcher, regions, normalized, cumulative)
    if cumulative:
        desc = "cumulative"
    else:
        desc = "daily"

    title = f"Epidemic pace ({desc} {CASE_TYPE_LONG[covid_matcher.case_type]}) among countries/regions"
    plot_type = check_string(plot_type, ('linear', 'log'))

    if normalized:
        xlabel = f"Time (days), origin at {offset_value} per {PREVALENCE_RATIO:,}"
        ylabel = f"{CASE_TYPE_LONG[covid_matcher.case_type].capitalize()} (per {PREVALENCE_RATIO:,})"
        hoverformat = HOVERFORMAT_NORMALIZED
        tickformat = TICKFORMAT_NORMALIZED
    else:
        xlabel = f"Time (days), origin at {offset_value} {CASE_TYPE_LONG[covid_matcher.case_type]}"
        ylabel = f"{CASE_TYPE_LONG[covid_matcher.case_type].capitalize()}"
        hoverformat = HOVERFORMAT_ABSOLUTE
        tickformat = TICKFORMAT_ABSOLUTE

    if use_plotly:
        fig = go.Figure()
    else:
        fig, ax = plt.subplots()
        ax.set_yscale(plot_type)
        ax.set_title(title)
        ax.set_ylabel(ylabel)
        plt.grid(True, which='both')

    for country, cases in covid_cases.items():

        cases = cases[cases >= min_prevalence]

        if do_offset:
            try:
                offset_date = cases[cases >= offset_value].index[0]
            except IndexError:
                raise OffsetError("Offset value (= %.3f) is greater than the max prevalence/number of cases (= %.3f)"
                                  % (offset_value, cases[-1]))
            cases.index -= offset_date
            cases.index = cases.index.days

        if use_plotly:
            fig.add_trace(go.Scatter(x=cases.index, y=cases, mode='lines', name=country))
        else:
            ax.plot(cases)

    if use_plotly:
        if do_offset:
            xaxis = dict(title=xlabel, ticksuffix=' days')
        else:
            xaxis = dict(title='')
        fig.update_layout(title=title,
                          yaxis=dict(title=ylabel, type=plot_type, hoverformat=hoverformat, tickformat=tickformat),
                          xaxis=xaxis, height=640, hovermode="x unified")
        fig.show()
    else:
        ax.legend(regions.name)
        if not do_offset:
            day_of_month = mdates.DayLocator(interval=int(max([len(cases) for _, cases in covid_cases.items()]) / 4))
            ax.xaxis.set_major_locator(day_of_month)
        else:
            ax.set_xlabel(xlabel)


def plot_country_pace(countries, case_type, normalized=True, plot_type="log", cumulative=True,
                      do_offset=False, offset_value=0, min_prevalence=0, use_plotly=True):
    """ Plot case occurrence pace of given countries on the same figure

    :param countries:
    :param case_type:
    :param normalized: (bool)
    :param plot_type: {"normal", "log"}
    :param cumulative:
    :param do_offset: (bool) offset at min_prevalence value
    :param offset_value: (per-thousand)
    :param min_prevalence:
    :param use_plotly: if True, use plotly for plots
    :return:
    """
    return plot_pace(WorldCovidMatcher(case_type), CountryCollection(countries), normalized, cumulative,
                     plot_type, do_offset, offset_value, min_prevalence, use_plotly)


if __name__ == "__main__":
    from utils.sys.timer import Timer
    with Timer() as t:
        # plot_country_pace(["China", "Iran", "Italy", "France", "US"], case_type="deaths", normalized=False,
        #                   do_offset=True)
        # plot_country_pace(["China", "Iran", "US", "France", "spain", "Italy"], "deaths",
        #                   normalized=False, do_offset=True, min_prevalence=0)
        # plot_country_cases(["France", "Spain"], case_type="deaths", normalized=True, cumulative=True, use_plotly=True)
        get_world_map("deaths", normalized=True)

    print("total time: %s" % t)
