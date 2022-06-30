#pet adoption explore module
#Stephen FitzSimon
import pandas as pd

def get_percent_outcome(df, target_col = 'target_outcome', cat_cols = ['animal_type', 'sex_upon_outcome', 'intake_type', 'intake_condition', 'sex_upon_intake']):
    """"
    Gets the proportion of each value in target_col for cat_cols passed and each subcategory
    in the cat_cols column.  Essentially performs a value_counts(normalize=True) on 
    each category for the target_col values
    """
    #stores the outputs
    outputs = []
    for cat in cat_cols:
        #get every subcategory in the column
        for subcat in list(df[cat].unique()):
            #get every outcome for each
            for outcome in list(df[target_col].unique()):
                #get the data and store it 
                output = {
                        'column':cat,
                        'column_subcat':subcat,
                        'outcome':outcome,
                        'total':(df[df[cat]==subcat].target_outcome == outcome).sum(),
                        'proportion': (df[df[cat]==subcat].target_outcome == outcome).mean()
                }
                #add the calculation to the outputs
                outputs.append(output)
    #return as a dataframe
    return pd.DataFrame(outputs)