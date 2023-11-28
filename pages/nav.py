import dash
from dash import html
import dash_mantine_components as dmc
from dash_iconify import DashIconify

all_icons = [
    'game-icons:globe',
    'mdi:events',
    'simple-line-icons:rocket',
    'simple-line-icons:rocket',
]


def navbar():
    return html.Div(
        [
            dmc.Anchor(
                "test",
                href='/'
            )
        ]
    )

