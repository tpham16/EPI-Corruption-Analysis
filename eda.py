from sqlalchemy import create_engine, func
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
import pandas as pd

# pull EPI data from postgres database using SQLalchemy
engine = create_engine('postgresql+psycopg2://postgres:password@localhost:5432/epi')
Base = automap_base()
Base.prepare(engine, reflect=True)

# save classes as variable, prepare classes
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

# save it back into postgres database
corr_df.to_sql('corruption_epi', engine, if_exists='replace', index = False)

corr_epi = epi_df.merge(corr_df, how="left", on="country")

corr_epi.head()

# generate scatter plot, bar graphs, histograms comparing Corruption Scores and EPI
corr_epi.plot.scatter(y ='epi', x ='score', title = 'Scatter Plot of Environmental Performance Index (EPI) Scores and Corruption')

corr_epi.plot.bar(y ='epi', x ='score', title = 'Bar Plot of Environmental Performance Index (EPI) Scores and Corruption', rot=0)

corr_epi.plot.hist(y ='epi', x ='score', title = 'Histogram of Environmental Performance Index (EPI) Scores and Corruption')
