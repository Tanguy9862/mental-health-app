import plotly.express as px
from utils.process_data import all_disorders_dataframes
from utils.utils_config import BG_TRANSPARENT, HOVERLABEL_TEMPLATE


def create_heatmap(df, disorder_name, entities, grouping_field):
    fig = px.imshow(
        df,
        color_continuous_scale=all_disorders_dataframes[disorder_name].color_scale,
        aspect='auto',
    )

    fig.update_layout(
        height=90*len(entities),
        xaxis=dict(
            title=dict(
                text=f'<i>Global Heatmap of {disorder_name} Disorder Prevalence</i>',
                font=dict(size=11),
                standoff=45,
            ),
            showspikes=False,
            dtick='M12',
            tickformat='%Y'
        ),
        yaxis=dict(title=None),
        margin=dict(pad=5, t=0, b=65, l=0, r=0),
        paper_bgcolor=BG_TRANSPARENT,
        plot_bgcolor=BG_TRANSPARENT,
        hovermode='x unified',
        hoverlabel=HOVERLABEL_TEMPLATE,
        coloraxis_colorbar=dict(
            len=1.5 if len(entities) == 1 else None,
            thickness=3,
        )
    )

    hovertemplate = f"{grouping_field}: %{{y}}<br>Year: %{{x}}<br>Normalized prevalence: %{{z}}<extra></extra>"
    for trace in fig.data:
        trace.hovertemplate = hovertemplate

    return fig
