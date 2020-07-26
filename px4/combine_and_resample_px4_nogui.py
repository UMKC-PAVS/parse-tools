# -*- coding: utf-8 -*-
"""
Written by:     Shawn Herrington, Paul Klappa, Cody Smith, Demetri Reed
Date:           09/12/2019
Purpose:        Combine data recorded at disparate rates into a master file
Purpose:        Developed on faux data and then modified to work specifically
                with PX4 data which has been converted using the pyulog utility
                (specically the ulog2csv module)
Notes:          Modified to remove gui interaction so that script can be called
                from higher level parser script, also converted to function
                for easy calling from parent script
Notes:          Fastest sampling time is calculated automatically, it is tested
                working but if conditions change and it stops working it would 
                be easier to just type in max freq by hand than to troubleshoot
                or modify, parts of the code containing the min freq nonsense
                have been noted
Notes:          Currently the output is saved to a directory which is created
                in order to avoid having the "results.csv" script read as input
                data if this script is run in a directory where it has already
                been run previously, this could be improved in future versions
                by specifically ignoring csv files that are output by this
                script when we build the list of csv files to crawl
Notes:          Currently only tested in Python 2.7; although, the print
                functions at the end which are just for convenience may be the
                only part that needs modification to run on Python 3
Notes:          When you run the script select the directory of interest (in
                most cases this will be Test_##\FlightData\).  The script will
                read in all constituent csv files (stored in FlightData) then
                process the timestamp and do some important operations on the
                df before resampling to the minimum frequency and writing the
                contents to a file called 'results.csv' in a directory called
                'combined' which will be created if it does not already exist
Notes:          The script does not need to be copied and pasted into the
                directory of interest, that is handled by the askdirectory() 
                function
Notes:          To change the files which are added to the master csv, modify 
                the keywords_in_wanted_files list. To change the columns which 
                are included in the master csv, modify the keywords_for_columns
                list.
Notes:          To make the ulog2csv converter work, install pyulog in the 
                iPython console. To run commands from the console, you might 
                need to preface it with '!' otherwise there will be a syntax
                error
    
Changelog:
07/10/2020 by Thomas Cacy
Changed how the programs move through directories so it cleans up after itself
and moved the making of a directory to the program that uses it to be fully 
contained

04/17/2020 by Thomas Cacy
Changed what files are read into the program so that it only read the files we 
want. Added some code to only take in the columns we want and obfuscate 
some data. Fixed the 'Time' column so it is in seconds not milliseconds

09/12/2019 by Shawn Herrington
Fixed some bozo mistakes on the index renaming on the resampled array.  Was
resuing the time_properformat var from the big_df var but that var was being
ffill-ed by the resample command and giving time values that made no sense,
found a method to extract the datetime index as an int and all is working now

"""

import os
import pandas as pd
import numpy as np
import sys
from quat2eul import quat2eul
from make_plots import make_plots
from assign_names import assign_names
# from obfuscate_gps import obfuscate


def combine_and_resample_px4_nogui(input_path,file_prefix=''):
    
    #list of file keywords to identify the files we want
    keywords_in_wanted_files = ['gps_position','combined','magnetometer_0',
                                'input_rc','battery_status','attitude',
                                'control','air_data','vehicle_status_0']
    
    #list of key words to identify the columns we want
    keywords_for_columns = ['lat','lon','alt','hdop','vdop','mode_slot',
                            'accelerometer_m_s2[0]','accelerometer_m_s2[1]',
                            'accelerometer_m_s2[2]','gyro_rad[0]','gyro_rad[1]'
                            ,'gyro_rad[2]','magnetometer_ga[0]',
                            'magnetometer_ga[1]','magnetometer_ga[2]',
                            'rc_failsafe','voltage_v','rssi','q[0]',
                            'q[1]','q[2]','q[3]','baro_alt','nav_state',
                            'values[0]','values[1]','values[2]','values[3]',
                            'values[4]','values[5]','values[6]','values[7]',
                            'values[8]','values[9]','values[10]','values[11]',
                            'values[12]','values[13]','values[14]','values[15]'
                            ,'values[16]','values[17]','values[18]']
    # save the current path to a variable so we can return to it later
    original_path = os.getcwd()
    
    os.chdir(input_path)
       
    # get list of filenames in directory ending with csv
    list_of_filenames = [f for f in os.listdir('.') if f.endswith('.csv')]
    
    #remove the files we know we do not want from the list
    list_of_filenames = [item for item in list_of_filenames if any(word in item for word in keywords_in_wanted_files)]
    
     #check if list_of_filenames is populated and exit if it is
    if len(list_of_filenames) == 0:
        sys.exit("There are no files to process in " + input_path)  
    
    # create empty list so we can append to it
    list_of_df = []
        
    #empty list so we can append it
    reject_column_list = []
    
    #empty list to append
    new_headers = []
    
    # iterate through the csv in the current directory, create a df for each
    # filename, put the df into a list of other df
    for current_filename in list_of_filenames:
        
        # this is the important read, read in the data we care about, the index
        # is stored in column 0, the header is stored in row 0, pandas will 
        # name columns automatically for us using the header row
        df = pd.read_csv(current_filename, index_col=0, header=0)
        
        # get a list of all the headers in the csv
        column_headers = df.columns
        
        # create an empty list to append
        columns_to_keep = []
        
        # get a list of the columns we want to keep for each csv by iterating 
        # through the file and getting the headers
        
        for header in column_headers:
            #get the list of keywords
            for keyword in keywords_for_columns:
                #check if the keyword is on the header
                if keyword in header:
                    #the word lat and alt is used in other headers this takes 
                    #care of the problem
                    if keyword == 'lat' and header == 'lat':
                        columns_to_keep.append(header)
                        assign_names(keyword, new_headers)
                    if keyword == 'alt' and header == 'alt':
                        columns_to_keep.append(header)
                        assign_names(keyword, new_headers)
                        
                    # add the header to the list of headers to keep if it has
                    # the keyword by calling the assignname_ function
                    if keyword != 'lat' and keyword != 'alt':
                        columns_to_keep.append(header)
                        assign_names(keyword, new_headers)

        
        #change the list to just have the columns we want
        reject_column_list = [header for header in column_headers if header not in columns_to_keep]
       
        #drop all columns that we do not want
        df = df.drop(columns = reject_column_list)

        # store the current df (from a single csv) into the big list of dfs
        list_of_df.append(df)
           
        
    # create the big df by using the concat method called on a list of small df
    big_df = pd.concat(list_of_df, axis=0, ignore_index=False, sort=False)

    # sort on the timestamp column, otherwise the small df are stuck together 
    # end-to-end which isn't what we want
    big_df = big_df.sort_values(by='timestamp')
    
    # for px4 some data files start with 0 for timestamp, we don't want this, 
    # so we will just discard these rows for now
    big_df = big_df.drop(0, errors="ignore")
     
    # offset time to zero just because we can
    big_df.index = big_df.index - big_df.index[0] 
    
    # fill the missing spaces, use ffill to move the most recent valid observation
    # forward
    big_df = big_df.fillna(method='ffill')
    
    # fill the remaining na with 0, these only happen at the beginning where we
    # previously did not have any observations to pass forward
    big_df = big_df.fillna(0)
    
    # get rid of duplicate rows, not sure this is needed but keeping just in case
    # UPDATE:  definitely needed, first line gets rid of duplicate time entries
    big_df = big_df[~big_df.index.duplicated()]
    
    # this one gets rid of duplicated output data, not sure this is required
    big_df = big_df.drop_duplicates()
    
    # create a time delta column with the proper format, note the use of 10**6 to 
    # modify time stamp since timestamp for px4 data is in microseconds, 'S' means
    # that this function is expected time formated ins seconds so the easiest way
    # to fix it is just to convert the number to seconds before passing it
    big_df['time_properformat'] = pd.to_timedelta(big_df.index/10.0**6,'S')
    
    # switch the index of the big_df to proper time delta column
    big_df.index = pd.to_datetime(big_df.time_properformat)
    
    # fix this for 250Hz rate since the auto calculator is causing issues
    min_sampletime = .004
    freq_arg = int(min_sampletime*10**6)
    freq_type = 'U'
    
    # create the resampled  df
    resampled_df = big_df.asfreq(str(freq_arg)+freq_type, method='ffill')
    
    # get rid of the annoying time index, switch back to delta time in seconds
    resampled_df.index = resampled_df.index.values.astype(np.uint64)/1000000
    
    # get rid of the unused column before we send it to csv
    resampled_df = resampled_df.drop(columns=['time_properformat'])

    #assign the new headers to the columns
    resampled_df.columns = new_headers
    
    #call the quat2eul function to change the attitude to eul
    r,p,y = quat2eul(resampled_df['Att.Qx'],resampled_df['Att.Qy'],resampled_df['Att.Qz'],resampled_df['Att.Qw'])

    # add the pitch roll and yaw to the resampled_df
    resampled_df['Att.roll'] = r
    resampled_df['Att.pitch'] = p
    resampled_df['Att.yaw'] = y
    
    #drop the columns with the quat data in them
    resampled_df = resampled_df.drop(columns = ['Att.Qx','Att.Qy','Att.Qz','Att.Qw'])
    
    # check if folder exists and create if needed, this avoid the script trying
    # to read it's own results.csv as one of the constituent files if we run
    # this script on a directory where it has been run at least once previously
    if not os.path.exists('combined'):
        os.mkdir('combined')
    
    # write the result, we want to write the index column, we want to label the index
    # column, feel free to change the name
    resampled_df.to_csv(path_or_buf=os.path.join('combined',file_prefix+'_results.csv'),index=True,index_label='Time')
    
    print('Resampling complete.')
    print('Minimum sample time is:\t%f s\nThe corresponding frequency is:\t%f Hz\nOutput saved to:  %s' % (min_sampletime,1/min_sampletime,os.path.join('combined',file_prefix+'_results.csv')))
    
    # call the make_plot function and pass the location of the results file
    make_plots('combined'+'/'+file_prefix+'_results.csv')
    
    # go back to the original directory so we can iterate through the rest of 
    # the files
    os.chdir(original_path)
