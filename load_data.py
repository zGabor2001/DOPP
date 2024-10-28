import pandas as pd
import os
import typing


def load_weather_data(weather_data_path: str) -> typing.Tuple[pd.DataFrame, pd.DataFrame]:
    """
    Load all weather data files and combine them into a single Pandas DataFrame.
    Split the tri-daily data from the daily data.
    For the tri-daily data create a new hour column using the indicated hour in the column names.
    Add a hierarchical index (year, month, day, hour).
    For the daily-only data also add a hierarchical index (year, month, day).

    Parameters
    --------
    weather_data_path: path to directory containing weather data CSV files

    Returns
    --------
    weather_data: data frame containing the tri-daily (hours) weather data
    weather_data_daily: data frame containing the daily weather data (e.g. precip, precipType, etc.)
    """
    import re

    dfs: list = []
    for file in os.listdir(weather_data_path):
        dfs.append(pd.read_csv(os.path.join(weather_data_path, file), sep=';'))

    df_merged: pd.DataFrame = pd.concat(dfs, ignore_index=True)
    df_merged['date'] = pd.to_datetime(df_merged['date'], format='%d.%m.%Y')

    tri_daily_index = (['date'] +
                       [col for col in df_merged.columns if col.endswith(('_7h', '_14h', '_19h'))])
    weather_data = df_merged[tri_daily_index]

    dfs_by_suffix: dict = {}
    for suffix in ['_7h', '_14h', '_19h']:
        dfs_by_suffix[suffix] = (weather_data[['date'] +
                                [col for col in weather_data.columns if col.endswith(suffix)]])

    hour_df_list: list = []
    for hour_tag in dfs_by_suffix.keys():
        dfs_by_suffix[hour_tag]['date']: pd.Series = (dfs_by_suffix[hour_tag]['date'].dt.floor('D') +
                                       pd.Timedelta(hours=int(re.sub(r'\D', '', hour_tag))))
        non_hour_cols: list = [re.sub(r'_[^_]*$', '', col) for col in dfs_by_suffix[hour_tag].columns]
        dfs_by_suffix[hour_tag].columns = non_hour_cols
        hour_df_list.append(dfs_by_suffix[hour_tag])

    weather_data: pd.DataFrame = pd.concat(hour_df_list, ignore_index=True)

    daily_index = [col for col in df_merged.columns if not col.endswith(('_7h', '_14h', '_19h'))]
    weather_data_daily: pd.DataFrame = df_merged[daily_index]

    weather_df_list: list = [weather_data_daily, weather_data]
    for df in weather_df_list:
        multi_index: pd.MultiIndex = pd.MultiIndex.from_arrays(
            [df['date'].dt.year,
             df['date'].dt.month,
             df['date'].dt.day,
             df['date'].dt.hour],
            names=['Year', 'Month', 'Day', 'Hour']
        )

        df.set_index(multi_index, inplace=True)
        df.drop(columns=['date'], inplace=True)
        df.sort_index(inplace=True)

    weather_data_daily: pd.DataFrame = weather_data_daily.droplevel(level=-1)

    return weather_data, weather_data_daily