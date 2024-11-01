import pandas as pd
def get_lowest_average_temp(data_frame: pd.DataFrame):
    year = 0
    month = 0

    monthly_avg_temp: pd.DataFrame = data_frame.groupby([data_frame.index.get_level_values('year'),
                                   data_frame.index.get_level_values('month')])['temp'].mean()

    lowest_avg_temp = monthly_avg_temp.idxmin()

    year = lowest_avg_temp[0]
    month = lowest_avg_temp[1]

    return year, month