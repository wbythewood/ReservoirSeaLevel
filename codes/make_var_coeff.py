#!/usr/bin/env python2.7
# -*- coding: utf-8 -*-
#
# William Hawley, 13 June 2016

'''
Make a file that will produce a timeseries of a lake's impoundment history.

Usage: 
    make_var_coeff.py RESERVOIR_NUMBER
    make_var_coeff.py -h

Options:
   -h, --help      Show this help
'''


import glob
import csv
from docopt import docopt
import sys
import numpy as np
from datetime import date
import config

# set up dir structure
dataDir = config.BaseDir+'data/'
tsPath = config.BaseDir+'time_series/'
varPath = config.BaseDir+'time_series/VAR/'

def read_info_var(res_no):
   "pull reservoir info from the timeseries file"

   # this has the satellite altimitry data
   fnVar = varPath+'var_'+str(res_no)+'.txt'

   try:
      #csvVar = csv.reader(open(fnVar), delimiter = ' ', skipinitialspace=True)
      VarArray = np.loadtxt(fnVar)
   except:
      print "trouble opening file",fnVar
      print "Are you sure it exists?"
      print ""
      sys.exit()
   
   return VarArray

def read_info_stat(res_no):
   "pull reservoir info from the impoundment file"
   
   # and this has the volume, area reported in GRAND
   fnCon = dataDir+'Res.Grand.txt'

   # pull res info
   ResInfo = np.loadtxt(fnCon)

   # search for the reservoir information
   for res in ResInfo:
      if int(res[0]) == int(res_no):
         vol = float(res[1])    # 10^6 m^3
	 area = float(res[2])   # 10^6 m^2 = km^2
	 # Mean depth
	 meanDepth = vol/area   # m
	 break
   return (area, meanDepth)

def time_series(Variations):
   "make the timeseries list from the numpy array"
   lastMonth = 0
   ts = []
   heights = []
   for datum in Variations:
      # first, if no data, continue
      dh = float(datum[3])
      if dh == 999.99:
         continue
      # different lakes have different NaNs
      if dh == 9999.99:
         continue
      ymd = str(datum[0])
      year = int(ymd[0:4])
      month = int(ymd[4:6])
      day = int(ymd[6:8])

      # we only need one data point per month, so let's just take the first
      if lastMonth == month:
         continue
      if int(month) > 12:
         continue
      
      t = date(year,month,day)
      lastMonth = month
      ts.append([dh,t])
      heights.append(dh)

   maxHeight = max(heights)
   # note that the last value is the maximum...
   ts.append(maxHeight)
   return ts

def convert_fractional(input_ts, maxHeight, averageHeight):
   "return a timeseries with the fraction filled that corresponds to a date"

   ts = []
   for obs in input_ts:
      # dh here will be the change from maximum, always a positive number
      # note that larger numbers mean lower lake levels
      dh =  maxHeight - obs[0]
      # also save time
      t = obs[1]

      # OK for now, we assume linear relationship from dh to dV 
      # which would be the case for a cube reservoir.
      # Perhaps more complicated shapes later...

      # here dh is change from max
      # averageHeight is assumed to be the depth of the reservoir
      # dh / average is the relative change from max, so ideally
      #   at max, dh = 0, so value is 0,
      #   at min, dh is no larger than the depth of the reservoir,
      #    and value is no larger than 1.
      # we then subtract this from 1 such that we get the fractional 
      # level of the reservoir, where 1 is full, and 0 is empty.
      dVFrac = 1. - dh/averageHeight
      # save to time series
      ts.append([dVFrac,t])
   
   return ts

def write_file(ts,ofn):
   "write the timeseries to a file"

   with open(ofn,"w") as f:
      for step in ts:
         f.write(str(step[0])+'\t'+str(step[1])+'\n')

if __name__ == "__main__":

    # Pull arguments from the input...
    arguments = docopt(__doc__)
    # The reservoir number
    res_no = arguments['RESERVOIR_NUMBER']

    ofn = varPath+'fractional_ts_res'+str(res_no)+'.txt'
    
    # get the info
    Variations = read_info_var(res_no)
    area, depth = read_info_stat(res_no)

    # Make the timeseries of lake level (in physical units)
    ts_m = time_series(Variations)
    # take out maximum here
    maxHeight = ts_m.pop()

    # convert that timeseries to fractional volume
    ts_f = convert_fractional(ts_m,maxHeight,depth)

    # and write it to a file
    write_file(ts_f,ofn)
