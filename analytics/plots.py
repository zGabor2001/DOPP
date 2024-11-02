import matplotlib.pyplot as plt
import pandas as pd


def plot_temperature(df: pd.DataFrame) -> None:
    time_index = pd.to_datetime({
        'year': df.index.get_level_values('year'),
        'month': df.index.get_level_values('month'),
        'day': df.index.get_level_values('day')
    })

    plt.figure(figsize=(12, 6))

    plt.plot(time_index, df['temp'], label='Temperature (°C)', color='orange')

    plt.xlabel('Time')
    plt.ylabel('Values')
    plt.title('Temperature Over Time')
    plt.legend()

    plt.xticks(rotation=45)
    plt.tight_layout()

    plt.show()


def plot_air_pressure():
    pass


def plot_sky_coverage():
    pass
