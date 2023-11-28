import dash
from dash import html, callback, Output, Input, State
import dash_mantine_components as dmc
from dash_iconify import DashIconify
from pages.nav import navbar

GITHUB = 'https://github.com/tanguy9862'
CONTACT_ICON_WIDTH = 30

header = html.Div(
    dmc.Grid(
        [
            dmc.Col(
                [
                    dmc.Group(
                        [
                            dmc.ActionIcon(
                                DashIconify(icon='fluent:navigation-16-filled', width=30),
                                id='nav-btn',
                                # className='nav-container',
                            ),
                            dmc.Anchor(
                                [
                                    DashIconify(icon='uil:github', color='#8d8d8d', width=CONTACT_ICON_WIDTH)
                                ],
                                href=GITHUB
                            )
                        ],
                        position='apart'
                    ),
                    dmc.Drawer(
                        [navbar()],
                        title=None,
                        id='nav-drawer',
                        padding='md',
                        withCloseButton=False,
                        overlayOpacity=0.85,
                        shadow=False,
                        styles={
                            'drawer': {
                                'background-color': 'rgba(0,0,0,0)',
                            }
                        }
                    )
                ],
                offsetMd=1,
                md=10,
            )
        ],
        mt='md',
        mb=60
    )
)


@callback(
    Output('nav-drawer', 'opened'),
    Input('nav-btn', 'n_clicks'),
    prevent_initial_call=True
)
def toggle_drawer(n):
    return True
