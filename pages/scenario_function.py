import pandas as pd
import os
import plotly.express as px

from plots.simulation.GE3_plots import sankeyplot, emission_data_dict_to_df
from ggmodel_dev.models.landuse import BE2_scenario, GE3_scenario
from ggmodel_dev.models.water import EW_scenario
from ggmodel_dev.models.transport import VEHC_scenario
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


def scenario_line_plot(var, df, ISO):  # ugly af
    fig = px.line(df.query(f"ISO == '{ISO}' and Year >= 2000"),
                  x='Year',
                  y=var,
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
    scenarios_results = {}

    data_dict = {key: value.loc[[ISO]] for key, value in data_dict.items()}

    data_dict = run_projection(EW_scenario.projection_dict, data_dict)

    scenarios_results['BAU'] = EW_scenario.run_scenario(data_dict)
    scenarios_results['scenario_one'] = EW_scenario.run_scenario(
        data_dict, **args_dict_1)
    scenarios_results['scenario_two'] = EW_scenario.run_scenario(
        data_dict, **args_dict_2)

    df_1 = format_var_results(scenarios_results, 'EW1')
    df_2 = format_var_results(scenarios_results, 'EW2')
    df_3 = format_var_results(scenarios_results, 'GDPC')

    fig_1 = scenario_line_plot('EW1', df_1, ISO)
    fig_2 = scenario_line_plot('EW2', df_2, ISO)
    fig_3 = scenario_line_plot('GDPC', df_3, ISO)

    return fig_1, fig_2, fig_3


def run_all_scenarios_BE2(data_dict, ISO, args_dict_1, args_dict_2):

    scenarios_results = {}

    data_dict = {k: v.loc[ISO, 2018:] for k, v in data_dict.items()}

    data_dict = run_projection(BE2_scenario.projection_dict, data_dict)

    scenarios_results['BAU'] = BE2_scenario.run_scenario(data_dict=data_dict)
    scenarios_results['scenario_one'] = BE2_scenario.run_scenario(
        data_dict=data_dict, **args_dict_1)
    scenarios_results['scenario_two'] = BE2_scenario.run_scenario(
        data_dict=data_dict, **args_dict_2)

    df_1 = format_var_results(scenarios_results, 'BE2')
    df_2 = format_var_results(scenarios_results, 'delta_CL')

    fig_1 = scenario_line_plot('BE2', df_1, ISO)
    fig_2 = scenario_line_plot('delta_CL', df_2, ISO)
    fig_3 = {}

    return fig_1, fig_2, fig_3


def run_all_scenarios_GE3(data_dict, ISO, args_dict_1, args_dict_2):
    scenarios_results = {}
    data_dict = {k: v.loc[ISO, 2018, :] for k, v in data_dict.items()}

    scenarios_results['BAU'] = GE3_scenario.run_scenario(
        data_dict=data_dict, MM_Ti=data_dict['MM_Ti'], MM_ASi=data_dict['MM_ASi'])
    scenarios_results['scenario_one'] = GE3_scenario.run_scenario(
        data_dict=data_dict, **args_dict_1)
    scenarios_results['scenario_two'] = GE3_scenario.run_scenario(
        data_dict=data_dict, **args_dict_2)

    df_0 = emission_data_dict_to_df({k: v for k, v in scenarios_results['scenario_one'].items() if k in ['TEE_CO2eq', 'TMA_CO2eq', 'TMT_CO2eq', 'TMP_CO2eq']})
    df_1 = emission_data_dict_to_df({k: v for k, v in scenarios_results['scenario_two'].items() if k in ['TEE_CO2eq', 'TMA_CO2eq', 'TMT_CO2eq', 'TMP_CO2eq']})

    fig_1 = sankeyplot(df_0, 'Item', 'Variable').update_layout(title='Scenario 1')
    fig_2 = sankeyplot(df_1, 'Item', 'Variable').update_layout(title='Scenario 2')

    return fig_1, fig_2, {}


def run_all_scenarios_VEHC(data_dict, ISO, args_dict_1, args_dict_2):

    scenarios_results = {}
    data_dict = {k: v.loc[[ISO]] for k, v in data_dict.items()}

    scenarios_results['BAU'] = VEHC_scenario.run_scenario(
        data_dict, MAX_sat=data_dict['MAX_sat'], GDPC_rate=1.02)
    scenarios_results['scenario_one'] = VEHC_scenario.run_scenario(
        data_dict, **args_dict_1)
    scenarios_results['scenario_two'] = VEHC_scenario.run_scenario(
        data_dict, **args_dict_2)


    df_1 = format_var_results(scenarios_results, 'VEHC')
    df_2 = format_var_results(scenarios_results, 'GDPC')

    fig_1 = scenario_line_plot('VEHC', df_1, ISO)
    fig_2 = scenario_line_plot('GDPC', df_2, ISO)
    fig_3 = {}

    return fig_1, fig_2, fig_3
