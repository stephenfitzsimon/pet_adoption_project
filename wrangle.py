import os
import requests
import pandas as pd
from sodapy import Socrata

## TOP LEVEL FLOW CONTROL FUNCTIONS ##

def get_pet_dataframe():
    df_o, df_i = get_pet_data()
    df_i = rename_intake(df_i)
    df = join_tables(df_o, df_i)
    return df

## FUNCTIONS TO JOIN TABLES ##

def join_tables(df_o, df_i):
    df_i = df_i.drop_duplicates(subset='animal_id_i', keep=False)
    df_o = df_o.drop_duplicates(subset='animal_id', keep=False)
    df = df_o.merge(df_i, how='inner', left_on='animal_id', right_on='animal_id_i')
    df = df.drop(columns=['animal_id_i'])
    return df

def rename_intake(df):
    return df.add_suffix('_i')

## FUNCTIONS TO RETRIVE DATA FROM URL OR FILE ##

def download_data():
    """
    Returns the pet outcome and pet intake dataframes from the SODA
    """
    client = Socrata("data.austintexas.gov", None)
    results_outcome = client.get("9t4d-g238", limit=200_000)
    results_intake = client.get("wter-evkm", limit=200_000)

    # Convert to pandas DataFrame
    df_outcome = pd.DataFrame.from_records(results_outcome)
    df_intake = pd.DataFrame.from_records(results_intake)
    return df_outcome, df_intake

def get_pet_data(query_url = False):
    file_o = 'pet_outcomes.csv'
    file_i = 'pet_intake.csv'
    if os.path.isfile(file_o) and os.path.isfile(file_i) and not query_url:
        #return dataframe from file
        print('Returning saved csv files.')
        df_o = pd.read_csv(file_o).drop(columns = ['Unnamed: 0'])
        df_i = pd.read_csv(file_i).drop(columns = ['Unnamed: 0'])
        return df_o, df_i
    else:
        print('Getting data from url...')
        df_o, df_i = download_data()
        print('Saving to .csv files...')
        df_o.to_csv(file_o)
        df_i.to_csv(file_i)
        print('Returned dataframes.')
        return df_o, df_i

## FUNCTIONS TO CLEAN THE COLUMNS ##

def make_date_columns(df):
    df['datetime'] = pd.to_datetime(df['datetime'])
    df['monthyear'] = pd.to_datetime(df['monthyear'])
    df['dateime_i'] = pd.to_datetime(df['datetime_i'])
    df['datetime2_i'] = pd.to_datetime(df['datetime2_i'])
    df['outcome_date'] = df['monthyear'].dt.strftime('%m %d, %Y')
    df['intake_date'] = df['monthyear'].dt.strftime('%m %d, %Y')
    df = df.drop(columns = ['datetime', 'monthyear', 'datetime_i', 'datetime2_i'])
    return df

def null_fill_and_drop(df):
    df.name = df.name.fillna('no name')
    df.outcome_subtype = df.outcome_subtype.fillna('no subtype')
    df = df.drop(columns=['name_i', 'breed_i', 'color_i', 'animal_type_i'])
    df = df.dropna()
    return df