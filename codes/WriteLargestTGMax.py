#!/usr/bin/env python2.7

# This code will use the file of maximum yearly tide gauge
# predictions and write a file that includes only the largest
# such changes, based on a user-specified threshhold. 

# set up
import sys
import os
import config
import numpy as np

tgDir = config.BaseDir+"data/TideGauge/"
ifn = tgDir+"TGMaxChange.txt"
ofn = tgDir+"LargestTGMaxChange.txt"

# threshhold -- above this we will write data to a new file
Thresh = 0.005

# load in data
InFile = np.loadtxt(ifn,dtype='float')

# initialize new matrix
TGList = []

for line in InFile:
    # read the max SL change
    dh = line[3]
    
    # skip if doesn't make the cut
    if dh < Thresh:
        continue
    # read in the rest
    TGNo = line[0]
    lat = line[1]
    lon = line[2]
    year = line[4]

    # Append this to the new list
    TGList.append([TGNo, lat, lon, dh, year])

# write to new file
TGArray = np.asarray(TGList)
np.savetxt(ofn, TGArray, delimiter = '\t')

print "successfully wrote "+str(len(TGList))+" TG predictions to new file."

print TGArray
