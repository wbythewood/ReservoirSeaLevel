#!/usr/bin/env python3.7
import sys
import os
import math
import numpy as np
from time import gmtime, strftime

import config
from res_subr import databases as DB
from res_subr import read_res_fp as rf

# This code will make a series of matrices that show the fingerprint of 
# sea level change for each year in the database.
#
# william b hawley
# whawley@seismo.berkeley.edu

# usage
if len(sys.argv) != 2:
    print("\nThis code will read the reservoir timeseries file and")
    print(" the associated reservoir fingerprints to generate a")
    print(" sea level time series file. \n")
    print("There is one fingerprint for each year.\n")
    print("Usage:")
    print(sys.argv[0]+" DB_name\n")
    print("DB_names are: \nG = GRanD\nC = under Construction\nP = Planned")
    sys.exit()

# set up paths
ts_path = config.BaseDir+'time_series/'

# set up constants
nr = config.nr
nc = config.nc
ne = nr*nc
eus = config.eus

#get db name
db,start,end = DB(sys.argv[1])
fpDir = config.FPDir+'/'+db+'/'

# where we will put the fingerprints
ofDir = ts_path+db+'/'
if os.path.isdir(ofDir) == False:
    os.mkdir(ofDir)
tTot = end+1-start

# read in the volumes
ResFn = ts_path+"TS.res."+db+".txt"         # filename
ResTS = np.loadtxt(ResFn,delimiter='\t')    # matrix
NoOfRes = len(ResTS)+1                      # the number of reservoirs
# for testing...
#NoOfRes = 1                               

# Initialize the matrix
# row for each year, fp assigned to a line
Matrix = np.zeros((tTot,ne))

# loop over reservoirs
for ResNo in range(1,NoOfRes):
    if ResNo == 1:
        print("Loading fingerprints, this will take a few minutes.")
        time = strftime("%H:%M:%S")
        print("Beginning with fingerprint for Res number "+str(ResNo)+" at "+time)
    if ResNo%400 == 0:
        time = strftime("%H:%M:%S")
        print("Beginning fingerprint for Res number "+str(ResNo)+" --- "+time)
    # Get volume
    vols = ResTS[ResNo-1]
    # Read in fingerprint
    try:
        fp = rf(fpDir,ResNo)
    except:
        print("Could not locate fingerprint... skipping reservoir "+str(ResNo))
        continue

    # loop over years
    for t,v in enumerate(vols):
        # t is years since start
        # v is vol for that t
        fpYr = np.multiply(fp,v)
        #print(np.amax(fpYr))
        Matrix[t]+=fpYr
    # debug... 
    #if ResNo > 10:
        #break

time = strftime("%H:%M:%S")
print("Reading reservoir fingerprints complete --- "+time)
# Now we have the large matrix... two options:
# (2) Save as individual files by year
for t,fp in enumerate(Matrix):
    Year = t+start
    print ("writing year "+str(Year))
    ofn = ofDir+'FP.'+str(Year)+'.txt'
    np.savetxt(ofn,fp,delimiter='\t')

time = strftime("%H:%M:%S")
print("\t...Done!")
print("\t\t---"+time)

