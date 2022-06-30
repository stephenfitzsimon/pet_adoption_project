#pet adoption explore module
#Stephen FitzSimon
from scipy import stats
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

def chi_square_test(df, cat_cols, target_col = 'target_outcome', alpha=0.05):
    """
    Performs a chi square test for all the aubcategories pass to cat_cols against the
    target_col
    """
    outputs = []
    for cat in cat_cols:
        for subcat in list(df[cat].unique()):
            for target_col_subcat in list(df['target_outcome'].unique()):
                #get the crosstab between the two variables
                observed = pd.crosstab(df[target_col]==target_col_subcat, df[cat]==subcat)
                #calculate the statistic
                chi2, p, degf, expected = stats.chi2_contingency(observed)
                #save the calculation
                output = {
                        'target_column':target_col,
                        'column':cat,
                        'target_col_subcat':target_col_subcat,
                        'column_subcat':subcat,
                        'null_hypothesis':f"{target_col_subcat} independent of {subcat}",
                        'chi2':chi2,
                        'p':p,
                        'reject_null':p < alpha
                }
                outputs.append(output)
    #return the dataframe
    return pd.DataFrame(outputs)