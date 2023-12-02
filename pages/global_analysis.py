import dash
import pandas as pd
import dash_mantine_components as dmc
import dash_extensions as de
from dash import html, dcc, callback, Input, Output, State, clientside_callback, no_update, Patch, ctx, ALL
from dash.exceptions import PreventUpdate
from dash_iconify import DashIconify

from utils.process_data import all_disorders_dataframes, continent_dict
from utils.ga_utils import calculate_slope, make_edit_icon, mapping_list_functions, filter_dataframe
from utils.ga_choropleth import create_choropleth_fig
from utils.ga_heatmap import create_heatmap
from utils.ga_tabs import tabs_heatmap, tabs_sankey
from utils.fig_config import FIG_CONFIG, BG_TRANSPARENT, MAIN_TITLE_COLOR, HIDE

url = 'https://lottie.host/f2933ddb-a454-4e35-bea0-de15f496c6c3/tgIm6ZNww2.json'
options = dict(loop=True, autoplay=True)

CHOROPLETH_INTERVAL = 50
SLIDER_YEAR_INCREMENT = 10
is_first_session = True

pd.set_option('display.max_rows', None)
pd.set_option('display.max_columns', None)

dash.register_page(
    __name__,
    path='/global-analysis',
    title='Mental Health - Analysis Dashboard'
)


def get_country_name(figure_data):
    if figure_data:
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
                                create_country_title(text='Exploring Mental Health Trends in', id='base-title'),
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
                                            'font-weight': 'bold',
                                            'text-decoration': 'underline'
                                        },
                                        'item': {'font-size': '0.9rem'}
                                    },
                                    persistence=True,
                                    persistence_type='session'
                                ),
                            ],
                            position='left',
                            spacing=7
                        ),
                        dmc.Text(
                            'Dive into specific categories to discover how location, age and sex contribute to the '
                            'prevalence of various mental health disorders.',
                            align='justify',
                            color='#4B4B4B',
                            mt='md'
                        )
                    ],

                    offsetLg=1,
                    lg=6
                )
            ],
        ),
        dmc.Grid(
            [
                dmc.Col(
                    [
                        dmc.Tabs(
                            [
                                dmc.TabsList(
                                    [
                                        dmc.Tab('Country and Continent Trends', value='heatmap'),
                                        dmc.Tab('Age and Gender Insights', value='sankey')
                                    ]
                                ),
                                dmc.TabsPanel(tabs_heatmap, value='heatmap'),
                                dmc.TabsPanel(tabs_sankey, value='sankey')
                            ],
                            value='heatmap',
                            color='grape'
                        ),
                        dmc.Divider(label='Quick Add: Select by Continent', mt='xl'),
                        dmc.Container(
                            [
                                dmc.Center(
                                    [
                                        dmc.CheckboxGroup(
                                            id='checkbox-continent',
                                            label=None,
                                            children=[
                                                dmc.Checkbox(
                                                    label=continent,
                                                    value=continent,
                                                )
                                                for continent in continent_dict.values()
                                            ]
                                        )
                                    ]
                                )
                            ],
                            mt='lg',
                            px=0
                        )
                    ],
                    offsetLg=1,
                    lg=6
                ),
                dmc.Col(
                    [
                        dmc.Group(
                            [
                                make_edit_icon(
                                    icon='lucide:undo',
                                    id='del-last-selected-country',
                                    tooltip='Remove the last country added'
                                ),
                                dmc.ActionIcon(
                                    DashIconify(icon='ph:play-pause-light', width=35),
                                    id='stop-interval',
                                    variant='transparent'
                                ),
                                make_edit_icon(
                                    icon='fluent:delete-12-regular',
                                    id='del-all-selected-country',
                                    color='red',
                                    tooltip='Clear all countries'
                                )
                            ],
                            position='center',
                            mb='xl'
                        ),
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
                            children=[dmc.Slider(id='year-slider', style=HIDE)],
                            px=0,
                            style={
                                'display': 'flex',
                                'flex-direction': 'column',
                                'align-items': 'center',
                            },
                            mt=50,
                        )
                    ],
                    lg=5
                )
            ],
            mt=35,
            mb=100
        ),
        dcc.Store(id='disorder-data'),
        dcc.Store(id='average-prevalence-per-country'),
        dcc.Store(id='annual-prevalence-per-country'),
        dcc.Store(id='selected-countries', data=[], storage_type='session')
    ],
    id='global-analysis-container',
    className='animate__animated animate__fadeIn animate__slow'
)


@callback(
    Output('disorder-data', 'data'),
    Input('select-disorder', 'value')
)
def update_selected_disorder_data(disorder_name):
    """
    Update data related to the disorder selected (anxiety, bipolar, ..)
    """
    return all_disorders_dataframes[disorder_name].prevalence_by_country.to_dict('records')


@callback(
    Output('range-slider-container', 'children'),
    Input('disorder-data', 'data'),
    State('select-disorder', 'value'),
    prevent_initial_call=True
)
def update_year_slider(_, disorder_name):
    """
    Update the Year Slider related to the min and max year of a specific disorder
    """
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
        persistence_type='session',
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
    Output('average-prevalence-per-country', 'data'),
    Input('year-slider', 'value'),
    State('disorder-data', 'data'),
    prevent_initial_call=True
)
def update_data_on_year(year_range, data):
    """
    Create a new subset from the main disorder data which is filtered on a specific year range
    """
    df = pd.DataFrame(data)
    filtered_on_year = df.query("@year_range[0] <= Year <= @year_range[1]")
    filtered_on_year_grouped = filtered_on_year.groupby(['Entity', 'Code'])['Value'].mean().reset_index()
    return filtered_on_year_grouped.to_dict('records')


@callback(
    Output('choropleth-container', 'children'),
    Output('choropleth-fig', 'figure', allow_duplicate=True),
    Input('average-prevalence-per-country', 'data'),
    State('select-disorder', 'value'),
    State('choropleth-fig', 'figure'),
    prevent_initial_call=True
)
def update_choropleth_fig(data, disorder_name, figure):
    """
    Update the choropleth figure with disorder data filtered on a specif year range
    """
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
    Output('selected-countries', 'data'),
    Input('choropleth-fig', 'clickData'),
    Input('del-last-selected-country', 'n_clicks'),
    Input('del-all-selected-country', 'n_clicks'),
    State('selected-countries', 'data'),
    State('select-disorder', 'value'),
    prevent_initial_call=True
)
def update_selected_countries(choropleth_data, _1, _2, current_countries, disorder_name):
    """
    Update the dcc.Store which contains the list of all selected countries
    """
    input_id = ctx.triggered_id

    # Get country on choropleth click
    if choropleth_data and input_id == 'choropleth-fig':
        new_country = get_country_name(choropleth_data)
        if new_country not in current_countries:
            current_countries.append(new_country)

    # Delete the last country selected or clear all the countries
    elif input_id.startswith('del') and current_countries:
        list_modifier = mapping_list_functions[input_id]
        list_modifier(current_countries)

    # Get a random country (initial load):
    elif not current_countries and not input_id:
        new_country = all_disorders_dataframes[disorder_name].prevalence_by_country['Entity'].sample(n=1).iloc[0]
        current_countries.append(new_country)

    return current_countries


@callback(
    Output('country-title-container', 'children'),
    Output('base-title', 'children'),
    Input('selected-countries', 'data'),
    prevent_initial_call=True
)
def update_country_title(selected_countries: list):
    """
    Update the main title based on the last selected country from the user
    """

    if selected_countries:
        return create_country_title(
            selected_countries[-1],
            'country-title-container',
            'animate__animated animate__flash'
        ), 'Exploring Mental Health Trends in'

    return None, 'Select a Country to Explore Mental Health Trends'


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
                    f'Avg. {disorder_name} Prevalence from {year_range[0]} to {year_range[1]}: '
                    f'{round(prevalence, 2)}%'
                )
            ],
            px=0
        ), 'rgba(11, 6, 81, 0.8)'

    raise PreventUpdate


@callback(
    Output('annual-prevalence-per-country', 'data'),
    Output('selected-countries', 'data', allow_duplicate=True),
    Input('selected-countries', 'data'),
    Input('disorder-data', 'data'),
    Input('year-slider', 'value'),
    Input('checkbox-continent', 'value'),
    State('annual-prevalence-per-country', 'data'),
    prevent_initial_call=True
)
def update_annual_prevalence_country(selected_countries, disorder_data, year_range, checkbox, old_annual_prevalence_df):
    """
    Update the annual prevalence country data.
    This callback is triggered when users click on countries (choropleth-map), edit the year interval (year-slider),
    edit the disorder data (disorder-data) or use checkbox to quickly add a continent (checkbox-continent).
    Finally, this will return a list which contains all the countries selected and will be used in another callback
    to build the charts (heatmap, sankey)
    """
    input_id = ctx.triggered_id
    df = pd.DataFrame(disorder_data)

    if input_id in {'selected-countries', 'disorder-data', 'year-slider'} and \
            all((selected_countries, disorder_data, year_range)):
        filtered_df = filter_dataframe(df, selected_countries, year_range, 'Entity')
        return filtered_df.to_dict('records'), no_update

    elif input_id == 'checkbox-continent' and all((disorder_data, year_range)):
        filtered_df = filter_dataframe(df, checkbox, year_range, 'Continent')
        concatenated_df = pd.concat([filtered_df, pd.DataFrame(old_annual_prevalence_df)]).drop_duplicates()
        new_selected_countries = concatenated_df['Entity'].unique().tolist()
        return concatenated_df.to_dict('records'), new_selected_countries

    if not selected_countries:
        return None, no_update

    raise PreventUpdate


@callback(
    Output('heatmap-container', 'children'),
    Input('annual-prevalence-per-country', 'data'),
    Input('switch-country-continent', 'checked'),
    prevent_initial_call=True
)
def update_heatmap_fig(filtered_data, switch_filter):
    if not filtered_data:
        return dmc.Container(children=[de.Lottie(url=url, options=options)], px=0, size=375)

    filtered_df = pd.DataFrame(filtered_data)
    disorder_name = filtered_df.iloc[0]['Disorder']
    grouping_field = (switch_filter and 'Continent') or 'Entity'  # Column to use when grouping filtered_df

    # Grouping by Continent and Year to compute the Mean per Continent before computing the slope
    if switch_filter:
        filtered_df = filtered_df.groupby(['Continent', 'Year'])['Value'].mean().reset_index()

    slope_by_entity = filtered_df.groupby(grouping_field)['Value'].apply(calculate_slope)
    sorted_entities = slope_by_entity.sort_values(ascending=False).index

    # Data management for plotting heatmap
    df_pivot = filtered_df.pivot(index=grouping_field, columns='Year', values='Value')
    df_normalized = df_pivot.apply(lambda x: (x - x.min()) / (x.max() - x.min()), axis=1).reindex(sorted_entities)

    return dcc.Graph(
        figure=create_heatmap(
            df=df_normalized,
            disorder_name=disorder_name,
            entities=sorted_entities,
            grouping_field='Country' if grouping_field == 'Entity' else grouping_field
        ),
        config=FIG_CONFIG
    )


@callback(
    Output('sankey-container', 'children'),
    Input('selected-countries', 'data'),
    Input('disorder-data', 'data'),
    Input('year-slider', 'value'),
    prevent_initial_call=True
)
def update_sankey_fig(selected_countries, disorder_data, year_range):
    input_id = ctx.triggered_id
    # print(f'input sankey: {input_id}')
    df = pd.DataFrame(disorder_data)

    ##############################
    if input_id and year_range:
        # fn utils filter df


        countries = selected_countries
        year_start, year_end = year_range[0], year_range[1]
        # Filter the data based on countries selection and year range
        filtered_df = df.query('Entity in @countries and Year >= @year_start and Year <= @year_end')
        # print(filtered_df)

    ########################

    return None


@callback(
    Output('switch-country-continent', 'disabled'),
    Input('selected-countries', 'data'),
    prevent_initial_call=True
)
def update_state_switcher(data):
    if not data:
        return True
    return False


@callback(
    Output('data-drawer', 'opened'),
    Input('about-data-management', 'n_clicks'),
    State('data-drawer', 'opened'),
    prevent_initial_call=True
)
def toggle_drawer(n, opened):
    return not opened


@callback(
    Output('choropleth-interval', 'max_intervals'),
    Input('stop-interval', 'n_clicks'),
    prevent_initial_call=True
)
def stop_animate_choropleth(n):
    if n % 2:
        return 0
    return -1


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
