import dash
import plotly.express as px
from random import choice
from dash import html, dcc, callback, Input, Output, State
import dash_mantine_components as dmc

from utils.ga_utils import create_country_title
from utils.process_surveys_data import merged_survey_df
from utils.sa_figures import create_bar_fig
from utils.sa_utils import filter_on_continent, filter_on_entity
from utils.utils_config import FIG_CONFIG_WITH_DOWNLOAD, add_loading_overlay, HIDE, STORAGE_SESSION
from utils.gdp_utils import income_levels

basic_cols = ['Entity', 'Code', 'Year', 'Continent']
all_questions = [question for question in merged_survey_df.columns if question not in basic_cols]
all_continents = [continent for continent in merged_survey_df['Continent'].unique() if continent != 'Unknown']

dash.register_page(
    __name__,
    path='/survey-analysis',
    order=3,
    title='Mental Health - Survey Analysis'
)

layout = html.Div(
    [
        dmc.Grid(
            [
                dmc.Col(
                    [
                        create_country_title('Insights from Global Mental Health Survey'),
                        dmc.Text(
                            """
                            Explore key findings and patterns from 2020 global mental health surveys, specifically 
                            focusing on anxiety and depressive disorders. Uncover trends in public perception, 
                            approaches to managing anxiety and depression, and the societal impact of these conditions 
                            during this period.
                            """,
                            align='justify',
                            color='#4B4B4B',
                            mt='md'
                        )
                    ],
                    offsetLg=1,
                    lg=9
                )
            ]
        ),
        dmc.Grid(
            [
                dmc.Col(
                    [
                        dmc.Select(
                            id='sa-select-question',
                            label='Select a question',
                            value=choice(all_questions),
                            data=sorted(
                                [{'value': question, 'label': question} for question in all_questions],
                                key=lambda x: x['label']
                            ),
                            persistence=True,
                            persistence_type=STORAGE_SESSION

                        )
                    ],
                    offsetLg=1,
                    lg=4
                ),
                dmc.Col(
                    [
                        dmc.Select(
                            id='sa-select-continent',
                            label='Select a country',
                            value=choice(all_continents),
                            data=sorted(
                                [{'value': continent, 'label': continent} for continent in all_continents],
                                key=lambda x: x['label']
                            ),
                            persistence=True,
                            persistence_type=STORAGE_SESSION

                        )
                    ],
                    lg=2
                ),
            ],
            mt='xl'
        ),
        dmc.Grid(
            [
                dmc.Col(
                    [
                        html.Div(id='question-title'),
                    ],
                    offsetLg=1,
                    span='content'
                ),
                dmc.Col(
                    [
                        html.Div(id='progress-container')
                    ],
                    span='auto',
                    pt=20,
                )
            ],
            mt=50,
        ),
        dmc.Grid(
            [
                dmc.Col(
                    [
                        dmc.Grid(
                            [
                                dmc.Col(
                                    [
                                        dmc.Stack(
                                            [
                                                dmc.Divider(label='Country Specific Rate'),
                                                add_loading_overlay(id='country-fig-container')
                                            ]
                                        ),
                                    ],
                                    lg=5,
                                ),
                                dmc.Col(
                                    [
                                        dmc.Stack(
                                            [
                                                dmc.Divider(label='Income Specific Rate', labelPosition='right'),
                                                add_loading_overlay(id='income-fig-container')
                                            ]
                                        )
                                    ],
                                    offsetLg=1,
                                    lg=5
                                )
                            ],
                            mt=35,
                            mb=100
                        )
                    ],
                    offsetLg=1,
                    lg=10
                )
            ]
        )
    ],
    id='survey-container',
    className='animate__animated animate__fadeIn animate__slow'
)


@callback(
    Output('question-title', 'children'),
    Output('progress-container', 'children'),
    Input('sa-select-question', 'value'),
    Input('sa-select-continent', 'value'),
)
def update_question_title(question, continent):
    survey_filtered = merged_survey_df[basic_cols + [question]]
    survey_continent_rates = round(filter_on_entity(survey_filtered, continent)[question].iloc[0])

    title = create_country_title(
        text=f'{question} in {continent}',
        order=3,
        id='question-title',
        animation='animate__animated animate__flash'
    )

    progress_bar = dmc.Progress(
        value=survey_continent_rates,
        color='teal',
        size='lg',
        sections=[
            {
                'value': survey_continent_rates,
                'color': 'teal',
                'label': f'{survey_continent_rates}%',
                'tooltip': 'Represents the proportion of the surveyed population that reported '
                           'experiencing the condition'
            }
        ],
        style={'width': '50%'}
    )

    return title, progress_bar


@callback(
    Output('country-fig-container', 'children'),
    Output('income-fig-container', 'children'),
    Input('sa-select-question', 'value'),
    Input('sa-select-continent', 'value'),
)
def update_country_fig(question, continent):
    survey_filtered = merged_survey_df[basic_cols + [question]]

    # Get all countries:
    survey_filtered_country = filter_on_continent(survey_filtered, continent)
    fig_country = create_bar_fig(
        survey_filtered_country,
        x='Entity',
        y=question,
        continent=continent,
        y_ticksuffix='   ',
        color_seq=px.colors.sequential.Agsunset_r
    )

    # Get value for incomes categories:
    survey_filtered_income = filter_on_entity(survey_filtered, income_levels)
    fig_income = create_bar_fig(
        survey_filtered_income,
        x='Entity',
        y=question,
        continent=continent,
        width_traces=0.1,
        side_yaxis='right',
        y_tickprefix='   ',
        autorange='reversed',
        color_seq=px.colors.sequential.Teal
    )

    country_graph_object = add_loading_overlay(
        dcc.Graph(figure=fig_country, config=FIG_CONFIG_WITH_DOWNLOAD, id='country-rate')
    )

    income_graph_object = dcc.Graph(figure=fig_income, config=FIG_CONFIG_WITH_DOWNLOAD, id='income-rate')

    return country_graph_object, income_graph_object
