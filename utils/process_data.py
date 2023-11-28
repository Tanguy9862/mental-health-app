import pandas as pd

DATA_PATH = 'data/'


def process_data(file_path, disorder_name):
    df = pd.read_csv(file_path)
    df.rename(columns={df.columns[-1]: 'Value'}, inplace=True)
    df['Disorder'] = disorder_name
    # print(df)
    grouped_by_year = df.groupby(['Year', 'Disorder'])['Value'].mean().reset_index().round(3)
    return df, grouped_by_year


file_paths = [
    f'{DATA_PATH}/anxiety-disorders-prevalence.csv',
    f'{DATA_PATH}/bipolar-disorder-prevalence.csv',
    f'{DATA_PATH}/depressive-disorders-prevalence-ihme.csv',
    f'{DATA_PATH}/eating-disorders-prevalence.csv',
]

# Prevalence per country and year:
anxiety_by_country = process_data(file_paths[0], 'Anxiety')[0]
bipolar_by_country = process_data(file_paths[0], 'Bipolar')[0]
depressive_by_country = process_data(file_paths[0], 'Depressive')[0]
eating_by_country = process_data(file_paths[0], 'Eating')[0]

# Prevalence grouped by year (all countries):
anxiety_prevalence = process_data(file_paths[0], 'Anxiety')[1]
bipolar_prevalence = process_data(file_paths[1], 'Bipolar')[1]
depressive_prevalence = process_data(file_paths[2], 'Depressive')[1]
eating_prevalence = process_data(file_paths[3], 'Eating')[1]
