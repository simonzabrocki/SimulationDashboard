import pandas as pd
from GM.demo_script import run_EW_scenario
from GM.demo_script_Hermen import format_data_dict_sankey, plot_sanky_GE3
import GM.demo_script_Hermen
import plotly.express as px


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


def run_all_scenarios_water(data_dict, ISO, args_dict_1, args_dict_2):
    scenarios_results = {}

    data_dict = {key: value.loc[[ISO]] for key, value in data_dict.items()}

    scenarios_results['BAU'] = run_EW_scenario(data_dict)
    scenarios_results['scenario_one'] = run_EW_scenario(data_dict_expanded=data_dict, **args_dict_1)
    scenarios_results['scenario_two'] = run_EW_scenario(data_dict_expanded=data_dict, **args_dict_2)

    df_1 = format_var_results(scenarios_results, 'EW1')
    df_2 = format_var_results(scenarios_results, 'EW2')
    df_3 = format_var_results(scenarios_results, 'GDPC')

    fig_1 = scenario_line_plot('EW1', df_1, ISO)
    fig_2 = scenario_line_plot('EW2', df_2, ISO)
    fig_3 = scenario_line_plot('GDPC', df_3, ISO)

    return fig_1, fig_2, fig_3


def run_all_scenarios_BE2(data_dict, ISO, args_dict_1, args_dict_2):
    
    scenarios_results = {}

    data_dict = {k: v.loc[ISO, 2018:] for k, v in data_dict.items() if k not in ['CL_corr_coef']}          
    data_dict = GM.demo_script_Hermen.run_BE2_projection(data_dict)
    
    data_dict['CL_corr_coef'] = 1.4
    data_dict['R_rate'].loc[:, 2018] = 0

    scenarios_results['BAU'] = GM.demo_script_Hermen.run_BE2_scenario(data_dict=data_dict)
    scenarios_results['scenario_one'] = GM.demo_script_Hermen.run_BE2_scenario(data_dict=data_dict, **args_dict_1)
    scenarios_results['scenario_two'] = GM.demo_script_Hermen.run_BE2_scenario(data_dict=data_dict, **args_dict_2)

    df_1 = format_var_results(scenarios_results, 'BE2')
    df_2 = format_var_results(scenarios_results, 'delta_CL')

    fig_1 = scenario_line_plot('BE2', df_1, ISO)
    fig_2 = scenario_line_plot('delta_CL', df_2, ISO)
    fig_3 = {}

    return fig_1, fig_2, fig_3


def run_all_scenarios_GE3(data_dict, ISO, args_dict_1, args_dict_2):
    scenarios_results = {}
    data_dict = {k: v.loc[ISO, 2018, :] for k, v in data_dict.items()}

    scenarios_results['BAU'] = GM.demo_script_Hermen.run_GE3_scenario(data_dict=data_dict, MM_Ti=data_dict['MM_Ti'],MM_ASi=data_dict['MM_ASi'])
    scenarios_results['scenario_one'] = GM.demo_script_Hermen.run_GE3_scenario(data_dict=data_dict, **args_dict_1)
    scenarios_results['scenario_two'] = GM.demo_script_Hermen.run_GE3_scenario(data_dict=data_dict, **args_dict_2)

    d_1, c_1 = format_data_dict_sankey({k: v for k, v in scenarios_results['scenario_one'].items() if k in ['TEE_CO2eq', 'TMA_CO2eq', 'TMT_CO2eq', 'TMP_CO2eq']})
    d_2, c_2 = format_data_dict_sankey({k: v for k, v in scenarios_results['scenario_two'].items() if k in ['TEE_CO2eq', 'TMA_CO2eq', 'TMT_CO2eq', 'TMP_CO2eq']})
    d_3, c_3 = format_data_dict_sankey({k: v for k, v in scenarios_results['BAU'].items() if k in ['TEE_CO2eq', 'TMA_CO2eq', 'TMT_CO2eq', 'TMP_CO2eq']})
   
    fig_1 = plot_sanky_GE3(d_1, c_1).update_layout(title='Scenario 1')
    fig_2 = plot_sanky_GE3(d_2, c_2).update_layout(title='Scenario 2')
    fig_3 = plot_sanky_GE3(d_3, c_3).update_layout(title='Business as Usual')

    return fig_1, fig_2, fig_3

