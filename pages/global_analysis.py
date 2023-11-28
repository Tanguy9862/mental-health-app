import dash
from dash import html, dcc, callback, Input, Output, State, clientside_callback
import dash_mantine_components as dmc
from dash_iconify import DashIconify

from utils.process_data import anxiety_by_country
from utils.ga_choropleth import create_choropleth_fig
from utils.fig_config import FIG_CONFIG, BG_TRANSPARENT

anxiety_by_country = anxiety_by_country.query("Year == 1990")
anxiety_by_country = anxiety_by_country.dropna(subset=['Code'])
# print(anxiety_by_country)

CHOROPLETH_INTERVAL = 50

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
                        )
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
                                    [
                                        dcc.Interval(id='choropleth-interval', interval=CHOROPLETH_INTERVAL),
                                        dcc.Graph(
                                            figure=create_choropleth_fig(anxiety_by_country),
                                            config=FIG_CONFIG,
                                            id='choropleth-fig',
                                            className='graph-container',
                                            responsive=True
                                        )
                                    ],
                                    label=None,
                                    color=BG_TRANSPARENT,
                                    id='choropleth-tooltip'
                                )
                            ]
                        )
                    ],
                    # style={'border': 'solid 1px green'},
                    md=5
                )
            ]
        )
    ],
    # px=0,
    id='global-analysis-container',
    className='animate__animated animate__fadeIn animate__slow'
)


@callback(
    Output('choropleth-tooltip', 'label'),
    Output('choropleth-tooltip', 'color'),
    Input('choropleth-fig', 'hoverData'),
    prevent_initial_call=True
)
def update_choropleth_tooltip(data):
    if data:
        # print(data)
        country, prevalence, country = data['points'][0]['location'], data['points'][0]['z'], data['points'][0]['customdata'][0]
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
                    spacing='sm'
                ),
                dmc.Text(f'Prevalence: {round(prevalence, 2)}%')
            ],
            px=0
        ), 'rgba(11, 6, 81, 0.8)'


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
