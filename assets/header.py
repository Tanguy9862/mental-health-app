import dash
from dash import dcc, html, callback, Output, Input, State
import dash_mantine_components as dmc
from dash_iconify import DashIconify

GITHUB = 'https://github.com/Tanguy9862/mental-health-app'
CONTACT_ICON_WIDTH = 30


def modal_data_source():

    return  dmc.Modal(
            id='modal-data-source',
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
                        
                        # About the Dataset
                        
                        Mental health is a crucial aspect of our lives and society, influencing well-being, 
                        work capability, and relationships with friends, family, and community. Hundreds of millions 
                        of people suffer from mental health conditions annually, with an estimated 1 in 3 women and 1 
                        in 5 men experiencing major depression in their lifetimes. Other conditions, like schizophrenia 
                        and bipolar disorder, though less common, also significantly impact people's lives.
                        
                        While mental illnesses are treatable and their impact can be reduced, treatment is often 
                        inadequate or of poor quality. Many individuals also feel uncomfortable sharing their symptoms 
                        with healthcare professionals or acquaintances, making it challenging to accurately estimate 
                        the prevalence of these conditions.
                        
                        To effectively support and treat mental health conditions, comprehensive and reliable data are 
                        essential. This dataset aims to provide insights into how, when, and why these conditions 
                        occur, their prevalence, and effective treatment methods.
                    
                        ## Source Information
                        
                        - **Authors:** Saloni Dattani, Lucas Rodés-Guirao, Hannah Ritchie, and Max Roser (2023)
                        - **Title:** "Mental Health"
                        - **Published Online:** OurWorldInData.org
                        - **Retrieved From:** [Kaggle Dataset](https://www.kaggle.com/datasets/amirhoseinmousavian/mental-health)
                        - **Temporal Coverage:** From 12/31/1989 to 12/31/2018
                        - **Geospatial Coverage:** Worldwide
                        - **License:** Attribution 4.0 International (CC BY 4.0)
                        
                        ## Collection Methodology
                        
                        The data was collected by visiting the publisher and includes information from the World 
                        Mental Health surveys conducted between 2001 and 2015.
                        
                        """
                    ],
                )
            ]
        )


header = html.Div(
    dmc.Grid(
        [
            modal_data_source(),
            dmc.Col(
                [
                    dmc.Group(
                        [
                            dmc.ActionIcon(
                                [
                                    DashIconify(icon='bx:data', color='#C8C8C8', width=25)
                                ],
                                variant='transparent',
                                id='about-data-source'
                            ),
                            dmc.Anchor(
                                [
                                    DashIconify(icon='uil:github', color='#8d8d8d', width=CONTACT_ICON_WIDTH),
                                ],
                                href=GITHUB
                            )
                        ],
                        spacing='xl',
                        position='right'
                    )
                ],
                offsetMd=1,
                md=10,
            )
        ],
        mt='md',
        mb=35
    )
)


@callback(
    Output('modal-data-source', 'opened'),
    Input('about-data-source', 'n_clicks'),
    State('modal-data-source', 'opened'),
    prevent_initial_call=True
)
def toggle_modal_sankey(_, opened):
    return not opened


