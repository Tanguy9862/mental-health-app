import dash
from dash import html, dcc, callback, Input, Output, State, ctx, no_update, clientside_callback
from dash_iconify import DashIconify
from dash.exceptions import PreventUpdate
import dash_mantine_components as dmc
import dash_extensions as de

from utils.overview_figures import disorder_bar_fig, graph_functions, prevalence_by_disorder
from utils.overview_accordion import disorders_accordion
from utils.utils_config import FIG_CONFIG_WITH_DOWNLOAD, BG_TRANSPARENT, MAIN_TITLE_COLOR

dash.register_page(
    __name__,
    path='/',
    order=0,
    title='Mental Health - Overview',
)


def estimate_case(estimate, disorder_name):
    return [
        dmc.Tooltip(
            label=f'Estimated affected people by {disorder_name} disorder in millions',
            children=[
                dmc.Group(
                    [
                        DashIconify(icon='fluent:people-team-16-regular', height=35,
                                    color=MAIN_TITLE_COLOR),
                        dmc.Title(f'{estimate}M', order=2, color=MAIN_TITLE_COLOR)
                    ],
                    position='center',
                    mb='lg',
                    id='group-estimate',
                ),
            ],
            withArrow=True,
            transition='fade'
        ),
    ]


layout = dmc.NotificationsProvider(
    [
        dmc.Grid(
            [
                dmc.Col(
                    [
                        dmc.Container(
                            [
                                dmc.Title(
                                    'Exploring the Impact of Demographic, Economic, and Geographic Factors on Mental '
                                    'Health Disorders',
                                    color=MAIN_TITLE_COLOR,
                                    align='justify',
                                    order=1
                                ),
                                dmc.Text(
                                    'This application delves into the world of mental health, analyzing how '
                                    'demographic, economic, and geographic factors influence the prevalence and '
                                    'treatment of mental disorders across various populations and regions. Utilizing '
                                    'data from reputable sources, we aim to uncover disparities and trends in mental'
                                    'health management, shedding light on the challenges and opportunities for'
                                    'improved care.',
                                    color='#4B4B4B',
                                    mt='lg',
                                    mb=40,
                                    align='justify'
                                ),
                                disorders_accordion
                            ],
                            px=0
                        )
                    ],
                    offsetMd=1,
                    md=6
                ),
                dmc.Col(
                    [
                        dmc.Stack(
                            [
                                dmc.Container(id='estimate-container', px=0, children=[html.Div(id='group-estimate')]),
                                dmc.FloatingTooltip(
                                    [dcc.Graph(figure=disorder_bar_fig, config=FIG_CONFIG_WITH_DOWNLOAD, id='disorder-fig')],
                                    label=None,
                                    width=275,
                                    color=BG_TRANSPARENT,
                                    id='fig-tooltip',
                                ),
                            ],
                            id='right-container',
                            align='center'
                        )
                    ],
                    md=5
                )
            ],
            justify='center',
            id='overview-container',
            className='animate__animated animate__fadeIn animate__slow'
        ),
        dmc.Container(id='notifications-container')
    ]
)


@callback(
    Output('fig-tooltip', 'label'),
    Output('fig-tooltip', 'color'),
    Output('estimate-container', 'children'),
    Input('disorder-fig', 'hoverData'),
)
def update_tooltip(fig_data):

    if fig_data:
        label = fig_data['points'][0]['label']
        return dmc.Container(
            [
                dmc.Text(f'{label} Disorder Prevalence (%)', italic=True, size='xs', color='white', mb=5),
                dcc.Graph(figure=graph_functions[label]())
            ],
            px=0
        ), 'rgba(11, 6, 81, 0.8)', estimate_case(
            prevalence_by_disorder.query('Disorder == @label')['EstimatedPeopleAffected'].iloc[0], label
        )
    else:
        return no_update, no_update, estimate_case(
            estimate=prevalence_by_disorder.query("Disorder == 'Anxiety'")['EstimatedPeopleAffected'].iloc[0],
            disorder_name='Anxiety'
        )


@callback(
    Output('notifications-container', 'children'),
    Input('notifications-container', 'id'),
)
def show_notifications(_):
    return [
        dmc.Notification(
            id='notif',
            title='Quick Navigation Tip',
            action='show',
            message=dmc.Container(
                [
                    "Use your keyboard's ", dmc.Kbd('←'), " and ", dmc.Kbd('→'), " to navigate"
                ],
                px=0
            ),
            autoClose=10000,
            radius='xl',
            icon=DashIconify(icon='material-symbols:privacy-tip-outline-rounded'),
        )
    ]


@callback(
    Output('group-estimate', 'className'),
    Input('disorder-fig', 'hoverData'),
    prevent_initial_call=True
)
def toggle_animation_estimate_case(_):
    return 'animate__animated animate__pulse animate__slow'

