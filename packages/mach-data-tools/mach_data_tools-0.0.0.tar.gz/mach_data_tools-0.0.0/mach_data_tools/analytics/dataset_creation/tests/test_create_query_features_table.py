import pytest

from bcirisktools.analytics.dataset_creation.create_query_features_table import (
    create_table_query,
    _create_logical_version_table,
    _create_query_unnest,
    _split_list,
)


def _remove_special_chars(string: str) -> str:
    return string.replace('\n', '').replace('\t', '').replace('  ', '').strip()


@pytest.fixture
def default_params():
    params = {
        "base_table": "base_table",
        "base_db": "base_database",
        "ref_date": "2023-01-01",
        "monthly_window": 3,
        "mode": "training",
        "base_name": "my_target",
        "model_name": "my_model",
        "model_version": 1,
        "features_schema":  {"my_table": {"logical_version": 1, "columns": ["col1", "col2", "col3"]}},
    }
    return params


def test_create_table_query(default_params):
    expected = """
        INSERT INTO machine_learning.monthly_training_features_iceberg

        WITH features AS (
            
        SELECT
                COALESCE(col1, NULL) AS my_table__col1,
                COALESCE(col2, NULL) AS my_table__col2,
                COALESCE(col3, NULL) AS my_table__col3,
                CAST(base_database.base_table.event_time AS TIMESTAMP(3)) AS event_time,
                base_database.base_table.mach_id,
                base_database.base_table.target_value
        FROM base_database.base_table
        
            LEFT JOIN machine_learning.my_table
                ON base_database.base_table.mach_id =
                    machine_learning.my_table.mach_id
                AND machine_learning.my_table.event_time =
                    base_database.base_table.event_time
                AND machine_learning.my_table.is_current_version = True
                AND machine_learning.my_table.is_deleted = False
        
        WHERE 
        base_database.base_table.event_time
            BETWEEN DATE_PARSE('2023-01-01', '%Y-%m-%d') - INTERVAL '2' MONTH
            AND DATE_PARSE('2023-01-01', '%Y-%m-%d')
            AND base_database.base_table.is_deleted = False
            AND base_database.base_table.is_current_version = True
        ),

        logical_version AS (
                        SELECT 'my_table' AS table_name, 1 AS logical_version
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
                AND table_name IN ('my_table')
        ),

        unnest_features AS (
            
            SELECT
                mach_id,
                event_time,
                DATE('2023-01-01') + INTERVAL '1' MONTH AS exec_date,
                SPLIT(feature_name_with_prefix, '__')[1] AS table_name,
                SPLIT(feature_name_with_prefix, '__')[2] AS feature_name,
                CAST(value AS VARCHAR) AS value
            FROM features,
            UNNEST(
                ARRAY['my_table__col1', 'my_table__col2', 'my_table__col3'],
                ARRAY[my_table__col1, my_table__col2, my_table__col3]
            ) AS t(feature_name_with_prefix, value)
        
        )

        SELECT
            features.mach_id,
            features.exec_date,
            info.table_name,
            version.logical_version,
            features.feature_name,
            info.feature_type,
            features.value,
            'my_target' AS target_name,
            'my_model' AS model_name,
            1 AS model_version,
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
    result = create_table_query(
        default_params["base_db"],
        default_params["base_table"],
        default_params["ref_date"],
        default_params["monthly_window"],
        default_params["mode"],
        default_params["base_name"],
        default_params["model_name"],
        default_params["model_version"],
        default_params["features_schema"],
    )
    assert _remove_special_chars(result) == _remove_special_chars(expected)


def test_create_logical_version_table():
    logical_versions = [(1, "table_1"), (2, "table_2"), (1, "table_3")]
    expected = """
        SELECT 'table_1' AS table_name, 1 AS logical_version
        UNION ALL
        SELECT 'table_2' AS table_name, 2 AS logical_version
        UNION ALL
        SELECT 'table_3' AS table_name, 1 AS logical_version
    """
    result = _create_logical_version_table(logical_versions)
    assert _remove_special_chars(result) == _remove_special_chars(expected)


def test_create_query_unnest():
    feature_chunks = [["feature1", "feature2"], ["feature3", "feature4"]]
    ref_date = "2022-01-01"
    expected = """
        SELECT
            mach_id,
            event_time,
            DATE('2022-01-01') + INTERVAL '1' MONTH AS exec_date,
            SPLIT(feature_name_with_prefix, '__')[1] AS table_name,
            SPLIT(feature_name_with_prefix, '__')[2] AS feature_name,
            CAST(value AS VARCHAR) AS value
        FROM features,
        UNNEST(
            ARRAY['feature1', 'feature2'],
            ARRAY[feature1, feature2]
        ) AS t(feature_name_with_prefix, value)
        UNION ALL
        SELECT
            mach_id,
            event_time,
            DATE('2022-01-01') + INTERVAL '1' MONTH AS exec_date,
            SPLIT(feature_name_with_prefix, '__')[1] AS table_name,
            SPLIT(feature_name_with_prefix, '__')[2] AS feature_name,
            CAST(value AS VARCHAR) AS value
        FROM features,
        UNNEST(
            ARRAY['feature3', 'feature4'],
            ARRAY[feature3, feature4]
        ) AS t(feature_name_with_prefix, value)
    """
    result = _create_query_unnest(feature_chunks, ref_date)
    assert _remove_special_chars(result) == _remove_special_chars(expected)


def test_split_list():
    lst = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
    chunk_size = 3

    expected_result = [[1, 2, 3], [4, 5, 6], [7, 8, 9], [10]]

    assert _split_list(lst, chunk_size) == expected_result
