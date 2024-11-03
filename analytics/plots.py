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


def plot_air_pressure(df: pd.DataFrame) -> None:
    time_index = pd.to_datetime({
        'year': df.index.get_level_values('year'),
        'month': df.index.get_level_values('month'),
        'day': df.index.get_level_values('day')
    })

    plt.figure(figsize=(12, 6))

    plt.plot(time_index, df['airPressure'], label='Air Pressure (hPa)', color='orange')

    plt.xlabel('Time')
    plt.ylabel('Values')
    plt.title('Air Pressure Over Time')
    plt.legend()

    plt.xticks(rotation=45)
    plt.tight_layout()

    plt.show()


def plot_sky_coverage(df: pd.DataFrame) -> None:
    time_index = pd.to_datetime({
        'year': df.index.get_level_values('year'),
        'month': df.index.get_level_values('month'),
        'day': df.index.get_level_values('day')
    })

    plt.figure(figsize=(12, 6))

    plt.plot(time_index, df['airPressure'], label='Temperature (°C)', color='orange')

    plt.xlabel('Time')
    plt.ylabel('Values')
    plt.title('Air Pressure Over Time')
    plt.legend()

    plt.xticks(rotation=45)
    plt.tight_layout()

    plt.show()


def plot_value_series(df: pd.DataFrame, column: str) -> None:
    """
    Plot the values in a specified column of the given DataFrame.

    Parameters:
    df (pd.DataFrame): DataFrame containing the data to plot
    column (str): Name of the column to plot as a time series
    """
    if column not in df.columns:
        raise ValueError(f"Column '{column}' does not exist in the DataFrame")

    # Plot the time series
    plt.figure(figsize=(10, 6))
    plt.plot(df.index, df[column], label=column, color="b", marker="o")

    # Label the axes and the plot
    plt.xlabel("Date")
    plt.ylabel("Value")
    plt.title(f"Time Series of {column}")
    plt.legend()
    plt.grid(True)
    plt.show()
