import pandas as pd
import pycountry_convert as pc
import plotly.express as px
from collections import namedtuple

pd.set_option('display.max_columns', None)

DATA_PATH = 'data/'
DATA_GDP_PATH = 'data/gdp'

file_paths = [
    f'{DATA_PATH}/anxiety-disorders-prevalence.csv',
    f'{DATA_PATH}/bipolar-disorder-prevalence.csv',
    f'{DATA_PATH}/depressive-disorders-prevalence-ihme.csv',
    f'{DATA_PATH}/eating-disorders-prevalence.csv',
]

file_gdp_paths = [
    f'{DATA_GDP_PATH}/anxiety-disorders-prevalence-vs-gdp.csv',
    f'{DATA_GDP_PATH}/depressive-disorders-prevalence-vs-gdp.csv',
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


def process_general_data(file_path, disorder_name):
    df = pd.read_csv(file_path)
    df.rename(columns={df.columns[-1]: 'Value'}, inplace=True)
    df['Disorder'] = disorder_name
    df['Continent'] = df['Code'].apply(country_code_to_continent_name)
    grouped_by_year = df.groupby(['Year', 'Disorder'])['Value'].mean().reset_index().round(3)
    return df, grouped_by_year


def process_gdp_data(file_path, disorder_name=None):
    df = pd.read_csv(file_path)
    df.rename(columns={df.columns[3]: 'Prevalence', df.columns[4]: 'GDP_per_capita_PPP_2017'}, inplace=True)
    df = df.dropna(subset=['Prevalence', 'GDP_per_capita_PPP_2017'])
    df['Continent'] = df['Code'].apply(country_code_to_continent_name)
    return df


# Disorder Prevalence by country and year:
DisorderDataframe = namedtuple(
    'DisorderDataframe',
    [
        'disorder_name',
        'prevalence_by_country',
        'prevalence_by_year',
        'prevalence_and_gdp',
        'pastel_color',
        'color_scale'
    ]
)

anxiety_disorder = DisorderDataframe(
    'Anxiety',
    *[process_general_data(file_paths[0], 'Anxiety')[i] for i in range(2)],
    process_gdp_data(file_gdp_paths[0]),
    '#7FC6A4',
    px.colors.sequential.Greens
)

bipolar_disorder = DisorderDataframe(
    'Bipolar',
    *[process_general_data(file_paths[1], 'Bipolar')[i] for i in range(2)],
    None,
    '#FF6B6B',
    px.colors.sequential.Reds
)

depressive_disorder = DisorderDataframe(
    'Depressive',
    *[process_general_data(file_paths[2], 'Depressive')[i] for i in range(2)],
    process_gdp_data(file_gdp_paths[1]),
    '#FFD580',
    px.colors.sequential.Oranges
)
eating_disorder = DisorderDataframe(
    'Eating',
    *[process_general_data(file_paths[3], 'Eating')[i] for i in range(2)],
    None,
    '#C5A3FF',
    px.colors.sequential.Magenta
)

all_disorders_dataframes = {
    'Anxiety': anxiety_disorder,
    'Depressive': depressive_disorder,
    'Bipolar': bipolar_disorder,
    'Eating': eating_disorder

}

# Faire une boucle du mapping (loop à travers liste 'anxiety', 'depressive', etc.)
