#!/usr/bin/env python3.7

# This script will read in the shapefiles in the current directory
# and put it in a format useful for this project.

# Output format is the following:
# [resNo] [Vol] [area] [year] [lat] [lon] [Vol_cumulative] [percent_vol_c]

# william b hawley
# whawley@seismo.berkeley.edu

import shapefile
from operator import itemgetter

# prepare a matrix to store data
Reservoirs = []
# and define output file name
ofn = '../Res.Grand.txt'

# read the shapefile
sf = shapefile.Reader('GRanD_dams_v1_1')

# keep track of total volume
total = 0.0

# pull the needed info
for i in range(len(sf.records())):
    rec = sf.record(i)
    # initialize a list for the reservoir
    res = []
    # get the desired parameters
    vol = rec['CAP_MCM']
    if vol < 0:  # 'No Data' is -99... don't want to subtract volume!
        vol = 0.0
    res.append(vol)
    res.append(rec['AREA_SKM'])
    res.append(rec['YEAR'])
    res.append(rec['LAT_DD'])
    res.append(rec['LONG_DD'])

    # append that list to the Reservoirs matrix
    Reservoirs.append(res)

    # add vol to total
    total += vol

# Now we want to sort the reservoirs...
# We want the volumes descending, but for reservoirs of the same volume,
# we want years ascending. Stary with years...
TimeSorted = sorted(Reservoirs, key=itemgetter(2))
# now sort that by volume
Sorted = sorted(TimeSorted, key=itemgetter(0), reverse=True)

# write to a file
with open(ofn,"w") as f:
    total_run = 0.0
    for i in range(len(Sorted)):
        total_run += Sorted[i][0]
        pct = total_run/total
        f.write(str(i+1)+'\t'+str(Sorted[i][0])+'\t'+str(Sorted[i][1])+'\t'+str(Sorted[i][2])+'\t'+str(Sorted[i][3])+'\t'+str(Sorted[i][4])+'\t'+str(total_run)+'\t'+str(pct)+'\n')
f.close()
