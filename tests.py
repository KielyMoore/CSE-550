import unittest
import pandas as pd
from Plot import DataPlot

class TestDataPlot (unittest.TestCase):
    
    def setUp(self):
        self.time_list = ['2020-01-17T23:48:00Z', '2020-01-17T23:49:00Z', '2020-01-17T23:50:00Z', '2020-01-17T23:51:00Z', '2020-01-17T23:52:00Z', '2020-01-17T23:53:00Z', '2020-01-17T23:54:00Z', '2020-01-17T23:55:00Z', '2020-01-17T23:56:00Z', '2020-01-17T23:57:00Z']
        self.temp_list = [30.155257, 29.9799, 29.713417, 29.416833, 29.2752, 29.4671, 29.84755, 30.069133, 30.031567, 30.0993]
        count, sum = 0, 0
        for t in self.temp_list:
            sum += t
            count += 1
        self.avg = sum / count
        self.df = pd.DataFrame({
            'times': self.time_list,
            'Temp avg': self.temp_list
        })
    
    def test_init(self):
        plot = DataPlot(self.df, 'Temp avg')
        self.assertIsInstance(plot, DataPlot)
        self.assertIs(self.df, plot.df)
        self.assertCountEqual(self.time_list, plot.times)
        self.assertCountEqual(self.temp_list, plot.values)
        self.assertEqual("line", plot.graphType)
        self.assertEqual("Temp avg", plot.propertyName)

    def test_get_plot(self):
        plot = DataPlot(self.df, 'Temp avg')
        self.assertIsNotNone(plot.get_plot())

    def test_changeGraphType(self):
        plot = DataPlot(self.df, 'Temp avg')
        plot.changeGraphType("scatter")
        self.assertEqual("scatter", plot.graphType)
        plot.changeGraphType("bar")
        self.assertEqual("bar", plot.graphType)
        plot.changeGraphType("histogram")
        self.assertEqual("histogram", plot.graphType)
        plot.changeGraphType("box")
        self.assertEqual("box", plot.graphType)
        plot.changeGraphType("line")
        self.assertEqual("line", plot.graphType)

    def test_calcluateAverage(self):
        plot = DataPlot(self.df, 'Temp avg')
        self.assertEqual(self.avg, plot.calculateAverage())
    
    def test_calculateStandardDev(self):
        plot = DataPlot(self.df, 'Temp avg')
        self.assertAlmostEqual(0.319150708, plot.calculateStandardDev())

    def test_calculateMedian(self):
        plot = DataPlot(self.df, 'Temp avg')
        self.assertAlmostEqual(29.913725, plot.calculateMedian())
    
    def test_findMaximum(self):
        plot = DataPlot(self.df, 'Temp avg')
        self.assertEqual(30.155257, plot.findMaximum())
    
    def test_findMinimum(self):
        plot = DataPlot(self.df, 'Temp avg')
        self.assertEqual(29.2752, plot.findMinimum())


if __name__=="__main__":
    unittest.main()