import dash
from dash import html, dcc, Input, Output, State, callback, no_update
import dash_mantine_components as dmc
import pandas as pd
import plotly.express as px

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
                            "Have a look at mental health disorders prevalence by looking at different countries' GDP",
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
                        html.H4('Animated GDP and population over decades'),
                        html.P("Select an animation:"),
                        dcc.RadioItems(
                            id='selection',
                            options=[{'label': "GDP - Scatter", 'value': 'GDP - Scatter'},
                                     {'label': "Population - Bar", 'value': 'Population - Bar'}],
                            value='GDP - Scatter',
                        ),
                        dcc.Loading(dcc.Graph(id="graph",style={"width":"1500px","height":"500px"}), type="cube")
                    ],
                    offsetLg=1,
                    lg=5
                )
            ]
        ),
        dmc.Grid(
            [
                dmc.Col(
                    [
                        # Partie avec les filtres ici (si cela a du sens pour votre application)
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
    Output("graph", "figure"), 
    Input("selection", "value")
     # ça permet de ne pas déclencher le callback au chargement de la page
    # car en gros tous les callbacks au premier chargement de la page sont automatiquement déclenchés même si les
    # inputs ne sont pas trigger
)

def update_graph(selection):
    df = anxiety_gdp
    animations = {
        'GDP - Scatter': px.scatter(
            df, x="GDP_per_capita_PPP_2017", y="Prevalence", animation_frame="Year", 
            animation_group="Entity", size="Population (historical estimates)", color="Continent", 
            hover_name="Entity", log_x=True, size_max=55, 
            range_x=[1000,20000], range_y=[0,10]),
        'Population - Bar': px.bar(
            df, x="Continent", y="Population (historical estimates)", color="Continent", 
            animation_frame="Year", animation_group="Entity", 
            range_y=[0,4000000000]),
    }
    return animations[selection]

