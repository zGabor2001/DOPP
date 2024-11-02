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
        hour = int(''.join([char for char in hour_tag if char.isdigit()]))
        dfs_by_suffix[hour_tag]['date'] = (dfs_by_suffix[hour_tag]['date'].dt.floor('D') +
                                           pd.Timedelta(hours=hour))

        non_hour_cols = [col.split('_')[0] for col in dfs_by_suffix[hour_tag].columns]
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
            names=['year', 'month', 'day', 'hour']
        )

        df.set_index(multi_index, inplace=True)
        df.drop(columns=['date'], inplace=True)
        df.sort_index(inplace=True)

    weather_data_daily: pd.DataFrame = weather_data_daily.droplevel(level=-1)

    return weather_data, weather_data_daily


def load_traffic_data() -> pd.DataFrame:
    """
    Load the traffic data from the files into a pndas dataframe

    Returns
    --------
    traffic_data: data frame containing the traffic data
    """

    traffic_data_path = "C:\\DS\\repos\\DOPP\\data\\traffic\\traffic_disruptions.csv"

    traffic: pd.DataFrame = pd.read_csv(traffic_data_path, sep=';')
    traffic['date'] = pd.to_datetime(traffic['Start']).dt.floor('D')

    multi_index: pd.MultiIndex = pd.MultiIndex.from_arrays(
        [traffic['date'].dt.year,
         traffic['date'].dt.month,
         traffic['date'].dt.day],
        names=['year', 'month', 'day']
    )

    traffic.set_index(multi_index, inplace=True)
    traffic.sort_index(inplace=True)

    for col in ['Titel', 'Beschreibung', 'Linie(n)']:
        traffic[col] = traffic[col].astype(str)

    for col in ['Start', 'Verkehrsaufnahme', 'Ende', 'date']:
        traffic[col] = pd.to_datetime(traffic[col])

    #traffic = traffic[traffic['Titel'].str.contains('Badner Bahn')]

    traffic['disruption'] = traffic['Titel'].str.replace(r'Badner Bahn:|,', '', regex=True)
    traffic['disruption'] = traffic['disruption'].str.extract(r'(\s\S{4}.*)')
    traffic['disruption'] = traffic['disruption'].str.strip()

    linie_regex_map = {
        'bus': '\d{2}[AB]',
        'subway': 'U[1-6](?![Zz])',
        'tram': '^(D|O|U2[Zz]|VRT|WLB|Badner Bahn|\b\d{1,2}\b)(?![A-Za-z])'
    }

    for key in linie_regex_map.keys():
        traffic[key] = traffic['Linie(n)'].str.contains(fr'{linie_regex_map[key]}')

    traffic['duration'] = traffic['Ende'] - traffic['Start']

    traffic = traffic[['disruption', 'bus', 'subway', 'tram', 'duration']]

    map_similar_entries = {'Fahrtbehinderung': 'Fahrbehinderung',
                           'Verspätungen': 'Verspätung',
                           'Schadhaftes Fahrzeug Verspätungen': 'Schadhaftes Fahrzeug',
                           'Regenbogenparade Verspätungen': 'Veranstaltung',
                           'Verkehrsbedingte Verspätung Verspätungen': 'Verkehrsbedingte Verspätungen',
                           'Verkehrsbedingt Verspätungen': 'Verkehrsbedingte Verspätungen',
                           'Verkehrsbedingt': 'Verkehrsbedingte Verspätungen',
                           'Verkehrsstörung Verspätungen': 'Verkehrsbedingte Verspätungen',
                           'Fremder Verkehrsunfall': 'Verkehrsunfall',
                           }
    traffic['disruption'] = traffic['disruption'].replace(map_similar_entries)

    return traffic
