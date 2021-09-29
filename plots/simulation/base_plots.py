import plotly.express as px

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
