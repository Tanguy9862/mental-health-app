import dash
import dash_mantine_components as dmc
import pandas as pd
import plotly.express as px
from dash import html, dcc, Input, Output, State, callback, ClientsideFunction, clientside_callback
from dash_iconify import DashIconify

from utils.ga_utils import create_country_title, update_no_data
from utils.process_data import all_disorders_dataframes
from utils.utils_config import FIG_CONFIG_WITH_DOWNLOAD, add_loading_overlay, HIDE, STORAGE_SESSION
from utils.gdp_bubble import create_bubble
from utils.gdp_utils import income_levels

all_cols = all_disorders_dataframes['Anxiety'].prevalence_and_gdp.columns
# pd.set_option('display.max_columns', None)

dash.register_page(
    __name__,
    path='/disorder-gdp',
    order=2,
    title='Mental Health - GDP Analysis',
    description="""
    Examine the correlation between economic factors, such as GDP, and the prevalence of mental health disorders. 
    Understand how economic development influences mental health across various regions
    """,
    image='miniature.png'
)

layout = html.Div(
    [
        dmc.Grid(
            [
                dmc.Col(
                    [
                        dmc.Group(
                            [
                                create_country_title('Exploring the Correlation between GDP and'),
                                dmc.Select(
                                    id='gdp-select-disease',
                                    data=[
                                        {'label': 'Anxiety', 'value': 'Anxiety'},
                                        {'label': 'Depressive', 'value': 'Depressive'}
                                    ],
                                    value='Anxiety',
                                    size='md',
                                    variant='unstyled',
                                    style={'width': '10rem'},
                                    styles={
                                        'input': {
                                            'font-size': '1.5625rem',
                                            'color': '#4e3a8e',
                                            'font-weight': 'bold',
                                            'text-decoration': 'underline'
                                        },
                                        'item': {'font-size': '0.9rem'}
                                    },
                                    persistence=True,
                                    persistence_type=STORAGE_SESSION
                                ),
                            ],
                            spacing=7
                        ),
                        dmc.Text(
                            "Explore the interplay between economic development, as measured by Gross Domestic Product "
                            "(GDP), and the prevalence of selected mental health disorders",
                            align='justify',
                            color='#4B4B4B',
                            mt='md'
                        )
                    ],
                    offsetLg=1,
                    lg=10
                )
            ]
        ),
        dmc.Grid(
            [
                dmc.Col(
                    [
                        dmc.Center(
                            [
                                dmc.Tooltip(
                                    [
                                        dmc.Switch(
                                            onLabel=DashIconify(icon='fluent-mdl2:world', height=15),
                                            offLabel=DashIconify(icon='grommet-icons:money', height=15),
                                            size='md',
                                            color='violet',
                                            id='switch-continent-incomes',
                                            persistence=True,
                                            persistence_type=STORAGE_SESSION,
                                        )
                                    ],
                                    label='Toggle to filter data by continents or income categories',
                                    transition='fade',
                                    withArrow=True
                                )
                            ]
                        )
                    ],
                    offsetLg=1,
                    lg=10,
                )
            ],
            mt='xl'
        ),
        dmc.Grid(
            [
                dmc.Col(
                    [
                        add_loading_overlay(
                            elements=[
                                html.Div(
                                    dcc.Graph(
                                        id='bubble-fig',
                                        figure=create_bubble(
                                            pd.DataFrame(columns=all_cols),
                                            switcher=False
                                        )
                                    ),
                                    id='bubble-container'
                                )
                            ]
                        )
                    ],
                    offsetLg=1,
                    lg=10
                )
            ],
            mt='lg'
        ),
        dmc.Grid(
            [
                dmc.Col(
                    [
                        dmc.Divider(label='Filter on a Continent', mb='lg'),
                        html.Div(id='gdp-select-container')
                    ],
                    offsetLg=1,
                    lg=10
                )
            ],
            mt='lg',
            mb=125
        )
    ],
    id='gdp-container',
    className='animate__animated animate__fadeIn animate__slow'
)


@callback(
    Output('gdp-select-container', 'children'),
    Input('gdp-select-disease', 'value')
)
def update_select_list_continent(disorder_name):
    all_entities = sorted([
        {'value': continent, 'label': continent}
        for continent in all_disorders_dataframes[disorder_name].prevalence_by_country['Continent'].unique()
        if continent != 'Unknown'
    ], key=lambda x: x['value'])

    all_continents = list(set([continent for entity in all_entities for continent in entity.values()]))

    return dmc.MultiSelect(
        label=None,
        value=all_continents,
        placeholder='Select a continent..',
        id='gdp-select-continent',
        persistence=True,
        persistence_type=STORAGE_SESSION,
        data=all_continents,
        style={'width': '100%'},
        styles={
            'input': {
                'background-color': 'rgba(0,0,0,0)',
                'border': 'none'
            },
            'item': {
                'font-size': '0.9rem',
            }
        },
    )


@callback(
    Output('bubble-container', 'children'),
    Input('gdp-select-disease', 'value'),
    Input('switch-continent-incomes', 'checked'),
    Input('gdp-select-continent', 'value'),
    prevent_initial_call=True
)
def update_bubble_fig(disorder_name: str, switcher: bool, selected_continents: list):
    df = all_disorders_dataframes[disorder_name].prevalence_and_gdp.sort_values(by='Year')

    # Filter on income levels or continents
    if switcher:
        df = df.query('Entity in @income_levels')
    else:
        df = df.query("Continent != 'Unknown' and Continent in @selected_continents")

    is_df_empty = df.empty
    if is_df_empty:
        return update_no_data(text='Please select continents from the dropdown list to display data.')

    fig = create_bubble(
        df=df,
        switcher=switcher
    )

    return dcc.Graph(id="bubble-fig", config=FIG_CONFIG_WITH_DOWNLOAD, figure=fig)


clientside_callback(
    ClientsideFunction(namespace='clientside', function_name='update_disabled_state_select_continent'),
    Output('gdp-select-continent', 'disabled'),
    Input('switch-continent-incomes', 'checked')
)
