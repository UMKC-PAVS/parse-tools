# -*- coding: utf-8 -*-
"""
Created on Wed Jul  1 13:43:06 2020

@author: Harrison Terry

Csv combiner and fixer for degradation analysis from pyulog for PX4

6/30/2020 Made basic functionality

7/10/2020 Combined with csv fixer document.

Adds functionality for proper naming structure. Copies name off of original ulg file, which should be renamed first
Adds functionality for putting in group and repitition so long as naming structure does not change
Moves combined data to a new folder so it does not need to be done manually

Adds a second file for the mean and stdev

7/13/2020 Creates a second analysis file for the magnetometer data along with its mean and stdev
Typo fixes
FUTURE WORK: Only works for 1 file at a time currently, add functionality for multiple files

7/19/20 Complete Rebuild for old test files with wrong naming structure

7/20/20 Fixed average and stdev
Removes csv writing in favor of xlsx writing
Removes lots of no longer used code and general tidiness improvements WIP
Leaves in call function for ulog2csv, may remove in future updates


"""




import os
import pandas as pd
from subprocess import call


#NOTE: If you do not use forward slashes instead of backslashes you must put it in the format of r'path' with no backslashes at the end of the path. Python will give you an error otherwise due to unicode
#directorypath = r'C:\Users\cuav\Documents\Python Scripts\071'
directorypath = r'C:\Users\het9t\OneDrive\Documents\PX4 Summary Statistics Sheets\complete'
os.chdir(directorypath)

#Set to 0 if group, sequential and rep need to be added

file_list = []
averages = []
deviations = []

qq = 0
if qq == 0:
    for file in os.listdir(directorypath):
        if file.endswith('combined.csv'):
            df3 = pd.read_csv(file)
            L = len(df3.index)
            Group2 = [float(file[8:-17])] * L
            names = float(file[11:-13])
            Repitition = [names] * L
            Sequential = list(range(1,L+1))
            df3.insert(0,'Seq',Sequential)
            df3.insert(1,'Group',Group2)
            df3.insert(2,'Rep',Repitition)
            file_list.append(df3)
            mean = df3.mean()
            stdev = df3.std()
            mean = mean.to_frame()
            stdev = stdev.to_frame()
            mean.columns = ['Mean']
            stdev.columns = ['Stdev']
                       
            
            mean = mean.transpose()
            #mean = mean[['Group','Seq','Rep','sensor_combined_0_gyro_rad[0]','sensor_combined_0_gyro_rad[1]','sensor_combined_0_gyro_rad[2]','sensor_combined_0_accelerometer_m_s2[0]','sensor_combined_0_accelerometer_m_s2[1]','sensor_combined_0_accelerometer_m_s2[2]','vehicle_magnetometer_0_magnetometer_ga[0]','vehicle_magnetometer_0_magnetometer_ga[1]','vehicle_magnetometer_0_magnetometer_ga[2]']]
            #mean = mean.rename(columns= {'sensor_combined_0_gyro_rad[0]':'GyroX','sensor_combined_0_gyro_rad[1]':'GyroY','sensor_combined_0_gyro_rad[2]':'GyroZ','sensor_combined_0_accelerometer_m_s2[0]':'AccelX','sensor_combined_0_accelerometer_m_s2[1]':'AccelY','sensor_combined_0_accelerometer_m_s2[2]':'AccelZ','vehicle_magnetometer_0_magnetometer_ga[0]':'MagX','vehicle_magnetometer_0_magnetometer_ga[1]':'MagY','vehicle_magnetometer_0_magnetometer_ga[2]':'MagZ'})
            mean = mean[['Group','Seq','Rep','gyro_rad[0]','gyro_rad[1]','gyro_rad[2]','accelerometer_m_s2[0]','accelerometer_m_s2[1]','accelerometer_m_s2[2]','magnetometer_ga[0]','magnetometer_ga[1]','magnetometer_ga[2]']]
            mean = mean.rename(columns= {'gyro_rad[0]':'GyroX','gyro_rad[1]':'GyroY','gyro_rad[2]':'GyroZ','accelerometer_m_s2[0]':'AccelX','accelerometer_m_s2[1]':'AccelY','accelerometer_m_s2[2]':'AccelZ','magnetometer_ga[0]':'MagX','magnetometer_ga[1]':'MagY','magnetometer_ga[2]':'MagZ'})

            mean = mean.drop(columns=['Seq'])
            
            stdev = stdev.transpose()
            #stdev = stdev[['Group','Seq','Rep','sensor_combined_0_gyro_rad[0]','sensor_combined_0_gyro_rad[1]','sensor_combined_0_gyro_rad[2]','sensor_combined_0_accelerometer_m_s2[0]','sensor_combined_0_accelerometer_m_s2[1]','sensor_combined_0_accelerometer_m_s2[2]','vehicle_magnetometer_0_magnetometer_ga[0]','vehicle_magnetometer_0_magnetometer_ga[1]','vehicle_magnetometer_0_magnetometer_ga[2]']]
            #stdev = stdev.rename(columns= {'sensor_combined_0_gyro_rad[0]':'GyroX','sensor_combined_0_gyro_rad[1]':'GyroY','sensor_combined_0_gyro_rad[2]':'GyroZ','sensor_combined_0_accelerometer_m_s2[0]':'AccelX','sensor_combined_0_accelerometer_m_s2[1]':'AccelY','sensor_combined_0_accelerometer_m_s2[2]':'AccelZ','vehicle_magnetometer_0_magnetometer_ga[0]':'MagX','vehicle_magnetometer_0_magnetometer_ga[1]':'MagY','vehicle_magnetometer_0_magnetometer_ga[2]':'MagZ'})
            stdev = stdev[['Group','Seq','Rep','gyro_rad[0]','gyro_rad[1]','gyro_rad[2]','accelerometer_m_s2[0]','accelerometer_m_s2[1]','accelerometer_m_s2[2]','magnetometer_ga[0]','magnetometer_ga[1]','magnetometer_ga[2]']]
            stdev = stdev.rename(columns= {'gyro_rad[0]':'GyroX','gyro_rad[1]':'GyroY','gyro_rad[2]':'GyroZ','accelerometer_m_s2[0]':'AccelX','accelerometer_m_s2[1]':'AccelY','accelerometer_m_s2[2]':'AccelZ','magnetometer_ga[0]':'MagX','magnetometer_ga[1]':'MagY','magnetometer_ga[2]':'MagZ'})

            
            stdev = stdev.drop(columns=['Seq'])
            stdev['Group'] = mean['Group'].values
            stdev['Rep'] = mean['Rep'].values
            
            averages.append(mean)
            deviations.append(stdev)

#This will create the other files. Please use pip to install pyulog within the console beforehand if not done so before. You will need to restart kernel using Ctrl + . as well

zz = 0
if zz == 1:
    
    for current_file in files:

        call(["ulog2csv",current_file])

os.chdir(directorypath)

#combine all files in the list
combined_csv = pd.concat(file_list,ignore_index=True)
Aves = pd.concat(averages,ignore_index=False)
Devs = pd.concat(deviations,ignore_index=False)


#Reads the new combined file
data = combined_csv

#For Gyro and Accelerometer Data
#df = data[['Group','Seq','Rep','sensor_combined_0_gyro_rad[0]','sensor_combined_0_gyro_rad[1]','sensor_combined_0_gyro_rad[2]','sensor_combined_0_accelerometer_m_s2[0]','sensor_combined_0_accelerometer_m_s2[1]','sensor_combined_0_accelerometer_m_s2[2]']]
df = data[['Group','Seq','Rep','gyro_rad[0]','gyro_rad[1]','gyro_rad[2]','accelerometer_m_s2[0]','accelerometer_m_s2[1]','accelerometer_m_s2[2]']]
df = df.rename(columns= {'gyro_rad[0]':'GyroX','gyro_rad[1]':'GyroY','gyro_rad[2]':'GyroZ','accelerometer_m_s2[0]':'AccelX','accelerometer_m_s2[1]':'AccelY','accelerometer_m_s2[2]':'AccelZ'})
#df = df.rename(columns= {'sensor_combined_0_gyro_rad[0]':'GyroX','sensor_combined_0_gyro_rad[1]':'GyroY','sensor_combined_0_gyro_rad[2]':'GyroZ','sensor_combined_0_accelerometer_m_s2[0]':'AccelX','sensor_combined_0_accelerometer_m_s2[1]':'AccelY','sensor_combined_0_accelerometer_m_s2[2]':'AccelZ'})


#For Magnetometer Data
#df2 = data[['Group','Seq','Rep','vehicle_magnetometer_0_magnetometer_ga[0]','vehicle_magnetometer_0_magnetometer_ga[1]','vehicle_magnetometer_0_magnetometer_ga[2]']]
df2 = data[['Group','Seq','Rep','magnetometer_ga[0]','magnetometer_ga[1]','magnetometer_ga[2]']]
df2 = df2.rename(columns= {'magnetometer_ga[0]':'MagX','magnetometer_ga[1]':'MagY','magnetometer_ga[2]':'MagZ'})
#df2 = df2.rename(columns= {'vehicle_magnetometer_0_magnetometer_ga[0]':'MagX','vehicle_magnetometer_0_magnetometer_ga[1]':'MagY','vehicle_magnetometer_0_magnetometer_ga[2]':'MagZ'})


#This deletes any rows that have null values
df = df.dropna()
df2 = df2.dropna()


path = os.getcwd()
directory = os.path.join(path,r'Degradation Data')
if not os.path.exists(directory):
    os.makedirs(directory)


#Changes directory to put it into the new folder
os.chdir(directory)

Comb_Data = pd.ExcelWriter('PX4-037-6-Data.xlsx', engine='xlsxwriter')
df.to_excel(Comb_Data,sheet_name='Accel&Gyro',index=False)
df2.to_excel(Comb_Data,sheet_name='Magnetometer',index=False)
Aves.to_excel(Comb_Data,sheet_name='Mean')
Devs.to_excel(Comb_Data,sheet_name='Stdev')
Comb_Data.save()    