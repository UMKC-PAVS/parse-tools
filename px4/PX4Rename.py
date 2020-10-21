# -*- coding: utf-8 -*-
"""
Created on Tue Oct 20 22:41:09 2020

Rewrites PX4 csvs to correct naming structure
"""


def PX4Rename(directory,platform,currentstructure,group):
    import os
    import pandas as pd
    os.chdir(directory)
    filelist = []
    dummy = 001
    for file in os.listdir(directory):
        if file.endswith('.csv'):
            if file.startswith(currentstructure):
                os.rename(directory + file, directory + platform + "-" + group + "-" + dummy + '.csv')
                dummy += 1