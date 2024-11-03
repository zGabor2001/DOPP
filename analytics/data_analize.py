import pandas as pd
import typing


def get_lowest_average_temp(data_frame: pd.DataFrame):
    year = 0
    month = 0

    monthly_avg_temp: pd.DataFrame = data_frame.groupby([data_frame.index.get_level_values('year'),
                                     data_frame.index.get_level_values('month')])['temp'].mean()

    lowest_avg_temp = monthly_avg_temp.idxmin()

    year = lowest_avg_temp[0]
    month = lowest_avg_temp[1]

    return year, month


def get_day_with_most_subway_disruptions(data_frame: pd.DataFrame,
                                         disruption_type: str
                                         ) -> typing.Tuple[int, int, int]:
    year = 0
    month = 0
    day = 0

    data_frame = data_frame[data_frame['disruption'] == disruption_type]
    subway_disrupt: pd.DataFrame = data_frame.groupby([data_frame.index.get_level_values('year'),
                                                       data_frame.index.get_level_values('month'),
                                                       data_frame.index.get_level_values('day')])['disruption'].count()

    most_disruptions = subway_disrupt.idxmax()

    year = most_disruptions[0]
    month = most_disruptions[1]
    day = most_disruptions[2]

    return year, month, day


def get_data_around_missing(df: pd.DataFrame, column: str,
                            delta_days: int = 2) -> typing.List[pd.DataFrame]:
    """
    Build a list of dataframes containing missing values indicated by column.
    Each dataframe contains rows around a missing (isna)
    value in column, within a date of +- delta_days.

    Parameters
    --------
    df: dataframe containing the missing values
    column: the column to look for missing values
    delta_days: the number of days +-around the date of the missing values to keep in the returned data frames

    Returns
    --------
    df_list: list of dataframes with some missing data
    """
    df_list = []

    for date in [df[df[column].isna()].index]:
        df_timedelta = df.loc[date - pd.Timedelta(days=delta_days):date + pd.Timedelta(days=delta_days)]
        df_list.append(df_timedelta)

    return df_list


def handle_missing_temp_values(df: pd.DataFrame) -> pd.DataFrame:
    """
    Handle missing temperature values appropriately!

    Parameters
    --------
    df: dataframe containing the missing values

    Returns
    --------
    df_ret: dataframe with fixed values
    """
    df_ret = df.copy()

    df_ret['temp'] = df_ret['temp'].interpolate(method='linear')

    return df_ret


def handle_missing_airPressure_values(df: pd.DataFrame) -> pd.DataFrame:
    """
    Handle missing air pressure values appropriately!

    Parameters
    --------
    df: dataframe containing the missing values

    Returns
    --------
    df_ret: dataframe with fixed values
    """
    df_ret = df.copy()

    df_ret['airPressure'] = df_ret['airPressure'].interpolate(method='linear')

    return df_ret


def handle_missing_windDir_values(df:pd.DataFrame) -> pd.DataFrame:
    df_ret = df.copy()

    df_ret.loc[df_ret['windBeauf'] == 0, 'windDir'] = 'C'

    df_ret['windDir'] = df_ret['windDir'].fillna(method='ffill')

    return df_ret


def handle_missing_values_weather(data: pd.DataFrame) -> pd.DataFrame:
    """
    Parameters
    --------
    data: data frame containing missing values

    Returns
    --------
    data: data frame not containing any missing values
    """

    data = handle_missing_temp_values(data)
    data = handle_missing_airPressure_values(data)
    data = handle_missing_windDir_values(data)

    return data
