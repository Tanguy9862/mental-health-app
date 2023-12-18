import plotly.express as px
from plotly import colors

from utils.utils_config import BG_TRANSPARENT, HOVERLABEL_TEMPLATE


def create_bubble(df, switcher):

    step_x = 5000
    step_y = 1

    max_x_range = [df['GDP'].min() - step_x, df['GDP'].max() + step_x]
    max_y_range = [df['Prevalence'].min() - step_y, df['Prevalence'].max() + step_y]

    if switcher:
        color_col = 'Entity'
        custom_data = ['Entity']
        hover_template = "<b>%{customdata[0]}</b><br>GDP: %{x}<br>Prevalence: %{y:.2f}%<extra></extra>"
    else:
        color_col = 'Continent'
        custom_data = ['Continent', 'Entity']
        hover_template = "<b>%{customdata[1]}</b><br>GDP: %{x}<br>Prevalence: %{y:.2f}%"

    fig = px.scatter(
        df,
        x='GDP',
        y='Prevalence',
        animation_frame='Year',
        animation_group='Entity',
        size='Prevalence',
        color=color_col,
        color_discrete_sequence=colors.qualitative.Safe,
        custom_data=custom_data
    )

    fig.update_layout(
        paper_bgcolor=BG_TRANSPARENT,
        plot_bgcolor=BG_TRANSPARENT,
        xaxis_range=max_x_range,
        yaxis_range=max_y_range,
        xaxis=dict(
            showgrid=False,
            zeroline=False,
            linecolor='#7159a3',
            linewidth=3,
            showspikes=False,
            title='GDP'
        ),
        yaxis=dict(
            showgrid=False,
            linecolor='#7159a3',
            linewidth=3,
            title='Prevalence (%)',
            ticksuffix="  ",
            zeroline=False
        ),
        hovermode='x unified',
        hoverlabel=HOVERLABEL_TEMPLATE
    )

    fig.update_traces(
        hovertemplate=hover_template
    )

    return fig

