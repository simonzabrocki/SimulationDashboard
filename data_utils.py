import pandas as pd


def add_rank_to_data(data):
    '''To improve'''

    data['Continental_Rank'] = data.groupby(["Year", "Continent", "Variable"])[
        "Value"].rank(method='dense', ascending=False)

    data['Income_Rank'] = data.groupby(["Year", "IncomeLevel", "Variable"])[
        "Value"].rank(method='dense', ascending=False)

    return data


def format_data(data):
    data = data.copy()
    variable_names = {
        'ESRU': 'Efficient and sustainable resource use',
        'NCP': 'Natural capital protection',
        'GEO': 'Green economic opportunities',
        'SI': 'Social inclusion',
        'EE': 'Efficient and and sustainable energy',
        'EW': 'Efficient and sustainable water use',
        'SL': 'Sustainable land use',
        'ME': 'Material use efficiency',
        'EQ': 'Environmental quality',
        'GE': 'Greenhouse gas emissions reductions',
        'BE': 'Biodiversity and ecosystem protection',
        'CV': 'Cultural and social value',
        'GV': 'Green investment',
        'GT': 'Green trade',
        'GJ': 'Green employment',
        'GN': 'Green innovation',
        'AB': 'Access to basic services and resources',
        'GB': 'Gender balance',
        'SE': 'Social equity',
        'SP': 'Social protection'
    }
    var_names = pd.DataFrame.from_dict(variable_names, orient='index')
    var_names.columns = ['Variable_name']
    data = data.set_index('Variable')
    data['Variable_name'] = var_names
    data = data.reset_index()

    data = add_rank_to_data(data)
    return data


def load_index_data(max_year):
    data = (
        pd.read_csv('data/GGIs_2005_2020.csv')
          .query(f"Year <=  {max_year}")
          .replace('America', 'Americas')
    )

    data = format_data(data)
    return data


def load_indicator_data():

    indicator_data = pd.read_csv('data/indicators/data.csv')
    dimension_properties = pd.read_csv(
        'data/indicators/dimension_properties.csv')
    indicator_properties = pd.read_csv(
        'data/indicators/indicator_properties.csv')

    return indicator_data, indicator_properties, dimension_properties


def get_ISO_options(data):
    return data[['ISO', 'Country']].drop_duplicates().values


def get_missing_values_stat(data, indicator_properties, max_year=2019):
    data = data[(data.Year >= 2005) & (data.Year <= max_year)]
    data = pd.merge(data, indicator_properties, on='Indicator')
    data['Year'] = data['Year'].astype(int)
    
    agg = ['ISO', 'Dimension']
    df = data.groupby(agg).apply(lambda x: x['Imputed'].sum() / x.shape[0] * 100)
    df = pd.DataFrame(df, columns=['% of imputed data'])
    df['imputed data points'] = data.groupby(
        agg).apply(lambda x: x['Imputed'].sum())

    df['corrected data points'] = data.groupby(
        agg).apply(lambda x: x['Corrected'].sum())

    df['% of corrected data points'] = data.groupby(agg).apply(
        lambda x: x['Corrected'].sum() / x.shape[0] * 100)

    df['Total data points'] = data.groupby(agg).apply(lambda x: x.shape[0])
    return df


def load_all_data(max_year=2019):
    data = load_index_data(max_year)

    indicator_data, indicator_properties, dimension_properties = load_indicator_data()

    data = pd.merge(data, indicator_properties[['Category', 'Dimension']].drop_duplicates(
    ), left_on='Variable', right_on='Category', how='left')


    missing_data = get_missing_values_stat(indicator_data, indicator_properties)

    ISO_options = get_ISO_options(data)

    return data, indicator_data, indicator_properties, dimension_properties, ISO_options, missing_data
