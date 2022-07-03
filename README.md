# Austin Shelter Pet Outcomes

## Contents <a name='contents'></a>

*Note: the following hyperlinks will only work on local copies of this notebook; they will not function on GitHub!*

1. <a href='introduction'>Introduction</a>
    1. <a href='repo_structure'> What Files Are In This Repo </a>
    1. <a href='data_source'>Data Source</a>
2. <a href='wrangle'>Wrangle Data</a>

## Introduction <a name='introduction'></a>

<a href='https://www.austintexas.gov/austin-animal-center'>Austin Animal Center</a> provides animal services for the city of Austin, and unincorporated Travis county.  Since 2010 they have implemented a <a href='https://www.austintexas.gov/page/no-kill-plan'>'no-kill' strategy</a> to increase live outcomes for adoptions; this included community partnerships, community education, increased animal services and better data collection.  The goal of this project is to help understand how the Austin Animal Center can provide better services and outcomes for the animals and owners that they serve.

#### Project Goals
- Determine drivers of adoption to help shelter staff manage resources efficiently
- Build a model to help staff determine the adoptability of an animal, allowing more resources to be saved for harder to adopt animals
- Analyze adoption data to help shelter implement the 'no-kill' policy enacted in 2010.

### What Files Are In This Repo <a name='repo_structure'></a>
- `wrangle.py` : contains all the functions to retrieve the data and prepare it for exploration
- `wrangle_notes.ipynb` : Contains notes and development for the `wrangle.py` functions

### Data Source <a name='data_source'></a>
The City of Austin provides an <a href='https://data.austintexas.gov/'>open data websit</a> where the data for this project can be found.
- <a href= 'https://data.austintexas.gov/Health-and-Community-Services/Austin-Animal-Center-Outcomes/9t4d-g238'>Outcome data can be found here</a>
- <a href= 'https://data.austintexas.gov/Health-and-Community-Services/Austin-Animal-Center-Intakes/wter-evkm'>Intake data can be found here</a>

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
- Classification models are used
- Calculated column representing length of stay is used in modeling, but is cast to `int`
- `intake_date` is transformed into an `int` representing the numeric representation of the month
- Baseline accuracy is $0.46$