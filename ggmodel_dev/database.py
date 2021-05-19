import os
import pandas as pd
from sqlalchemy import create_engine

username = os.environ.get("GGGI_db_username")
password = os.environ.get("GGGI_db_password")
endpoint = os.environ.get("GGGI_db_endpoint")
port = os.environ.get("GGGI_db_port")

db_connection_url = f"postgresql://{username}:{password}@{endpoint}:{port}"
engine = create_engine(db_connection_url)
 

def upload_df_to_dbtable(df, tablename, engine=engine):
    with engine.connect().execution_options(autocommit=True) as conn:
        df.to_sql(tablename, con=conn,
                  if_exists="replace", 
                  index=False, method="multi",
                  chunksize=10000)
        

def upload_dataset(df, meta_df, dataset, engine=engine):
    upload_df_to_dbtable(meta_df, f'meta{dataset}')
    upload_df_to_dbtable(df, dataset)        
    
    meta_df = select_all_metadata()
    
    upload_df_to_dbtable(meta_df, 'allvariables')

    
def select_table(tablename, engine=engine):
    sql = f'SELECT * FROM {tablename}'
    with engine.connect() as conn:
        df = pd.read_sql(sql, conn)
    return df


def select_dataset(dataset, engine=engine):
    '''Merge is done localy because otherwise data is too big to be pulled (Unless)'''
    df = select_table(dataset)
    meta_df = select_table(f'meta{dataset}')
    return pd.merge(df, meta_df, on='Variable')


def format_variable_list(variable_list):
    return "(\'" + ('\',\'').join(variable_list) + "\')"
    

def get_groups_from_df(grouped_df):
    groups = {}
    for key, value in grouped_df.groups.items():
        groups[key] = value.tolist()
    return groups


def get_variable_groups(df):
    return get_groups_from_df(df[['Variable', 'table']].set_index('Variable').groupby('table'))


def select_all_metadata(engine=engine):
    
    metatables = [table for table in engine.table_names() if 'meta' in table]
    dfs = [select_table(table).assign(table=table.replace('meta', '')) for table in metatables]
    
    df = pd.concat(dfs)
    
    return df


def get_variables_metadata(variables, engine=engine):
    
    variables_string = format_variable_list(variables)
    
    sql = f"SELECT * FROM allvariables WHERE allvariables.\"Variable\" in {variables_string};"
    with engine.connect() as conn:
        df = pd.read_sql(sql, conn)
    return df


def select_variables_in_table(variables, tablename, ISO=[], engine=engine):
    
    variables_string = "(\'" + ('\',\'').join(variables) + "\')"
    
    sql = f'SELECT * FROM {tablename} WHERE \"Variable\" in {variables_string}'
    
    if len(ISO) > 0:
        iso_string = "(\'" + ('\',\'').join(ISO) + "\')"
        sql += f'AND \"ISO\" in {iso_string}'
    
    
    with engine.connect() as conn:
        df = pd.read_sql(sql, conn)
        
    return df



def get_variables_df(variables, ISO=[], exclude_tables=[], engine=engine):
    '''To slow to do a single query'''
    
    variables_string = format_variable_list(variables)
    
    meta_df = get_variables_metadata(variables)
    
    variable_groups = get_variable_groups(meta_df)
    
    dfs = {}
    
    for table, variables in variable_groups.items():
        print(table, ', '.join(variables), end=': ')
        if table not in exclude_tables:            
            try:
                df = select_variables_in_table(variables, table, ISO).merge(meta_df.query(f"table == '{table}'"), on=['Variable'])
                dfs[table] = df
                print('Done')
            except Exception as e:
                print('Error', e)
        else:
            print('Excluded')
    return dfs
