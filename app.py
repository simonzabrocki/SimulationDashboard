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



def add_reference_to_data(data):
    '''To improve'''

    data['Continental_Rank'] = data.groupby(["Year", "Continent", "Variable"])[
        "Value"].rank(method='dense', ascending=False)

    data['Income_Rank'] = data.groupby(["Year", "IncomeLevel", "Variable"])[
        "Value"].rank(method='dense', ascending=False)

    Income_region_group = data.groupby(
        ['Variable', 'Year', 'IncomeLevel', 'Region', 'Aggregation']).mean().reset_index()
    Income_region_group['ISO'] = 'AVG' + '_' + \
        Income_region_group["IncomeLevel"] + \
        '_' + Income_region_group["Region"]
    

    Income_group = data.groupby(['Variable', 'Year', 'IncomeLevel',
                                 'Aggregation']).mean().reset_index()
    Income_group['ISO'] = 'AVG' + '_' + Income_group["IncomeLevel"]

    Income_group['Continental_Rank'] = np.nan
    Income_group['Income_Rank'] = np.nan

    Region_group = data.groupby(['Variable', 'Year', 'Continent',
                                 'Aggregation']).mean().reset_index()
    Region_group['ISO'] = 'AVG' + '_' + Region_group["Continent"]
    Region_group['Continental_Rank'] = np.nan
    Region_group['Income_Rank'] = np.nan

    data = pd.concat([data, Income_region_group, Region_group, Income_group])

    indicator_property = pd.read_csv(
        'data/indicators/indicator_properties.csv', index_col=0)
    indicator_property['Category'] = indicator_property['Indicator'].apply(
        lambda x: x[0:2])
    data = pd.merge(data, indicator_property[['Category', 'Dimension']].drop_duplicates(
    ), left_on='Variable', right_on='Category', how='left')

    return data

# to improve using double the amount of mem for nothing
data_bis = add_reference_to_data(data)
