import pandas as pd
from utils.process_data import get_continent_name, country_code_to_continent_name
from utils.ga_utils import clean_duplicated_columns

DATA_PATH = 'data/surveys'


def process_and_clean_survey_data():

    # APPROACHES WHEN DEALING WITH ANXIETY AND DEPRESSION PROCESSING
    approaches_df = pd.read_csv(f'{DATA_PATH}/dealing-with-anxiety-depression-approaches.csv')
    approaches_df['Continent'] = approaches_df['Code'].apply(country_code_to_continent_name)
    approaches_df.rename(columns={
        'Share - Question: mh8b - Engaged in religious/spiritual activities when anxious/depressed - Answer: Yes - Gender: all - Age_group: all': 'Engaged in Religious or Spiritual Activities when Anxious or Depressed',
        'Share - Question: mh8e - Improved healthy lifestyle behaviors when anxious/depressed - Answer: Yes - Gender: all - Age_group: all': 'Improved Healthy Lifestyle Behaviors when Anxious or Depressed',
        'Share - Question: mh8f - Made a change to work situation when anxious/depressed - Answer: Yes - Gender: all - Age_group: all': 'Made a Change to Work Situation when Anxious or Depressed',
        'Share - Question: mh8g - Made a change to personal relationships when anxious/depressed - Answer: Yes - Gender: all - Age_group: all': 'Made a Change to Personal Relationships when Anxious or Depressed',
        'Share - Question: mh8c - Talked to friends or family when anxious/depressed - Answer: Yes - Gender: all - Age_group: all': 'Talked to Friends or Family when Anxious or Depressed',
        'Share - Question: mh8d - Took prescribed medication when anxious/depressed - Answer: Yes - Gender: all - Age_group: all': 'Took Prescribed Medication when Anxious or Depressed',
        'Share - Question: mh8h - Spent time in nature/the outdoors when anxious/depressed - Answer: Yes - Gender: all - Age_group: all': 'Spent Time in Nature or Outdoors when Anxious or Depressed',
        'Share - Question: mh8a - Talked to mental health professional when anxious/depressed - Answer: Yes - Gender: all - Age_group: all': 'Talked to a Mental Health Professional when Anxious or Depressed'
    }, inplace=True)

    # DISCOMFORT SPEAKING ANXIETY AND DEPRESSION PROCESSING
    discomfort_df = pd.read_csv(f'{DATA_PATH}/discomfort-speaking-anxiety-depression.csv')
    discomfort_df.rename(columns={
        'Share - Question: mh5 - Someone local comfortable speaking about anxiety/depression with someone they know - Answer: Not at all comfortable - Gender: all - Age_group: all': 'Not Comfortable Discussing Anxiety/Depression with Acquaintances'
    }, inplace=True)
    discomfort_df['Continent'] = discomfort_df['Code'].apply(country_code_to_continent_name)

    # FUND RESEARCH ON ANXIETY AND DEPRESSION PROCESSING
    fund_df = pd.read_csv(f'{DATA_PATH}/fund-research-anxiety-depression.csv')
    fund_df.rename(columns={
        'Share - Question: mh4b - Important for national government to fund research on anxiety/depression - Answer: Extremely important - Gender: all - Age_group: all': 'View on National Government Funding for Anxiety/Depression Research as Extremely Important'
    }, inplace=True)
    fund_df['Continent'] = fund_df['Code'].apply(country_code_to_continent_name)

    fund_df = fund_df.dropna(subset=[
        'View on National Government Funding for Anxiety/Depression Research as Extremely Important',
    ])
    fund_df = fund_df.drop(columns=[
        'Population (historical estimates)',
        'GDP per capita, PPP (constant 2017 international $)'
    ])

    return approaches_df, discomfort_df, fund_df


approaches_df, discomfort_df, fund_df = process_and_clean_survey_data()
merged_survey_df = clean_duplicated_columns(approaches_df.merge(discomfort_df, on='Entity', how='inner'))
merged_survey_df = clean_duplicated_columns(merged_survey_df.merge(fund_df, on='Entity', how='inner'))





