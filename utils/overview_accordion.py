import dash_mantine_components as dmc
from dash import html

characters_list = [
    {
        "id": "anxiety",
        "image": "https://img.icons8.com/external-flaticons-lineal-color-flat-icons/64/external-anxiety-psychology"
                 "-flaticons-lineal-color-flat-icons-2.png",
        "label": "Anxiety Disorders",
        "description": "Varieties and Impact",
        "content": "Anxiety disorders encompass a range of mental health conditions characterized by significant "
                   "anxiety and fear. These disorders can manifest as generalized anxiety, panic attacks, "
                   "specific phobias, social anxiety, and more. Common symptoms include excessive worrying, "
                   "restlessness, and trouble with concentration, often impacting daily activities.",
    },
    {
        "id": "depressive",
        "image": "https://img.icons8.com/external-soft-fill-juicy-fish/60/external-depression-bankruptcy-soft-fill"
                 "-soft-fill-juicy-fish.png",
        "label": "Depressive Disorders",
        "description": "More Than Just Sadness",
        "content": "Depressive disorders represent a group of conditions marked by persistent feelings of sadness and "
                   "loss of interest. Major depression, persistent depressive disorder, and seasonal affective "
                   "disorder are among the types. Symptoms can vary but often include changes in sleep, appetite, "
                   "energy level, and self-esteem.",
    },
    {
        "id": "bipolar",
        "image": "https://img.icons8.com/external-flaticons-lineal-color-flat-icons/64/external-bipolar-psychology"
                 "-flaticons-lineal-color-flat-icons-3.png",
        "label": "Bipolar Disorder",
        "description": "The Highs and Lows of Mood",
        "content": "Bipolar disorder is characterized by extreme mood swings, from manic highs to depressive lows. "
                   "These shifts in mood, energy, and activity levels can affect an individual's ability to carry out "
                   "day-to-day tasks. Diagnosis and management require a careful and comprehensive approach.",
    },
    {
        "id": "schizophrenia",
        "image": "https://img.icons8.com/external-flaticons-lineal-color-flat-icons/64/external-schizophrenia"
                 "-psychology-flaticons-lineal-color-flat-icons-3.png",
        "label": "Schizophrenia Disorder",
        "description": "Complexity in Thought and Perception",
        "content": "Schizophrenia is a complex and chronic mental disorder characterized by disturbances in thought, "
                   "perception, and behavior. It often presents with symptoms like hallucinations, delusions, "
                   "and disorganized thinking, profoundly impacting daily functioning.",
    },
    {
        "id": "eating",
        "image": "https://img.icons8.com/external-flaticons-lineal-color-flat-icons/64/external-eating-disorder"
                 "-psychology-flaticons-lineal-color-flat-icons-2.png",
        "label": "Eating Disorders",
        "description": "Complexities of Eating Behavior",
        "content": "Eating disorders are serious conditions affecting eating behaviors and related thoughts and "
                   "emotions. Common types include anorexia nervosa, bulimia nervosa, and binge-eating disorder. "
                   "These disorders can have significant physical and psychological impacts and often require "
                   "comprehensive treatment."
    }
]


def create_accordion_label(label, image, description):
    return dmc.AccordionControl(
        dmc.Group(
            [
                dmc.Avatar(src=image, radius="xl", size="lg"),
                html.Div(
                    [
                        dmc.Text(label),
                        dmc.Text(description, size="sm", weight=400, color="dimmed"),
                    ]
                ),
            ]
        )
    )


def create_accordion_content(content):
    return dmc.AccordionPanel(dmc.Text(content, size="sm"))


disorders_accordion = dmc.Accordion(
    chevronPosition="right",
    variant="contained",
    children=[
        dmc.AccordionItem(
            [
                create_accordion_label(
                    character["label"], character["image"], character["description"]
                ),
                create_accordion_content(character["content"]),
            ],
            value=character["id"],
        )
        for character in characters_list
    ],
)
