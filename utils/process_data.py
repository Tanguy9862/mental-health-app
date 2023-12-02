import pandas as pd
import pycountry_convert as pc
import plotly.express as px
from collections import namedtuple


DATA_PATH = 'data/'

file_paths = [
    f'{DATA_PATH}/anxiety-disorders-prevalence.csv',
    f'{DATA_PATH}/bipolar-disorder-prevalence.csv',
    f'{DATA_PATH}/depressive-disorders-prevalence-ihme.csv',
    f'{DATA_PATH}/eating-disorders-prevalence.csv',
]

continent_dict = {
    "NA": "North America",
    "SA": "South America",
    "AS": "Asia",
    "AF": "Africa",
    "OC": "Oceania",
    "EU": "Europe",
    "AQ": "Antarctica"
}


def get_continent_name(continent_code: str) -> str:
    return continent_dict[continent_code]


def country_code_to_continent_name(country_code):
    try:
        code_a2 = pc.country_alpha3_to_country_alpha2(country_code)
        continent_code = pc.country_alpha2_to_continent_code(code_a2)
        continent_name = get_continent_name(continent_code)
        return continent_name
    except (KeyError, TypeError):
        return 'Unknown'


def process_data(file_path, disorder_name):
    df = pd.read_csv(file_path)
    df.rename(columns={df.columns[-1]: 'Value'}, inplace=True)
    df['Disorder'] = disorder_name
    df['Continent'] = df['Code'].apply(country_code_to_continent_name)
    grouped_by_year = df.groupby(['Year', 'Disorder'])['Value'].mean().reset_index().round(3)
    return df, grouped_by_year


# Disorder Prevalence by country and year:
DisorderDataframe = namedtuple(
    'DisorderDataframe',
    ['disorder_name', 'prevalence_by_country', 'prevalence_by_year', 'pastel_color', 'color_scale']
)

anxiety_disorder = DisorderDataframe(
    'Anxiety',
    *[process_data(file_paths[0], 'Anxiety')[i] for i in range(2)],
    '#7FC6A4',
    px.colors.sequential.Greens
)

bipolar_disorder = DisorderDataframe(
    'Bipolar',
    *[process_data(file_paths[1], 'Bipolar')[i] for i in range(2)],
    '#FF6B6B',
    px.colors.sequential.Reds
)

depressive_disorder = DisorderDataframe(
    'Depressive',
    *[process_data(file_paths[2], 'Depressive')[i] for i in range(2)],
    '#FFD580',
    px.colors.sequential.Oranges
)
eating_disorder = DisorderDataframe(
    'Eating',
    *[process_data(file_paths[3], 'Eating')[i] for i in range(2)],
    '#C5A3FF',
    px.colors.sequential.Magenta
)

all_disorders_dataframes = {
    'Anxiety': anxiety_disorder,
    'Depressive': depressive_disorder,
    'Bipolar': bipolar_disorder,
    'Eating': eating_disorder

}

# Faire une boucle du maping (loop à travers liste 'anxiety', 'depressive', etc.)


# anxiety_by_country = process_data(file_paths[0], 'Anxiety')[0]
# print(anxiety_by_country)
# bipolar_by_country = process_data(file_paths[0], 'Bipolar')[0]
# depressive_by_country = process_data(file_paths[0], 'Depressive')[0]
# eating_by_country = process_data(file_paths[0], 'Eating')[0]
#
# # Prevalence grouped by year (all countries):
# anxiety_prevalence = process_data(file_paths[0], 'Anxiety')[1]
# print(anxiety_prevalence)
# bipolar_prevalence = process_data(file_paths[1], 'Bipolar')[1]
# depressive_prevalence = process_data(file_paths[2], 'Depressive')[1]
# eating_prevalence = process_data(file_paths[3], 'Eating')[1]
