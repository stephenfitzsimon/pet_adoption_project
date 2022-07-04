# Austin Shelter Pet Outcomes

## Key Takeaways

- Strays in normal condition at intake are most likely to be adopted
- Average stay is 26 days for dogs and 40 for cats.
- A decision tree model is $0.73$ accurate at predicting animal outcomes

## Contents <a name='contents'></a>

*Note: the following hyperlinks will only work on local copies of this notebook; they will not function on GitHub!*

1. <a href='introduction'>Introduction</a>
    1. <a href='repo_structure'> What Files Are In This Repo </a>
    1. <a href='data_source'>Data Source</a>
2. <a href='wrangle'>Wrangle Data</a>
3. <a href='#exploring'>Exploring The Data</a>
4. <a href='#model'>Modeling</a>
5. <a href='#data_dictionary'>Data Dictionary</a>

## Introduction <a name='introduction'></a>

<a href='https://www.austintexas.gov/austin-animal-center'>Austin Animal Center</a> provides animal services for the city of Austin, and unincorporated Travis county.  Since 2010 they have implemented a <a href='https://www.austintexas.gov/page/no-kill-plan'>'no-kill' strategy</a> to increase live outcomes for adoptions; this included community partnerships, community education, increased animal services and better data collection.  The goal of this project is to help understand how the Austin Animal Center can provide better services and outcomes for the animals and owners that they serve.

#### Project Goals
- Determine drivers of adoption to help shelter staff manage resources efficiently
- Build a model to help staff determine the adoptability of an animal, allowing more resources to be saved for harder to adopt animals
- Analyze adoption data to help shelter implement the 'no-kill' policy enacted in 2010.

### What Files Are In This Repo <a name='repo_structure'></a>
- `wrangle.py` : contains all the functions to retrieve the data and prepare it for exploration
- `explore.py` : contains all function to perform calculations and statistical test used in the exploratory analysis
- `modelling.py` : contains all function to create models, mass model metrics, and making the ensemble model

### Data Source <a name='data_source'></a>
The City of Austin provides an <a href='https://data.austintexas.gov/'>open data website</a> where the data for this project can be found.
- <a href= 'https://data.austintexas.gov/Health-and-Community-Services/Austin-Animal-Center-Outcomes/9t4d-g238'>Outcome data can be found here</a>
- <a href= 'https://data.austintexas.gov/Health-and-Community-Services/Austin-Animal-Center-Intakes/wter-evkm'>Intake data can be found here</a>
    
### Intro to the Target Variable
    
The model attempts to predict the outcomes for animals the first time they arrive at the shelter.  In the interest of simplicity, the various categories in the `outcome_type` column are aggregated into four categories. The model attempts to predict one of for outcomes as aggregated from the `outcome_type` column of the data:
1. Adoption
2. Transfer
3. Return to Owner (include Rto-Adopt category)
4. Other (includes the following: euthanised, died, disposal, missing, relocate, lost)

Many of the outcomes in the Other category were due to non-pet status (for example `A860153` is a bat and `A860288` is a grackle, both of which at intake were injured).  Or of the euthanised/died animals, most were considered suffering/sick/injured.

<a href='contents'>Back to Contents</a>

## Wrangle Data <a name='wrangle'></a>

### Key Wrangle Takeaways
- Two tables of data are retrieved from the Austin <a href='https://data.austintexas.gov/'>open data website</a>
- The `Outcome` table contained 141170 records and 12 columns; the `Intake` table contained 141303 records and 12 columns
- Both tables were merged on the key `animal_id`
    - Duplicate records were dropped.  Many of the duplicate records were the same animal.
- Date columns were aggregated into `intake_date` and `outcome_date` and scaled to days
- Repeated columns were removed (example: `color` and `breed` were the same for both intake and outcome tables)
- `name` and `outcome_subtype` had null values inferred
- Remaining nulls were dropped
- Final table is 113944 rows and 16 columns

<a href='contents'>Back to Contents</a>

## Exploring The Data <a name='exploring'></a>

### Key Explore Takeaways
- Overall adoption rate is $0.43$; adoption and transfer represent the majority of outcomes ($0.76$ of all outcomes)
- As the majority of animals in the data are cats or dogs ($0.92$ of the data), the majority of the exploration focuses on these two animal types
    - The adoption rate among cats and dogs is $0.45$
- Most animals are brought in as strays ($0.72$) and are in normal condition ($0.84$)
- The average age of adoption of animals is 183 days old
- Intake and adoption rates peak in May-June, and is largely driven by seasonality of cat intakes
- The average length of stay at the shelter is 26 days for dogs and 40 for cats.

### Discussion

The overall adoption rate in the data is $0.43$.  However, the majority of the data ($0.92$) represents cats and dogs which have a higher adoption rate of $0.45$.  This would be expected as, based off of experience, the majority of people who visit a shelter are looking to adopt a cat or a dog.  In addition, $0.67$ of the non cat or dog animals were categorized as wildlife (the majority of which were bats), and are not adoptable.  This is also shown by the fact that dogs and cats represent $0.92$ of all adoptions and $0.96$ of all transfers.

In terms of animal intake, the most common intake type is stray, representing $0.72$ of all intakes.  The majority of these animals are classified as 'normal' condition, representing $0.84$ of all intakes.  Stray intakes represent $0.44$ of all adotions.  However, $0.58$ of all adoptions are owner surrenders; this might be surprising, as it might be expected that owners surrender problem pets, but this might not be the case. 

Younger animals are more adoptable; most animals are adotped at 183 days old.  There was not a major difference between animal types. Intakes for all animals peak in May-June, with adoptions peaking at the same time.  This is largely driven by cats; cat intakes and adoptions peak in the summer, whereas dog intake and adoption is relatively constant throughout the year. 

Happily, owners seem to not be looking for a particular breed/color to adopt. Among cats, the colors match up nearly perfectly; the one exception seems that black cats are slightly more difficult to adopt.  In terms of dog breed, Labrador Retrievers are easier to adopt; even though there are mainly Pit Bull Mixes that are more likely to be received at intake (there is a $-0.015$ difference between the numbers, every other column has a difference of less than $\pm 0.01$).

The average length of stay of adopted animals is 32 days; however, dogs are adopted about 2 weeks earlier than cats.

<a href='#contents'>Back to Contents</a>

## Modeling <a name='model'></a>

### Key Takeaways
- Only modeling for dogs and cats, as these represent the majority of the data
- The following classification models are used: DecisionTree, RandomForest, ExtraTrees, LogisticRegression, K-Nearest Neighbors
- Calculated column representing length of stay is used in modeling, but is cast to `int`
- `intake_date` is transformed into an `int` representing the numeric representation of the month
- Baseline accuracy is $0.43$
- A decision tree model with a max depth of six improves on baseline with an accuracy of $0.73$ on unseen data

<a href='#contents'>Back to Contents</a>

## Conclusion <a name='conclusion'></a>

The model and analysis for this project explore the characteristics of animals that are likely to get adopted.  With a model accuracy of $0.73$ reasources can be allocated to animals that need more help getting adopted.  For example, animals with a lower probability might simply need to be socialized, or given to fosters who will work with shelter staff to find potential owners. 

This model could be deployed to the shelter staff to via integration with existing database systems, or via a dashboard for shelter managers.  It could also be extended via other models that could predict the length of stay of a particular animal.  A survey of already adopted animals and their owners might also provide insight into what type of owners would be useful to determine best animal-owner fits; particularly if there is some metric for animal personality.  Transfers to partner shelters/organizations are common; there may be some animals that are more likely to be adopted by partners--therefore data on adoption outcomes from partners would be beneficial to determine which animals would most benefit from being transfered to partner organizations.

### Ideas for the Future

- Build a model to predict shelter length of stay.
- Build an example dashboard to show where current reasources might best be placed
- Try out more model types, with different features in order to improve model accuracy
    - Try a piecewise model for each animal type
    - Look more into breed and color as predictors of adoption


## Data Dictionary <a name='data_dictionary'></a>

- `animal_id` : unique identifier per animal   
- `name` : animal name      
- `outcome_type` : animal outcome as defined by Austin Animal Center       
- `animal_type` : animal species      
- `sex_upon_outcome` : sex as fixed/unfixed male/female
- ` breed ` : breed of animal   
- `color`: animal color    
- `outcome_subtype` : outcome subtype
- `found_location` : address of animal pickup
- `intake_type` : intake type (stray, owner surrender, etc)
- `intake_condition` : animal condition at intake
- `sex_upon_intake` : sex at intake, indicated fixed/unfixed
- `outcome_date` : date of outcome
- `intake_date`  : intake date
- `target_outcome` : feature engineer of four target outcomes 
- `age_at_outcome` : age at outcome in days
- `age_at_intake`  : age at intake in days