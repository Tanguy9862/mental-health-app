import dash
from dash import html, dcc, Input, Output, State, callback
import dash_mantine_components as dmc
import pandas as pd
import plotly.express as px

from utils.ga_utils import create_country_title
from utils.process_data import all_disorders_dataframes

anxiety_gdp = all_disorders_dataframes['Anxiety'].prevalence_and_gdp
anxiety_gdp_country = anxiety_gdp[anxiety_gdp["Continent"] != "Unknown"].sort_values(by="Year")
anxiety_gdp_groups = anxiety_gdp[anxiety_gdp["Continent"] == "Unknown"].sort_values(by="Year")

depressive_gdp = all_disorders_dataframes['Depressive'].prevalence_and_gdp
depressive_gdp_country = depressive_gdp[depressive_gdp["Continent"] != "Unknown"].sort_values(by="Year")
depressive_gdp_groups = depressive_gdp[depressive_gdp["Continent"] == "Unknown"].sort_values(by="Year")

pd.set_option('display.max_columns', None)
print(f'Anxiety gpd df:\n{anxiety_gdp}')
print(f'Anxiety per country gpd df:\n{anxiety_gdp_country}')
print(f'Anxiety per group gpd df :\n{anxiety_gdp_groups}')
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
                        ),
                        dmc.Select(id='select-disease',
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
                        dmc.Switch(
                            size="lg",
                            radius="sm",
                            label="Country/Group Of country Filter",
                            id='filter-switch'
                        ),
                        html.Div(
                            id='filter-text',
                            children="Filtre par groupe de pays"  # Default text when switch is active
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
                        html.H2('Animated GDP and population over decades'),
                        dcc.Loading(dcc.Graph(id="graph"), type="circle")
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


@callback(
    [Output("graph", "figure"),
     Output("filter-text", "children")],
    [Input("select-disease", "value"),
     Input("filter-switch", "checked")]
)
def update_graph(selected_disease, switch_checked):
    if selected_disease == 'Anxiety':
        df = anxiety_gdp_groups if switch_checked else anxiety_gdp_country
    elif selected_disease == 'Depressive':
        df = depressive_gdp_groups if switch_checked else depressive_gdp_country
    else:
        # Handle other diseases or default case
        df = anxiety_gdp_groups if switch_checked else anxiety_gdp_country  # You can change this to another default value or handle it accordingly
    
    animations = {
        'GDP - Scatter': px.scatter(
            df, x="GDP_per_capita_PPP_2017", y="Prevalence", animation_frame="Year",
            animation_group="Entity", size="GDP_per_capita_PPP_2017", color="Continent",
            hover_name="Entity", log_x=True),
    }

    filter_text = "Filtre par groupe de pays" if switch_checked else "Filtre par pays"
    
    return animations['GDP - Scatter'], filter_text
