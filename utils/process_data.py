import pandas as pd
import pycountry_convert as pc
import plotly.express as px
from collections import namedtuple

pd.set_option('display.max_columns', None)

DATA_PATH = 'data/'
DATA_GDP_PATH = 'data/gdp'
DATA_AGE_PATH = 'data/age'
DATA_SEX_PATH = 'data/sex'

file_paths = [
    f'{DATA_PATH}/anxiety-disorders-prevalence.csv',
    f'{DATA_PATH}/bipolar-disorder-prevalence.csv',
    f'{DATA_PATH}/depressive-disorders-prevalence-ihme.csv',
    f'{DATA_PATH}/eating-disorders-prevalence.csv',
    f'{DATA_PATH}/schizophrenia-prevalence.csv',
]

file_gdp_paths = [
    f'{DATA_GDP_PATH}/anxiety-disorders-prevalence-vs-gdp.csv',
    f'{DATA_GDP_PATH}/depressive-disorders-prevalence-vs-gdp.csv',
]

file_age_paths = [
    f'{DATA_AGE_PATH}/anxiety-disorders-prevalence-by-age.csv',
    f'{DATA_AGE_PATH}/bipolar-disorders-prevalence-by-age.csv',
    f'{DATA_AGE_PATH}/depressive-disorders-prevalence-by-age.csv',
    f'{DATA_AGE_PATH}/schizophrenia-prevalence-by-age.csv',
]

file_sex_paths = [
    f'{DATA_SEX_PATH}/anxiety-disorders-prevalence-males-vs-females.csv',
    f'{DATA_SEX_PATH}/bipolar-disorders-prevalence-males-vs-females.csv',
    f'{DATA_SEX_PATH}/depressive-disorders-prevalence-males-vs-females.csv',
    f'{DATA_SEX_PATH}/eating-disorders-prevalence-males-vs-females.csv',
    f'{DATA_SEX_PATH}/schizophrenia-prevalence-males-vs-females.csv',
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


def process_prevalence_by_age_data(file_path):
    df = pd.read_csv(file_path, encoding='utf-8')
    short_cols_names = ['5-14', '15-19', '20-24', '25-29', '30-34', '35-39', '40-44', '45-49', '50-54', '55-59', '60-64',
                '65-69', '70+', 'All ages', 'Age standardized']
    first_cols_names = df.columns[:3].tolist()
    new_cols_names = first_cols_names + short_cols_names
    df.columns = new_cols_names

    # Grouped age categories:
    new_age_groups = {
        '5-19 years': ['5-14', '15-19'],
        '20-34 years': ['20-24', '25-29', '30-34'],
        '35-54 years': ['35-39', '40-44', '45-49', '50-54'],
        '55-64 years': ['55-59', '60-64'],
        '65+ years': ['65-69', '70+']
    }

    for new_age, cols_to_mean in new_age_groups.items():
        cols_to_mean = [col for col in cols_to_mean if col in short_cols_names]
        df[new_age] = df[cols_to_mean].mean(axis=1)

    df = df.drop(short_cols_names, axis=1)
    df['Continent'] = df['Code'].apply(country_code_to_continent_name)
    return df


def process_prevalence_by_sex_data(file_path):
    df = pd.read_csv(file_path, encoding='utf-8')
    df_cleaned = df.drop(['Population (historical estimates)', 'Continent'], axis=1)
    sex_cols = ['Male', 'Female']
    first_cols_names = df.columns[:3].tolist()
    new_cols_names = first_cols_names + sex_cols
    df_cleaned.columns = new_cols_names
    df_cleaned['Continent'] = df_cleaned['Code'].apply(country_code_to_continent_name)
    return df_cleaned


def get_population_data(entities=None, year=None):
    df_pop = pd.read_csv(file_sex_paths[0])
    df_pop = df_pop.drop(
        [
            'Anxiety disorders (share of population) - Sex: Male - Age: All ages',
            'Anxiety disorders (share of population) - Sex: Female - Age: Age-standardized',
            'Continent'
        ],
        axis=1
    )
    df_pop = df_pop.rename(columns={'Population (historical estimates)': 'Population'})
    df_pop['Continent'] = df_pop['Code'].apply(country_code_to_continent_name)

    if year and entities:
        df_pop = df_pop.query('Entity in @entities and Year == @year')

    return df_pop


# Disorder Prevalence Data:
DisorderDataframe = namedtuple(
    'DisorderDataframe',
    [
        'disorder_name',
        'prevalence_by_country',
        'prevalence_by_year',
        'prevalence_and_gdp',
        'prevalence_by_age',
        'prevalence_by_sex',
        'pastel_color',
        'color_scale'
    ]
)

anxiety_disorder = DisorderDataframe(
    'Anxiety',
    *[process_general_data(file_paths[0], 'Anxiety')[i] for i in range(2)],
    process_gdp_data(file_gdp_paths[0]),
    process_prevalence_by_age_data(file_age_paths[0]),
    process_prevalence_by_sex_data(file_sex_paths[0]),
    '#7FC6A4',
    px.colors.sequential.Greens
)

bipolar_disorder = DisorderDataframe(
    'Bipolar',
    *[process_general_data(file_paths[1], 'Bipolar')[i] for i in range(2)],
    None,
    process_prevalence_by_age_data(file_age_paths[1]),
    process_prevalence_by_sex_data(file_sex_paths[1]),
    '#FF6B6B',
    px.colors.sequential.Reds
)

depressive_disorder = DisorderDataframe(
    'Depressive',
    *[process_general_data(file_paths[2], 'Depressive')[i] for i in range(2)],
    process_gdp_data(file_gdp_paths[1]),
    process_prevalence_by_age_data(file_age_paths[2]),
    process_prevalence_by_sex_data(file_sex_paths[2]),
    '#FFD580',
    px.colors.sequential.Oranges
)
eating_disorder = DisorderDataframe(
    'Eating',
    *[process_general_data(file_paths[3], 'Eating')[i] for i in range(2)],
    None,
    None,
    process_prevalence_by_sex_data(file_sex_paths[3]),
    '#C5A3FF',
    px.colors.sequential.Magenta
)

schizophrenia_disorder = DisorderDataframe(
    'Schizophrenia',
    *[process_general_data(file_paths[4], 'Schizophrenia')[i] for i in range(2)],
    None,
    process_prevalence_by_age_data(file_age_paths[3]),
    process_prevalence_by_sex_data(file_sex_paths[4]),
    '#A0D2EB',
    px.colors.sequential.Bluyl,
)

all_disorders_dataframes = {
    'Anxiety': anxiety_disorder,
    'Depressive': depressive_disorder,
    'Bipolar': bipolar_disorder,
    'Eating': eating_disorder,
    'Schizophrenia': schizophrenia_disorder

}

# Faire une boucle du mapping (loop à travers liste 'anxiety', 'depressive', etc.)
