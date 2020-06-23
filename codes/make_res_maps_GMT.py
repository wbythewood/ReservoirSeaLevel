#!/usr/bin/env python3.7

import sys
import os
import math
import subprocess
import config
from res_subr import databases as DB
from res_subr import GetData

# This code will make maps of reservoir locations, and scale the size of the 
# symbol to the reservoir volume. It does this in two steps:

# First, it makes GMT-suitable files to plot the reservoirs by volume and year.
# The output is formatted thus:
#  LON     LAT     YEAR    VOLUME
# These are placed in the GMT_files directory

# Then it calls a cshell script that has GMT code to make the maps.
# For Hawley et al 2020, figure 1,
# we use option L for Grand, and option S for Zarfl

#usage
if len(sys.argv) != 2:
    print("\nThis code makes a GMT-ready file to plot reservoirs")
    print(" with color according to year constructed and size")
    print(" according to reservoir volume.")
    print("These files are placed in the maps directory.")
    print("\nFormat:")
    print("Longitude    Latitude   Year   Volume")
    print("\nUsage:")
    print(sys.argv[0] + " L|S")
    print("\nWhere L will show only large reservoirs, V > 1000 * 10^6 m^3")
    print("And S will show smaller reservoirs, V > 10 * 10^6 m^3")
    sys.exit()

sl = sys.argv[1] 

if sl != 'L' and sl != 'S':
    print(sl+" is invalid. Please choose either \'L\' or \'S\'.")

# set up paths
MapsDir = "./GMT_files/"
DataDir = config.BaseDir+"data/"
FigDir = config.FigDir

if os.path.isdir(MapsDir) == False:
    os.mkdir(MapsDir)

# set up vol to circle size info
# opt S - show GRanD > 10*10^6m^3
if sl == 'S':
    base = 1.1
    denom = 130
    offset = -18
    vmax = 204500
    vmin = 10
    kvol = [100000,1000,10]
# opt2 - show only large GRanD > 1000 * 10^6 m^3
if sl == 'L':
    base = 30
    denom = 2
    offset = -1.9
    vmax = 204500
    vmin = 1000
    kvol = [100000,10000,1000]

Max = (math.log(float(vmax),base) + offset)/denom
Min = (math.log(float(vmin),base) + offset)/denom

print("max = "+str(Max))
print("min = "+str(Min))

## First we want to make the necessary files ##

# filenames
DBNames = ['G','P','C']
zfn = MapsDir+"Res.Zarfl.xyzm"
ZFile = open(zfn,"w")
zt = 0 # flag to only write key once in ZFile
for iname in DBNames:
    db,start,end = DB(iname)
    ifn = DataDir+"Res."+db+".txt"
    ofn = MapsDir+"Res."+db+".xyzm"

    # get res info
    ResList = GetData(ifn)

    # write to file the attributes you want
    OutFile = open(ofn,"w")
    j=0
    jstop = 10000
    # write out key -- three circles denoting size of reservoirs
    klat = [-40,-50,-60]
    klon = [-140,-149,-161.5]
    kyr = 1 # random early year: show up saturated (black) in color scale
    for n in range(len(klat)):
        size = (math.log(float(kvol[n]),base) + offset)/denom
        OutFile.write(str(klon[n])+'\t'+str(klat[n])+'\t'+str(kyr)+'\t'+str(size)+'\n')
        if zt == 0:
            ZFile.write(str(klon[n])+'\t'+str(klat[n])+'\t'+str(kyr)+'\t'+str(size)+'\n')
    zt = 1
    # now write the actual reservoirs
    for i in ResList:
        year = i[3]
        if int(year) < start:
            continue
        vol = i[1]
        if float(vol) < vmin:
            continue
        lon = i[5]
        lat = i[4]
        size = (math.log(float(vol),base) + offset)/denom
        OutFile.write(lon+'\t'+lat+'\t'+year+'\t'+str(size)+'\n')
        if db != 'Grand':
            ZFile.write(lon+'\t'+lat+'\t'+year+'\t'+str(size)+'\n')
        if j > jstop:
            sys.exit()
        j+=1
    OutFile.close()
ZFile.close()

## Now make the figures

# make file names
GrandFN = 'ReservoirMapGrand.'+sl+'.pdf'
ZarflFN = 'ReservoirMapZarfl.'+sl+'.pdf'

# call gmt script
subprocess.call(['Reservoirs_volume.csh',GrandFN,ZarflFN])

# move to figure directory
GrandMoved = FigDir+GrandFN
ZarflMoved = FigDir+ZarflFN
os.rename(GrandFN,GrandMoved)
os.rename(ZarflFN,ZarflMoved)
