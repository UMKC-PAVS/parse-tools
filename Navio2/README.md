# Parse Tools for Navio2 csv Files

In order to run the automated parser routine download all of the following:
*  `Navio2_parse.py`
*  `make_plots.py`

### Concept of Operations

Navio2 outputs log files in a csv .csv file. Csv files column names must be renamed to the standard names to be run through the make_plots scripts. The user runs the script Navio2_parse.py which invokes the make_plots function from the make_plots.py scipts.

### Notes

The parse method described here has been tested on Windows (in the Spyder IDE).

## Pre-requisites

1.  Install a working Python environment on your machine.  This can be a standalone environment or an IDE like Spyder.  Comprehensive support for getting different Python environments is not going to provided here. Installing and running scripts in Spyder seems to be the easiest and most consistent way of getting this up and running.
    1. You may also want to install pandas if not already installed (`pip install pandas`).
    2. If you are not using Spyder (Windows or Ubuntu (not tested on Mac)), you need to issue the command 'pip install pandas'.

## Directory Preparation

1.  Prepare a folder containing .csv files to be processed. The folder should be free of other extraneous files and should contain only .csv files.
2.  Download the scripts `Navio2_parse.py` and `make_plots.py` to the same directory.
3.  Your directory should now have one or more .csv files as well as two python scripts.

## Running the Scipt

1.  Run the script `Navio2_parse.py`
    1.  Open Spyder and open up the script `Navio2_parse.py` inside of the Spyder editor. Click the **run** button.
    2.  From the command line or terminal issue the command `python Navio2_parse.py`
2.  The script will step through the list of .csv files and create a directory for each .csv using the name of the .csv file as the name for the root directory.
3.  Within each directory, the script will create a directory named `FlightData`.
4.  The results.csv file will be saved in a directory inside of `FlightData` called `combined`.
5.  Plots are also now created and stored in the `Plots` directory.  Plot parameters can be changed and plots can be added omitted by modifying `make_plots.py`.