import pandas as pd
import plotly.express as px
from utils.process_data import all_disorders_dataframes
from utils.utils_config import BG_TRANSPARENT

WITH_PADDING = dict(pad=15, t=0, b=0, l=0, r=0)
HOVERLABEL_TEMPLATE = dict(
    bgcolor='rgba(11, 6, 81, 0.8)',
    bordercolor='rgba(11, 6, 81, 0.8)',
    font=dict(
        color='white'
    )
)
FONT_COLOR = '#5D5D5D'

# PROCESSING DATA:
concatenate_df = pd.concat(
    [all_disorders_dataframes[disorder].prevalence_by_year for disorder in [
        'Anxiety', 'Bipolar', 'Depressive', 'Eating', 'Schizophrenia']
     ],
    ignore_index=True
)
prevalence_by_disorder = concatenate_df.groupby('Disorder')['Value'].mean().reset_index()

# MAPPING FOR COLORS ASSOCIATED WITH DISORDER:
colors = {
    'Anxiety': all_disorders_dataframes['Anxiety'].pastel_color,
    'Depressive': all_disorders_dataframes['Depressive'].pastel_color,
    'Bipolar': all_disorders_dataframes['Bipolar'].pastel_color,
    'Eating': all_disorders_dataframes['Eating'].pastel_color,
    'Schizophrenia': all_disorders_dataframes['Schizophrenia'].pastel_color
}

prevalence_by_disorder['Color'] = prevalence_by_disorder['Disorder'].map(colors)
prevalence_by_disorder['EstimatedPeopleAffected'] = round(prevalence_by_disorder['Value'] / 100 * 7.8 * 1000, 1)
prevalence_by_disorder['FormattedValue'] = prevalence_by_disorder['Value'].apply(lambda x: f'{round(x, 1)}%')

# PLOT BAR CHART:
disorder_bar_fig = px.bar(
    prevalence_by_disorder,
    x='Disorder',
    y='Value',
    width=400,
    height=500
)

disorder_bar_fig.update_layout(
    plot_bgcolor=BG_TRANSPARENT,
    paper_bgcolor=BG_TRANSPARENT,
    bargap=0.2,
    showlegend=False,
    # hoverlabel=HOVERLABEL_TEMPLATE,
    margin=WITH_PADDING,
    coloraxis_showscale=False,
    yaxis=dict(
        showgrid=False,
        zeroline=False,
        color=FONT_COLOR,
        visible=False,
        title=None
    ),
    xaxis=dict(
        categoryorder='total descending',
        showgrid=False,
        zeroline=False,
        title=dict(
            text='<i>Average Worldwide Prevalence Rates of Mental Health Conditions</i>',
            font=dict(size=11),
            standoff=40
        )
    )
)

disorder_bar_fig.update_traces(
    text=prevalence_by_disorder['FormattedValue'],
    textposition='outside',
    marker_color=prevalence_by_disorder['Color'],
    width=0.5,
    marker=dict(line=dict(width=0)),
    # customdata=prevalance_by_disorder['EstimatedPeopleAffected'],
    # hovertemplate='%{y}%<br>Estimated Affected People: %{customdata} millions<extra></extra>'
    hovertemplate=None,
    hoverinfo='none'
)


# PLOT LINE CHART (CHART ON HOVER):
def plot_yearly_prevalence(df, line_color):
    min_x, max_x = df['Year'].min(), df['Year'].max()
    min_y, max_y = df['Value'].min(), df['Value'].max()

    fig = px.line(
        df,
        x='Year',
        y='Value',
        width=275,
        height=100
    )

    fig.update_layout(
        plot_bgcolor=BG_TRANSPARENT,
        paper_bgcolor=BG_TRANSPARENT,
        xaxis=dict(showgrid=False, showline=False, zeroline=False, title=None, tickvals=[min_x, max_x], color='white'),
        yaxis=dict(showgrid=False, showline=False, zeroline=False, title=None, tickvals=[min_y, max_y], color='white'),
        margin=dict(t=5, b=0, l=0, r=0, pad=8)
    )

    fig.update_traces(
        line=dict(color=line_color, width=2, shape='spline')
    )

    return fig


# MAP LABELS WITH CORRESPONDING DF:
graph_functions = {
    'Anxiety': lambda: plot_yearly_prevalence(all_disorders_dataframes['Anxiety'].prevalence_by_year, colors['Anxiety']),
    'Depressive': lambda: plot_yearly_prevalence(all_disorders_dataframes['Depressive'].prevalence_by_year, colors['Depressive']),
    'Bipolar': lambda: plot_yearly_prevalence(all_disorders_dataframes['Bipolar'].prevalence_by_year, colors['Bipolar']),
    'Eating': lambda: plot_yearly_prevalence(all_disorders_dataframes['Eating'].prevalence_by_year, colors['Eating']),
    'Schizophrenia': lambda: plot_yearly_prevalence(all_disorders_dataframes['Schizophrenia'].prevalence_by_year, colors['Schizophrenia']),
}
