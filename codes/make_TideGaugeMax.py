#!/usr/bin/env python2.7

# This code will make a file that includes all the maximum
# year-over-year increases in sea level at the points where
# tide gauges are located

# set up
import sys
import os
import config
from res_subr import GetIndex
from res_subr import GetMaxChange
from res_subr import GetMaxChangeAndTS
from res_subr import databases as DB
import numpy as np


#We only need to do this for GRanD
db,start,end = DB("G")

# for each point, extract the time series and find the largest point

# save the file
# tide gauge data dir
dataDir = config.BaseDir+"data/TideGauge/rlr_annual/"
tgdir = config.BaseDir+"data/TideGauge/"
tsDir = config.BaseDir+"time_series/"

# file where the locations are listed
tgfn = dataDir+"filelist.txt"
fpfn = tsDir+"TS.FP.res.Grand.txt"
#testfn = "LatLon.xy"

ofn = tgdir+"TGMaxChange.txt"

# read in the fingerprint file
print('Reading in fingerprint file... this may take a few minutes')
#latlon = np.loadtxt(testfn, dtype = 'float')
TSFP = np.loadtxt(fpfn,dtype='float')
print('done loading fingerprint')
# Read in tide gauge locations
TGList = []
TGFile = open(tgfn)

# loop over locations
for line in TGFile:
    # save location and tg number
    # TGList format:
    # [TG_No.] [Lat] [Lon] [Name] [?] [?] [?]
    TGNo = int(line.split(';')[0].strip())
    lat = float(line.split(';')[1].strip())
    lon = float(line.split(';')[2].strip())

    # file name for the time series
    tsofn = tgdir+'TideGaugePredictions/'+str(TGNo)+'.rlrpred.txt'

    # get the cell for the fingerprint associated with tg location
    #print ""
    cell = GetIndex(lat,lon)

    #print cell
    #print lat,lon
    #print latlon[cell]


    # find max change for that point
    dhMax, time, TGValues = GetMaxChangeAndTS(cell,TSFP)
    year = start + time
    TGList.append([TGNo, lat, lon, dhMax, year])

    # write predicted time series to file
    # Write array to right format
    TGTS = []
    for i,h in enumerate(TGValues):
        yeari = start + i
        #h = TGValues[i]
        TGTS.append([yeari,h])
    TGTSArray = np.asarray(TGTS)
    np.savetxt(tsofn, TGTSArray, delimiter = ';')

#sys.exit()
# write the tide gauge list to file
TGArray = np.asarray(TGList)

np.savetxt(ofn, TGArray, delimiter = '\t')


