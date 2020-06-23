#!/usr/bin/env python3.7

# This code will write a file that will be used to make histograms
# format:
# Year No_of_Reservoirs Volume Seepage

# william b hawley
# whawley@seismo.berkeley.edu

import sys
import config
import math
import numpy as np
from res_subr import databases as DB

#usage
if len(sys.argv) != 2:
    print("\nThis code will write a file that can be used to make histograms")
    print("The resulting file will be in the time_series directory:")
    print("Hist.DB.txt")
    print("Year\tNoOfReservoirs\tVolume\tSeepage")
    print("\nUsage:")
    print(sys.argv[0]+" DB_name\n")
    print("DB_names are: \nG = GRanD\nC = under Construction\nP = Planned\nA = All")
    sys.exit()

# location of database
db_path = config.BaseDir+'data/'
# where you want the time series saved
ts_path = config.BaseDir+'time_series/'

#get db name
db,start,end = DB(sys.argv[1])
time = np.arange(start,end)

ifn = db_path+"Res."+db+".txt"
ofn = ts_path+"Hist."+db+".txt"
ResList = []
InFile = open(ifn)
for line in InFile:
    ResList.append(line.split())
InFile.close()
Seep = 0

MatOut = []

for year in time:
    line = []
    No = 0
    Vol = 0
    SeepTotLast = Seep
    Seep = 0
    for res in ResList:
        if res[3] == str(int(year)):
            No += 1
            Vol += float(res[1])
        elif int(res[3]) < int(year):
            if int(res[3]) < start:
                continue
            dt = year - int(res[3])
            Seep += float(res[1])*0.05*math.sqrt(dt)

    Seep_Yr = Seep - SeepTotLast
    line.append(year)
    line.append(No)
    line.append(Vol)
    line.append(Seep_Yr)

    MatOut.append(line)

if db == 'All':
    MatAll = []
    year = 1830
    No = 0
    Vol = 0
    Seep = 0
    for i in MatOut:
        ydiff = i[0]-year
        if (ydiff < 10):
            No += i[1]
            Vol += i[2]
            Seep += i[3]

        elif (ydiff == 10):
            MatAll.append([float(year), float(No), float(Vol), float(Seep)])
            year = i[0]
            No = i[1]
            Vol = i[2]
            Seep = i[3]
    MatAll.append([float(year), float(No), float(Vol), float(Seep)])
    np.savetxt(ofn,MatAll,delimiter='\t')
    sys.exit()


np.savetxt(ofn,MatOut,delimiter='\t')
