#Pet Adoption wrangle.py
#Stephen FitzSimon
import os
import requests
import pandas as pd
from sklearn.model_selection import train_test_split
from sodapy import Socrata

RAND_SEED = 357

## TOP LEVEL FLOW CONTROL FUNCTIONS ##
# see called functions for more information

def get_pet_dataframe():
    """
    Flow control function to get dataframe from url or .csv file and join both tables
    """
    df_o, df_i = get_pet_data()
    df_i = rename_intake(df_i)
    df = join_tables(df_o, df_i)
    return df

def prepare_pet_dataframe(df):
    """
    Flow control function to prepare data
    """
    df = make_date_columns(df)
    df = make_target_column(df)
    df = null_fill_and_drop(df)
    df = convert_age_column(df)
    df = rename_intake_cols(df)
    df = replace_intake_conditions(df)
    return df

def make_pet_dataframe():
    """
    Flow control function to retrieve data and prepare it
    """
    df = get_pet_dataframe()
    df = prepare_pet_dataframe(df)
    return df

def make_model_sets(df):
    """
    Flow control function to make X and y sets for modeling
    """
    df = make_feature_columns_and_filter(df)
    df = drop_columns_for_model(df)
    X, y = make_X_and_y(df)
    X = make_dummies(X)
    return X, y

## FUNCTIONS TO JOIN TABLES ##

def replace_intake_conditions(df):
    df['intake_condition'] = df['intake_condition'].replace({
        'Med Attn':'Other',
        'Space':'Other', 
        'Med Urgent': 'Other', 
        'Agonal': 'Other', 
        'Panleuk':'Other'
        })
    return df

def join_tables(df_o, df_i):
    """
    Joins the intake and outake tables on the animal_id column
    """
    #drop duplicate records from each table
    df_i = df_i.drop_duplicates(subset='animal_id_i', keep=False)
    df_o = df_o.drop_duplicates(subset='animal_id', keep=False)
    #merge only files where iformation is present on both tables
    df = df_o.merge(df_i, how='inner', left_on='animal_id', right_on='animal_id_i')
    #drop unneeded key from the intake table
    df = df.drop(columns=['animal_id_i'])
    return df

def rename_intake(df):
    """"
    Suffixes the column names of the intake table to distinguish from outcome 
    columns after merge
    """
    return df.add_suffix('_i')

## FUNCTIONS TO RETRIVE DATA FROM URL OR FILE ##

def download_data():
    """
    Returns the pet outcome and pet intake dataframes from the SODA
    """
    #use the SODA API to retrieve data
    client = Socrata("data.austintexas.gov", None)
    #get the data from the particular tables
    results_outcome = client.get("9t4d-g238", limit=200_000)
    results_intake = client.get("wter-evkm", limit=200_000)
    # Convert to pandas DataFrame
    df_outcome = pd.DataFrame.from_records(results_outcome)
    df_intake = pd.DataFrame.from_records(results_intake)
    return df_outcome, df_intake

def get_pet_data(query_url = False):
    """"
    Checks if a csv file is present, and retrieves data from csv or url.  
    A url query can be forced via query_url=True
    """
    #filename constants
    file_o = 'pet_outcomes.csv'
    file_i = 'pet_intake.csv'
    #check for file existence
    if os.path.isfile(file_o) and os.path.isfile(file_i) and not query_url:
        #return dataframe from file
        print('Returning saved csv files.')
        #return files
        df_o = pd.read_csv(file_o).drop(columns = ['Unnamed: 0'])
        df_i = pd.read_csv(file_i).drop(columns = ['Unnamed: 0'])
        return df_o, df_i
    else:
        #get data from url
        print('Getting data from url...')
        df_o, df_i = download_data()
        print('Saving to .csv files...')
        #save data to csv.
        df_o.to_csv(file_o)
        df_i.to_csv(file_i)
        print('Returned dataframes.')
        #return to user
        return df_o, df_i

## FUNCTIONS TO CLEAN THE COLUMNS ##

def make_target_column(df):
    """
    Maps the various outcome_types to the target outcomes
    """
    new_data = []
    #go through each row
    for i, row in df.iterrows():
        #map the outcome_types to the aggregated categories
        if row['outcome_type'] == 'Adoption':
            target_string = 'Adoption'
        elif row['outcome_type'] == 'Transfer':
            target_string = 'Transfer'
        elif row['outcome_type'] in ['Returned to Owner', 'Rto-Adopt']:
            target_string = 'Return to Owner'
        else:
            target_string = 'Other'
        #add to the list of data
        datum_calc = {
            'animal_id':row['animal_id'],
            'target_outcome':target_string
        }
        new_data.append(datum_calc)
    #add to the dataframe
    df_calc = pd.DataFrame(new_data)
    df = df.merge(df_calc)
    #return dataframe
    return df

def make_date_columns(df):
    """"
    Aggregates datetime columns into outcome and intake dates
    """
    #cast columns to datatime dtype
    df['datetime'] = pd.to_datetime(df['datetime'])
    df['monthyear'] = pd.to_datetime(df['monthyear'])
    df['datetime_i'] = pd.to_datetime(df['datetime_i'])
    df['datetime2_i'] = pd.to_datetime(df['datetime2_i'])
    #extract needed dates
    df['outcome_date'] = df['monthyear'].dt.strftime('%m %d, %Y')
    df['intake_date'] = df['datetime_i'].dt.strftime('%m %d, %Y')
    #cast to datetime dtype
    df['outcome_date'] = pd.to_datetime(df['outcome_date'])
    df['intake_date'] = pd.to_datetime(df['intake_date'])
    #drop unneeded columns
    df = df.drop(columns = ['datetime', 'monthyear', 'datetime_i', 'datetime2_i'])
    return df

def null_fill_and_drop(df):
    """
    Fills nulls and drops null values. name columns nulls are inferred as no name and 
    outcome_subtype is inferred as no subtype.  remaining nulls are dropped
    """
    #fill name nulls
    df.name = df.name.fillna('no name')
    #fill outcome subtype nulls
    df.outcome_subtype = df.outcome_subtype.fillna('no subtype')
    #drop unneeded/repeated columns
    df = df.drop(columns=['name_i', 'breed_i', 'color_i', 'animal_type_i'])
    #drop nulls
    df = df.dropna()
    return df

def convert_age_column(df):
    """"
    Converts age columns to days
    """
    new_data = []
    #determine what to multiply by
    multipliers = {
        'day': 1,
        'days': 1,
        'week':7,
        'weeks':7,
        'month': 30.5,
        'months':30.5,
        'year':365.25,
        'years':365.25
    }
    #loop through every row of the dataframe
    for i, row in df.iterrows():
        #extract age information 
        outcome_age_split = row['age_upon_outcome'].split()
        #perform proper calculation
        outcome_age_calc = int(outcome_age_split[0])*multipliers[outcome_age_split[1]]
        #extract age information
        intake_age_split = row['age_upon_intake_i'].split()
        #perform proper calculation
        intake_age_calc = int(intake_age_split[0])*multipliers[intake_age_split[1]]
        #save data into a dictionary
        datum_calc = {
            'animal_id':row['animal_id'],
            'age_at_outcome':int(round(outcome_age_calc)),
            'age_at_intake':int(round(intake_age_calc)) 
        }
        #add to a list
        new_data.append(datum_calc)
    #make a dataframe
    df_calc = pd.DataFrame(new_data)
    #merge the dataframes on animal_id
    df = df.merge(df_calc)
    #drop converted columns
    return df.drop(columns = ['age_upon_outcome', 'age_upon_intake_i', 'date_of_birth'])

def rename_intake_cols(df):
    """"
    Renames the columns from the intake table to make calling them easier
    """
    df = df.rename(columns = {'found_location_i':'found_location',
                    'intake_type_i':'intake_type',
                    'intake_condition_i': 'intake_condition',
                    'sex_upon_intake_i': 'sex_upon_intake'})
    return df

## FUNCTIONS TO HELP WITH MODELING AND EXPLORATION

def split_data(df):
    '''splits the pet dataframe into train, test and validate subsets
    
    Args:
        df (DataFrame) : dataframe to split
    Return:
        train, test, validate (DataFrame) :  dataframes split from the original dataframe
    '''
    #make train and test
    train, test = train_test_split(df, train_size = 0.8, stratify=df[['target_outcome']], random_state=RAND_SEED)
    #make validate
    train, validate = train_test_split(train, train_size = 0.7, stratify=train[['target_outcome']], random_state=RAND_SEED)
    return train, validate, test

def make_feature_columns_and_filter(df):
    """
    Filters to only cats and dogs, and makes length_of_stay column
    """
    df = df[df['animal_type'].isin(['Cat', 'Dog'])]
    df = df[~df['intake_type'].isin(['Wildlife'])]
    df['length_of_stay'] = (df.outcome_date-df.intake_date).dt.days
    df['intake_date'] = df['intake_date'].dt.month
    df['breed'] = df['breed'].str.replace('/', ' ')
    df['color'] = df['color'].str.replace('/', ' ')
    color_column_list = [
        'Black',
        'White',
        'Brown',
        'Tabby',
        'Orange',
        'Tan',
        'Blue',
        'Tricolor',
        'Tortie',
        'Calico',
        'Red',
        'Torbie',
        'Brindle',
        'Cream',
        'Yellow',
        'Buff',
        'Sable',
        'Grey',
    ]
    for color_name in color_column_list:
        df[f'is_{color_name}'] = df['color'].str.contains(color_name)
    df['is_other_color'] = ~df['color'].isin(color_column_list)
    breed_column_list = [
        'Shorthair',
        'Medium Hair',
        'Longhair',
        'Mix',
        'Pit Bull',
        'Labrador Retriever',
        'Chihuahua',
        'German Shepherd',
        'Australian Cattle Dog',
        'Dachshund',
        'Border Collie',
        'Boxer',
        'Miniature Poodle',
        'Australian Shepherd',
        'Yorkshire Terrier',
        'Miniature Schnauzer',
        'Great Pyrenees',
        'Siberian Husky',
        'Rat Terrier',
        'Beagle',
        'Jack Russell Terrier',
        'Staffordshire',
        'Pointer'
        'Siamese'
    ]
    for breed_name in breed_column_list:
        df[f'is_{breed_name}'] = df['breed'].str.contains(breed_name)
    df['is_other_breed'] = ~df['breed'].isin(breed_column_list)
    return df

def make_X_and_y(df):
    '''Makes a X and y sets'''
    #drop relevant columns
    X_df = df.drop(columns = ['target_outcome'])
    #make y_Train
    y_df = df[['animal_id', 'target_outcome']]
    return X_df, y_df

def drop_columns_for_model(df):
    return df.drop(columns = ['outcome_date', 'breed', 'color', 'name', 'sex_upon_outcome', 'sex_upon_intake', 'outcome_type', 'outcome_subtype', 'found_location'])

def make_dummies(df):
    '''creates all catagorical columns into encoded columns'''
    #get all catagorical columns
    cat_cols = list(df.select_dtypes(include = ['object', 'bool']).iloc[:,1:].columns)
    # make dummy columns
    dummy_df = pd.get_dummies(df[cat_cols], dummy_na = False, drop_first = True)
    df = pd.concat([df, dummy_df], axis = 1)
    return df.drop(columns = list(df.select_dtypes(include = ['object']).columns))