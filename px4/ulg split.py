# -*- coding: utf-8 -*-
"""
Created on Tue Jul 28 13:05:58 2020

@author: het9t
"""


from subprocess import call
import os

dirpath = r'C:\Users\het9t\OneDrive\Documents\PX4 Summary Statistics Sheets\075'
os.chdir(dirpath)

filelist = []

for file in os.listdir(dirpath):
    if file.endswith('.ulg'):
        call(["ulog2csv",file])