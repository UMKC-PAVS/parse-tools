#!/usr/bin/python3

'''
Created 9/1/2019
Written by:     Paul Klappa, Shawn Herrington
Purpose:        Process PX4 data logs into some kind of digestable chunk, 
                previously this script was making a bunch of plots, now it has
                been modified to do things a bit differently but the central
                idea is that we are processing a binary file into some kind of
                human readable format (csv in this case) then we are reducing
                the csv data somehow to be useful (first it was by generating
                a bunch of plots)
Changelog:
09/05/2019  Shawn Herrington
            Include code written by Paul Klappa to make lots of plot from PX4
            data
09/12/2019  Shawn Herrington
            Remove code written by Paul Klappa to make lots of plots,
            incorporate a function written by Shawn Herrington which takes all
            constituent csv files and puts them into a single csv (also
            a new directory)
09/13/2019  Shawn Herrington
            Add the other methods supplied by pyulog (params, info, messages)
            and put the output in text files.  We are not using this info
            anywhere yet but will be using in the future (especially the
            messages file)
9/21/2019   Simeon Karnes (comment edited by Shawn Herrington)
            Encapsulate calls to pyulog methods inside of an if statement for
            ease of enable/disable behavior when rerunning analysis on data
            which has already been converted
09/26/2019  Shawn Herrington
            Moved enable/disable flag to the top of the file for ease of access
07/08/2020  Thomas Cacy
            Replaced a line that changes the working dir so that it works and 
            will process all files in a dir. Added some lines so the program 
            can tell which files have been processed and ignore them. Removed 
            unecassary copying and moving of large files. Moved the creation of
            directories to the program that uses them to be consistent
08/13/2020  Put the call to make plots in this script so that it will create 
            plots even if the file has be processed. Added message to tell when
            to program has finished
            
'''

# os library used for directory handing and traversing
import os
import sys
# this will be used for calling terminal command directly from python
from subprocess import call
from combine_and_resample_px4_nogui import combine_and_resample_px4_nogui
from make_plots import make_plots
from pandas import errors
python_version = sys.version_info

if python_version.major == 3:

    from tkinter.filedialog import askdirectory
    # shows dialog box and return the path
    path = askdirectory(title='Select Folder')

elif python_version.major == 2:

    import tkFileDialog
    from tkinter import Tk
    #create root window
    root = Tk()
    # shows dialog box and return the path
    path = tkFileDialog.askdirectory(title='Select Folder')
    
    #close root window
    root.quit()
    if path == None:
        sys.exit()
else:
    
    raise Exception('something is wrong with your Python version')

os.chdir(path)

# this will get a list of all files in the current directory ending with ".ulg"
files = [f for f in os.listdir('.') if f.endswith(".ulg")]

# check if there are any files to process and exit if not
if len(files) == 0:
    sys.exit("There are no files to process in " + path)

for current_file in files:

    # set convert_ulogs and to True so we can iterate through the directory this 
    # will be changed to False if the files were already converted
    convert_ulogs = True
    
    # create the required directory name from the name of the current_file
    # we are going to remove 4 chars from the end to get rid of ".ulg"
    endlen = len(current_file)
    dir_name = current_file[:endlen-4]

    # if statement to determine if directory exists
    if(not(os.path.isdir(dir_name))):
        # if no directory exists, create the directory
        os.mkdir(dir_name)

    # create list of subdirectories so we can create them as necessary in a 
    # fancy way
    subdir_names = ["Flight_Data"]

    for current_name in subdir_names:
        # check for subdirectories and create if necessary
        if os.path.isdir(os.path.join(dir_name,current_name)):
            # check if the directory has already been polupated meaning the 
            # ulog has already been converted
            if not(len(os.listdir(os.path.join(dir_name,current_name))) == 0):
                convert_ulogs = False
        else:
            os.mkdir(os.path.join(dir_name,current_name))
            
        
    # if statement to avoid reconverting all ulog files and just plot data.
    if convert_ulogs:
                
        # invoke the ulog2csv application, send the current_file as argument
        # this should create many csv in the current directory from a single 
        # ulg file
        call(["ulog2csv",'-i',current_file,'-o',dir_name+'/'+subdir_names[0]])
        
        # call the other pyulog methods and write the output to text files
        # open with 'w' option is write only and will overwrite existing files
        call(['ulog_info',current_file], stdout=open(dir_name+'/'+subdir_names[0]+'/'+dir_name+'_info.txt','w'))
        call(['ulog_params','-i',current_file], stdout=open(dir_name+'/'+subdir_names[0]+'/'+dir_name+'_params.txt','w'))
        call(['ulog_messages',current_file], stdout=open(dir_name+'/'+subdir_names[0]+'/'+dir_name+'_messages.txt','w'))
        
    # print report on ulog files
    else: 
        print('Ulog file has already been converted for: '+dir_name)
        
    # print a progress report as the name of the file as we work
    # through the files
    print('Working on: '+current_file)


    # pass the progress report path to the combine_and_resample_px4_nogui() 
    # function if it does not already exist function, it will combine all csvs 
    # then stick them in a new directory
    if os.path.isfile(os.path.join(dir_name,subdir_names[0],'combined',dir_name+'_results.csv')):
        print('Resampling already completed for: '+ current_file)
    else:
        try:
            combine_and_resample_px4_nogui(dir_name+'/'+subdir_names[0], dir_name)
            
        except (IOError,errors.EmptyDataError) as err: 
            print('An error occured: {0}'.format(err))
     
    # call the make_plot function and pass the location of the results file
    make_plots(os.path.join(dir_name,subdir_names[0],'combined',dir_name+'_results.csv'))
    
    print('Complete.')
    
print('All files processed')