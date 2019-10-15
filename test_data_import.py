import unittest
from data_import import ImportData
import datetime
import csv
import random
import os

class TestImportData(unittest.TestCase):
    def test_DataImport_readfile(self):
        data_times = []
        data_values = []
        with open("test_file.csv", mode="w") as test_data:
            data_writer = csv.writer(test_data, delimiter = ",")
            data_writer.writerow(["time", "value"])
            idate = datetime.datetime.now()
            for item in range(9):
                idatestr = idate.strftime("%m/%d/%Y %H:%M")
                randval = str(random.randint(0, 10000))
                data_writer.writerow([idatestr, randval])
                data_times.append(idatestr)
                data_values.append(randval)
                idate = idate + datetime.timedelta(hours=1)
            test_data.close()
        
        testdata = ImportData("test_file.csv")
        os.remove("test_file.csv")
        str_times = [val.strftime("%m/%d/%Y %H:%M") for val in testdata._time]
        self.assertEqual(str_times, data_times)
        self.assertEqual(testdata._value, data_values)

    def test_DataImport_linear_search_value(self):
        data_times = []
        data_values = []
        key_index = random.randint(0,9)
        key_time = None
        with open("test_file.csv", mode="w") as test_data:
            data_writer = csv.writer(test_data, delimiter = ",")
            data_writer.writerow(["time", "value"])
            idate = datetime.datetime.now()
            for item in range(9):
                idatestr = idate.strftime("%m/%d/%Y %H:%M")
                randval = str(random.randint(0, 10000))
                data_writer.writerow([idatestr, randval])
                data_times.append(idatestr)
                data_values.append(randval)
                idate = idate + datetime.timedelta(hours=1)
            test_data.close()
        
        testdata = ImportData("test_file.csv")
        key_time = testdata._time[key_index]
        os.remove("test_file.csv")
        self.assertEqual(testdata.linear_search_value(key_time), [data_values[key_index]])

if __name__ == "__main__":
        unittest.main()
