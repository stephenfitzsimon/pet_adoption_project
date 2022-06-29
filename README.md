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

## Explore Data