import pytest
from pytest_mock.plugin import MockerFixture
from bcirisktools.analytics.dataset_creation.create_query_features_dataset import (
    _create_feature_to_table_mapping,
    _create_select_features,
    _create_statement_filter_base_table,
    _create_statement_join_features,
    _create_query_features_dataset,
    _get_feature_columns,
    _get_feature_columns_from_data_catalog,
)


def _remove_special_chars(string: str) -> str:
    return string.replace('\t', '').replace('  ', '').strip()


@pytest.fixture
def default_params():
    params = {
        "base_table": "base_table",
        "base_db": "base_database",
        "ref_date": "2023-01-01",
        "ATHENA_MACHINE_LEARNING": "machine_learning",
        "monthly_window": 3,
    }
    return params


@pytest.fixture
def features_schema():
    schema = {
        "feature_table": {"logical_version": 1, "columns": ["col1", "col2", "col3"]},
    }
    return schema

@pytest.fixture
def feature_to_table():
    return {
        "col1": "feature_table",
        "col2": "feature_table",
        "col3": "feature_table",
    }

@pytest.fixture
def feature_tables():
    return ["feature_table_1", "feature_table_2"]


def test_create_select_features_inference(default_params, feature_to_table):
    select_columns = ["col1", "col2", "col3"]
    params = {**default_params, "mode": "inference"}
    expected = """
            COALESCE(col1, NULL) AS col1,
            COALESCE(col2, NULL) AS col2,
            COALESCE(col3, NULL) AS col3,
            CAST(base_database.base_table.event_time AS TIMESTAMP(3)) AS event_time,
            base_database.base_table.mach_id
    """
    result = _create_select_features(
        select_columns,
        feature_to_table,
        params["mode"],
        params["base_db"],
        params["base_table"],
    )
    assert _remove_special_chars(result) == _remove_special_chars(expected)


def test_create_select_features_training(default_params, feature_to_table):
    select_columns = ["col1", "col2", "col3"]
    params = {**default_params, "mode": "training"}
    expected = """
            COALESCE(col1, NULL) AS col1,
            COALESCE(col2, NULL) AS col2,
            COALESCE(col3, NULL) AS col3,
            CAST(base_database.base_table.event_time AS TIMESTAMP(3)) AS event_time,
            base_database.base_table.mach_id,
            base_database.base_table.target_value
    """
    result = _create_select_features(
        select_columns,
        feature_to_table,
        params["mode"],
        params["base_db"],
        params["base_table"],
    )
    assert _remove_special_chars(result) == _remove_special_chars(expected)


def test_create_select_features_fill_na(default_params, feature_to_table):
    select_columns = ["col1", "col2", "col3"]
    params = {**default_params, "mode": "training", "fill_na": "0"}
    expected = """
            COALESCE(col1, 0) AS col1,
            COALESCE(col2, 0) AS col2,
            COALESCE(col3, 0) AS col3,
            CAST(base_database.base_table.event_time AS TIMESTAMP(3)) AS event_time,
            base_database.base_table.mach_id,
            base_database.base_table.target_value
    """
    result = _create_select_features(
        select_columns,
        feature_to_table,
        params["mode"],
        params["base_db"],
        params["base_table"],
        params["fill_na"],
    )
    assert _remove_special_chars(result) == _remove_special_chars(expected)


def test_create_statement_join_features(default_params, features_schema):
    params = {**default_params, "features_schema": features_schema}
    expected = """
        LEFT JOIN machine_learning.feature_table
            ON base_database.base_table.mach_id =
                machine_learning.feature_table.mach_id
            AND machine_learning.feature_table.event_time =
                base_database.base_table.event_time
            AND machine_learning.feature_table.is_current_version = True
            AND machine_learning.feature_table.is_deleted = False
    """
    result = _create_statement_join_features(params["base_db"], params["base_table"], None, params["features_schema"])
    assert _remove_special_chars(result) == _remove_special_chars(expected)


def test_create_statement_join_features_glue_data_catalog(default_params, feature_tables):
    params = {**default_params, "feature_tables": feature_tables}
    expected = """
        LEFT JOIN machine_learning.feature_table_1
            ON base_database.base_table.mach_id =
                machine_learning.feature_table_1.mach_id
            AND machine_learning.feature_table_1.event_time =
                base_database.base_table.event_time
            AND machine_learning.feature_table_1.is_current_version = True
            AND machine_learning.feature_table_1.is_deleted = False
    
        LEFT JOIN machine_learning.feature_table_2
            ON base_database.base_table.mach_id =
                machine_learning.feature_table_2.mach_id
            AND machine_learning.feature_table_2.event_time =
                base_database.base_table.event_time
            AND machine_learning.feature_table_2.is_current_version = True
            AND machine_learning.feature_table_2.is_deleted = False
    """
    result = _create_statement_join_features(params["base_db"], params["base_table"], params["feature_tables"], None)
    assert _remove_special_chars(result) == _remove_special_chars(expected)


def test_create_statement_filter_base_table(default_params, features_schema):
    params = {**default_params, "features_schema": features_schema, "mode": "training"}
    expected = """
        base_database.base_table.event_time
            BETWEEN DATE_PARSE('2023-01-01', '%Y-%m-%d') - INTERVAL '2' MONTH
            AND DATE_PARSE('2023-01-01', '%Y-%m-%d')
            AND base_database.base_table.is_deleted = False
            AND base_database.base_table.is_current_version = True
    """
    result = _create_statement_filter_base_table(
        params["base_db"],
        params["base_table"],
        params["ref_date"],
        params["monthly_window"],
        params["mode"],
    )
    assert _remove_special_chars(result) == _remove_special_chars(expected)


def test_get_feature_columns_from_data_catalog(mocker: MockerFixture, default_params, feature_tables):
    return_values = [["col1", "col2", "col3"], ["col4", "col5", "col6"]]
    mocker.patch(
        "bcirisktools.analytics.dataset_creation.create_query_features_dataset.list_columns_of_table",
        side_effect=return_values,
    )
    params = {
        **default_params,
        "feature_tables": feature_tables,
        "glue_client": "glue_client",
        "cols_to_exclude": ["event_time", "mach_id", "is_current_version", "is_deleted"],
        "chars_to_exclude": ["default_name"],
    }
    expected = ['col1', 'col2', 'col3', 'col4', 'col5', 'col6']
    result = _get_feature_columns_from_data_catalog(
        params["feature_tables"],
        params["glue_client"],
        params["cols_to_exclude"],
        params["chars_to_exclude"],
    )
    assert result == expected


def test_get_feature_columns_feature_tables(mocker: MockerFixture, default_params, feature_tables):
    return_values = [["col1", "col2", "col3", "col4", "col5", "col6"]]
    mocker.patch(
        "bcirisktools.analytics.dataset_creation.create_query_features_dataset._get_feature_columns_from_data_catalog",
        side_effect=return_values,
    )
    params = {
        **default_params,
        "feature_tables": feature_tables,
    }
    expected = ["col1", "col2", "col3", "col4", "col5", "col6"]
    result = _get_feature_columns(params["feature_tables"])
    assert result == expected


def test_get_feature_columns_features_order(default_params):
    params = {
        **default_params,
        "features_order": ["col1", "col2"],
    }
    expected = ["col1", "col2"]
    result = _get_feature_columns(None, params["features_order"])
    assert result == expected


def test_get_feature_columns_features_schema(default_params, features_schema):
    params = {
        **default_params,
        "features_schema": features_schema,
    }
    expected = ["col1", "col2", "col3"]
    result = _get_feature_columns(None, None, params["features_schema"])
    assert result == expected


def test_create_query_features_dataset(default_params):
    select_features = """
        COALESCE(col1, NULL) AS col1,
        COALESCE(col2, NULL) AS col2,
        COALESCE(col3, NULL) AS col3,
        CAST(base_database.base_table.event_time AS TIMESTAMP(3)) AS event_time,
        base_database.base_table.mach_id
    """
    join_features = """
        LEFT JOIN machine_learning.feature_table
            ON base_database.base_table.mach_id =
                machine_learning.feature_table.mach_id
            AND machine_learning.feature_table.event_time =
                base_database.base_table.event_time
            AND machine_learning.feature_table.is_current_version = True
            AND machine_learning.feature_table.is_deleted = False
    """
    filters = """
        base_database.base_table.event_time
            BETWEEN DATE_PARSE('2023-01-01', '%Y-%m-%d') - INTERVAL '2' MONTH
            AND DATE_PARSE('2023-01-01', '%Y-%m-%d')
            AND base_database.base_table.is_current_version = True AND base_database.base_table.is_deleted = False
    """
    expected = """
        SELECT
            
        COALESCE(col1, NULL) AS col1,
        COALESCE(col2, NULL) AS col2,
        COALESCE(col3, NULL) AS col3,
        CAST(base_database.base_table.event_time AS TIMESTAMP(3)) AS event_time,
        base_database.base_table.mach_id
    
        FROM base_database.base_table
        
        LEFT JOIN machine_learning.feature_table
            ON base_database.base_table.mach_id =
                machine_learning.feature_table.mach_id
            AND machine_learning.feature_table.event_time =
                base_database.base_table.event_time
            AND machine_learning.feature_table.is_current_version = True
            AND machine_learning.feature_table.is_deleted = False
    
        WHERE 
        base_database.base_table.event_time
            BETWEEN DATE_PARSE('2023-01-01', '%Y-%m-%d') - INTERVAL '2' MONTH
            AND DATE_PARSE('2023-01-01', '%Y-%m-%d')
            AND base_database.base_table.is_current_version = True AND base_database.base_table.is_deleted = False
    """
    result = _create_query_features_dataset(
        default_params["base_db"],
        default_params["base_table"],
        select_features,
        join_features,
        filters
    )
    assert _remove_special_chars(result) == _remove_special_chars(expected)

def test_create_feature_to_table_mapping(features_schema):
    expected = {
        "col1": "feature_table",
        "col2": "feature_table",
        "col3": "feature_table",
    }
    result = _create_feature_to_table_mapping(features_schema)
    assert result == expected

