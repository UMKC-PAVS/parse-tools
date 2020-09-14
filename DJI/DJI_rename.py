# -*- coding: utf-8 -*-
'''
Written: Thomas Cacy, Harrison Terry
Date: 08/03/2020
Purpose: Read and process a .csv file after it has been converted from a .DAT
         file in a way that allows it to be plotted using make_plots.py under 
         the unified parsing program. This program relies on the order of the
         columns being the same every time

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
columns_to_keep = ['IMU_ATTI(0):roll','IMU_ATTI(0):pitch','IMU_ATTI(0):yaw','IMU_ATTI(0):barometer:Raw','IMU_ATTI(0):accel:X','IMU_ATTI(0):accel:Y','IMU_ATTI(0):accel:Z','IMU_ATTI(0):gyro:X','IMU_ATTI(0):gyro:Y','IMU_ATTI(0):gyro:Z','IMU_ATTI(0):mag:X','IMU_ATTI(0):mag:Y','IMU_ATTI(0):mag:Z','GPS(0):Long','GPS(0):Lat','GPS(0):heightMSL','GPS(0):pDOP','GPS(0):hDOP','RC:sigStrength','RC:connected','RC:Aileron','RC:Rudder','RC:Throttle','Controller:ctrlMode','RC:failSafe','RC_Info:sigStrength:C','Motor:Speed:RFront','Motor:Speed:LFront','Motor:Speed:RBack','Motor:Speed:LBack','IMU_ATTI(0):roll:C','IMU_ATTI(0):pitch:C','IMU_ATTI(0):yaw:C','IMU_ATTI(0):accelX','IMU_ATTI(0):accelY','IMU_ATTI(0):accelZ','IMU_ATTI(0):gyroX','IMU_ATTI(0):gyroY','IMU_ATTI(0):gyroZ','IMU_ATTI(0):magX','IMU_ATTI(0):magY','IMU_ATTI(0):magZ']

# list of column's new names   
new_headers = ['BaroAlt','Accel.x','Accel.y','Accel.z','Gyro.x','Gyro.y','Gyro.z','Mag.x','Mag.y','Mag.z','Att.roll','Att.pitch','Att.yaw','GPS.lon','GPS.lat','GPS.alt','GPS.vdop','GPS.hdop','RC.aileron','RC.rudder','RC.Throttle','Mode','RC.Failsafe','RC.Signalstrength','Motor.RF','Motor.LF','Motor.LB','Motor.RB']

# empty list to append later
reject_columns_list = []

# for loop to process every file in the directory
for current_file in files:
    
    # variable to control if the files need processing
    process_file = True
    
    # create the required directory name from the name of the current_file
    # we are going to remove 4 chars from the end to get rid of ".csv"
    endlen = len(current_file)
    dir_name = current_file[:endlen-4]

    # if statement to determine if directory exists
    if(not(os.path.isdir(dir_name))):
        # if no directory exists, create the directory
        os.mkdir(dir_name)
    
    #if statment to determine if we need to create dir
    if os.path.isdir(os.path.join(dir_name,'Flight Data')):
        pass
    else:
        os.mkdir(os.path.join(dir_name,'Flight Data'))
        
    # check if folder exists and create if needed
    if not os.path.exists(os.path.join(dir_name,'Flight Data','combined')):
        os.mkdir(os.path.join(dir_name,'Flight Data','combined'))
         
    # check if the directory has already been polupated meaning the 
    # file has been processed
    if not(len(os.listdir(os.path.join(dir_name,'Flight Data','combined'))) == 0):
        process_file = False
    
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
        #df.columns = new_headers
        df = df.rename(columns={'IMU_ATTI(0):barometer:Raw':'BaroAlt','IMU_ATTI(0):accel:X':'Accel.x','IMU_ATTI(0):accelX':'Accel.x','IMU_ATTI(0):accel:Y':'Accel.y','IMU_ATTI(0):accelY':'Accel.y',
                                'IMU_ATTI(0):accel:Z':'Accel.z','IMU_ATTI(0):accelZ':'Accel.z','IMU_ATTI(0):gyro:X':'Gyro.x','IMU_ATTI(0):gyroX':'Gyro.x','IMU_ATTI(0):gyro:Y':'Gyro.y',
                                 'IMU_ATTI(0):gyroY':'Gyro.y','IMU_ATTI(0):gyro:Z':'Gyro.z','IMU_ATTI(0):gyroZ':'Gyro.z','IMU_ATTI(0):mag:X':'Mag.x','IMU_ATTI(0):magX':'Mag.x',
                                 'IMU_ATTI(0):mag:Y':'Mag.y','IMU_ATTI(0):magY':'Mag.y','IMU_ATTI(0):mag:Z':'Mag.z','IMU_ATTI(0):magZ':'Mag.z','IMU_ATTI(0):roll':'Att.roll',
                                  'IMU_ATTI(0):roll:C':'Att.roll','IMU_ATTI(0):pitch':'Att.pitch','IMU_ATTI(0):pitch:C':'Att.pitch','IMU_ATTI(0):yaw':'Att.yaw','IMU_ATTI(0):yaw:C':'Att.yaw',
                                  'GPS(0):Long':'GPS.lon','GPS(0):Lat':'GPS.lat','GPS(0):heightMSL':'GPS.alt','GPS(0):pDOP':'GPS.vdop','GPS(0):hDOP':'GPS.hdop',
                                  'RC_Info:sigStrength:C':'RC.Signalstrength','RC:sigStrength':'RC.Signalstrength','RC.failSafe':'RC:Failsafe','RC:Aileron':'RC.aileron',
                                  'RC:Rudder':'RC.rudder','RC:Throttle':'RC.throttle','Controller:ctrlMode':'Mode','Motor:Speed:RFront':'Motor.RF','Motor:Speed:LFront':'Motor.LF',
                                  'Motor:Speed:RBack':'Motor.LB','Motor:Speed:LBack':'Motor.RB','BatteryInfo:ad_v:D':'Voltage'})
        
        # fill in values missing data
        df = df.fillna(method='ffill')
        
        # print a progress report as the name of the file as we work
        # through the files
        print('Working on: '+current_file)
        
        # change units from mvolts to volts
        try:
            df['Voltage'] = df['Voltage']/1000
        except:
            pass
        
        # change time units from microseconds to seconds
        df.index = df.index/10**6
        
        # replace failsafe and flight modes with numbers
        try:
            df['RC:connected'] = df['RC:connected'].replace({'Disconnected': 0, 'Connected': 1})
        except:
            pass
        try:
            df['Mode'] = df['Mode'].replace({'Manual': 0.0, 'GPS_Atti': 1.1, 'SPORT': 1.3, 'Position-GPS' : 2 , 'Atti' : 2.5,'AutoLanding': 3.8, 'FORCE_LANDING' : 3.9, 'ASST_TAKEOFF': 5, 'AssitedTakeoff' : 5, 'GoHome':6})
        except:
            pass
        
        # save the file in the right directory 
        df.to_csv(path_or_buf=os.path.join(dir_name,'Flight Data','combined',dir_name+'_results.csv'),index=True, index_label='Time')
        
    # print report on .csv files
    else: 
        print('Csv file has already been converted for '+dir_name)
        
    # call the make plots function to generate plots
    make_plots(os.path.join(dir_name,'Flight Data','combined',dir_name+'_results.csv'))
    
print('All files have been processed in ')
print(path)