#!/usr/bin/env python3.7

import sys
import os
import math
import numpy as np
from time import gmtime, strftime

import config
from res_subr import databases as DB 
from res_subr import read_res_fp as rf

# This code is intended to make a single fingerprint file that for all of 
# the reservoirs in the Const and Plan dataset. Should be okay to run only once. 

if len(sys.argv) != 2:
    print("\nThis code will combine all reservoir fingerprints for the two ")
    print(" databases Const and Plan. This code only needs to be run once. \n")
    print("Usage:")
    print(sys.argv[0]+" DB_name \n")
    print("DB_names are: \nG = GRanD\nC = under Construction\nP = Planned")
    sys.exit()

# set up some things

#get db info
db,start,end = DB(sys.argv[1])
if db == "Grand":
    print("you don't want to use this code with GRanD. Exiting...")
    sys.exit()
fpDir = config.FPDir+db+'/'

volDir = config.BaseDir+'data/'
DataFn = volDir+'Res.'+db+'.txt'

# where we will put the fingerprints
# one large matrix:
ofn = config.FPDir+db+"/seagl_grid_All.txt"

nr = config.nr
nc = config.nc

if (os.path.isfile(ofn) == True):
    print("Total fingerprint file already exists... do you want to continue?")
    ans = raw_input('>> (y|n) ')
    if ans == 'n':
        sys.exit()
    elif ans == 'y':
        os.remove(ofn)
    else:
        print("not recognized, please enter 'y' or 'n'!")
        sys.exit()

# get volumes
ResNos = []
Vols = []
Data = np.loadtxt(DataFn)
for i in Data:
    ResNos.append(int(i[0]))
    Vols.append(i[1])
NoOfRes = len(ResNos)

# make the new fingerprint file
FPTot = np.zeros((nr,nc))
for i in np.arange(NoOfRes):
    ResNo = ResNos[i]
    Vol = Vols[i]
    # debug
    if ResNo > 9999:
        continue
    # fingerprint file name
    fpFn = fpDir+"seagl_grid_"+str(ResNo)+".txt"
    # print status updates
    if ResNo%50 == 0:
        time = strftime("%H:%M:%S")
        print("Beginning fingerprint for Res number "+str(ResNo)+" --- "+time)
    # Read in fingerprint
    try:
        fp = np.loadtxt(fpFn)
    except:
        print("Could not locate fingerprint... skipping reservoir "+str(ResNo))
        continue
    # Scale fingerprint according to volume 
    fpScale = np.multiply(fp,Vol)
    # add fp to matrix
    FPTot = np.add(FPTot,fpScale)

# write final matrix
np.savetxt(ofn, FPTot, delimiter = '\t')

time = strftime("%H:%M:%S")
print("\t...Done!")
print("\t\t---"+time)
    
