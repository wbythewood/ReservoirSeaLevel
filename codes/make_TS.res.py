#!/usr/bin/env python3.7
import sys
import config
import math
import numpy as np
from res_subr import databases as DB

# This code will make a txt matrix
# Rows are successive years.
# Columns are different reservoirs.
#
# Large reservoirs are split into multiple years. Only a fraction of the 
# volume of the largest reservoirs fills in the stated year. This code accounts
# for that. Each reservor is assigned a number of years to fill, or is assumed 
# to be one. 


#usage
if len(sys.argv) != 2:
    print("\nThis code will take a reservoir database file Res.{db}.txt and")
    print(" make a timeseries of the impoundment.")
    print(" Columns are different reservoirs,")
    print(" Rows are successive years,")
    print(" output file is tab delimited\n")
    print("Usage:")
    print(sys.argv[0]+" DB_name\n")
    print("DB_names are: \nG = GRanD\nC = under Construction\nP = Planned")
    sys.exit()

# location of database
db_path = config.BaseDir+'data/'
# where you want the time series saved
ts_path = config.BaseDir+'time_series/'

#get db name
db,start,end = DB(sys.argv[1])

# set special time to fill
# GRanD
if db == "Grand":
    long_fill_doc = range(1,10) # reservoirs whose fill time I know
    long_fill_two = range(21,50) # reservoirs whose fill time I assume to be 2 years
    long_fill_three = range(10,21) # reservoirs whose fill time I assume to be 3 years
    time_to_fill = [6,7,12,8,8,6,3,3,3] # fill times for first set
    if len(long_fill_doc) != len(time_to_fill):
        print("\nError!\nNeed to specify length of time for certain reservoirs to fill")
        print("List lengths not the same. Exiting...\n")
        sys.exit()
else:
    long_fill_doc = [0]
    long_fill_two = [0]
    long_fill_three = [0]
    time_to_fill = []
# Find and open the database file

ifn = db_path+"Res."+db+".txt"
ofn = ts_path+"TS.res."+db+".txt"
ResList = []
InFile = open(ifn)
for line in InFile:
    ResList.append(line.split())
InFile.close()
TS = []

# Loop through reservoirs:
for res in ResList:
    res_v = []
    resYr = int(res[3])
    if resYr < 1800:        # Don't use those with no year (-99 or 0)
        resYr = 9999        # rather than forgetting about them, set them to very high year
                            # so they won't have any volume in the timeseries
                            
    resNo = int(res[0])     # get reservoir number
    resVol = float(res[1])  # and volume
    
    
    # first set up for the reservoirs that have a definite fill time
    if resNo in long_fill_doc:
        ttf = time_to_fill[resNo-1]    # get the time to fill from the matrix
    
    # Then the reservoirs that fill in three years
    elif resNo in long_fill_three:
        ttf = 3                        # time to fill hardwired to 3

    # Then the reservoirs that fill in two years
    elif resNo in long_fill_two:
        ttf = 2                        # time to fill hardwired to 2
         
    # then the reservoirs that fill in one
    else:                              
        ttf = 1                        # time to fill hardwired to 1

    # Now we calculate the volume that year

    # the seepage is complicated for reservoirs that take more than one year to fill.
    # The way I calculate it is thus:
    # Say the reservoir takes three years to fill:
      #  year 1:  V = 1/3 * resVol
      #  year 2:  V = 1/3 * resVol (imp yr 1) + 1/3 * resVol (imp yr 2) + seep (yr 1)
      #  year 3:  V = 1/3 * resVol (imp yr 1) + 1/3 * resVol (imp yr 2) + 1/3 * resVol (imp yr 3) + seep (imp yr 1) + seep (imp yr 2)
      #       ==> V = resVol (total) + seep (1/3 of volume imp 2 yr ago) + seep (1/3 of volume imp 1 yr ago)
      #  year 4:  V = resVol (total) + seep (imp yr 1) + seep (imp yr 2) + seep (imp yr 3)
      #  etc...
    # Seep = 0.05 * V * sqrt(dt)
    # The equation that results is:
    #
    # V(yr) = resVol/ttf * (FF * 0.05 * sum from n to dt of sqrt(dt))
    #
    # where:
     # ttf = time to fill
     # dt  = time since dam complete
     # FF  = factor    == dt+1 for dt<ttf, == ttf    for dt >= ttf
     # n   = start sum == 0    for dt<ttf, == dt-ttf for dt >= ttf

    for year in range(start,end+1):    # Loop over all the years
        if resYr > year:               # Before res is built, vol = 0
            res_v.append(0.0)
            continue                   # continue in loop
        elif resYr <= year:            # after built
            dt = year-resYr            # get age in years
            if dt < ttf:               # if age is less than time to fill,
                startSum = 0           # we begin our sum at 0
                RepFactor = dt+1       # and the factor is the age+1

            else:
                startSum = dt+1-ttf    # we begin sum at time since reservoir fully filled (+1 b/c dt=0 at y=Y and ttf=1)
                RepFactor = ttf        # and rep factor is the number of years to fill

            sumSqDt = 0.0              # initialize the sum over sqrts
            for i in range(startSum,dt+1):
                sumSqDt += math.sqrt(i)
            # now use equation from above
            volYr = resVol/ttf*(RepFactor+0.05*sumSqDt)

            # and finally add this to the vector that represents v(t) for this reservoir
            res_v.append(volYr)
    
    # Now we add this to the matrix
    TS.append(res_v)

# TS is one column per year, row per reservoir. We want the opposite. Take the transpose
TST = map(list,zip(*TS)) # TST = Transpose of TS

# save to file
#np.savetxt(ofn, TST, delimiter = '\t')
np.savetxt(ofn, TS, delimiter = '\t')
#with open(ofn,"w") as f:


