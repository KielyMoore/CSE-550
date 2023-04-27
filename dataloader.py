import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from datetime import datetime, timezone, timedelta
from Plot import DataPlot


def loadData(filter):
    # Ideally data is loaded from a sever and stored locally
    filePath = "./Dataset/" + datetime.strptime(
        filter["start_date"], '%m/%d/%Y').strftime('%Y%m%d') + "/" + filter["user"] + "/summary.csv"
    data = pd.read_csv(filePath)

    # configure a new "times" column for the dataframe that will represent the timestamp values
    if filter["localTime"]:
        # fill the "times" column with calculated "Local Time" timestamps
        data["times"] = data.apply(calc_time_col, axis=1)
    else:
        # fill the "times" column with "UTC" timestamps
        data["times"] = data["Datetime (UTC)"]

    # Drop the time related columns now that the time is stored in the "times" column
    columns_to_drop = ["Datetime (UTC)", "Timezone (minutes)",
                       "Unix Timestamp (UTC)"]

    for column in filter["columns"]:
        if not filter["columns"][column]:
            columns_to_drop.append(column)

    # Drop unneeded columns
    data = data.drop(columns=columns_to_drop, axis=1)

    print(data.columns)

    print(data[["times", "Acc magnitude avg"]])
    # return the pandas data frame
    return data


# function used to fill each "time" column row using the corresponding "Datetime (UTC)" and "Timezone (minutes)" row
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


# function used to take the panda's dataframe and construct an array of DataPlot objects (could also be an object)
def createDataPlotObjects(data: pd.DataFrame):
    dataPlots = []
    for col_name in data.columns:
        if col_name != "times":
            copy = data[["times", col_name]].copy()
            plotObject = DataPlot(copy, col_name)
            dataPlots.append(plotObject)

    print(dataPlots)
    return dataPlots


# DEPRECATED For Now
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


#class for the options of graph types to use
class Graph:
       def __init__(self, x_data, y_data, graph_type = 'line'):
            self.x_data = x_data
            self.y_data = y_data
            self.graph_type = graph_type
       
       def plot(self):
            if self.graph_type == 'line':
                plt.plot(self.x_data, self.y_data)
            elif self.graph_type == 'scatter':
                plt.scatter(self.x_data, self.y_data)
            elif self.graph_type == 'bar':
                plt.bar(self.x_data, self.y_data)
            elif self.graph_type == 'histogram':
                plt.hist(self.x_data, self.y_data)
            elif self.graph_type == 'box':
                plt.boxplot(self.x_data, self.y_data)
            else:
                raise ValueError('Invalid graph type')
                
       def set_graph_type(self, graph_type):
           self.graph_type = graph_type
