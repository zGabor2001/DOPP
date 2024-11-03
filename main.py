import os
import pandas as pd

from load_data import *
from tests.test_load_data import *
from analytics.data_analize import *
from analytics.plots import *

data_path = os.path.join(os.getcwd(), "data")
weather_data_path = os.path.join(data_path, 'weather')
traffic_data_path = os.path.join(data_path, 'traffic')

weather_data, daily_weather_data = load_weather_data(weather_data_path)
test_load_weather_data(weather_data_path)

lowest_year, lowest_month = get_lowest_average_temp(weather_data)

data_traffic = load_traffic_data()
test_load_traffic_data()

get_day_with_most_subway_disruptions(data_traffic, disruption_type='Schadhaftes Fahrzeug')

plot_temperature(weather_data)
plot_air_pressure(weather_data)
#####plot the skyyyyy

missing_temp_df_list: list = get_data_around_missing(weather_data, 'temp')
missing_airPressure_df_list: list = get_data_around_missing(weather_data, 'airPressure')

plot_value_series(missing_temp_df_list[0], 'temp')
plot_value_series(missing_airPressure_df_list[0], 'airPressure')

missing_temp_idx = 0

plot_value_series(handle_missing_temp_values(missing_temp_df_list[missing_temp_idx]), 'temp')

plot_value_series(handle_missing_airPressure_values(missing_temp_df_list[missing_temp_idx]), 'airPressure')

fix_wind_dir = handle_missing_windDir_values(weather_data)

weather_data_complete = handle_missing_values_weather(weather_data)