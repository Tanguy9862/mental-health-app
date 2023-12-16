import dash
import dash_mantine_components as dmc
from dash import html, dcc, callback, Input, Output, State, ALL
from dash.exceptions import PreventUpdate
from dash_iconify import DashIconify
from dash_extensions import EventListener

from assets.header import header

app = dash.Dash(
    __name__,
    use_pages=True,
    suppress_callback_exceptions=True,
    update_title=None,
    title='Mental Health Analysis',
    meta_tags=[
        {
            "name": "description",
            "content": """Explore an interactive mental health data platform that offers a deep dive into the 
            prevalence and management of anxiety and depressive disorders worldwide. With dynamic selection of 
            conditions and demographics, gain unique insights into mental health trends from global surveys, 
            including country and continent-specific analysis, and age and gender breakdowns."""
        },
        {
            "name": "keywords",
            "content": """global mental health, interactive data dashboard, anxiety trends, depressive disorders 
            analysis, mental health surveys, demographic insights, economic factors, health data visualization, 
            country-specific mental health, continent trends, age and gender prevalence, condition-specific research, 
            mental health management"""
        }
    ]
)

server = app.server

pages_order = [page['path'] for page in dash.page_registry.values() if page['module'] != 'pages.not_found_404']
style_btn_nav = {
    'color': '#7159a3',
    'border': 'solid 1px #7159a3'
}

app.layout = html.Div(
    [
        EventListener(id='event-listener'),
        header,
        dash.page_container,
        dmc.Footer(
            [
                dmc.Group(
                    [
                        dmc.ActionIcon(
                            DashIconify(icon='grommet-icons:previous'),
                            id='prev-button',
                            variant='outline',
                            radius='lg',
                            style=style_btn_nav
                        ),
                        *[
                            dmc.Anchor(
                                [
                                    dmc.ActionIcon(
                                        DashIconify(
                                            icon='radix-icons:dot-filled',
                                            color='#7159a3',
                                            id={'type': 'nav-dot', 'index': i},
                                            width=15
                                        ),
                                        className='nav-dot',
                                        variant="transparent"
                                    )
                                ],
                                href=page['path']
                            ) for i, page in enumerate(dash.page_registry.values()) if page['module'] != 'pages.not_found_404'
                        ],
                        dmc.ActionIcon(
                            DashIconify(icon='grommet-icons:next'),
                            id='next-button',
                            variant='outline',
                            radius='lg',
                            style=style_btn_nav
                        ),
                    ],
                    position='center'
                )
            ],
            # mt=100,
            height=40,
            fixed=True,
            style={'background-color': 'rgba(0,0,0,0)', 'border': 'none'}
        ),
        dcc.Location(id='url', refresh='callback-nav'),
        html.Div(id="keydown-listener", style={"outline": "none"})
    ]
)


@app.callback(
    Output('url', 'pathname'),
    Input('prev-button', 'n_clicks'),
    Input('next-button', 'n_clicks'),
    Input('event-listener', 'n_events'),
    State('event-listener', 'event'),
    State('url', 'pathname'),
    prevent_initial_call=True
)
def navigate(_1, _2, _3, event, current_path):
    ctx = dash.callback_context
    button_id = ctx.triggered[0]['prop_id'].split('.')[0]

    if current_path not in pages_order:
        return dash.no_update

    current_index = pages_order.index(current_path)

    if button_id == 'event-listener':
        if event['key'] == 'ArrowLeft' and current_index > 0:
            return pages_order[current_index - 1]
        elif event['key'] == 'ArrowRight' and current_index < len(pages_order) - 1:
            return pages_order[current_index + 1]
    elif button_id == 'prev-button' and current_index > 0:
        return pages_order[current_index - 1]
    elif button_id == 'next-button' and current_index < len(pages_order) - 1:
        return pages_order[current_index + 1]

    return dash.no_update


@callback(
    Output({'type': 'nav-dot', 'index': ALL}, 'color'),
    Output({'type': 'nav-dot', 'index': ALL}, 'width'),
    Input('url', 'pathname'),
)
def update_nav_dots(pathname):
    current_index = pages_order.index(pathname) if pathname in pages_order else None
    new_colors = ['#967bb6' if i == current_index else '#E0E0E0' for i in range(len(pages_order))]
    new_widths = [23 if i == current_index else 16 for i in range(len(pages_order))]
    return new_colors, new_widths


if __name__ == "__main__":
    app.run_server(debug=True)
