import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime
from ipywidgets import widgets
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
        # create dropdown widget for graph type
        self.graphTypes = ['line', 'scatter', 'bar', 'histogram', 'box']

        # define a dropdown widget for selecting the graph type
        self.graph_type_dropdown = widgets.Dropdown(
            options=self.graphTypes,
            value=self.graphType,
            description='Graph Type:',
            disabled=False
        )
        self.graph_type_dropdown.observe(self.graph_type_dropdown_changed)

    # display the dropdown widget and plot the data
    def display(self):
        display(self.graph_type_dropdown)
        self.get_plot().show()

    def graph_type_dropdown_changed(self, change):
        if change['type'] == 'change' and change['name'] == 'value':
            self.graphType = change['new']
    def get_plot(self):
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

        # update the graph type based on the dropdown selection
        def update_graph_type(*args):
            self.graphType = graph_type_var.get()
            self.get_plot()

        graph_type_var.trace('w', update_graph_type)

        # show the plot and return the plot object
        plt.show()
        return plt
        
        # observe changes in the dropdown
        self.graph_type_dropdown.observe(self.handle_graph_type_change, names='value')
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


# Testing stuffs
# df = pd.DataFrame({
#     'times': ['2020-01-17T23:48:00Z', '2020-01-17T23:49:00Z', '2020-01-17T23:50:00Z', '2020-01-17T23:51:00Z', '2020-01-17T23:52:00Z', '2020-01-17T23:53:00Z', '2020-01-17T23:54:00Z', '2020-01-17T23:55:00Z', '2020-01-17T23:56:00Z', '2020-01-17T23:57:00Z'],
#     'Temp avg': [30.155257, 29.9799, 29.713417, 29.416833, 29.2752, 29.4671, 29.84755, 30.069133, 30.031567, 30.0993]
# })

# plotObject = DataPlot(df, 'Temp avg')
# plotObject.get_plot().show()
