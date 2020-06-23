#!/usr/bin/env python2.7

# This script will plot the two sea level curves at a point for two
# fingerprints to compare the two. It is designed to help understand
# how important variability in lake level is on sea level in the 
# near-field.

import os
import sys
from matplotlib import pyplot as plt
import math
import numpy as np
from datetime import date
from matplotlib import dates
from res_subr import GetIndex,GetMaxChangeAndTS
from res_subr import databases as DB
import config

# usage
if len(sys.argv) != 2:
    print("\nThis code will write to file two sea level curves for a single point:")
    print(" One for the regular time series,")
    print(" and one for the time series that includes one reservoir's variable")
    print("  height from satellite altimetry data. \n")
    print("Only works for GRanD database reservoirs. \n")
    print("Usage:")
    print(sys.argv[0]+" ResNo\n")
    sys.exit()

#which reservoir
resNo = int(sys.argv[1])
resNoS = str(resNo)

# set up
db,start,end = DB('G')

# directories
dataDir = config.BaseDir+'data/'
figDir = config.BaseDir+'figures/'
TSDir = config.BaseDir+'time_series/'
VarDir = config.BaseDir+'time_series/VAR/'

# files we will use
ResInfoFN = dataDir+'Res.Grand.txt'
OrigFPFN = TSDir+'TS.FP.res.Grand.txt'
VarFPFN = VarDir+'TS.FP.Grand.var'+resNoS+'.txt'

# output files
OrigTSFN = VarDir+'TS.point.res'+resNoS+'.Orig.txt'
VarTSFN = VarDir+'TS.point.res'+resNoS+'.VAR.txt'

# check to see if you want to do this again...
if os.path.exists(OrigTSFN):
    print("Files for Reservoir "+resNoS+" already exist. Do you want to overwrite them?")
    ans = raw_input('>> y|n ')
    if ans == 'n':
        sys.exit()
    elif ans == 'y':
        os.remove(OrigTSFN)
        os.remove(VarTSFN)
    else:
        print("not recognized, please enter 'y' or 'n'!")
        sys.exit()

#location to check
ResInfo = np.loadtxt(ResInfoFN)
for res in ResInfo:
    if int(res[0]) == resNo:
        print("getting info for reservoir "+resNoS+"...")
        latc = float(res[5])
        lonc = float(res[4])

#find closest grid point
cell = GetIndex(latc,lonc)

# Read in the fingerprint curves
print("reading fingerprint file without variability...")
OrigFP = np.loadtxt(OrigFPFN)
print("reading fingerprint file with variability...")
VarFP = np.loadtxt(VarFPFN)

# Pull the curve from each file
#noVarSeaLevel = []
print("Retrieving sea level changes near reservoir...")
OdhMax, Otime, O_SLValues = GetMaxChangeAndTS(cell,OrigFP)
VdhMax, Vtime, V_SLValues = GetMaxChangeAndTS(cell,VarFP)

OSL = []
for i,h in enumerate(O_SLValues):
    year = start+i
    OSL.append([year,h])

# Pull the curve from the other file
VSL = []
for j,h in enumerate(V_SLValues):
    year = start+j
    VSL.append([year,h])

OArray = np.asarray(OSL)
VArray = np.asarray(VSL)

print("Writing files.")
np.savetxt(OrigTSFN, OArray, delimiter = '\t')
np.savetxt(VarTSFN, VArray, delimiter = '\t')

