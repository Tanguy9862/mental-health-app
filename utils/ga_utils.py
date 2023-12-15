import dash_mantine_components as dmc
from dash_iconify import DashIconify
import numpy as np
import dash_extensions as de
import datetime

from utils.utils_config import MAIN_TITLE_COLOR

url = 'https://lottie.host/f2933ddb-a454-4e35-bea0-de15f496c6c3/tgIm6ZNww2.json'
options = dict(loop=True, autoplay=True)


def update_no_data(text=None):
    return [
            dmc.Container(
                [de.Lottie(url=url, options=options)],
                px=0,
                size=375
            ),
            dmc.Text(text, color='#d3d3d3', italic=True, size='sm', align='center')
    ]


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
    if isinstance(year_range, list):
        year_start, year_end = year_range
        return df.query(f'{column_to_filter} in @entities and Year >= @year_start and Year <= @year_end')
    else:
        year = year_range
        return df.query(f'{column_to_filter} in @entities and Year == @year')


def get_last_added_entity(last_entity: list):
    last_continent, last_country = last_entity[-1][0], last_entity[-1][1]
    return last_country, last_continent


def update_last_entity(last_entity: list, new_continent: str, new_country: str):
    last_entity.append([new_continent, new_country])


def clean_duplicated_columns(df):
    df = df[[col for col in df.columns if not col.endswith('_y')]]
    df.columns = [col.replace('_x', '') for col in df.columns]
    return df
