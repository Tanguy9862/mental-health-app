import plotly.express as px
from utils.process_data import all_disorders_dataframes
from utils.fig_config import BG_TRANSPARENT, HOVERLABEL_TEMPLATE


def create_heatmap(df, disorder_name, entities, grouping_field):
    fig = px.imshow(
        df,
        color_continuous_scale=all_disorders_dataframes[disorder_name].color_scale,
        aspect='auto',
        # labels=dict(color="Normalized prevalence")
    )

    fig.update_layout(
        height=60*len(entities),
        xaxis=dict(
            title=dict(
                text=f'<i>Global Heatmap of {disorder_name} Disorder Prevalence</i>',
                font=dict(size=11),
                standoff=40
            ),
            showspikes=False
        ),
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

    hovertemplate = f"{grouping_field}: %{{y}}<br>Year: %{{x}}<br>Normalized prevalence: %{{z}}<extra></extra>"
    for trace in fig.data:
        trace.hovertemplate = hovertemplate

    return fig
