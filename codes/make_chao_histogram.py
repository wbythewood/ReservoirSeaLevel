#!/usr/bin/env python3.7

import sys
import config
import math
import numpy as np
from res_subr import databases as DB

# This code will take the Chao et al impoundment data, calculate the seepage
# term from those data, and write them to a new file

data_path = config.BaseDir+'data/'
ts_path = config.BaseDir+'time_series/'
ifn = data_path+'Res.Chao.txt'
ifnF = data_path+'Res.ChaoF.txt'
ofn = ts_path+'Hist.Chao.txt'
ofnF = ts_path+'Hist.ChaoF.txt'

# get data
# Chao
InFile = open(ifn)
data = []
for line in InFile:
    data.append(line.split())

InFile.close()

# output file here
Seep = 0
MatOut = []
TotV = 0
TotS = 0

time = np.arange(1900,2011)

for year in time:
    line = []
    No = -99
    Vol = 0
    SeepToLast = Seep
    Seep = 0
    for i in data:
        if int(float(i[3])) == year:
            Vol += float(i[1])
        elif int(float(i[3])) < year:
            dt = year - int(float(i[3]))
            Seep += float(i[1])*0.05*math.sqrt(dt)
    Seep_Yr = Seep - SeepToLast
    line.append(year)
    line.append(No)
    line.append(Vol)
    line.append(Seep_Yr)
    TotV += Vol
    TotS += Seep_Yr

    MatOut.append(line)

np.savetxt(ofn,MatOut,delimiter='\t')

# Chao + Zarfl
InFile = open(ifnF)
dataF = []
for line in InFile:
    dataF.append(line.split())
InFile.close()
# Chao projected with Zarfl here
Seep = 0
MatOut = []
# add four extra years (for when reservoirs are "built" and seepage five years after)
time=np.append(time,[2025,2030,2035,2040])

for year in time:
    line = []
    No = -99
    Vol = 0
    SeepToLast = Seep
    Seep = 0
    for i in dataF:
        if int(float(i[3])) == year:
            Vol += float(i[1])
        elif int(float(i[3])) < year:
            dt = year - int(float(i[3]))
            Seep += float(i[1])*0.05*math.sqrt(dt)
    Seep_Yr = Seep - SeepToLast
    line.append(year)
    line.append(No)
    line.append(Vol)
    line.append(Seep_Yr)

    MatOut.append(line)

np.savetxt(ofnF,MatOut,delimiter='\t')

