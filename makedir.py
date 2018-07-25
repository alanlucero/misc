# -*- coding: utf-8 -*-
"""
Created on Wed Jul 25 14:43:33 2018

@author: lucero
"""

import os, datetime, time
ts = time.time()
st = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d %H.%M.%S')

directory = './'+ st +' /.'

def createFolder(directory):
    try:
        if not os.path.exists(directory):
            os.makedirs(directory)
            print('Folder ' + st + ' in directory ' + directory + 'has been successfully created.')
    except OSError:
        print ('Error: Creating directory. ' +  directory)

#createFolder(directory)