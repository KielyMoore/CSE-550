import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from datetime import datetime, timezone, timedelta
from Plot import DataPlot


def loadData(filter):
    filePath = "./Dataset/" + datetime.strptime(
        filter["start_date"], '%m/%d/%Y').strftime('%Y%m%d') + "/" + filter["user"] + "/summary.csv"
    data = pd.read_csv(filePath)
    # Ideally data is loaded from a sever and stored locally

    columns_to_drop = []
    for column in filter["columns"]:
        if not filter["columns"][column]:
            columns_to_drop.append(column)

    # Drop unneeded columns
    data = data.drop(columns=columns_to_drop, axis=1)

    if filter["localTime"]:
        # configure panda's dataframe to create a new column called times that is equal to local time
        data["times"] = data.apply(calc_time_col, axis=1)
    else:
        # configure panda's dataframe to use create a new column called times that is equal to UTC time
        data["times"] = data["Datetime (UTC)"]

    # Drop the time related columns now that the time is stored in the times column
    data = data.drop(["Datetime (UTC)", "Timezone (minutes)",
                     "Unix Timestamp (UTC)"], axis=1)

    print(data.columns)

    print(data[["times", "Acc magnitude avg"]])
    # return the pandas data frame
    return data


def calc_time_col(row):
    return convert_utc_to_local(row["Datetime (UTC)"], row["Timezone (minutes)"])


def convert_utc_to_local(utc_string, offset_minutes):
    # Parse the input datetime string into a datetime object
    utc_dt = datetime.strptime(utc_string, '%Y-%m-%dT%H:%M:%SZ')
    # Convert the UTC datetime to a timezone-aware datetime object
    utc_dt = utc_dt.replace(tzinfo=timezone.utc)
    # Convert the timezone offset to a timedelta object
    offset = timedelta(minutes=offset_minutes)
    # Convert the datetime to the local timezone
    local_dt = utc_dt.astimezone(timezone(offset))
    # Return the local datetime as a string
    return local_dt.strftime('%Y-%m-%d %H:%M:%S')


def createDataPlotObjects(data: pd.DataFrame):
    dataPlots = []
    for col_name in data.columns:
        if col_name != "times":
            copy = data[["times", col_name]].copy()
            plotObject = DataPlot(copy, col_name)
            dataPlots.append(plotObject)

    print(dataPlots)
    return dataPlots


# Acc, Eda, Temp are the only columns that make sense to graph
# not sure how we would want to visualize the other columns

# TODO fix axis ticks. currently every timestamp is being displayed


def plot_Acc(data: pd.DataFrame):
    fig, ax = plt.subplots()
    ax.plot(data["Datetime (UTC)"], data["Acc magnitude avg"])
    plt.title("Acc Magnitude Average over time")
    plt.xlabel("Time")
    plt.ylabel("Acc Mag Avg")

    plt.show()  # automatically displays graph in seperate widow

    return fig  # May be needed for imbedding in tkinter


def plot_Eda(data: pd.DataFrame):
    fig, ax = plt.subplots()
    ax.plot(data["Datetime (UTC)"], data["Eda avg"])
    plt.title("Eda Average over time")
    plt.xlabel("Time")
    plt.ylabel("Eda Avg")
    plt.show()
    return fig


def plot_Temp(data: pd.DataFrame):
    fig, ax = plt.subplots()
    ax.plot(data["Datetime (UTC)"], data["Temp avg"])
    plt.title("Temperature Average over time")
    plt.xlabel("Time")
    plt.ylabel("temp Avg")
    plt.show()
    return fig
