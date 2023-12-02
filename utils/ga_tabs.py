from dash import html, dcc
import dash_mantine_components as dmc
from dash_iconify import DashIconify


tabs_heatmap = html.Div(
    [
        dmc.Drawer(
            id='data-drawer',
            padding='md',
            size='35%',
            styles={
                'drawer': {
                    'background-color': '#f2f2f2',
                }
            },
            children=[
                dcc.Markdown(
                    [
                        """
                        ## Data Management and Analysis Overview

                        ### Heatmap Visualization 
                        Our heatmap visualization presents the evolution of mental health 
                        disorder prevalence over the years across countries or continents based on user selection. We 
                        begin by filtering the dataset according to the countries chosen by the user and the 
                        specified year range. To ensure comparability across different entities, we normalize the 
                        prevalence data, adjusting each value to fall between 0 and 1, relative to the minimum and 
                        maximum values within its group.
                        
                        ### Understanding Normalized Prevalence 
                        Normalized Prevalence is a statistical method that scales prevalence rates to a common scale of 
                        0 to 1. This scaling process allows for direct comparisons across different entities or years 
                        by highlighting relative changes and trends in prevalence, rather than focusing on absolute 
                        numerical values.
                        
                        ### Sorting and Trend Analysis 
                        Our approach to highlighting significant trends involves sorting the data based on the slope 
                        of the prevalence trend line. The slope is calculated using a linear regression model for 
                        each country or continent, which quantifies the rate of change in prevalence over the selected 
                        years. A steeper slope indicates a more significant change. This method allows us to rank the 
                        entities by the degree of change in their disorder prevalence, thereby focusing on the most 
                        relevant trends for analysis.
                        
                        ### Continent-Level Aggregation 
                        In the continent-level view, the heatmap includes only the countries selected by the user, 
                        rather than aggregating all countries in a continent. This user-centric approach allows for a 
                        more customized and relevant analysis, focusing on the specific interests of the user. 
                        The data for these selected countries is then aggregated to represent the average prevalence 
                        on a continental level.
                        """
                    ],
                    # style={'color': 'red'}
                )
            ]
        ),
        dmc.Group(
            [
                dmc.Tooltip(
                    [
                        dmc.Switch(
                            onLabel=DashIconify(icon='fluent-mdl2:world', height=15),
                            offLabel=DashIconify(icon='ion:flag-sharp', height=15),
                            size='md',
                            color='violet',
                            id='switch-country-continent',
                            persistence=True,
                            persistence_type='memory'
                        )
                    ],
                    label='Switch to Continent or Country view',
                    transition='fade',
                    withArrow=True
                ),
                dmc.ActionIcon(
                    DashIconify(icon='ph:question'),
                    id='about-data-management',
                    size='md',
                    variant='transparent'
                )
            ],
            mt='lg',
            mb='lg',
            position='center'
        ),
        dmc.Container(id='heatmap-container', px=0),
    ]
)

tabs_sankey = html.Div(
    [
        dmc.Container(id='sankey-container', px=0)
    ]
)
