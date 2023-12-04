import dash_mantine_components as dmc
from dash_iconify import DashIconify
import numpy as np
import datetime

from utils.utils_config import MAIN_TITLE_COLOR


def get_country_continent_name(figure_data):
    if figure_data:
        country_path = figure_data['points'][0]['customdata']
        return country_path[0], country_path[-1]


def create_country_title(text, id='', animation=None):
    return dmc.Title(
        text,
        id=id,
        color=MAIN_TITLE_COLOR,
        align='justify',
        order=2,
        className=animation
    )


def calculate_slope(y_values):
    x_values = np.arange(len(y_values))
    slope, *_ = np.polyfit(x_values, y_values, 1)
    return slope


def make_edit_icon(icon, id, tooltip, color=None):
    return dmc.Tooltip(
        [
            dmc.ActionIcon(
                DashIconify(icon=icon, color=color),
                id=id,
                variant='transparent',
            )
        ],
        label=tooltip,
        withArrow=True,
        transition='fade'
    )


def filter_dataframe(df, entities, year_range, column_to_filter):
    year_start, year_end = year_range
    return df.query(f'{column_to_filter} in @entities and Year >= @year_start and Year <= @year_end')


def get_last_added_entity(last_entity: list):
    last_continent, last_country = last_entity[-1][0], last_entity[-1][1]
    return last_country, last_continent


def update_last_entity(last_entity: list, new_continent: str, new_country: str):
    last_entity.append([new_continent, new_country])
