import dash
import pandas as pd
from utils import format_data

app = dash.Dash(
    __name__, meta_tags=[{"name": "viewport", "content": "width=device-width"}],
    suppress_callback_exceptions=True
)
app.title = 'GreenGrowthIndex'

server = app.server


#####
# TO PUT SOMEWHERE ESLE
data = pd.read_csv('data/GGIs_2005_2020.csv')
data = data[data.Year < 2020]
data = data.replace('America', 'Americas')
# #### REQUEST TO REMOVE LATER !!!!!!!
# ISOs = ['TKM', 'KAZ', 'KGZ', 'TJK', 'UZB']
# custom_country = data[data.ISO.isin(ISOs)].groupby(['Aggregation', 'Year', 'Variable', 'Continent', 'UNregion', 'Region']).mean().reset_index()
# custom_country['ISO'] = 'TKM + KAZ + KGZ + TJK + UZB'
# custom_country['IncomeLevel'] = 'Lower middle income'
# custom_country['Country'] = 'Kazakhstan, Kyrgyz Republic, Tajikistan, Turkmenistan, Uzbekistan'
# data = pd.concat([custom_country, data])
# ##########


ISO_options = data[['ISO', 'Country']].drop_duplicates().values
data = format_data(data)

indicator_data = pd.read_csv('data/indicators/data.csv')
indicator_data['Source'] = indicator_data['Source'].apply(lambda x: x[0:50] + ' [...]')  # to be changed lol !


indicator_properties = pd.read_csv('data/indicators/indicator_properties.csv', index_col=0)

dimension_properties = pd.read_csv('data/indicators/dimension_properties.csv', index_col=0)
