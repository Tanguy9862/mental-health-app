import dash
import pandas as pd
from dash import html, dcc, callback, Input, Output, State, clientside_callback, no_update, Patch
from dash.exceptions import PreventUpdate
import dash_mantine_components as dmc
from dash_iconify import DashIconify

from utils.process_data import all_disorders_dataframes
from utils.ga_choropleth import create_choropleth_fig
from utils.fig_config import FIG_CONFIG, BG_TRANSPARENT, MAIN_TITLE_COLOR

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


def get_country_name(figure_data):
    country_path = figure_data['points'][0]['customdata']
    return country_path[0] if isinstance(country_path, list) else country_path


def create_country_title(text, id='', animation=None):
    return dmc.Title(
        text,
        id=id,
        color=MAIN_TITLE_COLOR,
        align='justify',
        order=2,
        className=animation
    )


layout = html.Div(
    [
        dmc.Grid(
            [
                dmc.Col(
                    [
                        dmc.Group(
                            [
                                create_country_title(text='Exploring Mental Health Trends in'),
                                dmc.Group(
                                    [
                                        html.Div(id='country-title-container'),
                                        create_country_title(text=':'),
                                    ], spacing=1
                                ),
                                dmc.Select(
                                    id='select-disorder',
                                    value='Anxiety',
                                    data=sorted(
                                        [{'value': k, 'label': k} for k in all_disorders_dataframes.keys()],
                                        key=lambda x: x['value']
                                    ),
                                    size='md',
                                    variant='unstyled',
                                    style={'width': '10rem'},
                                    styles={
                                        'input': {
                                            'font-size': '1.5625rem',
                                            'color': '#4e3a8e',
                                            'font-weight': 'bold'
                                        },
                                        'item': {'font-size': '0.9rem'}
                                    },
                                    persistence=True,
                                    persistence_type='memory'
                                ),
                            ],
                            position='left',
                            spacing=7
                        )
                    ],
                    offsetLg=1,
                    lg=6
                )
            ],
            # style={'border': 'solid 2px blue'},
        ),
        dmc.Grid(
            [
                dmc.Col(
                    [
                        dmc.Container(dmc.Text('test'), id='left-container', px=0)
                    ],
                    # style={'border': 'solid 1px red'},
                    offsetLg=1,
                    lg=6
                ),
                dmc.Col(
                    [
                        dmc.Center(
                            [
                                dmc.FloatingTooltip(
                                    [
                                        dmc.Container(
                                            [dcc.Graph(id='choropleth-fig', style={'display': 'none'})],
                                            id='choropleth-container',
                                            px=0
                                        )
                                    ],
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
                    lg=5
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
    color = all_disorders_dataframes[disorder_name].pastel_color
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
        persistence=True,
        persistence_type='memory',
        color='white',
        style={'width': '50%'},
        styles={
            'bar': {'background-color': f'{color}', 'height': '3px'},
            'track': {'height': '3px'},
            'mark': {'display': 'None'},
            'markLabel': {'margin-top': '15px'},
            'thumb': {'background-color': f'{color}', 'border': f'solid 2px {color}'}
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
    Output('choropleth-fig', 'figure', allow_duplicate=True),
    Input('filtered-data-on-year', 'data'),
    State('select-disorder', 'value'),
    State('choropleth-fig', 'figure'),
    prevent_initial_call=True
)
def update_choropleth_fig(data, disorder_name, figure):
    data_to_df = pd.DataFrame(data)

    if figure:
        color_scale_seq = all_disorders_dataframes[disorder_name].color_scale

        patched_choropleth = Patch()
        patched_choropleth['data'][0]['customdata'] = data_to_df['Entity']
        patched_choropleth['data'][0]['locations'] = data_to_df['Code']
        patched_choropleth['data'][0]['z'] = data_to_df['Value']
        patched_choropleth['layout']['coloraxis']['colorscale'] = [
            [i / (len(color_scale_seq) - 1), color] for i, color in enumerate(color_scale_seq)
        ]

        return no_update, patched_choropleth

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
    ], no_update


@callback(
    Output('country-title-container', 'children'),
    Input('choropleth-fig', 'clickData'),
    State('select-disorder', 'value'),
    prevent_initial_call=True
)
def update_main_title(data, disorder_name):
    if data:
        country = get_country_name(data)
        return create_country_title(country, 'country-title-container', 'animate__animated animate__flash')

    random_country = all_disorders_dataframes[disorder_name].prevalence_by_country['Entity'].sample(n=1).iloc[0]
    return create_country_title(random_country, 'country-title-container', 'animate__animated animate__flash')


@callback(
    Output('left-container', 'children'),
    Input('country-title-container', 'children'),
    Input('choropleth-fig', 'clickData'),
    prevent_initial_call=True
)
def update_left_content(initial_country_title, data):
    if data:
        country = get_country_name(data)
        print(f'new country: {country}')
    else:
        print(f'initial country title: {initial_country_title}')

    return no_update


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
        country, prevalence = get_country_name(data), data['points'][0]['z']

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
