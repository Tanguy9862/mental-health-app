import pandas as pd
import plotly.graph_objects as go
from plotly import colors
from utils.utils_config import BG_TRANSPARENT


def create_sankey(
        filtered_df: pd.DataFrame,
        filtered_categories: list,
        country_filter_selection: str,
        title: str,
        color_categories: list = None
):

    data_sankey = {
        'source': [],
        'target': [],
        'value': [],
        'label': [],
        'color': [],
        'customdata': []
    }
    palette = colors.qualitative.Pastel2

    # Nodes for continents, countries and age categories
    continents = filtered_df['Continent'].unique().tolist()
    continent_indices = {continent: i for i, continent in enumerate(continents)}

    countries = filtered_df['Entity'].unique().tolist()
    country_indices = {country: i + len(continents) for i, country in enumerate(countries)}

    # Mapping for age categories with indices (from sources to target)
    filtered_categories_indices = {category: i + len(continents) + len(countries) for i, category in enumerate(filtered_categories)}

    data_sankey['label'] = continents + countries + filtered_categories

    # Associate each continent with a color
    continent_to_color = {continent: palette[i] for i, continent in enumerate(continents)}

    # Compute MeanPrevalence and TotalPrevalence for each country
    df_mean_sum_filtered_category_prevalence = filtered_df.copy()
    df_mean_sum_filtered_category_prevalence['MeanPrevalence'] = df_mean_sum_filtered_category_prevalence[
        filtered_categories].mean(axis=1)
    df_mean_sum_filtered_category_prevalence['TotalPrevalence'] = df_mean_sum_filtered_category_prevalence[
        filtered_categories].sum(axis=1)
    df_mean_sum_filtered_category_prevalence = df_mean_sum_filtered_category_prevalence.sort_values(
        by=['Continent', 'GlobalPrevalence'],
        ascending=[True, False]
    )

    df_mean_sum_filtered_category_prevalence['EstimatedAffected'] = (df_mean_sum_filtered_category_prevalence[
                                                                         'GlobalPrevalence'] / 100) * \
                                                                    df_mean_sum_filtered_category_prevalence[
                                                                        'Population']
    df_mean_sum_filtered_category_prevalence['EstimatedAffected'] = df_mean_sum_filtered_category_prevalence[
        'EstimatedAffected'].round().astype(int)

    # Update categories with estimated affected people
    for index, row in df_mean_sum_filtered_category_prevalence.iterrows():
        sum_of_prevalences = sum(row[category] for category in filtered_categories)
        for category in filtered_categories:
            if sum_of_prevalences > 0:
                row[category] = row['EstimatedAffected'] * (row[category] / sum_of_prevalences)
        df_mean_sum_filtered_category_prevalence.loc[index, filtered_categories] = row[filtered_categories]

    if country_filter_selection == 'top-5':
        top_5 = df_mean_sum_filtered_category_prevalence.groupby('Continent').apply(
            lambda x: x.nlargest(5, 'GlobalPrevalence')).reset_index(drop=True)
        max_prevalence_per_continent = top_5.groupby('Continent')['GlobalPrevalence'].max()
        df_with_max = top_5.merge(max_prevalence_per_continent.rename('MaxPrevalence'), on='Continent')
        df_mean_sum_filtered_category_prevalence = df_with_max.sort_values(
            by=['MaxPrevalence', 'Continent', 'GlobalPrevalence'],
            ascending=[False, True, False]
        )


    # Flow from continents to countries
    for _, row in df_mean_sum_filtered_category_prevalence.iterrows():
        data_sankey['source'].append(continent_indices[row['Continent']])
        data_sankey['target'].append(country_indices[row['Entity']])
        data_sankey['value'].append(row['EstimatedAffected'])
        data_sankey['color'].append(continent_to_color[row['Continent']])
        data_sankey['customdata'].append([row['Continent'], row['Entity'], row['GlobalPrevalence']])

    # Flow from countries to age categories
    for _, row in df_mean_sum_filtered_category_prevalence.iterrows():
        country_index = country_indices[row['Entity']]
        for category in filtered_categories:
            data_sankey['source'].append(country_index)
            data_sankey['target'].append(filtered_categories_indices[category])
            data_sankey['value'].append(row[category])
            data_sankey['color'].append(continent_to_color[row['Continent']])
            data_sankey['customdata'].append([row['Continent'], row['Entity'], row['GlobalPrevalence']])

    # Colors for nodes
    node_colors = []
    for label in data_sankey['label']:
        if label in continents:
            # Color for node continent
            node_colors.append(continent_to_color[label])
        elif label in countries:
            # Color for node country
            continent = filtered_df[filtered_df['Entity'] == label]['Continent'].iloc[0]
            node_colors.append(continent_to_color[continent])
        else:
            # Color for node age categories
            color_categories = color_categories or colors.qualitative.Pastel1
            node_colors.extend(color_categories)

    # Plot Sankey
    fig = go.Figure(data=[go.Sankey(
        node=dict(
            pad=15,
            label=data_sankey['label'],
            color=node_colors
        ),
        link=dict(
            source=data_sankey['source'],
            target=data_sankey['target'],
            value=data_sankey['value'],
            color=data_sankey['color'],
            customdata=data_sankey['customdata'],
            hovertemplate="""
            <b>%{customdata[0]}:</b> %{customdata[1]} (%{customdata[2]:.2f}%)<br>
             <i>%{value} individuals estimated to be affected</i><extra></extra>
            """
        ),
    )])

    fig.update_layout(
        font_size=10,
        paper_bgcolor=BG_TRANSPARENT,
        height=450,
        margin=dict(t=10, b=60, l=50, r=50),
        annotations=[
            dict(
                text=f"<i>{title}</i>",
                showarrow=False,
                xref="paper",
                yref="paper",
                x=0.5,
                y=-0.1,
                xanchor='center',
                yanchor='top',
                font=dict(
                    size=11
                )
            )
        ],
    )

    # fig.update_traces(
        # hovertemplate=None,
        # hoverinfo='none'
    # )

    return fig
