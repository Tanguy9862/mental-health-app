import dash
from dash import html, callback, Output, Input, State
import dash_mantine_components as dmc
from dash_iconify import DashIconify

GITHUB = 'https://github.com/Tanguy9862/mental-health-app'
CONTACT_ICON_WIDTH = 30

header = html.Div(
    dmc.Grid(
        [
            dmc.Col(
                [
                    dmc.Group(
                        [
                            dmc.Anchor(
                                [
                                    DashIconify(icon='uil:github', color='#8d8d8d', width=CONTACT_ICON_WIDTH)
                                ],
                                href=GITHUB
                            )
                        ],
                        position='right'
                    )
                ],
                offsetMd=1,
                md=10,
            )
        ],
        mt='md',
        mb=35
    )
)
