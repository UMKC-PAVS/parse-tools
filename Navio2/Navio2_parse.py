# -*- coding: utf-8 -*-
"""
Written:        Thomas Cacy
Date:           07/10/2020
Purpose:        To take a Navio2 csv and spit out only the columns we want and 
                plot data
"""

# os library used for directory handing and traversing
import os
import sys
import pandas as pd
from make_plots import make_plots

# determine what version of python we are using to determine what command to issue
python_version = sys.version_info

# use the gui to get the directory name
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
    
    # check if th user clicked 'cancel'
    if path == None:
        sys.exit()
else:
    
    raise Exception('something is wrong with your Python version')

# change to the directory where we will be processing the files
os.chdir(path)

# list of new headers
new_headers = ['micro_seconds','Channels_in.0','Channels_in.1','Channels_in.2','Channels_in.3','Channels_in.4','Channels_in.5','Voltage','Att.roll','Att.pitch','Att.yaw','Accel.x','Accel.y',
               'Accel.z','Gyro.x','Gyro.y','Gyro.z','Mag.x','Mag.y','Mag.z',
               'GPS.lat','GPS.lon','GPS.alt','GPS.hdop','GPS.vdop']

# list that contains every column we want to keep
needed_headers = ['microseconds_since_start','rc0_scaled','rc1_scaled','rc2_scaled','rc3_scaled','rc4_scaled','rc5_scaled','adc_array2','roll_mpu_mahony',
                  'pitch_mpu_mahony','yaw_mpu_mahony','a_mpu[0]','a_mpu[1]',
                  'a_mpu[2]','g_mpu[0]','g_mpu[1]','g_mpu[2]','m_mpu[0]',
                  'm_mpu[1]','m_mpu[2]','lat','lng','alt_ellipsoid',
                  'horz_accuracy','vert_accuracy']

# this will get a list of all files in the current directory ending with ".ulg"
files = [f for f in os.listdir('.') if f.endswith(".csv")]

# check if there are any files to process and exit if not
if len(files) == 0:
    sys.exit("There are no files to process in "+path)

# for loop to iterate through the directory
for current_filename in files:

    # set change_names to True so we can iterate through the directory this 
    # will be changed to False if the files were already converted
    DoChangeNames = False
    
    # variable to control of the files will be processed
    DoMakePlots = False
    
    # create the required directory name from the name of the current_file
    # we are going to remove 4 chars from the end to get rid of ".csv"
    endlen = len(current_filename)
    dir_name = current_filename[:endlen-4]
    
    # if statement to determine if directory exists
    if(not(os.path.isdir(dir_name))):
        # if no directory exists, create the directory
        os.mkdir(dir_name)

    # check for subdirectories and create if necessary
    if os.path.isdir(os.path.join(dir_name,'Flight_Data')):
        
        # check if folder exists and create if needed, this avoid the script trying
        # to read it's own results.csv as one of the constituent files if we run
        # this script on a directory where it has been run at least once previously
        if os.path.exists(os.path.join(dir_name,'Flight_Data','combined')):
            
            # check if the directory has already been polupated meaning the 
            # file has already been processed
            if len(os.listdir(os.path.join(dir_name,'Flight_Data','combined'))) == 0:
                DoChangeNames = True
                
        else: 
            os.mkdir(os.path.join(dir_name,'Flight_Data','combined'))
            DoChangeNames = True
    
    else:
        os.mkdir(os.path.join(dir_name,'Flight_Data'))
        os.mkdir(os.path.join(dir_name,'Flight_Data','combined'))
        DoChangeNames = True
        
    # if statement to determine if the file needs plotting
    if os.path.exists(os.path.join(dir_name,'Plots')):
        
        # check if the directory has already been polupated meaning the 
        # file has already been plotted
        if len(os.listdir(os.path.join(os.path.join(dir_name,'Plots')))) == 0:
            DoMakePlots = True
    else:
        DoMakePlots = True
        
    # print a progress report as the name of the file as we work
    # through the files
    print('Working on '+current_filename)
    
    # process the files if they need processing
    if DoChangeNames:
        
        # try block to handle errors in reading the files
        try:
            # this is the important read, read in the data we care about, the index
            # is stored in column 0, the header is stored in row 0, pandas will 
            # name columns automatically for us using the header row
            df = pd.read_csv(path+'/'+current_filename, index_col=0, header=0)
            
            # get list of columns
            headers = df.columns
            
            # change the list to just have the columns we want
            reject_column_list = [header for header in headers if header not in needed_headers]
    
            # remove the headers we do not want
            df = df.drop(columns = reject_column_list)
            
            # rename the columns to the right names
            df.columns = new_headers
            
            # set the micro second column to the index
            df.set_index('micro_seconds', inplace=True)
        
            # change to seconds from micro seconds
            df.index = df.index/10**6
            
            # write the result, we want to write the index column, we want to label the
            # index column, feel free to change the name
            df.to_csv(path_or_buf=(dir_name+'/Flight_Data/combined/'+dir_name+'_results.csv'),index=True,index_label='Time')
            
            # print report of files processed
            print('File converted: '+current_filename)
            
        # except block to handling input/output errors and empty file errors 
        # when tryin to read columns
        except (IOError,pd.errors.EmptyDataError) as err:
            
            # print a message and the error
            print('An Error occured. Error is {0}'.format(err))
            
    else:
        # print a report
        print(current_filename+' already processed')
    
    # if the plots need to be created, create them    
    if DoMakePlots:
        
        # try block to handle errors saving the files
        try:
            # call the make_plots function and pass it the right file
            make_plots(dir_name+'/Flight_Data/combined/'+dir_name+'_results.csv')
            
        # except block to handle the errors writing the file
        except IOError as err:
            print('An Error occured. Error is {0}'.format(err))
    else:
        print('Plots already plotted for '+current_filename)

    print('Complete.')