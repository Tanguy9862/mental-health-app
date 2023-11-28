import plotly.express as px
from utils.fig_config import BG_TRANSPARENT


# FIGURE:
def create_choropleth_fig(df, color_scale):
    fig = px.choropleth(
        df,
        locations='Code',
        color='Value',
        color_continuous_scale=color_scale,
        custom_data=['Entity']
    )

    fig.update_geos(
        projection_type='orthographic',
        projection_rotation_lon=-170,  # 110
        projection_rotation_lat=20,
        showocean=True,
        oceancolor='#87CEEB',
        showcoastlines=True,
        coastlinecolor='#333333',
        coastlinewidth=1,
        showland=True,
        landcolor='#4B4B4B',  # couleur continent
        showlakes=False,
        lakecolor='#202E78',  # couleur lac
        showcountries=False,
        countrycolor='white',
        bgcolor=BG_TRANSPARENT,
        framewidth=1,
        framecolor='white',  # couleur du contour
    )

    fig.update_layout(
        margin={"r": 0, "t": 0, "l": 0, "b": 0},
        paper_bgcolor='rgba(0,0,0,0)',
        showlegend=False,
        coloraxis_showscale=False,
        hoverlabel=dict(
            bgcolor='rgba(11, 6, 81, 0.8)',
            bordercolor='rgba(11, 6, 81, 0.8)',
            font=dict(
                color='white'
            )
        )
    )

    fig.update_traces(
        marker_line_width=1,
        marker_line_color='white',
        hovertemplate=None,
        hoverinfo='none'
    )

    return fig
