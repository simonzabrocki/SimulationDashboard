import dash
import pandas as pd
from utils import format_data
import numpy as np

app = dash.Dash(
    __name__, meta_tags=[{"name": "viewport", "content": "width=device-width"}],
    suppress_callback_exceptions=True,
    
)
app.title = 'GreenGrowthIndex'

server = app.server


#####
# TO PUT SOMEWHERE ESLE
data = pd.read_csv('data/GGIs_2005_2020.csv')
data = data[data.Year < 2020]
data = data.replace('America', 'Americas')

ISO_options = data[['ISO', 'Country']].drop_duplicates().values
data = format_data(data)


indicator_data = pd.read_csv('data/indicators/data.csv')

indicator_properties = pd.read_csv('data/indicators/indicator_properties.csv',index_col=0)

dimension_properties = pd.read_csv('data/indicators/dimension_properties.csv', index_col=0)



def add_rank_to_data(data):
    '''To improve'''

    data['Continental_Rank'] = data.groupby(["Year", "Continent", "Variable"])[
        "Value"].rank(method='dense', ascending=False)

    data['Income_Rank'] = data.groupby(["Year", "IncomeLevel", "Variable"])[
        "Value"].rank(method='dense', ascending=False)

    return data

data = add_rank_to_data(data)

indicator_properties = pd.read_csv('data/indicators/indicator_properties.csv', index_col=0)
indicator_properties['Category'] = indicator_properties['Indicator'].apply(lambda x: x[0:2])
data = pd.merge(data, indicator_properties[['Category', 'Dimension']].drop_duplicates(), left_on='Variable', right_on='Category', how='left')
