# The Analysis of 2010 Environmental Performance Index (EPI) and Corruption Index on Western European Countries 
A ETL (Extract, Transform, Load) project ... which moves data from a source into a database. 
## About The Project 
For this project, I built a ETL pipeline in Python. In order to accomplish this, I pulled EPI data from my postgres databases and saved it into a dataframe using SQLAlchemy, a Python SQL toolkit that allows me to access and manage SQL databses using Python. Using Pandas, I loaded the 'Corruption Index' dataset to explore the analysis between EPIs and measurements of Corruption. I then filtered the data according to a specific geographic subregion. For this project, I selected Western Europe. After filting the data, I generated 3 visualizations (scatter-plots, bar-graphs, histograms) that describe the relationship between EPI and corruption scores. 

## Built With
* [pandas](https://pandas.pydata.org/docs/)
* [sqlalchemy](https://www.sqlalchemy.org/)

## Getting Started
### Install SQLAlchemy

* SQLAlchemy 
  ```sh
  pip install sqlalchemy -g
  ```

## Usage 
First, I created an engine object using 'create_object' and passed the location of the database that created in Postgres. Then, I created a connection object by connecting the engine. 

```
# psycopg2
engine = create_engine('postgresql+psycopg2://postgres:password@localhost:5432/epi')
session = Session(engine)
```
After extracting the EPI dataframe into the eda.py file, I filtered to a specific subregion and saved into a dataframe. 

```
# filter data to a specific geographic subregion 
rows = query.filter(epi_country.geo_subregion == 'Western Europe').all()
# save EPI data into a dataframe
epi_df = pd.DataFrame(rows, columns=["country", "air_h", "water_h", "biodiversity", "fisheries", "epi", "geo_subregion"])
```

Then, I created and imported a new dataframe using Pandas and saved it back into the Postgres database. 
```
# save it back into postgres database
corr_df.to_sql('corruption_epi', engine, if_exists='replace', index = False)

corr_epi = epi_df.merge(corr_df, how="left", on="country")

```
## Findings 
Finally, I generated 3 visualizations (scatter-plots, bar-graphs, histograms)