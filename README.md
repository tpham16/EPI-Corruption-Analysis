# The Analysis of 2010 Environmental Performance Index (EPI) and Corruption Index on Western European Countries 
An EPI and Corruption Index ETL project using Python and SQLAlchemy.  
## About The Project 
In order to perform any kind of data anaylys, raw data needs to be cleaned and structured. Data pipeline ETL, extract, transform, and load is a core concept in data analysis. 

![](https://github.com/tpham16/EPI_Analysis/blob/main/resources/ETL.png)

For this project, I built a ETL pipeline in Python to practice this concept. In order to accomplish this, I pulled EPI data from my postgres databases and saved it into a dataframe using SQLAlchemy, a Python SQL toolkit that allows me to access and manage SQL databses using Python. Using Pandas, I loaded the 'Corruption Index' dataset to explore the analysis between EPIs and measurements of Corruption. I then filtered the data according to a specific geographic subregion. For this project, I selected Western Europe. After filting the data, I generated 3 visualizations (scatter-plots, bar-graphs, histograms) that describe the relationship between EPI and corruption scores. 

## Built With
* [pandas](https://pandas.pydata.org/docs/)
* [sqlalchemy](https://www.sqlalchemy.org/)
* PostgreSQL and PgAdmin
* Python 3.7
* Jupyter Notebook

## Getting Started
### Install SQLAlchemy

* SQLAlchemy 
  ```sh
  pip install sqlalchemy
  ```

## Usage 
First, I created an engine object using 'create_object' and passed the location of the database that created in Postgres. Then, I created a connection object by connecting the engine. 

```sh 
# create an SQLAlchemy engine using psycopg2
engine = create_engine('postgresql+psycopg2://postgres:password@localhost:5432/epi')
session = Session(engine)
```
After extracting the EPI dataframe into the eda.py file, I filtered to a specific subregion and saved the EPI data into a dataframe. 

```sh 
rows = query.filter(epi_country.geo_subregion == 'Western Europe').all()

epi_df = pd.DataFrame(rows, columns=["country", "air_h", "water_h", "biodiversity", "fisheries", "epi", "geo_subregion"])
```

Then, I loaded in the Corruption Index dataset using Pandas and performed a 'left join' on EPI data on the newly loaded Corruption Index dataset. 

```sh

corr_df = pd.read_csv('CPI-2010-new_200601_105629.csv')

corr_df.to_sql('corruption_epi', engine, if_exists='replace', index = False)

corr_epi = epi_df.merge(corr_df, how="left", on="country")

```

## Findings 
After performing a left join, I generated 3 visualizations (scatter-plots, bar-graphs, histograms) using in-built Pandas functions. In the scatter plot, there is a low positive correlation between EPI and Corruption for European Countries. 
```sh
corr_epi.plot.scatter(y ='epi', x ='score', title = 'Scatter Plot of Environmental Performance Index (EPI) Scores and Corruption')
```
![Scatter-Plot](https://github.com/tpham16/EPI_Analysis/blob/main/resources/scatter-plot.png)

The bar graph does not provide enough data to draw a between the Environmental Performance Index (EPI) and Corruption. 

![Bar-Plot](https://github.com/tpham16/EPI_Analysis/blob/main/resources/bar-plot.png)

In the histogram, the distribution is slightly right skewed and most of the values in the distribution fall into the range of EPI score of 70-80.

![Hist-Plot](https://github.com/tpham16/EPI_Analysis/blob/main/resources/hist-plot.png)

With these findings, there is a slight positive correlation between EPI and higher corruption index scores. However, there is not enought data to draw conclusions due to various outliers which showed that countries with lower corruption index scores having similar EPIs.
