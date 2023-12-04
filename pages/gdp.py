import dash
from dash import html, dcc, Input, Output, State, callback, no_update
import dash_mantine_components as dmc
import pandas as pd

from utils.ga_utils import create_country_title
from utils.process_data import all_disorders_dataframes

anxiety_gdp = all_disorders_dataframes['Anxiety'].prevalence_and_gdp
depressive_gdp = all_disorders_dataframes['Depressive'].prevalence_and_gdp

pd.set_option('display.max_columns', None)
print(f'Anxiety gpd df:\n{anxiety_gdp}')
print(f'Depressive gpd df:\n{depressive_gdp}')

dash.register_page(
    __name__,
    path='/disorder-gdp',
    order=2,
    title='Mental Health - GDP'
)

layout = html.Div(
    [
        dmc.Grid(
            [
                dmc.Col(
                    [
                        create_country_title('Exploring the Correlation between GDP and Mental Health Disorder'),
                        dmc.Text(
                            'text descriptif',
                            align='justify',
                            color='#4B4B4B',
                            mt='md'
                        )
                    ],
                    offsetLg=1,
                    lg=6
                )
            ]
        ),
        dmc.Grid(
            [
                dmc.Col(
                    [
                        'votre code ici (partie gauche)',
                        dmc.Button('Click', id='click-btn'),
                        dmc.Container(px=0, id='demo-container')
                    ],
                    offsetLg=1,
                    lg=5,
                    style={'border': 'solid 1px red'}
                ),
                dmc.Col(
                    [
                        'votre code ici (partie droite)'
                    ],
                    offsetLg=1,
                    lg=5,
                    style={'border': 'solid 1px blue'}
                )
            ],
            mt=35
        ),
        dmc.Grid(
            [
                dmc.Col(
                    [
                        'partie avec les filtres ici ? ou au début si ça rend mieux'
                    ],
                    offsetLg=1,
                    style={'border': 'solid 1px green'}
                )
            ],
            mt='xl'
        )
    ],
    id='gdp-container',
    className='animate__animated animate__fadeIn animate__slow'
)


# toujours 2 lignes vides (au-dessus et en-dessous) entre un callback/fonction et un élément en-dessous/dessus (conventions)
@callback(
    Output('demo-container', 'children'),
    Input('click-btn', 'n_clicks'),
    prevent_initial_call=True  # ça permet de ne pas déclencher le callback au chargement de la page
    # car en gros tous les callbacks au premier chargement de la page sont automatiquement déclenchés même si les
    # inputs ne sont pas trigger
)
def update_container(n):
    return n

