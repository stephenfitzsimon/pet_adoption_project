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

def chi_square_mass_test(df, cat_cols, target_col = 'target_outcome', alpha=0.05):
    """
    Performs a chi square test for all the aubcategories pass to cat_cols against the
    target_col
    """
    outputs = []
    for cat in cat_cols:
        for subcat in list(df[cat].unique()):
            for target_col_subcat in list(df[target_col].unique()):
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

def chi_square_test(var_one, var_two, alpha = 0.05):
    outputs = []
    observed = pd.crosstab(var_one, var_two)
    chi2, p, degf, expected = stats.chi2_contingency(observed)
    output = {
        'χ^2' : chi2,
        'p' : p,
        'reject_null': p < alpha
    }
    outputs.append(output)
    return pd.DataFrame(outputs)

def t_test_lesser(df, column_cat, subcat_val, column_cont, alpha = 0.05):
    '''Perform a t-test that mean is lesser than pop'''
    #get subsets
    category_x = df[df[column_cat] == subcat_val][column_cont]
    not_category_x = df[~(df[column_cat] == subcat_val)][column_cont].mean()
    #perform test
    t, p = stats.ttest_1samp(category_x, not_category_x)
    #organize results
    output = {
        'category_name':column_cat,
        'category_value':subcat_val,
        't-stat': t,
        'p-value':p,
        'reject_null': p/2 < alpha and t < 0
    }
    #return results
    return pd.DataFrame([output])

def get_top_ten_compare(df, outcome, animal, cat, normalized = True):
    top_ten_1 = df[(df.target_outcome==outcome)&(df.animal_type==animal)][cat].value_counts(normalize= normalized)
    top_ten_2 = df[(df.animal_type==animal)][cat].value_counts(normalize = normalized)
    top_ten_1 = top_ten_1.rename(f"Most common {cat} at {outcome}")
    top_ten_2 = top_ten_2.rename(f"Most common {cat} at intake")
    compare_df = pd.concat([top_ten_1, top_ten_2], axis=1)
    compare_df['difference'] = compare_df[f"Most common {cat} at {outcome}"] - compare_df[f"Most common {cat} at intake"]
    return compare_df

def mann_whitney(sample_1, sample_2, alpha=0.05):
    outputs = []
    stat, p = stats.mannwhitneyu(sample_1, sample_2, alternative='less')
    output = {
        'U-Stat':stat,
        'p-value':p,
        'reject_null': p/2 < alpha
    }
    outputs.append(output)
    return pd.DataFrame(outputs)
