import pandas as pd


def add_rank_to_data(data):
    '''To improve'''

    data['Continental_Rank'] = data.groupby(["Year", "Continent", "Variable"])[
        "Value"].rank(method='dense', ascending=False)

    data['Income_Rank'] = data.groupby(["Year", "IncomeLevel", "Variable"])[
        "Value"].rank(method='dense', ascending=False)

    return data


def continent_grouping(data):
    europe_america = ['Northern Europe', 'Southern Europe', 'Western Europe', 'Eastern Europe', 'Northern America']
    latin_America = ['Central America', 'South America']
    caribbean = ['Caribbean']
    central_south_asia = ['Central Asia', 'Southern Asia']
    east_asia = ['South-Eastern Asia', 'Eastern Asia']
    northen_africa = ['Northern Africa', 'Western Asia']
    sub_afr = ['Middle Africa', 'Western Africa', 'Southern Africa', 'Eastern Africa'] 
    oceania = ['Melanesia', 'Micronesia', 'Polynesia', 'Australia and New Zealand']

    names = [
        (oceania, 'Oceania, Australia and New Zealand'),
        (europe_america, 'Europe and Northern America'),
        (latin_America, 'Latin America'),
        (caribbean, 'Caribbean'),
        (central_south_asia, 'Central and Southern Asia'),
        (east_asia, 'Eastern and South-Eastern Asia'),
        (northen_africa, 'Northern Africa and Western Asia'),
        (sub_afr, 'Sub-Saharan Africa'),
    ]

    region = pd.concat([
    pd.DataFrame(name[0]).assign(Continent=name[1]) for name in names
    ]).rename(columns={0: 'UNregion'})

    return data.drop(columns=['Continent']).merge(region, on='UNregion')


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
          .round(2)
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


def get_missing_values_stat(data, indicator_properties, max_year=2020, min_year=2010):
    data = data[(data.Year >= min_year) & (data.Year <= max_year)]
    data = pd.merge(data, indicator_properties, on='Indicator').astype({'Year': int})

    
    total_points = (indicator_properties.groupby('Category').Indicator.count() * (max_year - min_year + 1))
    
    #df =  data.groupby(['ISO', 'Category']).apply(lambda x: x.shape[0]).divide(total_points) * 100
    df =  data.query("Imputed == False").groupby(['ISO', 'Category']).apply(lambda x: x.shape[0]).divide(total_points) * 100

    ISOs = data.ISO.unique()
    Categorys = indicator_properties.Category.unique()
    full_index = pd.MultiIndex.from_product([ISOs, Categorys],
                               names=['ISO', 'Category'])
    
    return df.reindex(full_index, fill_value=0).to_frame(name='Data availability (%)')


def load_all_data(max_year=2019):
    data = load_index_data(max_year)

    data = continent_grouping(data)

    indicator_data, indicator_properties, dimension_properties = load_indicator_data()

    # indicator_data = indicator_data.query("Indicator not in ['GT2', 'GN2']")
    # indicator_properties = indicator_properties.query("Indicator not in ['GT2', 'GN2']")
    # data = data.query("Variable not in ['GT2','GN2']")

    data = pd.merge(data, indicator_properties[['Category', 'Dimension']].drop_duplicates(
    ), left_on='Variable', right_on='Category', how='left').query("Year >= 2015")


    missing_data = get_missing_values_stat(indicator_data, indicator_properties, max_year=2020, min_year=2015)

    ISO_options = get_ISO_options(data)

    return data, indicator_data, indicator_properties, dimension_properties, ISO_options, missing_data
