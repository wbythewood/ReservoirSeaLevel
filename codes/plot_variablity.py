#!/usr/bin/env python2.7

# This script will plot the two sea level curves at a point for two
# fingerprints to compare the two. It is designed to help understand
# how important variability in lake level is on sea level in the 
# near-field.

import sys
from matplotlib import pyplot as plt
import math
import numpy as np
from datetime import date
from matplotlib import dates
from res_subr import GetIndex
from res_subr import databases as DB
import config

# usage
if len(sys.argv) != 2:
    print("\nThis code will plot two sea level curves for a single point:")
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
start2 = 1900
end2 = 2011

# directories
dataDir = config.BaseDir+'data/'
figDir = config.BaseDir+'figures/'
TSDir = config.BaseDir+'time_series/'
VarDir = config.BaseDir+'time_series/VAR/'

# files we will use
OrigTSFN = VarDir+'TS.point.res'+resNoS+'.Orig.txt'
VarTSFN = VarDir+'TS.point.res'+resNoS+'.VAR.txt'

# read in files
OTS = np.loadtxt(OrigTSFN)
VTS = np.loadtxt(VarTSFN)

# set up vectors
hO = []
tO = []
hV = []
tV = []

for i in OTS:
    tO.append(i[0])
    hO.append(i[1]*1000)
for j in VTS:
    tV.append(j[0])
    hV.append(j[1]*1000)


# Initialize the vector that has the dates saved
timeVector = range(start,end+1)


# Plot the curves
plt.plot(tO,hO, color='mediumblue', label = 'No Variability')
plt.plot(tV,hV, color='maroon', ls='dashed', label = 'With Variability')
plt.xlim(start2,end2)
plt.xlabel("Year")
plt.ylabel("Sea Level Change (mm)")
if resNo == 7:
    plt.title("Effect of lake level variability at Lake Guri")
    afn = figDir+"GuriVar.pdf"
elif resNo == 43:
    plt.title("Effect of lake level variability at Lake Powell")
    afn = figDir+"PowellVar.pdf"
plt.legend(loc=2)
fig = plt.gcf()
#fig.set_size_inches(8,4.5)
fig.savefig(afn)
plt.show()
plt.close()

