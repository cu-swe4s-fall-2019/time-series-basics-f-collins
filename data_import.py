import csv
import dateutil.parser
from os import listdir
from os.path import isfile, join
import argparse
import datetime


class ImportData:
    def __init__(self, data_csv):
        # open file, create a reader from csv.DictReader,
        # and read input times and values
        self._time = []
        self._value = []
        self._roundtime = []
        self._roundvalue = []

        if data_csv.split('_') == "activity" or data_csv.split('_') \
                == "bolus" or data_csv.split('_') == "meal":
            self.sumvals = 1
        else:
            self.sumvals = 0

        with open(data_csv, "r") as data_file:
            reader = csv.DictReader(data_file)
            for row in reader:
                try:
                    self._time.append(dateutil.parser.parse(row["time"]))
                except ValueError:
                    continue
                if row["value"] == "low":
                    self._value.append(40)
                    print("Replacing low with 40.")
                elif row["value"] == "high":
                    self._value.append(300)
                    print("Replacing high with 300.")
                else:
                    self._value.append(row["value"])
            data_file.close()

    def linear_search_value(self, key_time):
        # return list of value(s) associated with key_time
        # if none, return -1 and error message
        out = []
        for i in range(len(self._roundtime)):
            if self._roundtime[i] == key_time:
                out.append(self._roundvalue[i])

        if len(out) == 0:
            return -1
        return out

    def binary_search_value(self, key_time):
        pass
        # optional extra credit
        # return list of value(s) associated with key_time
        # if none, return -1 and error message


def roundTimeArray(obj, res):
    # Inputs: obj (ImportData Object) and res (rounding resoultion)
    # objective:
    # create a list of datetime entries and associated values
    # with the times rounded to the nearest rounding resolution (res)
    # ensure no duplicated times
    # handle duplicated values for a single timestamp based on instructions in
    # the assignmenj
    # return: iterable zip object of the two lists
    # note: you can create additional variables to help with this task
    # which are not returned
    timedict = {}
    for (times, values) in zip(obj._time, obj._value):
        dtime = datetime.timedelta(minutes=(times.minute % res))
        resmin = datetime.timedelta(minutes=res)
        if (times.minute % res) <= res / 2:
            obj._roundtime.append(times - dtime)
        else:
            obj._roundtime.append(times + resmin - dtime)
        try:
            obj._roundvalue.append(float(values))
        except ValueError:
            obj._roundvalue.append(0)

    for (times, values) in zip(obj._roundtime, obj._roundvalue):
        currenttime = times.strftime("%m/%d/%Y %H:%M")
        if currenttime not in timedict:
            timedict[currenttime] = obj.linear_search_value(times)

    _newtimes = []
    _newvalues = []
    for key in timedict:
        _newtimes.append(key)
        if obj.sumvals == 1:
            _newvalues.append(sum(timedict[key]))
        else:
            _newvalues.append(sum(timedict[key])/len(timedict[key]))

    return zip(_newtimes, _newvalues)


def printArray(data_list, annotation_list, base_name, key_file):
    # combine and print on the key_file
    key_index = -1
    for index in range(len(annotation_list)):
        if annotation_list[index] == key_file.split("/")[1]:
            key_index = index
            break

    if key_index == -1:
        raise(ValueError("keyfile not in file list."))

    with open(base_name + ".csv", mode="wt") as outfile:
        csvfile = csv.writer(outfile, delimiter=",")
        header = []
        header.append("time")
        header.append(key_file)
        for name in annotation_list:
            if name != key_file:
                header.append(name)
        csvfile.writerow(header)

        for entry in data_list[key_index]:
            currentrow = [entry[0], entry[1]]
            for zipdata in data_list:
                if zipdata == data_list[key_index]:
                    continue
                timefound = 0
                for pair in zipdata:
                    if pair[0] == entry[0]:
                        currentrow.append(pair[1])
                        timefound = 1
                if timefound == 0:
                    currentrow.append(0)
            csvfile.writerow(currentrow)


if __name__ == '__main__':

    # adding arguments
    parser = argparse.ArgumentParser(description='A class to import, combine, \
            and print data from a folder.', prog='dataImport')

    parser.add_argument('--folder_name', type=str, help='Name of the folder')

    parser.add_argument('--output_file', type=str, help='Name of Output file')

    parser.add_argument('--sort_key', type=str, help='File to sort on')

    parser.add_argument('--number_of_files', type=int,
                        help="Number of Files", required=False)

    args = parser.parse_args()

    # pull all the folders in the file
    files_lst = []  # list the folders

    for filename in listdir(args.folder_name):
        if filename.split(".")[-1] == "csv":
            files_lst.append(filename)

    # import all the files into a list of ImportData objects (in a loop!)
    data_lst = []

    for csvfile in files_lst:
        data_lst.append(ImportData(args.folder_name + "/" + csvfile))

    # create two new lists of zip objects
    # do this in a loop, where you loop through the data_lst
    data_5 = []  # a list with time rounded to 5min
    data_15 = []  # a list with time rounded to 15min

    for dataitem in data_lst:
        data_5.append(roundTimeArray(dataitem, 5))
        data_15.append(roundTimeArray(dataitem, 15))

    # print to a csv file
    printArray(data_5, files_lst, args.output_file+'_5', args.sort_key)
    printArray(data_15, files_lst, args.output_file+'_15', args.sort_key)
