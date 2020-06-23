#!/usr/bin/env python3.7

# This code will make a fingerprint for either a single reservoir, or for a year.
# william b hawley
# whawley@seismo.berkeley.edu

import sys
import os
import subprocess
from res_subr import databases as DB
from res_subr import read_res_fp as rf 
from res_subr import diff_fp as df 
from res_subr import GetLatLon as gl
from res_subr import GetLatLonV as glv
from res_subr import writeXYZ as wxyz
import numpy as np
import config

# usage:
if len(sys.argv) < 3:
    print("\nThis code will print a fingerprint, either for a single reservoir")
    print(" or for a specified time range. \n")
    print("Usage:")
    print(sys.argv[0]+" DB_name r|t [ResNo] | [YearBegin YearEnd]\n")
    print("DB_names are: \nG = GRanD\nC = under Construction\nP = Planned\nF = Future (C+P)")
    print("[ResNo] = All to plot all reservoirs for a database")
    print(" To print all future time, include F as the first arg, na as the second")
    sys.exit()

#get db name
db,dbStart,dbEnd = DB(sys.argv[1])
rfpDir = config.FPDir+db+'/'
tfpDir = config.BaseDir+'time_series/'+db+'/'
ofng = "gridinp.txt"
DataFN = config.BaseDir+'data/Res.'+db+'.txt'
FPFigDir = config.BaseDir+'figures/Fingerprints/'

if os.path.isdir(FPFigDir) == False:
    os.mkdir(FPFigDir)

# Decide if Reservoir or Timeseries
# then get the fingerprint
RT = sys.argv[2]

# Reservoir
if RT == 'r':
    if len(sys.argv) != 4:
        print("Error interpreting arguments. For Reservoir option, Usage:")
        print(sys.argv[0]+" DB_name r resNo\n")
        sys.exit()
    resNo = sys.argv[3]

    # get volume info
    Data = np.loadtxt(DataFN)
    ResNos = []
    Vols = []
    if (resNo != 'All'):
        for i in Data:
            ResNos.append(int(i[0]))
            Vols.append(i[1])
        index = ResNos.index(int(resNo))
        Vol = Vols[index]

    print("Plotting fingerprint for reservoir "+str(resNo))

    # Get the reservoir fingerprint
    print("getting fingerprint...")
    fp = rf(rfpDir, resNo)
    if (resNo != 'All'):
        fp = np.multiply(fp,Vol)

    # define title for plot
    Title = "Fingerprint of Reservoir "+db+" - "+str(resNo)

    # define file name
    ofn = FPFigDir+"FP_"+db+"_R"+str(resNo)+".pdf"

# Difference between years
elif RT == 't':
    if len(sys.argv) != 5:
        print("Error interpreting arguments. For Timeseries option, Usage:")
        print(sys.argv[0]+" DB_name t YearBegin YearEnd\n")
        sys.exit()
    Begin = int(sys.argv[3])
    End = int(sys.argv[4])
    if Begin > End:
        print("Time should not run backwards. Ensure start time is before end time...")
        sys.exit()
    print("Plotting fingerprint from "+str(Begin)+" to "+str(End))

    # extract the fingerprint
    print("getting fingerprint...")
    fpB = tfpDir+'FP.'+str(Begin)+'.txt'
    fpE = tfpDir+'FP.'+str(End)+'.txt'
    fp = df(fpB,fpE)

    # define title for plot
    Title = "Fingerprint of change between "+str(Begin)+" and "+str(End)

    # define file name
    ofn = FPFigDir+"FP_"+db+"_"+str(Begin)+"-"+str(End)+".pdf"

# hacky future case because my hard drive is read-only right now...
elif RT == 'na':

    # the databases
    cdb,a,b = DB("C")
    pdb,a,b = DB("P")

    # the FP directories
    cfpDir = config.FPDir+cdb+'/'
    pfpDir = config.FPDir+pdb+'/'

    # not in the same place anymore... 
    fp = rf(config.FPDir, "All") 

    Title = "Fingerprint of Future Construction"
    ofn = FPFigDir+"FP_Future.pdf"

    
else:
    print(RT+": Type not recognized. Please enter either:")
    print(" r for a reservoir fingerprint or\n t for a timeseries fingerprint")
    sys.exit()

# make title file
TitleFN = open("gmtTitle.txt","w")
TitleFN.write("0 0 "+Title)
TitleFN.close()

# Prepare xyz file

#get lat lon
print("get latlon...")
lat,lon = glv()

# make unit mm
fp = fp*1000

print("preparing xyz file...")
xyz = wxyz(lon, lat, fp)

np.savetxt(ofng,xyz,delimiter = "\t")

## PLOTTING

print("plotting fingerprint...")
subprocess.call("gmt_fingerprint.csh")

os.rename("Fingerprint.pdf",ofn)
