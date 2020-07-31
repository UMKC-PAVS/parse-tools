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


#NOTE: If you do not use forward slashes instead of backslashes you must put it in the format of r'path' with no backslashes at the end of the path. Python will give you an error otherwise due to unicode
#directorypath = r'C:\Users\cuav\Documents\Python Scripts\071'
directorypath = r'C:\Users\het9t\OneDrive\Documents\PX4 Summary Statistics Sheets\complete'
os.chdir(directorypath)

#Set to 0 if group, sequential and rep need to be added

file_list = []
file_list2 = []
averages = []
deviations = []

qq = 0
if qq == 0:
    for file in os.listdir(directorypath):
        if file.startswith('PX4-075'):
            if file.endswith('.csv'):
                df3 = pd.read_csv(file)
            
                df = df3[['gyro_rad[0]','gyro_rad[1]','gyro_rad[2]','accelerometer_m_s2[0]','accelerometer_m_s2[1]','accelerometer_m_s2[2]']]
                df = df.dropna()
            
                df2 = df3[['magnetometer_ga[0]','magnetometer_ga[1]','magnetometer_ga[2]']]
                df2 = df2.dropna()

            
            
                L = len(df.index)
                LL = len(df2.index)
            
                Group2 = [float(file[8])] * L
                Group3= [float(file[8])] * LL
                names = float(file[11])
                Repitition = [names] * L
                Repitition2 = [names] * LL
            
                Sequential = list(range(1,L+1))
                Seq2 = list(range(1,LL+1))
                
                df.insert(0,'Seq',Sequential)
                df.insert(1,'Group',Group2)
                df.insert(2,'Rep',Repitition)
                
                df2.insert(0,'Seq',Seq2)
                df2.insert(1,'Group',Group3)
                df2.insert(2,'Rep',Repitition2)
                
                            
                mean = df.mean()
                stdev = df.std()
                mean = mean.to_frame()
                stdev = stdev.to_frame()
                mean.columns = ['Mean']
                stdev.columns = ['Stdev']
                           
                
                mean2 = df2.mean()
                stdev2 = df2.std()
                mean2 = mean2.to_frame()
                stdev2 = stdev2.to_frame()
                mean2.columns = ['Mean']
                stdev2.columns = ['Stdev']
                
                
                
                mean = mean.transpose()
                mean2 = mean2.transpose()
                #mean = mean[['Group','Seq','Rep','sensor_combined_0_gyro_rad[0]','sensor_combined_0_gyro_rad[1]','sensor_combined_0_gyro_rad[2]','sensor_combined_0_accelerometer_m_s2[0]','sensor_combined_0_accelerometer_m_s2[1]','sensor_combined_0_accelerometer_m_s2[2]','vehicle_magnetometer_0_magnetometer_ga[0]','vehicle_magnetometer_0_magnetometer_ga[1]','vehicle_magnetometer_0_magnetometer_ga[2]']]
                #mean = mean.rename(columns= {'sensor_combined_0_gyro_rad[0]':'GyroX','sensor_combined_0_gyro_rad[1]':'GyroY','sensor_combined_0_gyro_rad[2]':'GyroZ','sensor_combined_0_accelerometer_m_s2[0]':'AccelX','sensor_combined_0_accelerometer_m_s2[1]':'AccelY','sensor_combined_0_accelerometer_m_s2[2]':'AccelZ','vehicle_magnetometer_0_magnetometer_ga[0]':'MagX','vehicle_magnetometer_0_magnetometer_ga[1]':'MagY','vehicle_magnetometer_0_magnetometer_ga[2]':'MagZ'})
                mean = mean[['Group','Seq','Rep','gyro_rad[0]','gyro_rad[1]','gyro_rad[2]','accelerometer_m_s2[0]','accelerometer_m_s2[1]','accelerometer_m_s2[2]']]
                mean2 = mean2[['Group','Seq','Rep','magnetometer_ga[0]','magnetometer_ga[1]','magnetometer_ga[2]']]
                mean = mean.rename(columns= {'gyro_rad[0]':'GyroX','gyro_rad[1]':'GyroY','gyro_rad[2]':'GyroZ','accelerometer_m_s2[0]':'AccelX','accelerometer_m_s2[1]':'AccelY','accelerometer_m_s2[2]':'AccelZ'})
                mean2 = mean2.rename(columns= {'magnetometer_ga[0]':'MagX','magnetometer_ga[1]':'MagY','magnetometer_ga[2]':'MagZ'})
                mean = mean.drop(columns=['Seq'])
                mean2 = mean2.drop(columns=['Seq'])
                
                
                stdev = stdev.transpose()
                stdev2 = stdev2.transpose()
                #stdev = stdev[['Group','Seq','Rep','sensor_combined_0_gyro_rad[0]','sensor_combined_0_gyro_rad[1]','sensor_combined_0_gyro_rad[2]','sensor_combined_0_accelerometer_m_s2[0]','sensor_combined_0_accelerometer_m_s2[1]','sensor_combined_0_accelerometer_m_s2[2]','vehicle_magnetometer_0_magnetometer_ga[0]','vehicle_magnetometer_0_magnetometer_ga[1]','vehicle_magnetometer_0_magnetometer_ga[2]']]
                #stdev = stdev.rename(columns= {'sensor_combined_0_gyro_rad[0]':'GyroX','sensor_combined_0_gyro_rad[1]':'GyroY','sensor_combined_0_gyro_rad[2]':'GyroZ','sensor_combined_0_accelerometer_m_s2[0]':'AccelX','sensor_combined_0_accelerometer_m_s2[1]':'AccelY','sensor_combined_0_accelerometer_m_s2[2]':'AccelZ','vehicle_magnetometer_0_magnetometer_ga[0]':'MagX','vehicle_magnetometer_0_magnetometer_ga[1]':'MagY','vehicle_magnetometer_0_magnetometer_ga[2]':'MagZ'})
                stdev = stdev[['Group','Seq','Rep','gyro_rad[0]','gyro_rad[1]','gyro_rad[2]','accelerometer_m_s2[0]','accelerometer_m_s2[1]','accelerometer_m_s2[2]']]
                stdev2 = stdev2[['Group','Seq','Rep','magnetometer_ga[0]','magnetometer_ga[1]','magnetometer_ga[2]']]
                stdev = stdev.rename(columns= {'gyro_rad[0]':'GyroX','gyro_rad[1]':'GyroY','gyro_rad[2]':'GyroZ','accelerometer_m_s2[0]':'AccelX','accelerometer_m_s2[1]':'AccelY','accelerometer_m_s2[2]':'AccelZ'})
                stdev2 = stdev2.rename(columns= {'magnetometer_ga[0]':'MagX','magnetometer_ga[1]':'MagY','magnetometer_ga[2]':'MagZ'})
                
                stdev = stdev.drop(columns=['Seq'])
                stdev2 = stdev2.drop(columns=['Seq'])
                
                stdev['Group'] = mean['Group'].values
                stdev['Rep'] = mean['Rep'].values
                stdev2['Group'] = mean2['Group'].values
                stdev2['Rep'] = mean2['Rep'].values
                
                aavv = pd.concat([mean,mean2],ignore_index=True)
                aavv = aavv.ffill()
                aavv = aavv.dropna()
                
                ddvv = pd.concat([stdev,stdev2],ignore_index=True)
                ddvv = ddvv.ffill()
                ddvv = ddvv.dropna()
                
                df = df.rename(columns= {'gyro_rad[0]':'GyroX','gyro_rad[1]':'GyroY','gyro_rad[2]':'GyroZ','accelerometer_m_s2[0]':'AccelX','accelerometer_m_s2[1]':'AccelY','accelerometer_m_s2[2]':'AccelZ'})
                df2 = df2.rename(columns= {'magnetometer_ga[0]':'MagX','magnetometer_ga[1]':'MagY','magnetometer_ga[2]':'MagZ'})
                
                file_list.append(df)
                file_list2.append(df2)
                
                averages.append(aavv)
                deviations.append(ddvv)

#This will create the other files. Please use pip to install pyulog within the console beforehand if not done so before. You will need to restart kernel using Ctrl + . as well


os.chdir(directorypath)

#combine all files in the list
data = pd.concat(file_list,ignore_index=True)
data2 = pd.concat(file_list2,ignore_index=True)
Aves = pd.concat(averages,ignore_index=True)
Devs = pd.concat(deviations,ignore_index=True)

#For Gyro and Accelerometer Data
#df = data[['Group','Seq','Rep','sensor_combined_0_gyro_rad[0]','sensor_combined_0_gyro_rad[1]','sensor_combined_0_gyro_rad[2]','sensor_combined_0_accelerometer_m_s2[0]','sensor_combined_0_accelerometer_m_s2[1]','sensor_combined_0_accelerometer_m_s2[2]']]
#df = data[['Group','Seq','Rep','gyro_rad[0]','gyro_rad[1]','gyro_rad[2]','accelerometer_m_s2[0]','accelerometer_m_s2[1]','accelerometer_m_s2[2]']]
#df = df.rename(columns= {'sensor_combined_0_gyro_rad[0]':'GyroX','sensor_combined_0_gyro_rad[1]':'GyroY','sensor_combined_0_gyro_rad[2]':'GyroZ','sensor_combined_0_accelerometer_m_s2[0]':'AccelX','sensor_combined_0_accelerometer_m_s2[1]':'AccelY','sensor_combined_0_accelerometer_m_s2[2]':'AccelZ'})


#For Magnetometer Data
#df2 = data[['Group','Seq','Rep','vehicle_magnetometer_0_magnetometer_ga[0]','vehicle_magnetometer_0_magnetometer_ga[1]','vehicle_magnetometer_0_magnetometer_ga[2]']]
#df2 = data[['Group','Seq','Rep','magnetometer_ga[0]','magnetometer_ga[1]','magnetometer_ga[2]']]
#df2 = df2.rename(columns= {'vehicle_magnetometer_0_magnetometer_ga[0]':'MagX','vehicle_magnetometer_0_magnetometer_ga[1]':'MagY','vehicle_magnetometer_0_magnetometer_ga[2]':'MagZ'})



path = os.getcwd()
directory = os.path.join(path,r'Degradation Data')
if not os.path.exists(directory):
    os.makedirs(directory)


#Changes directory to put it into the new folder
os.chdir(directory)

Comb_Data = pd.ExcelWriter('PX4-075-Data.xlsx', engine='xlsxwriter')
data.to_excel(Comb_Data,sheet_name='Accel&Gyro',index=False)
data2.to_excel(Comb_Data,sheet_name='Magnetometer',index=False)
Aves.to_excel(Comb_Data,sheet_name='Mean',index=False)
Devs.to_excel(Comb_Data,sheet_name='Stdev',index=False)
Comb_Data.save()    