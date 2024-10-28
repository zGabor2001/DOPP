import pandas as pd
import os

from load_data import load_weather_data

def test_load_weather_data(weather_data_path: str) -> None:
    weather_data, weather_data_daily = load_weather_data(weather_data_path)

    df_list = []
    for file in os.listdir(weather_data_path):
        df = pd.read_csv(os.path.join(weather_data_path, file), sep=';')
        df_list.append(df)

    df_merged: pd.DataFrame = pd.concat(df_list, ignore_index=True)

    assert len(df_merged) == len(weather_data_daily), "Daily weather data rows seem to be missing."
    assert len(df_merged) == len(weather_data) / 3, "Tri daily weather data rows seem to be missing."

    hour_cols = [col for col in df_merged.columns if col.endswith(('_7h', '_14h', '_19h'))]
    assert len(weather_data.columns) == len(df_merged[hour_cols].columns) / 3, "Tri daily data columns are incorrect."

    non_hour_cols = [col for col in df_merged.columns if '_' not in col]

    assert len(non_hour_cols) == len(weather_data_daily.columns) + 1, "Daily data columns are incorrect."

    multiindex_expected = [
        [2009, 2023],
        [1, 12],
        [1, 31],
        [0, 24]
    ]
    function_output_df_list = [weather_data, weather_data_daily]
    for df in function_output_df_list:
        for i in range(0, df.index.nlevels):
            level_values = df.index.get_level_values(i).unique()
            assert (level_values.min() >= multiindex_expected[i][0]
                    and level_values.max() <= multiindex_expected[i][0],
                    f"Value in multiindex level {i} not in expected {multiindex_expected[i]}")

    print("All tests passed")