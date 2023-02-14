# Analysis of 2010 Environmental Performance Index (EPI) and Corruption Index Scores on Western Europe Countries 
An EPI and Corruption Index Exploratory Data Analysis (EDA) project using Python and SQLAlchemy that explores the effects of corruption on Environmental Performance Index (EPI) of Western Europe countries in 2010. 
## About The Project 
Exploratory Data Analysis (EDA) is the crucial process of using statistics and graphs to perform preliminary investigations on data in order to uncover patterns, trends, detect anomalies, and test hypotheses. Before performing any kind of data analysis, raw data needs to be cleaned and stuctured via the ETL pipeline, a core concept of extracting, transforming, and loading data. 

![](https://github.com/tpham16/EPI_Analysis/blob/main/resources/ETL%20pipeline.png)

For this EDA project, I explored the effects of corruption on environmental performance on Western Europe Countries. 

## Built With
* [pandas](https://pandas.pydata.org/docs/)
* [sqlalchemy](https://www.sqlalchemy.org/)
* PostgreSQL and PgAdmin
* Python 3.7
* Jupyter Notebook

## Getting Started
### Install SQLAlchemy
SQLAlchemy 
  ```sh
  pip install sqlalchemy
  ```
## Usage 

In order to get the project running, I pulled EPI data from the database by connecting to the database using SQLAlchemy, a Python SQL toolkit that allows me to access and manage SQL databses using Python. Then, I create an epi table object by using 'create_object' and passing the location of the database that created in Postgres. 

```sh 
engine = create_engine('postgresql+psycopg2://postgres:password@localhost:5432/epi')
session = Session(engine)
```
After extracting the EPI dataframe into the eda.py file, I filtered to a specific subregion and saved that EPI data into a dataframe. 

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
After performing a left join, I generated 3 visualizations (scatter-plots, bar-graphs, histograms) using in-built Pandas functions. In the scatter plot, there is a low positive correlation between EPI and Corruption for West European Countries. 
```sh
scatter_plot = corr_epi.plot.scatter(y ='epi', x ='score', title = 'Scatter Plot of EPI and Corruption Index Scores (2010)',bins=20)
scatter_plot.figure.savefig('resources/scatter.png', dpi=300)
```
![Scatter-Plot](https://github.com/tpham16/EPI_Analysis/blob/main/resources/scatter.png)

The bar graph does not provide enough data to draw a correlation between the Environmental Performance Index (EPI) and Corruption. 

![Bar-Plot](https://github.com/tpham16/EPI_Analysis/blob/main/resources/bar.png)

In the histogram, the distribution is slightly right skewed and most of the values in the distribution fall into the range of EPI score of 70-80.

![Hist-Plot](https://github.com/tpham16/EPI_Analysis/blob/main/resources/hist.png)

With these findings, there is a slight positive correlation between EPI and higher corruption index scores. However, there is not enough data to draw conclusions due to various outliers which showed that countries with lower corruption index scores having similar EPIs.
