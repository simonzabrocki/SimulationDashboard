import plotly.express as px


def density_map(df):
    fig =   px.density_mapbox(df,
                     lat='latitude',
                     lon='longitude',
                     z='Water Withdrawal (m3)',
                     hover_data={'Name':True, 'Generation (GWh)':True, 'latitude': False, 'longitude': False, 'Fuel': True},
                     width=1200,
                     height=1000,
                     radius=35,
                     zoom=5.3,
                     opacity=None,
                     ).update_layout(margin={"r": 0, "t": 0, "l": 0, "b": 0},
                                    geo=dict(showframe=False,
                                             resolution=50,
                                             showcoastlines=False,
                                             visible=True,
                                             fitbounds="locations",
                                             showcountries=True
                                             ),
                                     legend=dict(orientation="h"),
                                     mapbox_style="carto-positron",
                                     dragmode=False,
                                     
                                     )
    return fig


def ghg_capa_ww_plot(df):
    fig = px.bar(df.groupby('Fuel')[['CO2 emissions (tonnes)','Generation (GWh)', 'Water Withdrawal (m3)']].sum().reset_index().melt(id_vars=['Fuel']),
                 x='Fuel',
                 y='value',
                 color='Fuel',
                 facet_col='variable',
                 facet_col_spacing=0.05,
                 width=1200,
                 height=500,
                 ).update_yaxes(matches=None, showticklabels=True, )

    return fig