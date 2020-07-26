# -- coding: utf-8 --
"""

Written by:     Shawn Herrington, Simeon Karnes, Cody Smith
Date:           9/16/2019
Purpose:        Modified from simple example and converted to create and save
                plots automatically inside of automated parser
Notes:          Modified original file to accept filename from auto parser,
                most of the rest of the script is unchanged
Change Log:     Thomas Cacy
Date:           07/08/2020
                changed so it works with unified parsing script's new headers
                and removed convertions that happen in the combine_and_resample
                script. Removed gragh of trigger. Moved the creation of the 
                'Plots' directory to this program. Added var names for paths
                so the same calculation is not preformed many times. Program 
                will not figure out what plots are missing and only save those
                it needs
"""

import pandas as pd
import os
from matplotlib import pyplot as plt
#from tkinter.filedialog import askopenfilename
# get filename from the dialogue
#filename = askopenfilename(title='Select file',filetypes=[('csv files','*.csv')])

def make_plots(filename_in):
       
    filename = os.path.join(os.getcwd(),filename_in)
    
    print('Creating and saving plots from:')
    
    print(filename_in)
    
    just_the_pathname, just_the_filename = os.path.split(filename)
    #illumination = int(input('Time of illumination (s):     '))
    
    plot_r_p_y = True
    plot_accel = True
    plot_gyro = True
    plot_mag = True
    plot_batt = True
    plot_baro = True
    plot_GPS = True
    plot_alt = True
    plot_vdop_hdop = True
    plot_mode = True
    plot_rc = True
    plot_channels = True
    
    # directory that contains Plots directory
    path_to_Plots = os.path.join(os.path.dirname(os.path.dirname(just_the_pathname)),'Plots')
    
    # path to the file
    dir_Plots = path_to_Plots+'/'+just_the_filename[:-4]
    
    # plot file location
    r_p_y_path = dir_Plots+'_R_P_Y_State.png'
    accel_path = dir_Plots+'_Accelerometer.png'
    gyro_path = dir_Plots+'_Gyroscope.png'
    mag_path = dir_Plots+'_Magnetometer.png'
    batt_path = dir_Plots+'_Battery_voltage.png'
    baro_path = dir_Plots+'_BaroAlt.png'
    GPS_path = dir_Plots+'_GSP_lat_lon.png'
    alt_path = dir_Plots+'_GPS_alt.png'
    vdop_hdop_path = dir_Plots+'_vdop_hdop.png'
    mode_path = dir_Plots+'_Mode.png'
    channels_path = dir_Plots+'_Channels.png'
    rc_path = dir_Plots+'_RC.png'
    
    # make a directory to save the plots if one does not exist and determine 
    # what needs to be plotted
    if(not(os.path.isdir(path_to_Plots))):
        os.mkdir(path_to_Plots)
    if os.path.isfile(r_p_y_path):
        plot_r_p_y = False
    if os.path.isfile(accel_path):
        plot_accel = False
    if os.path.isfile(gyro_path):
        plot_gyro = False
    if os.path.isfile(mag_path):
        plot_mag = False
    if os.path.isfile(batt_path):
        plot_batt = False
    if os.path.isfile(baro_path):
        plot_gyro = False
    if os.path.isfile(GPS_path):
        plot_GPS = False
    if os.path.isfile(alt_path):
        plot_alt = False
    if os.path.isfile(vdop_hdop_path):
        plot_vdop_hdop = False
    if os.path.isfile(rc_path):
        plot_rc = False
    if os.path.isfile(channels_path):
        plot_channels = False
    
    # read in the data to a var called df (dataframe)
    df = pd.read_csv(filename, index_col=0, header=0)
    df['time_seconds'] = df.index
    
    # check if the r p y plot exists
    if plot_r_p_y:
        
        # try block to handle not finding the right data
        try:

            #Create a new figure to graph r p y
            plt.figure()
            plt.plot(df['time_seconds'],df["Att.roll"])
            plt.plot(df['time_seconds'],df["Att.pitch"])
            plt.plot(df['time_seconds'],df["Att.yaw"])
            #plt.axvline(x=illumination, linewidth=0.5, color='red')
            plt.title('R/P/Y')
            plt.xlabel('Time, s')
            plt.ylabel('Radians per Sec')
            plt.legend(['Roll','Pitch','Yaw'])
            
            plt.savefig(r_p_y_path,dpi=600,bbox_inche='tight')
            
            print('Plot Roll Pitch Yaw')
        
        # print report
        except: print('Roll Pitch Yaw data not found')
        
    else: 
        print('Roll Pitch Yaw plot already exists for: '+just_the_filename[:-4])
    
    # check if the accel plot exists
    if plot_accel:
        
        # try block to handle not finding the right data
        try:
            
            #Graph Accelerometer
            plt.figure()
            plt.plot(df['time_seconds'],df['Accel.x'])
            plt.plot(df['time_seconds'],df['Accel.y'])
            plt.plot(df['time_seconds'],df['Accel.z'])
            #plt.axvline(x=illumination, linewidth=0.5, color='red')
            plt.title('Accelerometer')
            plt.xlabel('Time, s')
            plt.ylabel('m/s^2')
            plt.legend(['x-axis','y-axis','z-axis'])
            plt.savefig(accel_path,dpi=600,bbox_inche='tight')
            
            print('Plot Accelerometer')
        
        # print report
        except: print('Accelerometer data not found')
        
    else: 
        print('Accelerometer plot already exists for: '+just_the_filename[:-4])
        
    # check if gyro plot exist
    if plot_gyro:
        
        # try block to handle not finding the right data
        try:
            
            #Graph Gyroscope
            plt.figure()
            plt.plot(df['time_seconds'],df['Gyro.x'])
            plt.plot(df['time_seconds'],df['Gyro.y'])
            plt.plot(df['time_seconds'],df['Gyro.z'])
            #plt.axvline(x=illumination, linewidth=0.5, color='red')
            plt.title('Gyroscope')
            plt.xlabel('Time, s')
            plt.ylabel('Radians')
            plt.legend(['x-axis','y-axis','z-axis'])
            plt.savefig(gyro_path,dpi=600,bbox_inche='tight')
            
            print('Plot Gyroscope')
            
        except: print('Gyroscope data not found')
    
    # print report        
    else: 
        print('Gyro plot already exists for: '+just_the_filename[:-4])
            
    # check if the mag plot exists
    if plot_mag:
        
        # try block to handle not finding the right data
        try:

            #Create a new figure to graph mag
            plt.figure()
            plt.plot(df['time_seconds'],df["Mag.x"])
            plt.plot(df['time_seconds'],df["Mag.y"])
            plt.plot(df['time_seconds'],df["Mag.z"])
            #plt.axvline(x=illumination, linewidth=0.5, color='red')
            plt.title('Mag')
            plt.xlabel('Time, s')
            plt.ylabel('Gauss')
            plt.legend(['X','Y','Z'])
            
            plt.savefig(mag_path,dpi=600,bbox_inche='tight')
            
            print('Plot Mag')
        
        # print report
        except: print('Mag data not found')
        
    else: 
        print('Magnetometer plot already exists for: '+just_the_filename[:-4])
        
    # check if the batt plot exists
    if plot_batt:
        
        # try block to handle not finding the right data
        try:

            #Create a new figure to graph batt
            plt.figure()
            plt.plot(df['time_seconds'],df["Voltage"])
            #plt.axvline(x=illumination, linewidth=0.5, color='red')
            plt.title('Battery_Voltage')
            plt.xlabel('Time, s')
            plt.ylabel('Volts')
            plt.legend(['Battery_Voltage'])
            
            plt.savefig(batt_path,dpi=600,bbox_inche='tight')
            
            print('Plot Battery Voltage')
        
        # print report
        except: print('Voltage data not found')
        
    else: 
        print('Battery Voltage plot already exists for: '+just_the_filename[:-4])
    
    # check if the baro plot exists
    if plot_baro:
        
        # try block to handle not finding the right data
        try:

            #Create a new figure to graph baro
            plt.figure()
            plt.plot(df['time_seconds'],df["BaroAlt"])
            #plt.axvline(x=illumination, linewidth=0.5, color='red')
            plt.title('BaroAlt')
            plt.xlabel('Time, s')
            plt.ylabel('Meters')
            
            plt.savefig(baro_path,dpi=600,bbox_inche='tight')
            
            print('Plot Barometer')
        
        # print report
        except: print('Baro Alt data not found')
        
    else: 
        print('Baro Alt plot already exists for: '+just_the_filename[:-4])
    
    # check if the GPS plot exists
    if plot_GPS:
        
        # try block to handle not finding the right data
        try:

            #Create a new figure to graph gps
            plt.figure()
            plt.plot(df['GPS.lat'],df["GPS.lon"])
            #plt.axvline(x=illumination, linewidth=0.5, color='red')
            plt.title('GPS')
            plt.xlabel('Latitude')
            plt.ylabel('Longitude')
            
            plt.savefig(GPS_path,dpi=600,bbox_inche='tight')
            
            print('Plot GPS Lat and Lon')
        
        # print report
        except: print('Lat Lon data not found')
        
    else: 
        print('Lat Lon plot already exists for: '+just_the_filename[:-4])
    
    # check if the alt vdop and hdop plot exists
    if plot_alt:
        
        # try block to handle not finding the right data
        try:

            #Create a new figure to graph alt
            plt.figure()
            plt.plot(df['time_seconds'],df["GPS.alt"])
            #plt.axvline(x=illumination, linewidth=0.5, color='red')
            plt.title('Alt')
            plt.xlabel('Time, s')
            plt.ylabel('Meters')
            
            plt.savefig(alt_path,dpi=600,bbox_inche='tight')
            
            print('Plot GPS Alt')
        
        # print report
        except: print('Alt Vdop')
        
    else: 
        print('Alt plot already exists for: '+just_the_filename[:-4])
    
    # check if the vdop and hdop
    if plot_vdop_hdop:
        
        # try block to handle not finding the right data
        try:
            
            # Create a new figure to gragh vdop and hdop
            plt.figure()
            plt.plot(df['time_seconds'],df['GPS.vdop'])
            plt.plot(df['time_seconds'],df['GPS.hdop'])
            plt.title('VDOP and HDOP')
            plt.xlabel('Time, s')
            plt.ylabel('')
            plt.legend(['VDOP','HDOP'])
            
            plt.savefig(vdop_hdop_path,dpi=600,bbox_inche='tight')
            
            print('Plot VDOP and HDOP')
            
        # print report
        except: print('VDOP and HDOP date not found')
            
    else:
        print('VDOP and HDOP plots alread exist for: '+just_the_filename[:-4])
        
    # check if the mode plot exists
    if plot_mode:
        
        # try block to handle not finding the right data
        try:

            #Create a new figure to graph Mode
            plt.figure()
            plt.plot(df['time_seconds'],df["Mode"])
            #plt.axvline(x=illumination, linewidth=0.5, color='red')
            plt.title('Flight Mode')
            plt.xlabel('Time, s')
            plt.ylabel('Mode')
            plt.text(2, .4, "0 = Manual\n1.1 = Stabilized\n1.2 = Altitude\n2.0 = Position\n4.0 = Mission",
                    bbox=dict(boxstyle = "square",
                  facecolor = "white"))
            
            plt.savefig(mode_path,dpi=600,bbox_inche='tight')
            
            print('Plot Mode')
        
        # print report
        except: print('Flight Mode data not found')
        
    else: 
        print('Mode plot already exists for: '+just_the_filename[:-4])
    
    # check if the rc exists
    if plot_channels:
        
        # try block to handle not finding the right data
        try:

            #Create a new figure to graph channels
            plt.figure()
            plt.plot(df['time_seconds'],df["Channels_in.0"])
            plt.plot(df['time_seconds'],df["Channels_in.1"])
            plt.plot(df['time_seconds'],df["Channels_in.2"])
            plt.plot(df['time_seconds'],df["Channels_in.3"])
            plt.plot(df['time_seconds'],df["Channels_in.4"])
            plt.plot(df['time_seconds'],df["Channels_in.5"])
            
            
            plt.title('RC channels')
            plt.xlabel('Time, s')
            plt.ylabel('')
            plt.legend(['Channel 0','Channel 1','Channel 2','Channel 3','Channel 4','Channel 5'])
            
            plt.savefig(channels_path,dpi=600,bbox_inche='tight')
            
            print('Plot Channels')
        
        # print report
        except: print('RC channels not found')
        
    else: 
        print('Channels plot already exists for: '+just_the_filename[:-4])
        
    # check if the rc exist
    if plot_rc:
        
        # try block to handle not finding the right data
        try:
            
            # Create a new figure to gragh rc
            plt.figure()
            plt.plot(df['time_seconds'],df["RC.Signalstrength"])
            plt.plot(df['time_seconds'],df["RC.Failsafe"])
            
            plt.title('RC in')
            plt.xlabel('Time, s')
            plt.ylabel('')
            plt.legend(['Signal Strength','Failsafe'])
            
            plt.savefig(rc_path,dpi=600,bbox_iche='tight')
            
            print('Plot RC')
        
        # print report
        except: print('RC in data not found')
     
    else:
        print('RC plots already exist for: '+just_the_filename[:-4])
        
    # close all plots
    plt.close('all')