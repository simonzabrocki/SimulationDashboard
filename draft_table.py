import pandas as pd
import plotly.express as px
from app import data
import numpy as np


def add_reference_to_data(data):
    data['Continental_Rank'] = data.groupby(["Year", "Continent", "Variable"])["Value"].rank(method='dense', ascending=False)
    
    data['Income_Rank'] = data.groupby(["Year", "IncomeLevel", "Variable"])["Value"].rank(method='dense', ascending=False)


    Income_region_group = data.groupby(['Variable', 'Year', 'IncomeLevel', 'Region', 'Aggregation']).mean().reset_index()
    Income_region_group['ISO'] = 'AVG' + '_' + Income_region_group["IncomeLevel"] + '_' + Income_region_group["Region"]

    Income_group = data.groupby(['Variable', 'Year', 'IncomeLevel', 'Aggregation']).mean().reset_index()
    Income_group['ISO'] = 'AVG' + '_' + Income_group["IncomeLevel"]
    Income_group['Continental_Rank'] = np.nan
    Income_group['Income_Rank'] = np.nan


    Region_group = data.groupby(['Variable', 'Year', 'Continent', 'Aggregation']).mean().reset_index()
    Region_group['ISO'] = 'AVG' + '_' + Region_group["Continent"]
    Region_group['Continental_Rank'] = np.nan
    Region_group['Income_Rank'] = np.nan

    data = pd.concat([data, Income_region_group, Region_group, Income_group])
    
    return data


data = add_reference_to_data(data)




def make_continent_heatmap_df(Continent):
    '''Sacré bricolage'''
    
    df = data[(data.Continent == Continent) & (data.Aggregation.isin(['Dimension', 'Index'])) & (data.Year.isin([2005, 2019]))].fillna(0)
    df = df.round(2).astype({'Year':int})
    
    dimension_df = (df.query("Year == 2019").replace(2019, 'Dimensions 2019')
           .pivot(index=['Country', 'UNregion'], columns=['Variable', 'Year'], values='Value')
           .loc[:, (['ESRU', 'NCP', 'GEO', 'SI'], slice(None))]
           .swaplevel(0, 1, axis=1)
       )
    
    index_df = (df.pivot(index=['Country', 'UNregion'], columns=['Variable', 'Year'], values='Value')
          .loc[:, (['Index'], slice(None))]
          .droplevel(level='Variable', axis=1)
       )
    
    rank_df = (df.query("Variable == 'Index'")[['Country', 'UNregion', 'Continental_Rank', 'Year']].astype({'Continental_Rank': float})
                 .pivot(index=['Country', 'UNregion'], columns='Year', values='Continental_Rank'))
    
    index_rank_df = pd.concat([index_df, rank_df], axis=1, keys=['Index', "Rank"]).swaplevel(0, 1, axis=1)[[2005, 2019]]

    
    df = pd.concat([dimension_df, index_rank_df], axis=1).sort_values(by=[(2019, 'Rank')]).dropna(subset=[(2019, 'Rank')])
    
    return df



df = make_continent_heatmap_df('Africa').reset_index()
print(df)
print()
colnames = (df.columns.to_frame()['Year'].astype(str) + '_' + df.columns.to_frame()['Variable']).values
df.columns= colnames

print(df)

df['Performance'] = df['2005_Rank'].apply(lambda x: '↗️' if x > 10 else '↘️')
df['2005_Rank'] = df['2005_Rank'].astype(str)

import dash
import dash_table
import pandas as pd


app = dash.Dash(__name__)



app.layout = dash_table.DataTable(
    id='table',
    columns=[{"name": i, "id": i} for i in df.columns],
    data=df.to_dict('records'),
    style_data_conditional=[
        {
            'if': {
                'filter_query': '{Dimensions 2019_ESRU} > 19',
                'column_id': 'Dimensions 2019_ESRU'
            },
            'color': 'tomato',
            'fontWeight': 'bold'
        },
        {
            'if': {
                'filter_query': '{2005_Index} < 50',
                'column_id': '2005_Index'
            },
            'backgroundColor': 'tomato'
        }
    ]
)

if __name__ == '__main__':
    app.run_server(debug=True, host='localhost')
    