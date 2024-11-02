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
