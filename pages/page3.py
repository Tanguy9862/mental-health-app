import dash
from dash import html, dcc
import dash_mantine_components as dmc

dash.register_page(
    __name__,
    path='/page3',
    title='Page 3'
)

layout = dmc.Grid(
    [
        dmc.Col(
            [
                dmc.Title('Page 3 content', id='page3-title', className="animate__animated animate__fadeIn")
            ]
        )
    ],
    mb=100
)
