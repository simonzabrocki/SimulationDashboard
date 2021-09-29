import pandas as pd
import os
import plotly.express as px

from plots.simulation.GE3_plots import sankeyplot, emission_data_dict_to_df
from ggmodel_dev.models.landuse import BE2_scenario, GE3_scenario, GE3, BE2
from ggmodel_dev.models.water import EW_scenario, EW
from ggmodel_dev.models.transport import VEHC_scenario, VEHC
from ggmodel_dev.models.energy import ELEC, ELEC_scenario
from ggmodel_dev.models.material import RECYCLE, RECYCLE_scenario
from ggmodel_dev.projection import run_projection


def format_var_results(scenarios_results, var):
    df = pd.concat([
        scenarios_results['scenario_one'][var].reset_index().assign(
            scenario='Scenario 1'),
        scenarios_results['scenario_two'][var].reset_index().assign(
            scenario='Scenario 2'),
        scenarios_results['BAU'][var].reset_index().assign(scenario='BAU'),
    ], axis=0).rename(columns={0: var})
    return df


def scenario_line_plot(var, df, ISO, summary_df):  # ugly af

    var_info = summary_df.loc[var]
    var_name = var_info['name']
    df = df.rename(columns={var: var_name})
    fig = px.line(df.query(f"ISO == '{ISO}' and Year >= 2000"),
                  x='Year',
                  y=var_name,
                  color='scenario',
                  color_discrete_map={'Scenario 1': '#D8A488',
                                      'Scenario 2': '#86BBD8',
                                      'BAU': '#A9A9A9'},
                  )

    fig.add_vline(x=2019, line_width=3, line_dash="dash", line_color="green")
    fig.update_layout(hovermode="x")
    fig.update_layout(legend_title_text='Scenario')
    return fig


def get_data_dict_from_folder(folder_name):
    files = os.listdir(folder_name)
    data_dict = {file.split('.')[0]: pd.read_csv(
        f'{folder_name}/{file}') for file in files}

    data_dict = {name: df.set_index([col for col in df.columns if col != name]).squeeze(
    ) for name, df in data_dict.items()}

    return data_dict


def get_data_dict_from_folder_parquet(folder_name):
    files = os.listdir(folder_name)
    data_dict = {file.split('.')[0]: pd.read_parquet(
        f'{folder_name}/{file}') for file in files}
    data_dict = {name: df[name] for name, df in data_dict.items()}
    return data_dict


def run_all_scenarios_water(data_dict, ISO, args_dict_1, args_dict_2):

    data_dict = {key: value.loc[[ISO]] for key, value in data_dict.items()}

    scenarios_results = EW_scenario.run_all_scenarios(data_dict, args_dict_1, args_dict_2)

    df_1 = format_var_results(scenarios_results, 'EW1')
    df_2 = format_var_results(scenarios_results, 'EW2')
    df_3 = format_var_results(scenarios_results, 'GDPC')

    summary_df = EW.model_dictionnary['EW_model'].summary_df

    fig_1 = scenario_line_plot('EW1', df_1, ISO, summary_df)
    fig_2 = scenario_line_plot('EW2', df_2, ISO, summary_df)
    fig_3 = scenario_line_plot('GDPC', df_3, ISO, summary_df)

    return fig_1, fig_2, fig_3, scenarios_results


def run_all_scenarios_BE2(data_dict, ISO, args_dict_1, args_dict_2):
    
    data_dict = {k: v.loc[ISO, 2018:] for k, v in data_dict.items()}


    scenarios_results = BE2_scenario.run_all_scenarios(data_dict, args_dict_1, args_dict_2)

    df_1 = format_var_results(scenarios_results, 'BE2')
    df_2 = format_var_results(scenarios_results, 'delta_CL')

    summary_df = BE2.model_dictionnary['BE2_model'].summary_df

    fig_1 = scenario_line_plot('BE2', df_1, ISO, summary_df)
    fig_2 = scenario_line_plot('delta_CL', df_2, ISO, summary_df)
    fig_3 = {}

    return fig_1, fig_2, fig_3, scenarios_results


def run_all_scenarios_GE3(data_dict, ISO, args_dict_1, args_dict_2):
    data_dict = {k: v.loc[ISO, 2018, :] for k, v in data_dict.items()}

    scenarios_results = GE3_scenario.run_all_scenarios(data_dict, args_dict_1, args_dict_2)

    displayed_variables = ['TEE_CO2eq', 'TMA_CO2eq', 'TMT_CO2eq', 'TMP_CO2eq']

    df_0 = emission_data_dict_to_df(
        {k: v for k, v in scenarios_results['BAU'].items() if k in displayed_variables})
    df_1 = emission_data_dict_to_df(
        {k: v for k, v in scenarios_results['scenario_one'].items() if k in displayed_variables})
    df_2 = emission_data_dict_to_df(
        {k: v for k, v in scenarios_results['scenario_two'].items() if k in displayed_variables})

    df = pd.concat([df_0.assign(scenario='BAU'), df_1.assign(
        scenario='scenario 1'), df_2.assign(scenario='scenario 2')], axis=0)

    df = df.merge(GE3.model_dictionnary['GE3_model'].summary_df[[
                  'name', 'unit']], left_on='Variable', right_index=True, how='left')

    fig_1 = px.treemap(df.query('Variable != "GE3_partial"'), path=['scenario', 'Item', 'name'], values='Value',  color='scenario', color_discrete_map={
                       'BAU': 'grey', 'scenario 1': '#D8A488', 'scenario 2': '#86BBD8'}, height=600).update_layout(title="Agriculture non CO2 emissions Tree Map")

    df.loc[df.Variable == 'GE3_partial', 'unit'] = 'gigagrams (CO2eq)'
    df.loc[df.Variable == 'GE3_partial',
           'name'] = 'Non-CO2 agricultural emissions'

    df = df.merge(GE3.model_dictionnary['GE3_model'].summary_df[[
                  'name']], left_on='Item', right_index=True, how='left', suffixes=('_target', '_source'))
    df['name'] = df['name_target']
    df.loc[df.name_source.isna(), 'name'] = df.loc[df.name_source.isna(), 'Item']

    df.loc[df.name_source.isna(), 'name_source'] = df.loc[df.name_source.isna(), 'Item']

    df.loc[df.name_target.isna(
    ), 'name_target'] = df.loc[df.name_target.isna(), 'Variable']

    fig_2 = sankeyplot(df, 'name_source', 'name_target').update_layout(
        title="Agriculture non CO2 emissions sankey diagram").update_layout(height=600)
    return fig_1, fig_2, {}, scenarios_results


def run_all_scenarios_VEHC(data_dict, ISO, args_dict_1, args_dict_2):

    scenarios_results = {}
    data_dict = {k: v.loc[[ISO]] for k, v in data_dict.items()}

    scenarios_results['BAU'] = VEHC_scenario.run_scenario(
        data_dict, MAX_sat=data_dict['MAX_sat'], GDPC_rate=1.02)
    scenarios_results['scenario_one'] = VEHC_scenario.run_scenario(
        data_dict, **args_dict_1)
    scenarios_results['scenario_two'] = VEHC_scenario.run_scenario(
        data_dict, **args_dict_2)
    
    #results_to_excel(scenarios_results, VEHC.model_dictionnary['VEHC_model'], 'outputs/simulation_results.xlsx')


    df_1 = format_var_results(scenarios_results, 'VEHC')
    df_2 = format_var_results(scenarios_results, 'GDPC')

    # to standardize and automize
    summary_df = VEHC.model_dictionnary['VEHC_model'].summary_df
    fig_1 = scenario_line_plot('VEHC', df_1, ISO, summary_df)
    fig_2 = scenario_line_plot('GDPC', df_2, ISO, summary_df)
    fig_3 = {}

    return fig_1, fig_2, fig_3, scenarios_results



# ELEC TO CLEAN UP

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


def format_ELEC_results(results):
    df = pd.concat([s.to_frame(name=n) for n, s in results.items() if n in ['ELECPRODi', 'ELECWWi', 'ELECGHGi']], axis=1)
    return (
        df.reset_index()
          .dropna()
          .rename(columns={'ELECWWi': 'Water Withdrawal (m3)', 'ELECGHGi': 'CO2 emissions (tonnes)', 'ELECPRODi': 'Generation (GWh)'})
    )

def run_all_scenarios_ELEC(data_dict, ISO, args_dict_1, args_dict_2):
    scenarios_results = {}

    data_dict = {k: (v.loc[[ISO]] if 'ISO' in v.index.names else v) for k, v in data_dict.items()}
    
    
    results = ELEC_scenario.run_scenario(data_dict, **args_dict_1, **args_dict_2)
    scenarios_results['BAU'] = results
    #results_to_excel(scenarios_results, ELEC.model_dictionnary['ELEC_model'], 'outputs/simulation_results.xlsx')

    results_df = format_ELEC_results(results)
    
    fig_1 = density_map(results_df)
    fig_2 = ghg_capa_ww_plot(results_df)

    return fig_1, fig_2, {}, scenarios_results



def format_RECYCLE_result(results):
    df = pd.concat([s.to_frame(name=n) for n, s in results.items() if n in ['MSi', 'RMSi', 'INFLOWi', 'SBMi', 'WASTEi']], axis=1)
    return df

def format_RECYLE(scenarios_results):
    dfs = []
    for scenario, results in scenarios_results.items():
        dfs.append(format_RECYCLE_result(results).assign(scenario=scenario))

    return pd.concat(dfs, axis=0)

def run_all_scenarios_RECYCLE(data_dict, ISO, args_dict_1, args_dict_2):

    scenarios_results = {}

    data_dict = {k: (v.loc[[ISO]] if 'ISO' in v.index.names else v) for k, v in data_dict.items()}

    # TO BE PUT IN DB !!!!!
    LDi_mu = pd.Series(index=['Biomass', 'Fossil fuels', 'Metal ores', 'Non-metallic minerals'], data=[0, 0, 40, 8.5])
    LDi_std = pd.Series(index=['Biomass', 'Fossil fuels', 'Metal ores', 'Non-metallic minerals'], data=[1e-10, 1e-10, 16, 80])
    data_dict['LDi_mu'] = LDi_mu
    data_dict['LDi_std'] = LDi_std

    # TO BE PUT IN SCENARIO
    data_dict['PLOSSi'] = 1
    data_dict['MLOSSi'] = 1   


    scenarios_results['BAU'] = RECYCLE_scenario.run_scenario(data_dict, RRi=0.1)
    scenarios_results['scenario_one'] = RECYCLE_scenario.run_scenario(data_dict, **args_dict_1)
    scenarios_results['scenario_two'] = RECYCLE_scenario.run_scenario(data_dict, **args_dict_2)

    #results_to_excel(scenarios_results, RECYCLE.model_dictionnary['RECYCLE_model'], 'outputs/simulation_results.xlsx')

    df = format_RECYLE(scenarios_results).reset_index().query("Item not in ['Biomass', 'Fossil fuels']").melt(id_vars=['ISO', 'Item', 'Year', 'scenario'])

    fig_1 = px.line(df.query("variable in ['INFLOWi', 'MSi']"),
            x='Year',
            y='value',
            facet_col='Item',
            facet_row='variable',
            color='scenario',
             height=800,
       width=1200).update_yaxes(matches=None, showticklabels=True)

    fig_2 = px.line(df.query("variable in ['RMSi', 'WASTEi']"),
        x='Year',
        y='value',
        facet_col='Item',
        facet_row='variable',
        color='scenario',
         height=800,
       width=1200).update_yaxes(matches=None, showticklabels=True)
    return fig_1, fig_2, {}, scenarios_results