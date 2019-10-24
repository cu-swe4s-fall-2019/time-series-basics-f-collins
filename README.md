# time-series-basics

This script allows one to input a number of sets of data in the csv format with a time and value column, round the times to a certain number of minutes, and output a csv file with a key set of data alongside the other datasets input with the times matched together.

# Usage

```
usage: dataImport [-h] [--folder_name FOLDER_NAME] [--output_file OUTPUT_FILE]
                  [--sort_key SORT_KEY] [--number_of_files NUMBER_OF_FILES]

A class to import, combine, and print data from a folder.

optional arguments:
  -h, --help            show this help message and exit
  --folder_name FOLDER_NAME
                        Name of the folder
  --output_file OUTPUT_FILE
                        Name of Output file
  --sort_key SORT_KEY   File to sort on
  --number_of_files NUMBER_OF_FILES
                        Number of Files
```

# Installation

Python 3 is required, and so are the dateutil, os, csv, datetime, and argparse modules.
