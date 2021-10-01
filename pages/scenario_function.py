import pandas as pd
import plotly.express as px
from plots.simulation.GE3_plots import sankeyplot, emission_data_dict_to_df
from plots.simulation.ELEC_plots import density_map, ghg_capa_ww_plot
from plots.simulation.base_plots import scenario_line_plot

from ggmodel_dev.models.landuse import BE2_scenario, GE3_scenario
from ggmodel_dev.models.water import EW_scenario
from ggmodel_dev.models.transport import VEHC_scenario
from ggmodel_dev.models.energy import ELEC_scenario
from ggmodel_dev.models.material import RECYCLE_scenario


def format_var_results(scenarios_results, var):
    df = pd.concat([
        scenarios_results['scenario_one'][var].reset_index().assign(
            scenario='Scenario 1'),
        scenarios_results['scenario_two'][var].reset_index().assign(
            scenario='Scenario 2'),
        scenarios_results['BAU'][var].reset_index().assign(scenario='BAU'),
    ], axis=0).rename(columns={0: var})
    return df


# WATER

def run_all_scenarios_EW(data_dict, ISO, args_dict_1, args_dict_2):

    data_dict = {key: value.loc[[ISO]] for key, value in data_dict.items()}

    scenarios_results = EW_scenario.run_all_scenarios(data_dict, args_dict_1, args_dict_2)

    df_1 = format_var_results(scenarios_results, 'EW1')
    df_2 = format_var_results(scenarios_results, 'EW2')
    df_3 = format_var_results(scenarios_results, 'GDPC')

    summary_df = EW_scenario.MODEL.summary_df

    fig_1 = scenario_line_plot('EW1', df_1, ISO, summary_df)
    fig_2 = scenario_line_plot('EW2', df_2, ISO, summary_df)
    fig_3 = scenario_line_plot('GDPC', df_3, ISO, summary_df)

    return fig_1, fig_2, fig_3, scenarios_results, EW_scenario

# BE2

def run_all_scenarios_BE2(data_dict, ISO, args_dict_1, args_dict_2):
    
    data_dict = {k: v.loc[ISO, 2018:] for k, v in data_dict.items()}


    scenarios_results = BE2_scenario.run_all_scenarios(data_dict, args_dict_1, args_dict_2)

    df_1 = format_var_results(scenarios_results, 'BE2')
    df_2 = format_var_results(scenarios_results, 'delta_CL')

    summary_df = BE2_scenario.MODEL.summary_df

    fig_1 = scenario_line_plot('BE2', df_1, ISO, summary_df)
    fig_2 = scenario_line_plot('delta_CL', df_2, ISO, summary_df)
    fig_3 = {}

    return fig_1, fig_2, fig_3, scenarios_results, BE2_scenario

# GE3

def run_all_scenarios_GE3(data_dict, ISO, args_dict_1, args_dict_2):
    data_dict = {k: v.loc[ISO, 2018, :] for k, v in data_dict.items()}

    scenarios_results = GE3_scenario.run_all_scenarios(data_dict, args_dict_1, args_dict_2)

    displayed_variables = ['TEE_CO2eq', 'TMA_CO2eq', 'TMT_CO2eq', 'TMP_CO2eq']


    summary_df = GE3_scenario.MODEL.summary_df

    df_0 = emission_data_dict_to_df(
        {k: v for k, v in scenarios_results['BAU'].items() if k in displayed_variables})
    df_1 = emission_data_dict_to_df(
        {k: v for k, v in scenarios_results['scenario_one'].items() if k in displayed_variables})
    df_2 = emission_data_dict_to_df(
        {k: v for k, v in scenarios_results['scenario_two'].items() if k in displayed_variables})

    df = pd.concat([df_0.assign(scenario='BAU'), df_1.assign(
        scenario='scenario 1'), df_2.assign(scenario='scenario 2')], axis=0)

    df = df.merge(summary_df[['name', 'unit']], left_on='Variable', right_index=True, how='left')

    fig_1 = px.treemap(df.query('Variable != "GE3_partial"'), path=['scenario', 'Item', 'name'], values='Value',  color='scenario', color_discrete_map={
                       'BAU': 'grey', 'scenario 1': '#D8A488', 'scenario 2': '#86BBD8'}, height=600).update_layout(title="Agriculture non CO2 emissions Tree Map")

    df.loc[df.Variable == 'GE3_partial', 'unit'] = 'gigagrams (CO2eq)'
    df.loc[df.Variable == 'GE3_partial',
           'name'] = 'Non-CO2 agricultural emissions'

    df = df.merge(summary_df[['name']], left_on='Item', right_index=True, how='left', suffixes=('_target', '_source'))
    df['name'] = df['name_target']
    df.loc[df.name_source.isna(), 'name'] = df.loc[df.name_source.isna(), 'Item']

    df.loc[df.name_source.isna(), 'name_source'] = df.loc[df.name_source.isna(), 'Item']

    df.loc[df.name_target.isna(
    ), 'name_target'] = df.loc[df.name_target.isna(), 'Variable']

    fig_2 = sankeyplot(df, 'name_source', 'name_target').update_layout(
        title="Agriculture non CO2 emissions sankey diagram").update_layout(height=600)
    return fig_1, fig_2, {}, scenarios_results, GE3_scenario


# VEHC

def run_all_scenarios_VEHC(data_dict, ISO, args_dict_1, args_dict_2):

    scenarios_results = {}
    data_dict = {k: v.loc[[ISO]] for k, v in data_dict.items()}
    scenarios_results = VEHC_scenario.run_all_scenarios(data_dict, args_dict_1, args_dict_2)

    df_1 = format_var_results(scenarios_results, 'VEHC')
    df_2 = format_var_results(scenarios_results, 'GDPC')

    # to standardize and automize
    summary_df = VEHC_scenario.MODEL.summary_df
    fig_1 = scenario_line_plot('VEHC', df_1, ISO, summary_df)
    fig_2 = scenario_line_plot('GDPC', df_2, ISO, summary_df)
    fig_3 = {}

    return fig_1, fig_2, fig_3, scenarios_results, VEHC_scenario


# ELEC

def format_ELEC_results(results):
    df = pd.concat([s.to_frame(name=n) for n, s in results.items() if n in ['ELECPRODi', 'ELECWWi', 'ELECGHGi']], axis=1)
    return (
        df.reset_index()
          .dropna()
          .rename(columns={'ELECWWi': 'Water Withdrawal (m3)', 'ELECGHGi': 'CO2 emissions (tonnes)', 'ELECPRODi': 'Generation (GWh)'})
    )

def run_all_scenarios_ELEC(data_dict, ISO, args_dict_1, args_dict_2):

    data_dict = {k: (v.loc[[ISO]] if 'ISO' in v.index.names else v) for k, v in data_dict.items()}
    
    scenarios_results = ELEC_scenario.run_all_scenarios(data_dict, args_dict_1, args_dict_2)
    results = scenarios_results['BAU']

    results_df = format_ELEC_results(results)
    
    fig_1 = density_map(results_df)
    fig_2 = ghg_capa_ww_plot(results_df)

    return fig_1, fig_2, {}, scenarios_results, ELEC_scenario

# RECYCLE

def format_RECYCLE_result(results):
    df = pd.concat([s.to_frame(name=n) for n, s in results.items() if n in ['MSi', 'RMSi', 'INFLOWi','OUTFLOWi', 'SBMi', 'WASTEi']], axis=1)
    return df

def format_RECYLE(scenarios_results):
    dfs = []
    for scenario, results in scenarios_results.items():
        dfs.append(format_RECYCLE_result(results).assign(scenario=scenario))

    return pd.concat(dfs, axis=0)

def run_all_scenarios_RECYCLE(data_dict, ISO, args_dict_1, args_dict_2):


    data_dict = {k: (v.loc[[ISO]] if 'ISO' in v.index.names else v) for k, v in data_dict.items()}

    scenarios_results = RECYCLE_scenario.run_all_scenarios(data_dict, args_dict_1, args_dict_2)

    df = format_RECYLE(scenarios_results).reset_index().query("Item not in ['Biomass', 'Fossil fuels']").melt(id_vars=['ISO', 'Item', 'Year', 'scenario']).replace({'scenario_one': 'Scenario 1','scenario_two': 'Scenario 2'})

    fig_1 = px.line(df.query("variable in ['INFLOWi', 'OUTFLOWi']"),
            x='Year',
            y='value',
            facet_col='Item',
            facet_row='variable',
            color='scenario',
            color_discrete_map={'Scenario 1': '#D8A488',
                                      'Scenario 2': '#86BBD8',
                                      'BAU': '#A9A9A9'},  
             height=800,
       width=1200).update_yaxes(matches=None, showticklabels=True)

    fig_2 = px.line(df.query("variable in ['RMSi', 'WASTEi']"),
        x='Year',
        y='value',
        facet_col='Item',
        facet_row='variable',
        color='scenario',
        color_discrete_map={'Scenario 1': '#D8A488',
                            'Scenario 2': '#86BBD8',
                            'BAU': '#A9A9A9'},        
        height=800,
       width=1200).update_yaxes(matches=None, showticklabels=True)

    return fig_1, fig_2, {}, scenarios_results, RECYCLE_scenario