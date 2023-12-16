from dash import html, dcc
import dash_mantine_components as dmc
from dash_iconify import DashIconify

from utils.utils_config import add_loading_overlay


tabs_heatmap = html.Div(
    [
        dmc.Modal(
            id='data-modal-heatmap',
            size='55%',
            styles={
                'modal': {
                    'background-color': '#f2f2f2',
                }
            },
            children=[
                dcc.Markdown(
                    [
                        """
                        ## Data Management and Analysis Overview
                        ---

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
                         You now have the flexibility to choose between adding individual countries or entire 
                         continents to your view. This feature allows for a more customizable and comprehensive 
                         analysis, focusing on the specific areas that interest you. When you add an entire continent, 
                         the heatmap aggregates data from all the countries within that continent, providing a 
                         broad overview. Alternatively, you can select specific countries for a more focused analysis.
                        """
                    ],
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
                            persistence_type='session'
                        )
                    ],
                    label='Switch to Continent or Country view',
                    transition='fade',
                    withArrow=True
                ),
                dmc.ActionIcon(
                    DashIconify(icon='ph:question'),
                    id='about-data-management-heatmap',
                    size='md',
                    variant='transparent'
                )
            ],
            mt='lg',
            mb='lg',
            position='center'
        ),
        add_loading_overlay(elements=dmc.Container(id='heatmap-container', px=0)),
    ]
)

tabs_sankey = html.Div(
    [
        dmc.Modal(
            id='data-modal-sankey',
            size='55%',
            styles={
                'modal': {
                    'background-color': '#f2f2f2',
                }
            },
            children=[
                dcc.Markdown(
                    [
                        """
                        ## Data Management and Methodology Explanation
                        ---
                        
                        ### Sankey Visualization
                        In this analysis, we focus on the prevalence of a specific disease across various demographic categories. 
                        The data is structured to reflect the disease's prevalence across different continents, 
                        countries, and within specific demographic categories like age and gender.
                                                
                        ### Prevalence Calculation
                        The prevalence data is initially segmented into different demographic categories 
                        *(e.g., age groups and gender)*. For each country, we have an estimated total number 
                        of affected individuals and prevalence rates for each category.
                        
                        ### Normalization Across Categories
                        To ensure comparability across different categories and to align the data with the total 
                        estimated cases, we performed a normalization process:
                        
                        **Total Prevalence Summation:** For each row in the dataset, representing a country, 
                        we calculate the sum of prevalences for all categories.
                        
                        **Proportional Distribution:** We then distribute the estimated affected number 
                        proportionally among the categories based on their share of the total prevalence.
                        
                        **Resulting Values:** The final values in each category reflect an estimated count of 
                        affected individuals, proportionally adjusted to align with the total prevalence observed 
                        in that country.
                        
                        ## Understanding the Sankey Diagram Output
                        
                        -----
                        
                        In the **All** view of the Sankey diagram, the representation encompasses all countries within 
                        a selected continent. This comprehensive display prioritizes the absolute number of individuals 
                        affected by the mental health disorder. Countries that are higher up in the diagram indicate 
                        a larger affected population. This view is particularly useful for understanding the total 
                        impact of the disorder across each country, highlighting where the largest populations 
                        in need of resources and attention are located.
                        
                        The **Top 5** view shifts the focus to the prevalence of the disorder, rather than its 
                        absolute impact. In this mode, the diagram displays the top five countries with the 
                        highest mean prevalence of the disorder within each continent. While the size of the 
                        flows still represents the number of affected individuals, the selection of countries is 
                        based on their relative prevalence rates. This approach offers a nuanced perspective, 
                        highlighting countries where the disorder is most prevalent proportionally, which can be 
                        particularly insightful for understanding the relative severity of the disorder in 
                        different regions.
                        """
                    ],
                )
            ]
        ),
        dmc.Container(
            [
                dmc.Group(
                    [
                        dmc.Switch(
                            onLabel=DashIconify(icon='ri:time-line', height=15),
                            offLabel=DashIconify(icon='fontisto:intersex', height=15),
                            size='md',
                            color='violet',
                            id='switch-age-sex',
                            persistence=True,
                            persistence_type='session',
                        ),
                        dmc.ActionIcon(
                            DashIconify(icon='ph:question'),
                            id='about-data-management-sankey',
                            size='md',
                            variant='transparent'
                        )
                    ],
                    mt='lg',
                    position='center'
                ),
                dmc.Container(id='sankey-container', px=0, mt='xl'),
                dcc.Tooltip(id='sankey-tooltip', background_color='black'),
                dcc.Interval(id='sankey-interval', interval=1000, max_intervals=0),
                dmc.Group(
                    [
                        dmc.ActionIcon(
                            [
                                DashIconify(icon='akar-icons:play', width=30, color='#967bb6'),
                            ],
                            n_clicks=0,
                            variant='transparent',
                            id='play-sankey-animation'
                        ),
                        dmc.Slider(
                            id='sankey-year-slider',
                            persistence=True,
                            persistence_type='session',
                            color='white',
                            style={'width': '50%'},
                            styles={
                                'bar': {'background-color': '#7159a3', 'height': '2px'},
                                'track': {'height': '2px'},
                                'mark': {'display': 'None'},
                                'markLabel': {'margin-top': '15px'},
                                'thumb': {'background-color': '#7159a3', 'border': f'solid 1px #7159a3'}
                            }
                        ),
                    ],
                    mt='lg',
                    position='center'
                ),
                dmc.Divider(label='Country Display Preferences', mt=75),
                dmc.RadioGroup(
                    [
                        dmc.Radio('Top 5', value='top-5'),
                        dmc.Radio('All', value='all')
                    ],
                    id='sankey-country-filter-selection',
                    value='top-5',
                    mt='md',
                    ml='xl',
                )
            ],
            id='sankey-tab',
            px=0
        )
    ]
)
