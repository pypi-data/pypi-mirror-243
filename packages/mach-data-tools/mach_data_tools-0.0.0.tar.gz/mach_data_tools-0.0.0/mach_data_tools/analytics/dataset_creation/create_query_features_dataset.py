from boto3 import client

from mach_data_tools.aws.glue import list_columns_of_table


def create_dataset_query(
            base_db: str,
            base_table: str,
            ref_date: str,
            monthly_window: int,
            mode: str,
            base_filter: str = '',
            fill_na: int = None,
            features_schema: dict = None,
            features_order: list[str] = None,
            feature_tables: list[str] = None,
            cols_to_exclude: list[str] = None,
            chars_to_exclude: list[str] = None,
            glue_client: client = None,
            add_table_prefix: bool = False,
        ) -> str:
    """
    Generates a query to create a dataset with event_time, mach_id, features (and target value if in 'inference' mode).

    Parameters
    ----------
    base_db : str
        Database where the base table is located.
    base_table : str
        Base table name.
    ref_date : str
        Reference date to create the dataset.
    monthly_window : int
        Number of months to create the dataset.
    mode : str
        Mode to create the dataset. It can be 'training' or 'inference'.
    base_filter : str, optional
        Filter to apply to the base table.
    fill_na : int, optional
        Value to fill nulls.
    features_schema : dict, optional
        Schema of the features. Used for inference mode in production.
    features_order : list[str], optional
        List of features in the order they should be in the dataset.
    feature_tables : list[str], optional
        List of feature tables. Used for training mode in development.
    cols_to_exclude : list[str], optional
        List of columns to exclude from the feature tables.
    chars_to_exclude : list[str], optional
        List of characters to exclude from the feature tables.
    glue_client : boto3.client, optional
        Glue client.
    add_table_prefix : bool, optional
        Whether to add the table name as prefix to the feature columns.
    """
    if mode not in ['training', 'inference']:
        raise ValueError("mode must be either 'training' or 'inference'.")
    feature_columns = _get_feature_columns(
        feature_tables,
        features_order,
        features_schema,
        glue_client,
        cols_to_exclude,
        chars_to_exclude,
    )
    feature_to_table = {}
    if add_table_prefix:
        feature_to_table = _create_feature_to_table_mapping(features_schema)
    select_features = _create_select_features(
        feature_columns,
        feature_to_table,
        mode,
        base_db,
        base_table,
        fill_na,
        add_table_prefix
    )
    join_features = _create_statement_join_features(base_db, base_table, feature_tables, features_schema)
    filters = _create_statement_filter_base_table(base_db, base_table, ref_date, monthly_window, mode, base_filter)
    query = _create_query_features_dataset(base_db, base_table, select_features, join_features, filters)
    return query


def _create_feature_to_table_mapping(features_schema: dict) -> dict[str, str]:
    feature_to_table = {}
    for table_name, table in features_schema.items():
        for column in table['columns']:
            feature_to_table[column] = table_name
    return feature_to_table


def _create_select_features(
            select_columns: list[str],
            feature_to_table: dict[str, str],
            mode: str,
            base_db: str,
            base_table: str,
            fill_na: int = None,
            add_table_prefix: bool = False,
        ) -> str:
    columns = []
    fill_na_value = 'NULL' if fill_na is None else fill_na
    for col in select_columns:
        table_prefix = feature_to_table[col] + '__' if add_table_prefix else '' 
        columns.append('\t\tCOALESCE(' + col + f', {fill_na_value}) AS {table_prefix}{col}')
    columns.append(f"\t\tCAST({base_db}.{base_table}.event_time AS TIMESTAMP(3)) "
                   "AS event_time")
    columns.append(f"\t\t{base_db}.{base_table}.mach_id")
    if mode == 'training':
        columns.append(f"\t\t{base_db}.{base_table}.target_value")
    return ',\n'.join(columns)


def _create_statement_join_features(
            base_db: str,
            base_table: str,
            feature_tables: list[str] = None,
            features_schema: dict = None,
        ) -> str:
    join_features_list = []
    param_to_choose = feature_tables if feature_tables is not None else features_schema
    for feature in param_to_choose:
        join_features_list.append(f"""
            LEFT JOIN machine_learning.{feature}
                ON {base_db}.{base_table}.mach_id =
                    machine_learning.{feature}.mach_id
                AND machine_learning.{feature}.event_time =
                    {base_db}.{base_table}.event_time
                AND machine_learning.{feature}.is_current_version = True
                AND machine_learning.{feature}.is_deleted = False
        """)
    return ''.join(join_features_list)


def _create_statement_filter_base_table(
            base_db: str,
            base_table: str,
            ref_date: str,
            monthly_window: int,
            mode: str,
            base_filter: str = '',
        ) -> str:
    filter_last_version = f"AND {base_db}.{base_table}.is_current_version = True" if mode == 'training' else ''
    statement_filters = f"""
        {base_db}.{base_table}.event_time
            BETWEEN DATE_PARSE(\'{ref_date}\', '%Y-%m-%d') - INTERVAL '{monthly_window - 1}' MONTH
            AND DATE_PARSE('{ref_date}', '%Y-%m-%d')
            AND {base_db}.{base_table}.is_deleted = False
            {filter_last_version}
            {base_filter}
    """
    return statement_filters


def _create_query_features_dataset(
            base_db: str,
            base_table: str,
            select_features: str,
            join_features: str,
            filters_base_table: str,
        ) -> str:
    query_features = f"""
        SELECT
            {select_features}
        FROM {base_db}.{base_table}
        {join_features}
        WHERE {filters_base_table}
    """
    return query_features


def _get_feature_columns_from_data_catalog(
            feature_tables: list[str],
            glue_client,
            cols_to_exclude: set[str],
            chars_to_exclude: list[str],
        ) -> list[str]:
    feature_columns = []
    for feature in feature_tables:
        feature_columns += list_columns_of_table(
            glue_client=glue_client,
            database='machine_learning',
            table=feature,
            cols_to_exclude=cols_to_exclude,
            chars_to_exclude=chars_to_exclude,
        )
    return feature_columns

def _get_feature_columns(
            feature_tables: list[str] = None,
            features_order: list[str] = None,
            features_schema: dict = None,
            glue_client = None,
            cols_to_exclude: set[str] = None,
            chars_to_exclude: list[str] = None,
        ) -> list[str]:
    if feature_tables is not None:
        feature_columns = _get_feature_columns_from_data_catalog(
            feature_tables,
            glue_client,
            cols_to_exclude,
            chars_to_exclude,
        )
    elif features_order is not None:
        feature_columns = features_order
    elif features_schema is not None:
        feature_columns = []
        for table in features_schema.values():
            feature_columns += table['columns']
    else:
        raise ValueError('You need to either specify feature_tables, features_order or features_schema.')
    return feature_columns
