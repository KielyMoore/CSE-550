import unittest
import pandas as pd
from Plot import DataPlot
from datetime import datetime
import ui
import dataloader

class date:
    def __init__(self, date):
        self.date = date
    def get(self):
        return self.date

class user:
    def __init__(self, name):
        self.name = name
    def get(self):
        return self.name


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

class TestUI (unittest.TestCase):
    def setUp(self):
        ui.datasetPath = "./TestData/"
    
    def test_getDatesFromFolder(self):
        self.assertListEqual(["01/01/2023", "01/02/2023","01/03/2023","01/04/2023"], ui.get_dates_from_folder())
    
    def test_validateDates(self):
        ui.start_date = date("01/18/2020")
        ui.end_date = date("01/20/2020")
        self.assertEqual("", ui.validateDates())
        ui.start_date = date("01/21/2020")
        self.assertIsNot("", ui.validateDates())

    def test_getUsersWithinTimePeriod(self):
        self.assertListEqual(["310", "311", "312"], ui.get_users_within_time_period("01/01/2023", "01/02/2023"))
    
    def test_validateUserWithinDateRange(self):
        ui.start_date = date("01/01/2023")
        ui.end_date = date("01/02/2023")
        ui.user = user("310")
        self.assertTrue(ui.validateUserWithinDateRange())
        ui.user = user("313")
        self.assertFalse(ui.validateUserWithinDateRange())

class TestDataLoader(unittest.TestCase):
    
    def setUp(self):
        self.filter = {
            "start_date": "01/01/2023",
            "end_date": "01/02/2023",
            "user": "310",
            "localTime": False,
            "columns": {
                "Acc magnitude avg": True,
                "Eda avg": True,
                "Temp avg": True,
                "Movement intensity": False,
                "Steps count": False,
                "Rest": False,
                "On Wrist": False
            }
        }
        self.data = pd.DataFrame()
        df1 = pd.read_csv("./TestData/20230101/310/summary.csv")
        df2 = pd.read_csv("./TestData/20230102/310/summary.csv")
        self.data = pd.concat([df1, df2], ignore_index=True)
        self.data["times"] = self.data["Datetime (UTC)"]
        drop = [
            "Datetime (UTC)", 
            "Timezone (minutes)", 
            "Unix Timestamp (UTC)",
            "Movement intensity",
            "Steps count",
            "Rest",
            "On Wrist"
            ]
        self.data.drop(columns=drop, inplace=True)

    def test_loadData(self):
        # Need more test cases for this function
        loaded = dataloader.loadData(self.filter, "./TestData/")
        self.assertIsInstance(loaded, pd.DataFrame)
        self.assertListEqual(self.data.columns.to_list(), loaded.columns.to_list())
        self.assertEqual(self.data.shape[0], loaded.shape[0])
        #self.assertIs(self.data, loaded)

    def test_convertUtcToLocal(self):
        utc = "2020-01-17T08:40:00Z"
        self.assertEqual("2020-01-17 04:40:00", dataloader.convert_utc_to_local(utc, -4*60))

    def test_createDataPlotObjects(self):
        validatePlots = [ 
            DataPlot(self.data[["times", "Acc magnitude avg"]], "Acc magnitude avg"),
            DataPlot(self.data[["times", "Eda avg"]], "Eda avg"),
            DataPlot(self.data[["times", "Temp avg"]], "Temp avg")
        ]
        testPlots = dataloader.createDataPlotObjects(self.data)
        self.assertEqual(validatePlots[0].calculateAverage(), testPlots[0].calculateAverage())
        self.assertEqual(validatePlots[1].calculateAverage(), testPlots[1].calculateAverage())
        self.assertEqual(validatePlots[2].calculateAverage(), testPlots[2].calculateAverage())

if __name__=="__main__":
    unittest.main()