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

10/16/20 Complete Rewrite so it can be used easier by other people

10/20/20 Typos

"""

'''
README: This is written for the PX4 platform, which has different timing for magnetometer versus the accelerometer and gyroscope. This would be easier in other platforms such as DJI which has a unified timing structure.

The mean and stdev have two separate arrays which get combined due to this different timing. It probably could be done together but would need yet another rewrite which isn't likely to be necessary at this time'
'''





import os
import pandas as pd

directorypath = input("Please input directory of files needed. If files are named incorrectly then please use renaming file: ")
os.chdir(directorypath)

platform = input("Please input the vehicle number and platform the files start with (example PX4-075-) ")

file_list = []
file_list2 = []
averages = []
deviations = []

for file in os.listdir(directorypath):
    if file.startswith(platform):
        if file.endswith('.csv'):
                df3 = pd.read_csv(file)
            
                df = df3[['gyro_rad[0]','gyro_rad[1]','gyro_rad[2]','accelerometer_m_s2[0]','accelerometer_m_s2[1]','accelerometer_m_s2[2]']]
                df = df.dropna()
            
                df2 = df3[['magnetometer_ga[0]','magnetometer_ga[1]','magnetometer_ga[2]']]
                df2 = df2.dropna()

#Finds the length of the array for sequential purposes
                L = len(df.index)
                LL = len(df2.index)
            
#Current naming structure has the group on the 8th index of the string and the repetition number on the 11th index. This could be changed in the future, and may need to be adjusted for that change
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
                mean = mean[['Group','Rep','gyro_rad[0]','gyro_rad[1]','gyro_rad[2]','accelerometer_m_s2[0]','accelerometer_m_s2[1]','accelerometer_m_s2[2]']]
                mean2 = mean2[['Group','Rep','magnetometer_ga[0]','magnetometer_ga[1]','magnetometer_ga[2]']]
                mean = mean.rename(columns= {'gyro_rad[0]':'GyroX','gyro_rad[1]':'GyroY','gyro_rad[2]':'GyroZ','accelerometer_m_s2[0]':'AccelX','accelerometer_m_s2[1]':'AccelY','accelerometer_m_s2[2]':'AccelZ'})
                mean2 = mean2.rename(columns= {'magnetometer_ga[0]':'MagX','magnetometer_ga[1]':'MagY','magnetometer_ga[2]':'MagZ'})
            
                stdev = stdev.transpose()
                stdev2 = stdev2.transpose()
                stdev = stdev[['Group','Rep','gyro_rad[0]','gyro_rad[1]','gyro_rad[2]','accelerometer_m_s2[0]','accelerometer_m_s2[1]','accelerometer_m_s2[2]']]
                stdev2 = stdev2[['Group','Rep','magnetometer_ga[0]','magnetometer_ga[1]','magnetometer_ga[2]']]
                stdev = stdev.rename(columns= {'gyro_rad[0]':'GyroX','gyro_rad[1]':'GyroY','gyro_rad[2]':'GyroZ','accelerometer_m_s2[0]':'AccelX','accelerometer_m_s2[1]':'AccelY','accelerometer_m_s2[2]':'AccelZ'})
                stdev2 = stdev2.rename(columns= {'magnetometer_ga[0]':'MagX','magnetometer_ga[1]':'MagY','magnetometer_ga[2]':'MagZ'})
                
                
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


path = os.getcwd()
directory = os.path.join(path,r'Degradation Data')
if not os.path.exists(directory):
    os.makedirs(directory)

#Changes directory to put it into the new folder
os.chdir(directory)

Comb_Data = pd.ExcelWriter(platform + "Data.csv", engine='xlsxwriter')
data.to_excel(Comb_Data,sheet_name='Accel&Gyro',index=False)
data2.to_excel(Comb_Data,sheet_name='Magnetometer',index=False)
Aves.to_excel(Comb_Data,sheet_name='Mean',index=False)
Devs.to_excel(Comb_Data,sheet_name='Stdev',index=False)
Comb_Data.save()