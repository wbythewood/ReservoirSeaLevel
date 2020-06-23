#!/usr/bin/env python3.7

# this file has subroutines used multiple times by different codes
# within this directory

import sys
import numpy as np
import math

ThisDir = "/Users/wbhawley/Research/Reservoirs/codes/"

##### Get database name, start, and end years .................................
def databases(db_name):
 # GRanD
 if db_name == "G":
     db = "Grand"
     start = 1835
     end = 2011
 # Construction
 elif db_name == "C":
     db = "Const"
     start = 2021
     end = 2040
 # Planned
 elif db_name == "P":
     db = "Plan"
     start = 2031
     end = 2040
 # All    
 elif db_name == "A":
     db = "All"
     start = 1835
     end = 2031
     end = 2041
 # Future
 elif db_name == "F":
     db = "Future"
     start = 2011
     end = 2040
 # Abort
 else:
     print ("\nDatabase name not recognized:")
     print ("Please choose G, C, P, or A.\n")
     sys.exit()
 return db,start,end


##### Read a reservoir's fingerprint ..........................................
def read_res_fp(fpDir,resNo):
 fpName = fpDir+"seagl_grid_"+str(resNo)+".txt"
 fp = np.loadtxt(fpName)
 # ravel turns the matrix into a single line
 fp = np.ravel(fp)
 return fp


##### Read the fp change between two fingerprints .............................
def diff_fp(fpFn1,fpFn2):
 fp1 = np.loadtxt(fpFn1)
 fp2 = np.loadtxt(fpFn2)
 fpo = np.subtract(fp2,fp1)

 return fpo 


##### For a FP timeseries, calculate the difference between two years .........
def diff_yr(FPfn,r1,r2):
 TimeSeries = GetData(FPfn)
 fp1 = TimeSeries[r1]
 fp2 = TimeSeries[r2]
 # initialize
 fp = np.zeros(len(fp1))
 # numpy seems to take a while; do a for loop
 for i in range(len(fp1)):
  fp[i] = float(fp2[i])-float(fp1[i])
 
 return fp


##### Read a file into a list of lists ........................................
def GetData(ifn):
 List = []
 InFile = open(ifn)
 for line in InFile:
     List.append(line.split())
 InFile.close()

 return List


##### Get lat lon .............................................................
def GetLatLon(nlat,nlon):
 # get latitudes from Jerry's file
 #glat512 = np.loadtxt("glat512_w")
 glat512 = np.loadtxt(ThisDir+"glat512_w")
 if nlat != (len(glat512)*2)+1:
     print("Inconsistent number of latitudes... check nr. Exiting.")
     print("nr = "+str(nlat))
     print("glat = "+str((len(glat512)*2)+1))
     sys.exit()
 # Initialize
 lat = np.zeros(nlat)
 # loop through to write the vector
 for i in range(len(glat512)):
  # Colat_i = arccos(glat_i) in radians
  lat[i] = 90. - (math.acos(glat512[i])*(180./math.pi))
  # mirror image... lat[-1] = lat[0], lat[-2] = lat[1], etc.
  lat[-(i+1)] = 0. - lat[i]
 
 # longitudes are evenly spaced
 dlon = 360./nlon
 lon = np.arange(0,360,dlon)

 return lat,lon

##### Get Lat Lon file from longer file .......................................
def GetLatLonV():
 xy = np.loadtxt('LatLon.xy')
 lat = xy[:,0]
 lon = xy[:,1]
 return lat,lon
 
##### From lat lon, get index for fingerprint timeseries file .................
def GetIndex(lat,lon):

 # lat has 513 possibilities, so find which is closest
 #latp = math.floor(((90.-lat)/180)*513)
 latp = round(((90.-lat)/180)*513)
 # lon has 1025
 # lon has the added complication that it may be negative... 
 if lon < 0.:
     #lonp = math.floor(((360.+lon)/360)*1025)
     lonp = round(((360.+lon)/360)*1025)
 else:
     #lonp = math.floor((lon/360.)*1025)
     lonp = round((lon/360.)*1025)
 cell = int(latp*1025+lonp)
 return cell

##### Get max sea level change year and change for a location 
def GetMaxChange(cell,TS):
 # TS is numpy array
 time = -1
 dhMax = -1.
 prev = 0
 
 pointTS = TS[:,cell]
 # loop over each year
 for y in pointTS:
     # keep track of time
     time += 1
     # take the difference 
     dh = y-prev
     # overwrite the previous value
     prev = y
     # check to see if it's the biggest jump
     if dh > dhMax:
         # if it is, make it dhMax
         dhMax = dh
         # and save the year too
         yearMax = time

 # return the max value and the time that occurred
 return dhMax, yearMax

def GetMaxChangeAndTS(cell,TS):
 # TS is numpy array
 time = -1
 dhMax = -1.
 prev = 0

 pointTS = TS[:,cell]
 # loop over each year
 for y in pointTS:
     # keep track of time
     time += 1
     # take the difference 
     dh = y-prev
     # overwrite the previous value
     prev = y
     # check to see if it's the biggest jump
     if dh > dhMax:
         # if it is, make it dhMax
         dhMax = dh
         # and save the year too
         yearMax = time

 # return the max value and the time that occurred
 return dhMax, yearMax, pointTS



##### write a fingerprint as an XYZ file ......................................
def writeXYZ(fp,lat,lon):
 # write a fingerprint as an xyz file... fp must already be one column
 nr = len(fp)
 if (nr != len(lat)):
     print("error: check lengths of files")
     print("fp = "+str(nr))
     print("lat = "+str(len(lat)))
     print("lon = "+str(len(lon)))
     sys.exit()
 grid = []
 for i in range(nr):
     grid.append([fp[i],lat[i],lon[i]])
 
 return grid
