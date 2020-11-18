import dash
import pandas as pd
import numpy as np
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
ISO_options = data[['ISO', 'Country']].drop_duplicates().values
data = format_data(data)

indicator_data = pd.read_csv('data/indicators/data.csv', index_col=0)
indicator_data['From'] = indicator_data['From'] + ' ' + indicator_data['Imputed From'].fillna('') + ' ' + indicator_data['Imputed from Year'].fillna('').astype(str)
indicator_data['Source'] = indicator_data['Source'].apply(lambda x: x[0:50] + ' [...]')  # to be changed lol !


indicator_properties = pd.read_csv('data/indicators/indicator_properties.csv', index_col=0)

dimension_properties = pd.read_csv('data/indicators/dimension_properties.csv', index_col=0)


# data['Continental_Rank'] = data.groupby(["Year", "Continent", "Variable"])["Value"].rank(method='dense', ascending=False)
# data['Income_Rank'] = data.groupby(["Year", "IncomeLevel", "Variable"])["Value"].rank(method='dense', ascending=False)
#
#
# Income_region_group = data.groupby(['Variable', 'Year', 'IncomeLevel', 'Region', 'Aggregation']).mean().reset_index()
# Income_region_group['ISO'] = 'AVG' + '_' + Income_region_group["IncomeLevel"] + '_' + Income_region_group["Region"]
#
# Income_group = data.groupby(['Variable', 'Year', 'IncomeLevel', 'Aggregation']).mean().reset_index()
# Income_group['ISO'] = 'AVG' + '_' + Income_group["IncomeLevel"]
# Income_group['Continental_Rank'] = np.nan
# Income_group['Income_Rank'] = np.nan
#
#
# Region_group = data.groupby(['Variable', 'Year', 'Continent', 'Aggregation']).mean().reset_index()
# Region_group['ISO'] = 'AVG' + '_' + Region_group["Continent"]
# Region_group['Continental_Rank'] = np.nan
# Region_group['Income_Rank'] = np.nan
#
# data = pd.concat([data, Income_region_group, Region_group, Income_group])
