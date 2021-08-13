from sklearn.metrics import r2_score, mean_squared_error
import plotly.express as px
import numpy as np
import pandas as pd


'''
TO IMPROVE
Make the graph more flexible in terms of hoverdata etc, function has now weird parameters
also plot_comp_base have reveresed agruments
check model should plot the one that are not checked
'''



def score_model_old(Model, X, y_true):
    '''Run a model without scenario to check that the aggregation is correct

    TO CLEAN UP: put result in dataframe

    '''

    results = Model.run(X)
    scores = []
    for var in y_true.keys():
        print(var)
        score = score_variable_old(y_true[var], results[var])
        score['Variable'] = var
        scores.append(score)

    return pd.DataFrame(scores)


def score_variable_old(baseline, computation):
    '''Scores a variable'''
    base_comp = pd.concat([baseline, computation], axis=1).replace(
        [np.inf, -np.inf], np.nan).dropna()

    base_comp.columns = ['baseline', 'computation']

    return {'r2': r2_score(base_comp.baseline, base_comp.computation),
            'correlation': base_comp.baseline.corr(base_comp.computation),
            'rmse': mean_squared_error(base_comp.baseline, base_comp.computation)}


def plot_baseline_vs_computation(baseline, computation, hover_data=[], color=None, trendline='ols'):
    '''Wrapper for plotly scatter plot'''
    df = pd.concat([baseline, computation], axis=1).dropna()
    df.columns = ['baseline', 'computation']
    fig = px.scatter(df.reset_index(), x=f'baseline', y=f'computation',
                     hover_data=hover_data, trendline=trendline, color=color)
    return fig


def plot_diagnostic(Model, X, y_true, var, hover_data=[], color=None, trendline='ols'):
    results = Model.run(X)
    return plot_baseline_vs_computation(y_true[var], results[var], hover_data=hover_data, trendline=trendline, color=color)


def data_dict_to_df(data_dict):
    
    data_dict = data_dict.copy()
    
    data = pd.concat([v.to_frame(name='Value').assign(Variable=k).reset_index() for k, v in data_dict.items()], axis=0)
        
    return data

def get_X_y_from_data(model, data_dict):
    '''TO CLEAN UP'''
    X = {key: data_dict[key] for key in model.inputs_() + model.parameters_()}
    y = {key: data_dict[key] for key in model.variables_() + model.outputs_() if key in data_dict}
    return X, y


def make_baseline_computation_df(y, y_pred):
    baseline = data_dict_to_df(y)
    computation = data_dict_to_df(y_pred)
    
    merge_on = [col for col in computation.columns if col != 'Value']
    
    baseline_computation_df = (
        baseline.merge(computation, on=merge_on, suffixes=('_baseline', '_computation'))
        .replace([np.inf, -np.inf], np.nan)
        .dropna(subset=['Value_baseline', 'Value_computation'])
    )
    
    return baseline_computation_df


def score_variable(baseline, computation):
    
    scores = {
        'r2': r2_score(baseline, computation),
        'correlation': baseline.corr(computation),
        'rmse': mean_squared_error(baseline, computation)
    }
    return pd.Series(scores)


def agg_score_by(baseline_computation_df, by=['ISO', 'Variable']):
    return (
        baseline_computation_df.groupby(by)
                               .apply(lambda x: score_variable(x['Value_baseline'], x['Value_computation']))
    )


def score_model(model, data_dict):
    X, y = get_X_y_from_data(model, data_dict)
    result = model.run(X)
    y_pred = {k: v for k, v in result.items() if k in y}

    baseline_computation_df = make_baseline_computation_df(y, y_pred)
    
    return {
        'score_by_Variable': agg_score_by(baseline_computation_df, by='Variable'),
        'score_by_ISO': agg_score_by(baseline_computation_df, by='ISO'),
        'score_by_ISO_Variable': agg_score_by(baseline_computation_df, by=['ISO', 'Variable'])
    }


def score_model_dictionnary(model_dictionnary, data_dict):
    scores = {}
    for model_name, model in model_dictionnary.items():
    
        print(model_name, end=': ')
        try:
            scores[model_name] = score_model(model, data_dict)
            print('Done')
        except Exception as e:
            print('Error:', e)
    
    return scores
