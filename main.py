import os
import pandas as pd

from load_data import load_weather_data, load_traffic_data
from tests.test_load_data import test_load_weather_data
from analytics.data_analize import get_lowest_average_temp

data_path = os.path.join(os.getcwd(), "data")
weather_data_path = os.path.join(data_path, 'weather')
traffic_data_path = os.path.join(data_path, 'traffic')

weather_data, daily_weather_data = load_weather_data(weather_data_path)
test_load_weather_data(weather_data_path)

lowest_year, lowest_month = get_lowest_average_temp(weather_data)

data_traffic = load_traffic_data()

