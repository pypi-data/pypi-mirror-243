from typing import Any

from .create_query_features_dataset import create_dataset_query, _create_feature_to_table_mapping, _get_feature_columns


def create_table_query(
            base_db: str,
            base_table: str,
            ref_date: str,
            monthly_window: int,
            mode: str,
            base_name: str,
            model_name: str,
            model_version: int,
            features_schema: dict,
            base_filter: str = '',
            fill_na: int = None,
            features_order: list[str] = None,
        ) -> str:
    """
    Generates the query to create the features table that is going to be loaded in
    'monthly_inference_features_iceberg' (inference mode) or 'monthly_training_features_iceberg' (training mode).

    Args:
        base_db (str): database where the base table is located.
        base_table (str): base table
        ref_date (str): Reference date to create the dataset
        monthly_window (int): Number of months to create the dataset
        mode (str): Mode to create the dataset. It can be 'training' or 'inference'
        base_name (str): Name of the audience (inference) or target (training)
        model_name (str): model name
        model_version (int): model version
        features_schema (dict, optional): schema of the features
        base_filter (str, optional): Filter to apply to the base table. Defaults to ''.
        fill_na (int, optional): value to fill nulls. Defaults to None.
        features_order (list[str], optional): list of features in the order they should be in the dataset.
            Defaults to None.
    
    Returns:
        str: query to create the features table
    """
    query_features_dataset = create_dataset_query(
        base_db=base_db,
        base_table=base_table,
        ref_date=ref_date,
        monthly_window=monthly_window,
        mode=mode,
        base_filter=base_filter,
        fill_na=fill_na,
        features_schema=features_schema,
        features_order=features_order,
        add_table_prefix=True,
    )
    logical_versions_tuple = [
        (features_schema[table_name]['logical_version'], table_name)
        for table_name in features_schema.keys()
    ]
    logical_version_table = _create_logical_version_table(logical_versions_tuple)
    feature_to_table = _create_feature_to_table_mapping(features_schema)
    feature_columns = _get_feature_columns(features_order=features_order, features_schema=features_schema)
    feature_columns_with_prefix = [
        feature_to_table[col] + '__' + col
        for col in feature_columns
    ]
    # Split the list of features in chunks of 254 columns (due to Athena limitations of array size)
    feature_chunks = _split_list(feature_columns_with_prefix, 254)
    query_unnest = _create_query_unnest(feature_chunks, ref_date)
    query_features_table = _create_query_features_table(
        query_features_dataset,
        list(features_schema.keys()),
        query_unnest,
        logical_version_table,
        base_name,
        model_name,
        model_version,
        mode,
    )
    return query_features_table


def _create_logical_version_table(logical_versions: list[tuple[int, str]]) -> str:
    columns = []
    for logical_version, table_name in logical_versions:
        columns.append(f"\t\tSELECT '{table_name}' AS table_name, {logical_version} AS logical_version")
        columns.append("\t\tUNION ALL")
    return '\n'.join(columns[:-1])


def _create_query_features_table(
            features_dataset: str,
            feature_tables: list[str], 
            query_unnest: str,
            logical_version_table: str,
            base_name: str,
            model_name: str,
            model_version: int,
            mode: str,
        ) -> str:
    output_table = 'monthly_inference_features_iceberg' if mode == 'inference' else 'monthly_training_features_iceberg'
    base_col = 'audience_name' if mode == 'inference' else 'target_name'
    table_filter = ','.join([f"'{table_name}'" for table_name in feature_tables])
    query_features_table = f"""
        INSERT INTO machine_learning.{output_table}

        WITH features AS (
            {features_dataset}
        ),

        logical_version AS (
            {logical_version_table}
        ),

        features_information AS (
            SELECT
                table_name,
                column_name,
                CASE
                    WHEN data_type = 'integer' THEN 'int'
                    ELSE data_type
                END AS feature_type
            FROM information_schema.columns
            WHERE table_schema = 'machine_learning'
                AND table_name IN ({table_filter})
        ),

        unnest_features AS (
            {query_unnest}
        )

        SELECT
            features.mach_id,
            features.exec_date,
            info.table_name,
            version.logical_version,
            features.feature_name,
            info.feature_type,
            features.value,
            '{base_name}' AS {base_col},
            '{model_name}' AS model_name,
            {model_version} AS model_version,
            features.event_time,
            LOCALTIMESTAMP AS write_time,
            False AS is_deleted
        FROM unnest_features features
        LEFT JOIN features_information info
            ON features.feature_name = info.column_name
            AND features.table_name = info.table_name
        LEFT JOIN logical_version version
            ON info.table_name = version.table_name
    """
    return query_features_table


def _create_query_unnest(feature_chunks: list[list[str]], ref_date: str) -> str:
    query_unnest = ''
    total_chunks = len(feature_chunks)
    for n_chunk, feat_chunk in enumerate(feature_chunks):
        feat_cols = ', '.join(feat_chunk)
        query_unnest += f"""
            SELECT
                mach_id,
                event_time,
                DATE('{ref_date}') + INTERVAL '1' MONTH AS exec_date,
                SPLIT(feature_name_with_prefix, '__')[1] AS table_name,
                SPLIT(feature_name_with_prefix, '__')[2] AS feature_name,
                CAST(value AS VARCHAR) AS value
            FROM features,
            UNNEST(
                ARRAY{feat_chunk},
                ARRAY[{feat_cols}]
            ) AS t(feature_name_with_prefix, value)
        """
        if n_chunk != total_chunks - 1:
            query_unnest += "UNION ALL"
    return query_unnest


def _split_list(lst: list[Any], chunk_size: int) -> list[list[Any]]:
    """Splits a list into a list of lists of size equals to chunk_size.
        The last element of the list has the remaining elements of the original list
        (not necessary equals to chunk_size).

    Args:
        lst (List[Any]): list
        chunk_size (int): size of the chunk

    Returns:
        List[List[Any]]: chunked list of lists
    """
    return [lst[i:i + chunk_size] for i in range(0, len(lst), chunk_size)]
