import pandas as pd
import matplotlib.pyplot as plt
import statistics


class DataPlot:
    def __init__(self, df, propertyName):
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

    def changeGraphType(self, new_graph_type):
        self.graphType = new_graph_type

    def filterData(self, start_time, end_time):
        print(
            "set time and data arrays by filtering down the initial Panda's dataframe (df)")
        filtered_df = self.filter_dataframe_by_time(
            self.df, start_time, end_time)
        self.times = filtered_df["times"]
        self.values = filtered_df["values"]

    def filter_dataframe_by_time(df: pd.DataFrame, start_time, end_time):
        df["times"] = pd.to_datetime(df["times"], utc=True)
        df["times"] = pd.to_datetime(df["times"])
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


# df = pd.DataFrame({
#     'times': ['2020-01-17T23:48:00Z', '2020-01-17T23:49:00Z', '2020-01-17T23:50:00Z', '2020-01-17T23:51:00Z', '2020-01-17T23:52:00Z', '2020-01-17T23:53:00Z', '2020-01-17T23:54:00Z', '2020-01-17T23:55:00Z', '2020-01-17T23:56:00Z', '2020-01-17T23:57:00Z'],
#     'values': [30.155257, 29.9799, 29.713417, 29.416833, 29.2752, 29.4671, 29.84755, 30.069133, 30.031567, 30.0993]
# })

# plotObject = DataPlot(df, 'Temp avg')
# plotObject.plot_data()
