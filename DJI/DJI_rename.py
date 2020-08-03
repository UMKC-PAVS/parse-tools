# -*- coding: utf-8 -*-
'''
Written: Thomas Cacy, Harrison Terry
Date: 08/03/2020
Purpose: Read and process a .csv file after it has been converted from a .DAT 
         file in a way that allows it to be plotted using make_plots.py under 
         the unified parsing program

'''
import pandas as pd
import sys
import os
from make_plots import make_plots

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

# change to the right directory so look for all the files
os.chdir(path)

# this will get a list of all files in the current directory ending with ".csv"
files = [f for f in os.listdir('.') if f.endswith(".csv")]

# check if there are any files to procees
if len(files) == 0:
    sys.exit('There were no files to process in '+path)

# a list to hold columns we do not want
columns_to_keep = ['IMU_ATTI(0):roll:C','IMU_ATTI(0):pitch:C','IMU_ATTI(0):yaw:C','IMU_ATTI(0):accelX','IMU_ATTI(0):accelY','IMU_ATTI(0):accelZ','IMU_ATTI(0):gyroX','IMU_ATTI(0):gyroY','IMU_ATTI(0):gyroZ','IMU_ATTI(0):magX','IMU_ATTI(0):magY','IMU_ATTI(0):magZ','GPS:Long','GPS:Lat','GPS:heightMSL','GPS:pDOP','GPS:hDOP','Controller:ctrl_pitch:D','Controller:ctrl_roll:D','Controller:ctrl_yaw:D','Controller:ctrl_thr:D','Controller:ctrl_mode','RC:failSafe','RC_Info:sigStrength:C','BatteryInfo:Vol:D']

# list of column's new names   
new_headers = ['Att.roll','Att.pitch','Att.yaw','Accel.x','Accel.y','Accel.z','Gyro.x','Gyro.y','Gyro.z','Mag.x','Mag.y','Mag.z','GPS.lon','GPS.lat','GPS.alt','GPS.vdop','GPS.hdop','RC.Pitch','RC.Roll','RC.Yaw','RC.Throttle','Mode','RC.Failsafe','SignalStrength','Voltage']

# empty list to append later
reject_columns_list = []

# for loop to process every file in the directory
for current_file in files:
    
    # variable to control if the files need processing
    process_file = True
    
    # create the required directory name from the name of the current_file
    # we are going to remove 4 chars from the end to get rid of ".DAT"
    endlen = len(current_file)
    dir_name = current_file[:endlen-4]

    # if statement to determine if directory exists
    if(not(os.path.isdir(dir_name))):
        # if no directory exists, create the directory
        os.mkdir(dir_name)
    
    #if statment to determine if we need to create dir
    if os.path.isdir(os.path.join(dir_name,'Flight Data')):
        
        # check if folder exists and create if needed
        if not os.path.exists(os.path.join(dir_name,'Flight Data','combined')):
            os.mkdir(os.path.join(dir_name,'Flight Data','combined'))
            
        # check if the directory has already been polupated meaning the 
        # file has been processed
        if not(len(os.listdir(os.path.join(dir_name,'Flight Data','combined'))) == 0):
            process_file = False
    else:
        os.mkdir(os.path.join(dir_name,'Flight Data'))
    
    # if statement to determine id the file should be read
    if process_file == True:
        
        # read the file
        df = pd.read_csv(current_file, index_col=0, header=0, engine='python')
         
        # get list of columns
        headers = df.columns
        
        # change the list to just have the columns we want
        reject_column_list = [header for header in headers if header not in columns_to_keep]
        
        # remove the headers we do not want
        df = df.drop(columns = reject_column_list)
        
        # rename the columns to the right names
        df.columns = new_headers
        
        # fill in values missing data
        df = df.fillna(method='ffill')
        
        # print a progress report as the name of the file as we work
        # through the files
        print('Working on: '+current_file)

        # variables to hold the first coordinates
        xx = df['GPS.lat'].iloc[0]
        yy = df['GPS.lon'].iloc[0]
        
        # subtract first point from all the others
        df['GPS.lat'] = df['GPS.lat'] - xx
        df['GPS.lon'] = df['GPS.lon'] - yy
        
        # reset the first coordinates to zero
        xx = 0
        yy = 0
        
        # change units from mvolts to volts
        df['Voltage'] = df['Voltage']/1000
        
        
        # replace failsafe and flight modes with numbers
        df["RC.Failsafe"] = df["RC.Failsafe"].replace({'Hover': 1, 'DisConnected': 2})
        df["Mode"] = df["Mode"].replace({'GPS_Atti': 1.1, 'Sport': 1.3, 'Position-GPS' : 2 , 'Position-ATTI' : 2.5})
    
        # save the file in the right directory 
        df.to_csv(path_or_buf=os.path.join(dir_name,'Flight Data','combined',dir_name+'_results.csv'),index=True, index_label='Time')
        
    # print report on .DAT files
    else: 
        print('Csv file has already been converted for '+dir_name)
        
    # call the make plots function to generate plots
    make_plots(os.path.join(dir_name,'Flight Data','combined',dir_name+'_results.csv'))
    
print('All files have been processed in ')
print(path)
