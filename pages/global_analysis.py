import dash
import pandas as pd
from dash import html, dcc, callback, Input, Output, State, clientside_callback, no_update
from dash.exceptions import PreventUpdate
import dash_mantine_components as dmc
from dash_iconify import DashIconify

from utils.process_data import all_disorders_dataframes
from utils.ga_choropleth import create_choropleth_fig
from utils.fig_config import FIG_CONFIG, BG_TRANSPARENT

# anxiety_by_country = anxiety_disorder.prevalence_by_country.query("Year == 1990")
# anxiety_by_country = anxiety_by_country.dropna(subset=['Code'])
# print(anxiety_by_country)

CHOROPLETH_INTERVAL = 50
SLIDER_YEAR_INCREMENT = 10

dash.register_page(
    __name__,
    path='/global-analysis',
    title='Mental Health - Analysis Dashboard'
)

layout = html.Div(
    [
        dmc.Grid(
            [
                dmc.Col(
                    [
                        dmc.Title(
                            'Worldwide Mental Health Overview',
                            color='#4e3a8e',
                            align='justify',
                            order=2
                        ),
                        dmc.Select(
                            id='select-disorder',
                            value='Anxiety',
                            data=sorted(
                                [{'value': k, 'label': k} for k in all_disorders_dataframes.keys()],
                                key=lambda x: x['value']
                            )
                        ),
                    ],
                    offsetMd=1,
                    md=6
                )
            ],
            # style={'border': 'solid 2px blue'},
        ),
        dmc.Grid(
            [
                dmc.Col(
                    [

                    ],
                    # style={'border': 'solid 1px red'},
                    offsetMd=1,
                    md=6
                ),
                dmc.Col(
                    [
                        dmc.Center(
                            [
                                dmc.FloatingTooltip(
                                    [dmc.Container(id='choropleth-container', px=0)],
                                    label=None,
                                    color=BG_TRANSPARENT,
                                    id='choropleth-tooltip'
                                ),
                            ]
                        ),
                        dmc.Container(
                            id='range-slider-container',
                            px=0,
                            style={
                                'display': 'flex',
                                'flex-direction': 'column',
                                'align-items': 'center',
                            },
                            mt=50
                        )
                    ],
                    md=5
                )
            ]
        ),
        dcc.Store(id='disorder-data'),
        dcc.Store(id='filtered-data-on-year')
    ],
    id='global-analysis-container',
    className='animate__animated animate__fadeIn animate__slow'
)


@callback(
    Output('disorder-data', 'data'),
    Input('select-disorder', 'value')
)
def update_selected_disorder_data(disorder_name):
    return all_disorders_dataframes[disorder_name].prevalence_by_country.to_dict('records')


@callback(
    Output('range-slider-container', 'children'),
    Input('disorder-data', 'data'),
    State('select-disorder', 'value'),
    prevent_initial_call=True
)
def update_year_slider(_, disorder_name):
    disorder_df = all_disorders_dataframes[disorder_name].prevalence_by_country
    min_year, max_year = disorder_df['Year'].min(), disorder_df['Year'].max()

    return dmc.RangeSlider(
        id='year-slider',
        value=[min_year, max_year],
        min=min_year,
        max=max_year,
        minRange=1,
        marks=[
            {'value': i, 'label': i} for i in range(min_year, max_year + 2, SLIDER_YEAR_INCREMENT)
        ],
        color='white',
        style={'width': '50%'},
        styles={
            'bar': {'background-color': '#967bb6', 'height': '3px'},
            'track': {'height': '3px'},
            'mark': {'display': 'None'},
            'markLabel': {'margin-top': '15px'},
            'thumb': {'background-color': '#967bb6', 'border': 'solid 2px #967bb6'}
        }
    )


@callback(
    Output('filtered-data-on-year', 'data'),
    Input('year-slider', 'value'),
    State('disorder-data', 'data'),
    prevent_initial_call=True
)
def update_data_on_year(year_range, data):
    df = pd.DataFrame(data)
    filtered_on_year = df.query("@year_range[0] <= Year <= @year_range[1]")
    filtered_on_year_grouped = filtered_on_year.groupby(['Entity', 'Code'])['Value'].mean().reset_index()
    return filtered_on_year_grouped.to_dict('records')


@callback(
    Output('choropleth-container', 'children'),
    Input('filtered-data-on-year', 'data'),
    State('select-disorder', 'value'),
    prevent_initial_call=True
)
def update_choropleth_fig(data, disorder_name):
    data_to_df = pd.DataFrame(data)

    return [
        dcc.Graph(
            figure=create_choropleth_fig(
                data_to_df,
                color_scale=all_disorders_dataframes[disorder_name].color_scale
            ),
            config=FIG_CONFIG,
            id='choropleth-fig',
            className='graph-container',
            responsive=True
        ),
        dcc.Interval(id='choropleth-interval', interval=CHOROPLETH_INTERVAL),
    ]


@callback(
    Output('choropleth-tooltip', 'label'),
    Output('choropleth-tooltip', 'color'),
    Input('choropleth-fig', 'hoverData'),
    State('select-disorder', 'value'),
    State('year-slider', 'value'),
    prevent_initial_call=True
)
def update_choropleth_tooltip(data, disorder_name, year_range):
    if data:
        country, prevalence, country = data['points'][0]['location'], data['points'][0]['z'], \
            data['points'][0]['customdata'][0]

        return dmc.Container(
            [
                dmc.Group(
                    [
                        dmc.Text(country, weight=500),
                        DashIconify(
                            icon=f'emojione:flag-for-{country.lower().replace(" ", "-")}',
                            height=20,
                        )
                    ],
                    spacing='xs'
                ),
                dmc.Text(
                    f'Avg. {disorder_name} Disorder Prevalence from {year_range[0]} to {year_range[1]}: '
                    f'{round(prevalence, 2)}%'
                )
            ],
            px=0
        ), 'rgba(11, 6, 81, 0.8)'

    raise PreventUpdate


clientside_callback(
    """
    function(_, figure) {
        let rotation_lon = figure.layout.geo.projection.rotation.lon;
        let rotation_lat = figure.layout.geo.projection.rotation.lat;

        if (rotation_lon <= -180) {
            rotation_lon = 180;
        }

        if (rotation_lon >= 180) {
            rotation_lon = -180;
        }

        if (rotation_lat >= 90) {
            rotation_lat = 90;
        } else if (rotation_lat <= -90) {
            rotation_lat = -90;
        }

        if (Math.abs(0 - rotation_lat) < 0.01) {
            rotation_lat = 0;
        }

        const updatedFigure = Object.assign({}, figure);
        updatedFigure.layout.geo.projection.rotation.lon = rotation_lon + 0.5;
        updatedFigure.layout.geo.projection.rotation.lat = rotation_lat;

        return updatedFigure;
    }
    """,
    Output('choropleth-fig', 'figure'),
    Input('choropleth-interval', 'n_intervals'),
    State('choropleth-fig', 'figure'),
    prevent_initial_call=True
)
