import pandas as pd
import numpy as np


def stability_stat(
            df: pd.DataFrame,
            cols_to_exclude: list[str] = ['mach_id', 'target_value'],
            timestamp_col: str = 'event_time'
        ) -> tuple[pd.DataFrame, ...]:
    df = df.drop(cols_to_exclude, axis=1)

    df_mean = _get_mean(df, timestamp_col)
    # Get mean variation
    df_mean_var = df_mean.pct_change()[1:].T
    df_mean = df_mean.T.fillna(np.NaN)

    df_std = _get_standard_deviation(df, timestamp_col)
    df_nulls = _get_percent_nulls(df, timestamp_col)
    df_coeff_var = df_std / df_mean

    return df_mean_var, df_std, df_nulls, df_coeff_var


def csi_stat(
            df: pd.DataFrame,
            cols_to_exclude: list[str] = ['mach_id', 'event_time', 'target_value'],
            timestamp_col: str = 'event_time'
        ) -> pd.DataFrame:
    cols_to_analyze = [i for i in df.columns if i not in cols_to_exclude]

    df_append = pd.DataFrame()

    for feature in cols_to_analyze:
        df_feat = df[[feature, timestamp_col]].dropna()
        n_quantiles = _get_number_of_quantiles(df_feat, feature)
        if n_quantiles == 0:
            continue
        df_feat = _get_quantile_distribution(df_feat, feature, n_quantiles)
        csi = _calculate_csi(df_feat, feature, n_quantiles)
        df_append = pd.concat([df_append, csi], axis=0)

    df_append = _assign_stability(df_append)

    return df_append


def get_features_with_low_variability(
        df: pd.DataFrame,
        cols_to_exclude: list[str] = ['mach_id', 'target_value'],
        threshold: float = 0.95) -> list[str]:
    """
    Returns a list of features with low variability (i.e. features with a single value in more than 95%
    of the observations)
    """
    df = df.drop(cols_to_exclude, axis=1)
    features = df.columns.to_list()
    features_low_variability = []
    for feature in features:
        max_percent_concentration = df[feature].value_counts(normalize=True).max()
        if max_percent_concentration > threshold:
            features_low_variability.append(feature)
    return features_low_variability


def _get_standard_deviation(df: pd.DataFrame, timestamp_col: str) -> pd.DataFrame:
    df = df.groupby(by=[timestamp_col]).std().reset_index().set_index(timestamp_col).T
    return df


def _get_mean(df: pd.DataFrame, timestamp_col: str) -> pd.DataFrame:
    df = df.groupby(by=[timestamp_col]).mean().reset_index().set_index(timestamp_col)
    return df


def _get_percent_nulls(df: pd.DataFrame, timestamp_col: str) -> pd.DataFrame:
    df = df.set_index(timestamp_col).isna().groupby(level=0).mean().T
    return df


def _get_number_of_quantiles(df: pd.DataFrame, col: str) -> int:
    unique_values = len(df[col].round(decimals=4).unique())
    return min(unique_values, 10)


def _get_quantile_distribution(df: pd.DataFrame, col: str, n_quantiles: int) -> pd.DataFrame:
    df.loc[:, 'quantile'] = pd.cut(df[col], n_quantiles)
    df = (
        df.groupby(by=['event_time', 'quantile'])
        .agg({col: 'count'})
        .reset_index()
        .rename(columns={col: 'count'})
    )
    df = df.pivot(index='quantile', columns='event_time', values='count')
    df = df.div(df.sum(axis=0), axis=1)
    return df


def _calculate_csi(df: pd.DataFrame, col: str, n_quantiles: int) -> float:
    df_out = df.copy()

    for i in range(df.shape[1] - 1):
        actual = df.iloc[:, i + 1] + 10e-20
        expected = df.iloc[:, i] + 10e-20
        df_out.iloc[:, i + 1] = (actual - expected) * np.log(actual / expected)

    df_out = df_out.drop(columns=df.columns[0])
    df_out = pd.DataFrame(df_out.sum()).rename(columns={0: col}).T
    df_out['quantile'] = n_quantiles

    return df_out


def _assign_stability(df: pd.DataFrame) -> pd.DataFrame:
    df['status'] = '🟢'
    df['status_2'] = 'low'

    bool_med_csi = (df.iloc[:, :-3] >= 0.1) & (df.iloc[:, :-3] < 0.2)
    bool_med_csi = bool_med_csi.any(axis=1)

    bool_high_csi = df.iloc[:, :-3] > 0.2
    bool_high_csi = bool_high_csi.any(axis=1)

    df.loc[bool_med_csi, 'status'] = '🟡'
    df.loc[bool_med_csi, 'status_2'] = 'medium'
    df.loc[bool_high_csi, 'status'] = '🔴'
    df.loc[bool_high_csi, 'status_2'] = 'high'

    return df
