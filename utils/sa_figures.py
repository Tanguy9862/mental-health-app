import plotly.express as px
import pandas as pd
from plotly import colors
from utils.utils_config import BG_TRANSPARENT, HOVERLABEL_TEMPLATE


def create_bar_fig(
        df: pd.DataFrame, x: str,
        y: str,
        continent: str,
        color_seq,
        y_tickprefix=None,
        y_ticksuffix=None,
        autorange=None,
        title=None,
        side_yaxis: str = 'left',
        width_traces: float = 0.3,
        height=None,
        r_padding: int = 0
):

    fig = px.bar(
        df,
        x=y,
        y=x,
        orientation='h',
        color=y,
        color_continuous_scale=color_seq,
        height=height
    )

    fig.update_layout(
        plot_bgcolor=BG_TRANSPARENT,
        paper_bgcolor=BG_TRANSPARENT,
        bargap=0.1,
        showlegend=False,
        hovermode='y unified',
        hoverlabel=HOVERLABEL_TEMPLATE,
        margin=dict(pad=0, t=0, l=0, r=r_padding, b=0),
        coloraxis_showscale=False,
        yaxis=dict(
            categoryorder='total ascending',
            side=side_yaxis,
            ticksuffix=y_ticksuffix,
            tickprefix=y_tickprefix,
            showspikes=False,
            showgrid=False,
            zeroline=False,
            visible=True,
            title=None
        ),
        xaxis=dict(
            showgrid=False,
            visible=False,
            zeroline=False,
            title=title,
            autorange=autorange,
        )
    )

    fig.update_traces(
        width=width_traces,
        marker=dict(line=dict(width=0)),
        hovertemplate='Response Rate: %{x:.1f}%<extra></extra>'
    )

    return fig
