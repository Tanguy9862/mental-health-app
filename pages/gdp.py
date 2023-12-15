import dash
import dash_mantine_components as dmc
import pandas as pd
import plotly.express as px
from dash import html, dcc, Input, Output, State, callback
from dash_iconify import DashIconify

from utils.ga_utils import create_country_title
from utils.process_data import all_disorders_dataframes
from utils.utils_config import FIG_CONFIG_WITH_DOWNLOAD
from utils.gdp_bubble import create_bubble

anxiety_gdp = all_disorders_dataframes['Anxiety'].prevalence_and_gdp

income_levels = [
    'Low-income countries',
    'Lower-middle-income countries',
    'Upper-middle-income countries',
    'High-income countries'
]

###################
anxiety_gdp_country = anxiety_gdp[anxiety_gdp["Continent"] != "Unknown"].sort_values(by="Year")
anxiety_gdp_groups = anxiety_gdp[anxiety_gdp["Continent"] == "Unknown"].sort_values(by="Year")

depressive_gdp = all_disorders_dataframes['Depressive'].prevalence_and_gdp
depressive_gdp_country = depressive_gdp[depressive_gdp["Continent"] != "Unknown"].sort_values(by="Year")
depressive_gdp_groups = depressive_gdp[depressive_gdp["Continent"] == "Unknown"].sort_values(by="Year")

pop_per_country = anxiety_gdp[['Entity', 'Population (historical estimates)']]

pd.set_option('display.max_columns', None)

dash.register_page(
    __name__,
    path='/disorder-gdp',
    order=2,
    title='Mental Health - GDP Analysis'
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
                                    persistence=True
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
                                dmc.Switch(
                                    onLabel=DashIconify(icon='fluent-mdl2:world', height=15),
                                    offLabel=DashIconify(icon='grommet-icons:money', height=15),
                                    size='md',
                                    color='violet',
                                    id='switch-continent-incomes',
                                    persistence=True,
                                    persistence_type='session',
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
                        dcc.Loading(
                            dcc.Graph(id="bubble-fig", config=FIG_CONFIG_WITH_DOWNLOAD),
                            color='#967bb6',
                            type='circle')
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
            mt='lg'
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
    return dmc.MultiSelect(
        label=None,
        placeholder='Select a continent..',
        id='gdp-select-continent',
        persistence=True,
        persistence_type='session',
        data=sorted([
            {'value': continent, 'label': continent}
            for continent in all_disorders_dataframes[disorder_name].prevalence_by_country['Continent'].unique()
            if continent != 'Unknown'
        ], key=lambda x: x['value']),
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
    Output('bubble-fig', 'figure'),
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

    fig = create_bubble(
        df=df,
        switcher=switcher
    )

    return fig


@callback(
    Output('gdp-select-continent', 'disabled'),
    Input('switch-continent-incomes', 'checked'),
    prevent_initial_call=True
)
def update_disabled_state_select_continent(checked):
    if checked:
        return True
    return False

# @callback(
#     Output("graph", "figure"),
#     Output("filter-text", "children"),
#     Input("select-disease", "value"),
#     Input("filter-switch", "checked")
# )
# def update_graph(selected_disease, switch_checked):
#
#     if selected_disease == 'Anxiety':
#         df = anxiety_gdp_groups if switch_checked else anxiety_gdp_country
#     elif selected_disease == 'Depressive':
#         df = depressive_gdp_groups if switch_checked else depressive_gdp_country
#     else:
#         df = anxiety_gdp_groups if switch_checked else anxiety_gdp_country
#
#     if switch_checked:
#         # Scatter plot adapté aux variables pour les pays de continent unknown
#         scatter_plot = px.scatter(
#             df, x="GDP_per_capita_PPP_2017", y="Prevalence", animation_frame="Year",
#             animation_group="Entity", size="GDP_per_capita_PPP_2017", color="Entity",
#             hover_name="Entity", log_x=True
#         )
#     else:
#         # Scatter plot par défaut pour les autres pays
#         scatter_plot = px.scatter(
#             df, x="GDP_per_capita_PPP_2017", y="Prevalence", animation_frame="Year",
#             animation_group="Entity", size="GDP_per_capita_PPP_2017", color="Continent",
#             hover_name="Entity", log_x=True
#         )
#
#     # Ajouter la population au survol de la souris
#     scatter_plot.update_traces(
#         hovertemplate='<b>%{hovertext}</b><br>Population: %{text}',
#         text=df['Population (historical estimates)']
#     )
#
#     filter_text = "Filtre par groupe de pays" if switch_checked else "Filtre par pays"
#
#     return scatter_plot, filter_text
