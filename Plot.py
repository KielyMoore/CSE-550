import pandas as pd
import matplotlib.pyplot as plt


class Dataset:
    def __init__(self, df, n):
        self.times = df['times']
        self.values = df['values']
        self.name = n

    def plot_data(self):
        # create plot
        plt.rcParams.update({'font.size': 8})
        plt.plot(self.times, self.values, color='maroon')

        # label graph
        plt.xlabel("Time")
        plt.ylabel(self.name)
        plt.title("name")

        # format graph
        plt.xticks(rotation=30)
        # plt.tight_layout()
        plt.subplots_adjust(bottom=0.3)

        plt.show()


df = pd.DataFrame({
    'times': ['2020-01-17T23:48:00Z', '2020-01-17T23:49:00Z', '2020-01-17T23:50:00Z', '2020-01-17T23:51:00Z', '2020-01-17T23:52:00Z', '2020-01-17T23:53:00Z', '2020-01-17T23:54:00Z', '2020-01-17T23:55:00Z', '2020-01-17T23:56:00Z', '2020-01-17T23:57:00Z'],
    'values': [30.155257, 29.9799, 29.713417, 29.416833, 29.2752, 29.4671, 29.84755, 30.069133, 30.031567, 30.0993]

})

thingy = Dataset(df, 'NAME')
thingy.plot_data()

