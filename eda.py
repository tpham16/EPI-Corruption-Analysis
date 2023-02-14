from sqlalchemy import create_engine, func
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
import pandas as pd

# connect to database and create an epi table object
engine = create_engine('postgresql+psycopg2://postgres:password@localhost:5432/epi')
Base = automap_base()
Base.prepare(engine, reflect=True)

epi_country = Base.classes.epi_country

# query database 
session = Session(engine)

# make a query for selected rows 
query = session.query(
    epi_country.country, 
    epi_country.air_h, 
    epi_country.water_h, 
    epi_country.biodiversity, 
    epi_country.fisheries, 
    epi_country.epi, 
    epi_country.geo_subregion
)

# filter data to a specific geographic subregion 
rows = query.filter(epi_country.geo_subregion == 'Western Europe').all()

# save EPI data into a dataframe
epi_df = pd.DataFrame(rows, columns=["country", "air_h", "water_h", "biodiversity", "fisheries", "epi", "geo_subregion"])

# load CSV file into pipeline as a dataframe using Pandas
corr_df = pd.read_csv('CPI-2010-new_200601_105629.csv')

# lowercase all countries in corr_df
corr_df.columns = [col.lower() for col in corr_df.columns]

# save it back into postgres database
corr_df.to_sql('corruption_epi', engine, if_exists='replace')

corr_epi = epi_df.merge(corr_df, how="left", on="country")

# generate scatter plot, bar graphs, histograms comparing Corruption Scores and EPI
scatter_plot = corr_epi.plot.scatter(y ='epi', x ='score', title = 'Scatter Plot of EPI and Corruption Index Scores (2010)',bins=20)
scatter_plot.figure.savefig('resources/scatter.png', dpi=300)

bar_plot = corr_epi.plot.bar(y ='epi', x ='score', title = 'Bar Plot of EPI and Corruption Index Scores (2010)', rot=0)
bar_plot.figure.savefig('resources/bar.png', dpi=300)

hist_plot = corr_epi.plot.hist(y ='epi', x ='score', title = 'Histogram of EPI and Corruption Index Scores (2010)',bins=20)
hist_plot.figure.savefig('resources/hist.png', dpi=300)