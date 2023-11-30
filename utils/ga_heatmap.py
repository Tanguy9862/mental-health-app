import plotly.express as px
from utils.process_data import all_disorders_dataframes
from utils.fig_config import BG_TRANSPARENT, HOVERLABEL_TEMPLATE


def create_heatmap(df, countries, disorder_name):
    fig = px.imshow(
        df,
        color_continuous_scale=all_disorders_dataframes[disorder_name].color_scale,
        aspect='auto',
        # labels=dict(color="Normalized prevalence")
    )

    fig.update_layout(
        height=60*len(countries),
        xaxis=dict(title=None, showspikes=False),
        yaxis=dict(title=None),
        margin=dict(pad=7, t=0, b=0, l=0, r=0),
        paper_bgcolor=BG_TRANSPARENT,
        plot_bgcolor=BG_TRANSPARENT,
        hovermode='x unified',
        hoverlabel=HOVERLABEL_TEMPLATE,
        coloraxis_colorbar=dict(
            thickness=3,
        )
    )

    hovertemplate = "Country: %{y}<br>Year: %{x}<br>Normalized prevalence: %{z}<extra></extra>"
    for trace in fig.data:
        trace.hovertemplate = hovertemplate

    return fig
