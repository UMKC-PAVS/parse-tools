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



WARNING: ulg file MUST use proper naming structure or the new columns will be incorrect
"""


"""
README: This program is meant for a workflow where once somebody gets a PX4 log file off the cube it goes for immediate processing while the team gets the next drone ready to get logs off
Therefore, it is meant for folders empty of other csv files, as it does not check for specific csvs within the directory but every file in the directory.


The directory must be changed to the new folder in order to get the file. Please copy and paste the folder path to the ulg file you are looking to get csvs and analysis. This is found on line 49 of the code


"""




import os
import glob
import pandas as pd
from subprocess import call


#NOTE: If you do not use forward slashes instead of backslashes you must put it in the format of r'path' with no backslashes at the end of the path. Python will give you an error otherwise due to unicode
directorypath = r'C:\Users\het9t\OneDrive\Documents\PX4 Summary Statistics Sheets\075'

os.chdir(directorypath)

#Set to 0 if group, sequential and rep need to be added

file_list = []

qq = 0
if qq == 0:
    for file in os.listdir(directorypath):
        if file.endswith('combined.csv'):
            df3 = pd.read_csv(file)
            L = len(df3.index)
            Group2 = [1] * L
            names = float(file[6:-13])
            Repitition = [names] * L
            Sequential = list(range(1,L+1))
            df3.insert(0,'Seq',Sequential)
            df3.insert(1,'Group',Group2)
            df3.insert(2,'Rep',Repitition)
            file_list.append(df3)
                        


#This will create the other files. Please use pip to install pyulog within the console beforehand if not done so before. You will need to restart kernel using Ctrl + . as well

zz = 0
if zz == 1:
    
    for current_file in files:

        call(["ulog2csv",current_file])

os.chdir(directorypath)

#combine all files in the list
combined_csv = pd.concat(file_list,ignore_index=True)
#export to csv
#name = current_file.replace('.ulg','.csv')
#combined_csv.to_csv( name, index=False, encoding='utf-8-sig')

combined_csv.to_csv('data.csv')

#Reads the new combined file
data = combined_csv

#For Gyro and Accelerometer Data
df = data[['Group','Seq','Rep','sensor_combined_0_gyro_rad[0]','sensor_combined_0_gyro_rad[1]','sensor_combined_0_gyro_rad[2]','sensor_combined_0_accelerometer_m_s2[0]','sensor_combined_0_accelerometer_m_s2[1]','sensor_combined_0_accelerometer_m_s2[2]']]

df = df.rename(columns= {'sensor_combined_0_gyro_rad[0]':'GyroX','sensor_combined_0_gyro_rad[1]':'GyroY','sensor_combined_0_gyro_rad[2]':'GyroZ','sensor_combined_0_accelerometer_m_s2[0]':'AccelX','sensor_combined_0_accelerometer_m_s2[1]':'AccelY','sensor_combined_0_accelerometer_m_s2[2]':'AccelZ'})

#For Magnetometer Data
df2 = data[['Group','Seq','Rep','vehicle_magnetometer_0_magnetometer_ga[0]','vehicle_magnetometer_0_magnetometer_ga[1]','vehicle_magnetometer_0_magnetometer_ga[2]']]
df2 = df2.rename(columns= {'vehicle_magnetometer_0_magnetometer_ga[0]':'MagX','vehicle_magnetometer_0_magnetometer_ga[1]':'MagY','vehicle_magnetometer_0_magnetometer_ga[2]':'MagZ'})


#This deletes any rows that have null values
df = df.dropna()
df2 = df2.dropna()


#Find the mean and stdev values of each column, create new dataframe with those values
mean = df.mean()
stdev = df.std()

mean2 = df2.mean()
stdev2 = df2.std()


mean = mean.to_frame()
stdev = stdev.to_frame()

mean2 = mean2.to_frame()
stdev2 = stdev2.to_frame()


#Combine the mean and stdev dataframes

mean.columns = ['Mean']
mean.insert(1,'Stdev',stdev)

mean2.columns = ['Mean']
mean2.insert(1,'Stdev',stdev2)

mean.drop(index=['Group','Rep','Seq'])
mean2.drop(index=['Group','Rep','Seq'])

#This provides us the length of the current data so it can be used to make new columns
N = len(df.index)
NN = len(df2.index)

#Group number is in 8th index of file name, Rep is 12th ONLY if naming structure does not change


if zz == 1:
    Number = name[8]
    Rep = name[12]
    Group = [Number] * N
    Repit = [Rep] * N
    Group3 = [Number] * NN
    Repit3 = [Rep] * NN

    seq = list(range(1,N+1))
    seq2 = list(range(1,NN+1))
#Insert these columns in their correct spots on the combined dataframe

    df.insert(0,'Seq',seq)
    df.insert(1,'Group',Group)
    df.insert(2,'Rep',Repit)


    df2.insert(0,'Seq',seq2)
    df2.insert(1,'Group',Group3)
    df2.insert(2,'Rep',Repit3)


    name2 = name.replace('.csv','-Degradation-Data.csv')
    name3 = name.replace('.csv','-Degradation-Statistics.csv')
    name4 = name.replace('.csv','-Magnet-Statistics.csv')
    name5 = name.replace('.csv','-Magnet-Data.csv')

#Insert Group and Rep within the statistics dataframe mean with correct length
    Group2 = [Number] * 2
    Repit2 = [Rep] * 2
    mean = mean.T
    mean2 = mean2.T
    mean.insert(0,'Group',Group2)
    mean.insert(1,'Rep',Repit2)
    mean2.insert(0,'Group',Group2)
    mean2.insert(1,'Rep',Repit2)

#Creates new folder for the combined csv or moves to that directory if it already exists

    path = os.getcwd()
    directory = os.path.join(path,r'Degradation Data')
    if not os.path.exists(directory):
        os.makedirs(directory)


#Changes directory to put it into the new folder
    os.chdir(directory)

#Writes to csv in new folder
    df.to_csv(name2,index=False)
    df2.to_csv(name5,index=False)
    mean.to_csv(name3,index=True)
    mean2.to_csv(name4,index=True)
