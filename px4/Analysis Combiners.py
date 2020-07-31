# -*- coding: utf-8 -*-
"""

Analysis combiners

@author: Harrison Terry

Combines all previously created Statistical csvs into one concatenated file

Not ready for running 

"""

import os
import pandas as pd

#Overarching folder that holds subfolders with combined files
src_dir = r'C:\Users\het9t\OneDrive\Documents\PX4 Summary Statistics Sheets\075'
#src_dir= r'C:\Users\het9t\OneDrive\Documents\PX4 Summary Statistics Sheets\complete'
#Directory for degradation files
dst_dir= r'C:\Users\het9t\OneDrive\Documents\PX4 Summary Statistics Sheets\complete'

name = 'PX4-075_3_05'

os.chdir(src_dir)

files_list = []
for root, dirs, files in os.walk(src_dir):
    for f in files:
        if f.startswith(name):
            if f.endswith('.csv'):
                df3 = pd.read_csv(f)
                files_list.append(df3)            
        #if f.endswith('Statistics.csv'):
         #   shutil.copy(os.path.join(root,f), dst_dir)
         
frame = pd.concat(files_list)

#frame = frame.drop(['Unnamed: 0'],axis=1)

os.chdir(dst_dir)

frame.to_csv(name + '-Data.csv')