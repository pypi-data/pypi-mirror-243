import pandas as pd
from datetime import datetime
import awswrangler as wr


def list_columns_of_table(
            glue_client,
            database: str,
            table: str,
            cols_to_exclude: set[str] = None,
            chars_to_exclude: str = ' ',
        ) -> list[str]:
    if cols_to_exclude is None:
        cols_to_exclude = set()
    columns = []
    response = glue_client.get_table(DatabaseName=database, Name=table)
    while True:
        for item in response['Table']['StorageDescriptor']['Columns']:
            if item['Name'] not in cols_to_exclude and not any(chars in item['Name'] for chars in chars_to_exclude):
                columns.append(item['Name'])
        if 'NextToken' not in response:
            break
        response = glue_client.get_table(DatabaseName=database, Name=table, NextToken=response['NextToken'])
    assert len(columns) == len(set(columns)), f'Column names are not unique: {columns}'
    return columns


def list_feature_tables_of_database(
            glue_client,
            database: str,
            tables_to_exclude: set[str] = None,
            expression: str = '',
        ) -> list[str]:
    if tables_to_exclude is None:
        tables_to_exclude = set()
    tables = []
    response = glue_client.get_tables(DatabaseName=database, Expression=expression)
    while True:
        for item in response['TableList']:
            if item['Name'] not in tables_to_exclude:
                tables.append(item['Name'])
        if 'NextToken' not in response:
            break
        response = glue_client.get_tables(DatabaseName=database, Expression=expression, NextToken=response['NextToken'])
    return tables


def load_dataframe_to_iceberg_table(
            df: pd.DataFrame,
            database: str,
            table: str,
            table_location: str,
            s3_output: str = 's3://078659683085-sandbox-tempusu/temp',
        ) -> None:
    slash = '' if s3_output[-1] == '/' else '/'
    timestamp_str = datetime.now().strftime('%Y-%m-%dT%H:%M:%S')
    unique_temp_path = s3_output + slash + database + '/' + table + '/' + timestamp_str
    wr.athena.to_iceberg(
        df=df,
        database=database,
        table=table,
        temp_path=unique_temp_path,
        workgroup='tech_users',
        table_location=table_location,
    )
