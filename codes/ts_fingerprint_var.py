#!/usr/bin/env python2.7
# -*- coding: utf-8 -*-
#
# William B Hawley June 2016

'''
Make a timeseries fingerprint that includes variations in one reservoir.

Usage: 
    ts_fingerprint_var.py RESERVOIR_NUMBER
    ts_fingerprint_var.py -h

Options:
    -h, --help         Show this help
'''

import glob
import csv
from datetime import date, datetime
from docopt import docopt
import sys
import numpy as np
import config
from res_subr import read_res_fp
from res_subr import databases as DB

# some directories 
dataDir = config.BaseDir+'data/'
TSDir = config.BaseDir+'time_series/'
varDir = config.BaseDir+'time_series/VAR/'
FPDir = config.BaseDir+'res_fingerprints/Grand/'

# years
db,start,end = DB('G')

def read_static():
   "read the fingerprint timeseries without variations"
   #ts_txt = 'ts_fingerprint.txt'
   ts_txt = TSDir+'TS.FP.res.Grand.txt' #'ts_cumulative.txt'
   #static = csv.reader(open(ts_txt),delimiter = '\t')
   # original fingerprint
   OFP = np.loadtxt(ts_txt,dtype = 'float')

   return OFP

def get_volume(resNo,ResInfoFN):
   "read the volume of the reservoir as a factor by which to multiply the fingerprint"
   ResInfo = np.loadtxt(ResInfoFN)
   for res in ResInfo:
       if int(res[0]) == int(resNo):
           vol = res[1]
   return vol

def make_years():
   "make years object"
   years_txt = csv.reader(open('years.txt'),delimiter = '\n')

   years = {}
   i=0
   for year in years_txt:
      if i == 0:
         begin = int(year[0])
      else:
         pass
      years[int(year[0])]=i
      i+=1

   return years

def read_var(res_no):
   "read the variable impoundment for RESERVOIR NUMBER"
   ts_var_fn = varDir+'fractional_ts_res'+str(res_no)+'.txt'

   ts_var_csv = csv.reader(open(ts_var_fn),delimiter = '\t')
   ts_var = []

   for row in ts_var_csv:
      ts_var.append([row[0],row[1]])
   return ts_var

def modify_ts(orig,res_fp,res_ts,years):
   "modify the original fingerprint timeseries to include the new variable volume"

   for year in years:
      year = int(year)
      
      for step in res_ts:
         time = date(int(step[1][0:4]),int(step[1][5:7]),int(step[1][8:10]))

	 if year < time.year:
	    print "before,"+ str(year)
	    factor = 1.
	    break

	 if time.year == year:
	    print "new,"+ str(year)
	    factor_old = factor
	    factor = float(step[0])
	    #factor = 1-factor
	    factor_cum = factor_old-factor
	    #print factor
	    dfp_year = np.multiply(res_fp,factor_cum)
	    orig[years[year]] = np.subtract(orig[years[year]],dfp_year)
	    break
      
   return orig

#def modify_ts_avg(orig,res_fp,res_ts,years):
def modify_ts_avg(orig,res_fp,res_ts,vol):
   "modify the original fingerprint timeseries to include yearly averages of the variable volume"

   factor = 1.
   #we will multiply the fp by this factor, then subtract that from the original

   # the list that stores how full the reservoir is each year
   factors = []
   # the list that keeps track of the average height, one per year
   averages = []

   for year in range(start,end):
       year = int(year)
       print str(year)
       # need to keep track of all water levels for this year
       heights = []

       # loop through the altimetry timeseries
       for step in res_ts:
           # extract time
           time = date(int(step[1][0:4]),int(step[1][5:7]),int(step[1][8:10]))
           
           # if the years match, append height to heights
           if year == time.year:
               heights.append(float(step[0]))

       # Now we've added all the heights. If new values, take average. If not, keep it 1.
       if heights == []:
           height = 1.
       else:
           height = sum(heights)/float(len(heights))

       # now that we have the average of the altimetry, add it to "averages"
       averages.append(height)

       # this list of averages is the percent full per year. Since we're subtracting, we want to 
       # multiply the fingerprint by 1 - height, and then subtract that from the fingerprint.

       factor = 1. - height

       # need to also account for reservoir's volume in factor
       factors.append(factor*vol)

   print factors
   print averages
   for i in range(len(factors)):
       if factors[i] == 0:
           pass
       # the fingerprint for that year, scaled, to subtract
       dfp_year = np.multiply(res_fp,factors[i])
       # subtract the fingerprint
       orig[i] = np.subtract(orig[i],dfp_year)
       #orig = "test"

   return orig
       


def write_fp(fp,ofn):
   "write fingerprint to file"

   np.savetxt(ofn,fp,delimiter = '\t')


## MAIN   #######
##
##


if __name__ == "__main__":
   # pull argumets from input
   arguments = docopt(__doc__)
   res_no = arguments['RESERVOIR_NUMBER']

   #ofn = 'ts_fingerprint_var_TEST'+str(res_no)+'.txt'
   ofn = varDir+'TS.FP.'+db+'.var'+str(res_no)+'.txt'
   ResInfoFN = dataDir+'Res.Grand.txt'

   # read in info
   FPTS_noVar = read_static()
   # get the volume
   vol = get_volume(res_no,ResInfoFN)
   #years = make_years()
   reservoir_fp = read_res_fp(FPDir,res_no)
   var_ts = read_var(res_no)

   # make new time series
   #fp_var = modify_ts_avg(static_ts,reservoir_fp,var_ts,years)
   fp_var = modify_ts_avg(FPTS_noVar,reservoir_fp,var_ts,vol)

   # write to file
   write_fp(fp_var,ofn)






