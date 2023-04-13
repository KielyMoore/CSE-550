import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime
import statistics


class DataPlot:
    # the df property is the original panda's dataframe for a data property, this property is ReadOnly
    # the times and values properties are used when filtering the time and data columns within the data frame, they are also used when plotting the data and performing statistics
    def __init__(self, df: pd.DataFrame, propertyName: str):
        self.df = df
        self.times = df['times']
        self.values = df[propertyName]
        self.graphType = "line"
        self.propertyName = propertyName

    def get_plot(self):
        # create plot
        plt.rcParams.update({'font.size': 8})

        if self.graphType == 'line':
            plt.plot(self.times, self.values, color='maroon')
        elif self.graphType == 'scatter':
            plt.scatter(self.times, self.values)
        elif self.graphType == 'bar':
            plt.bar(self.times, self.values)
        elif self.graphType == 'histogram':
            plt.hist(self.values)
        elif self.graphType == "box":
            plt.boxplot(self.values)

        # label graph
        plt.xlabel("Time")
        plt.ylabel(self.propertyName)
        plt.title(self.propertyName + " Plot")

        # format graph
        plt.xticks(rotation=30)
        # plt.tight_layout()
        plt.subplots_adjust(bottom=0.3)
        # return the plot itself, so that it can be placed its own widget
        return plt

    def changeGraphType(self, new_graph_type: str):
        self.graphType = new_graph_type

    def filterData(self, start_time: str, end_time: str):
        start_time_datetime = datetime.strptime(
            start_time, '%Y-%m-%dT%H:%M:%SZ')
        end_time_datetime = datetime.strptime(end_time, '%Y-%m-%dT%H:%M:%SZ')
        copyDF = self.df.copy()
        filtered_df = self.filter_dataframe_by_time(
            copyDF, start_time_datetime, end_time_datetime)
        self.times = filtered_df["times"]
        self.values = filtered_df[self.propertyName]

    def filter_dataframe_by_time(df: pd.DataFrame, start_time, end_time):
        df["times"] = pd.to_datetime(df["times"], utc=True)
        filtered_df = df.loc[(df["times"] >= start_time)
                             & (df["times"] <= end_time)]
        return filtered_df

    def calculateAverage(self):
        return float(sum(self.values)) / float(len(self.values))

    def calculateStandardDev(self):
        statistics.stdev(self.values)

    def calculateMedian(self):
        return statistics.median(self.values)

    def findMaximum(self):
        return max(self.values)

    def findMinimum(self):
        return min(self.values)

