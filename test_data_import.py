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
                randval = random.randint(0, 10000)
                data_writer.writerow([idatestr, randval])
                data_times.append(idatestr)
                data_values.append(randval)
                idate = idate + datetime.timedelta(hours=1)
        
        testdata = ImportData("test_file.csv")
        os.remove("test_file.csv")
        self.assertEqual(testdata._time, data_times)
        self.assertEqual(testdata._value, data_values)


if __name__ == "__main__":
        unittest.main()
