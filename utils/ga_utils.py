import dash_mantine_components as dmc
from dash_iconify import DashIconify
import numpy as np

mapping_list_functions = {
    'del-last-selected-country': lambda x: x.pop(),
    'del-all-selected-country': lambda x: x.clear(),
}


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


