import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from datetime import datetime

def loadData(filter):
    filePath = filter["file_label"] +"/"+ datetime.strptime(filter["start_date"], '%m/%d/%Y').strftime('%Y%m%d') +"/"+ filter["user"] + "/summary.csv"
    data = pd.read_csv(filePath)
    # Ideally data is loaded from a sever and stored locally
    
    columns_to_drop = []
    for column in filter["columns"]:
        if not filter["columns"][column]:
            columns_to_drop.append(column)

    # Drop unneeded columns
    data = data.drop(columns=columns_to_drop, axis=1)
    return data


# Acc, Eda, Temp are the only columns that make sense to graph
# not sure how we would want to visualize the other columns

# TODO fix axis ticks. currently every timestamp is being displayed

def plot_Acc(data: pd.DataFrame):
    fig, ax = plt.subplots()
    ax.plot(data["Datetime (UTC)"], data["Acc magnitude avg"])
    plt.title("Acc Magnitude Average over time")
    plt.xlabel("Time")
    plt.ylabel("Acc Mag Avg")

    plt.show() # automatically displays graph in seperate widow
    
    return fig # May be needed for imbedding in tkinter

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
