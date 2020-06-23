#!/usr/bin/env python2.7

# This code will make a series of files of predicted tide gauge
# time series

# set up
import sys
import os
import config
from res_subr import GetIndex
from res_subr import GetMaxChange
from res_subr import databases as DB
import numpy as np


#We only need to do this for GRanD
db,start,end = DB("G")
PointList = [
[5.617,0.000],
[49.233,-68.133],
[5.265,103.187],
[48.483,-68.517],
[58.093,11.833],
[58.348,11.895]
]

# for each point, extract the time series 

# tide gauge data dir
dataDir = config.BaseDir+"data/TideGauge/rlr_annual/"
tgdir = config.BaseDir+"data/TideGauge/"
tsDir = config.BaseDir+"time_series/"

# file where the locations are listed
tgfn = dataDir+"filelist.txt"
fpfn = tsDir+"TS.FP.res.Grand.txt"
#testfn = "LatLon.xy"

ofn = tgdir+"PointTS.txt"

# read in the fingerprint file
print('Reading in fingerprint file... this may take a few minutes')
#latlon = np.loadtxt(testfn, dtype = 'float')
TSFP = np.loadtxt(fpfn,dtype='float')
print('done loading fingerprint')
# Read in tide gauge locations
TGList = []
TGFile = open(tgfn)

# loop over locations
for line in PointList:
    # save location and tg number
    # TGList format:
    # [TG_No.] [Lat] [Lon] [Name] [?] [?] [?]
    TGNo = int(line.split(';')[0].strip())
    lat = float(line.split(';')[1].strip())
    lon = float(line.split(';')[2].strip())

    # get the cell for the fingerprint associated with tg location
    #print ""
    cell = GetIndex(lat,lon)

    #print cell
    #print lat,lon
    #print latlon[cell]


    # find max change for that point
    dhMax, time = GetMaxChange(cell,TSFP)
    year = start + time
    TGList.append([TGNo, lat, lon, dhMax, year])

#sys.exit()
# write the tide gauge list to file
TGArray = np.asarray(TGList)

np.savetxt(ofn, TGArray, delimiter = '\t')


