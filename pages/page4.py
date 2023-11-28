import dash
from dash import html, dcc
import dash_mantine_components as dmc

dash.register_page(
    __name__,
    path='/page4',
    title='Page 4'
)

layout = dmc.Grid(
    [
        dmc.Col(
            [
                dmc.Title('Page 4 content', id='page4-title', className="animate__animated animate__fadeIn")
            ]
        )
    ],
    mb=100
)
