

import os
import pandas as pd
import numpy as np



list_of_filenames = [f for f in os.listdir(r'C:\Users\het9t\OneDrive\Documents\PX4 Summary Statistics Sheets\Ardupilot') if f.endswith('.csv')]
list_of_df = []

dont_reject_list = ['AETR','AHR2','BARO','MODE','BAT','CTUN','GPA','GPS','RAD','IOMC','IMU','MAG','NTUN','POWR','RCIN','STAT','RSSI']

list_of_filenames = [item for item in list_of_filenames if any(word in item for word in dont_reject_list)]

os.chdir(r'C:\Users\het9t\OneDrive\Documents\PX4 Summary Statistics Sheets\Ardupilot')

for current_filename in list_of_filenames:
    
    print('current_filename: '+current_filename)
    
    df = pd.read_csv(current_filename, index_col=1, header=0)
            # create list of df columns
    list_of_column_names = list(df.columns)
    list_of_new_column_names = []


            # store the current df (from a single csv) into the big list of dfs
    list_of_df.append(df)


rcou = [f for f in os.listdir(r'C:\Users\het9t\OneDrive\Documents\PX4 Summary Statistics Sheets\Ardupilot') if f.endswith('RCOU.csv')]
df = pd.read_csv(rcou[0],index_col=1,header=0)
df = df.rename(columns={'C1':'RCOUTC1','C2':'RCOUTC2','C3':'RCOUTC3','C4':'RCOUTC4','C5':'RCOUTC5','C6':'RCOUTC6','C7':'RCOUTC7','C8':'RCOUTC8','C9':'RCOUTC9','C10':'RCOUTC10','C11':'RCOUTC11','C12':'RCOUTC12','C13':'RCOUTC13','C14':'RCOUTC14',})
list_of_df.append(df)    


        # create the big df by using the concat method called on a list of small df
big_df = pd.concat(list_of_df, axis=0, ignore_index=False, sort=False)

        # sort on the timestamp column, otherwise the small df are stuck together end
        #-to-end which isn't what we want
#        big_df = big_df.sort_index(axis=0)
big_df.sort_index(axis=0,inplace=True)

        # for px4 some data files start with 0 for timestamp, we don't want this, so
        # we will just discard these rows for now
big_df = big_df.drop(0, errors="ignore")

big_df = big_df[big_df.columns.drop(list(big_df.filter(regex='timestamp')))]

        # offset time to zero just because we can
big_df.index = big_df.index - big_df.index[0]

        # fill the missing spaces, use ffill to move the most recent valid observation
        # forward
big_df = big_df.fillna(method='ffill')
big_df = big_df.fillna(method='bfill')

        # fill the remaining na with 0, these only happen at the beginning where we
        # previously did not have any observations to pass forward
big_df = big_df.fillna(0)

        # get rid of duplicate rows, not sure this iis needed but keeping just in case
        # UPDATE:  definitely needed, first line gets rid of duplicate time entries
big_df = big_df[~big_df.index.duplicated()]
        # this one gets rid of duplicated output data, not sure this is required
big_df = big_df.drop_duplicates()

        # create a time delta column with the proper format, note the use of 10**6 to
        # modify time stamp since timestamp for px4 data is in microseconds, 'S' means
        # that this function is expected time formated ins seconds so the easiest way
        # to fix it is just to convert the number to seconds before passing it
big_df['time_properformat'] = pd.to_datetime(big_df.index,unit='us')

        # switch the index of the big_df to proper time delta column
big_df.index = pd.to_datetime(big_df.time_properformat)

freq_arg = 20
freq_type = 'L'

        # create the resampled  df
resampled_df = big_df.asfreq(str(freq_arg)+freq_type,method='ffill')

        # get rid of the annoying time index, switch back to delta time in seconds
resampled_df.index = resampled_df.index.values.astype(np.uint64)/1000

        # get rid of the unused column before we send it to csv
resampled_df = resampled_df.drop(columns=['SAcc','Rsn','ModeNum','Q1','Q2','Q3','Q4','RemRSSI','TxBuf','VV','Delta','RemNoise','Noise','RxErrors','Fixed','VAcc','HAcc','time_properformat','VoltR','Curr','CurrTot','EnrgTot','Res','NavRoll','NavPitch','ThrOut','RdrOut','Aspd','OfsX','OfsY','OfsZ','MOfsX','MOfsY','MOfsZ','S','WpDist','TBrg','NavBrg','AltErr','XT','XTi','ThrDem','Press','CRt','GndTemp', 'Temp' ,'Status' , 'GMS','GWk','NSats', 'U', 'Spd','VZ','EG','EA','T','GH','AH','GHz','AHz','GCrs','ArspdErr','TLat','TLng','TAlt','Vcc','VServo','Flags','Safety','Hit','Stage','Still','Armed','Crash','isFlyProb','isFlying','SMS','Offset'])

resampled_df = resampled_df.rename(columns={"Health":"RCfailsafe",'C3':'C3:Throttle',"Lat":"GPS.Lat","Lng":"GPS.Lon","Alt":"GPS.Alt","GyrX" : "GyroX", "GyrY" : "GyroY", "GyrZ" : "GyroZ","AccZ": "AccelZ", "AccX":"AccelX","AccY":"AccelY"})


#Normalize GPS signals 
xx = resampled_df['GPS.Lat'].iloc[0]
yy = resampled_df['GPS.Lon'].iloc[0]
zz = resampled_df['GPS.Alt'].iloc[0]

resampled_df['GPS.Lat'] = resampled_df["GPS.Lat"] - xx

resampled_df['GPS.Lon'] = resampled_df["GPS.Lon"] - yy

#resampled_df['GPS.alt'] = resampled_df["GPS.alt"] - zz

#resampled_df = resampled_df.sub([1], resampled_df[1,0])

#send it to CSV
#resampled_df.to_csv('UDF.csv')
