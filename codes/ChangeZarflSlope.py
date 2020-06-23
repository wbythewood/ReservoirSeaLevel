#!/usr/bin/env python3.7

import sys
import numpy as np

from res_subr import databases as DB
from res_subr import GetData
import config

if len(sys.argv) != 3:
    print("\nThis code will use the Zarfl et al. databases of capacity (MW) and")
    print(" write a file that estimates the volume, using a supplied slope.")
    print(" Grill et al 2015 estimate:")
    print(" S = P * m    where:")
    print(" S = Storage (10**6 m**3)")
    print(" P = Power capacity (MW)")
    print(" m = slope... mean = 3.19, s.d = 8.5\n")
    print("  ... I assume the slope should not be negative, so if you enter a negative number")
    print("  the program will assign the absolute value of that number to each and every reservoir")
    print(" i.e., slope of 3 will multiply the given P by 3 for every reservoir")
    print(" but a slope of -1000 will give every reservoir a volume of 1000 * 10**6 m**3")
    print("\nUsage:")
    print(sys.argv[0]+" DB_name Slope\n")
    print(" DB_names are: \nC = under Construction\nP = Planned")
    sys.exit()

# Format is ResNo Vol Area Year Lon Lat Vol_cumulative Vc/Vt
# Year for plan/const
ConstYr = float(2025)
PlanYr = float(2035)

# where to save the file
db_path = config.BaseDir+'data/'
db,start,end = DB(sys.argv[1])
if db == 'Grand':
    print("You don't want to use this code with the GRanD data. Exiting...")
    sys.exit()

factor = float(sys.argv[2])

#filenames
ifn = db_path+db+".txt"
ofn = db_path+"Res."+db+".txt"
meta = db_path+"meta."+db+".txt"

#get data
ResList = GetData(ifn)
# where to save the info we want to save
M = []
#loop over reservoirs
for line in ResList:
    Res = []
    if len(line) != 4:
        continue
    # ResNo
    #Res.append(float(line[0]))
    Res.append(line[0])
    # Vol
    if factor > 0:
        Res.append(float(line[1])*factor)
    else:
        Res.append(0. - factor)
    # Area
    Res.append(-99)
    # Year 
    if db == 'Const':
        Res.append(ConstYr)
    if db == 'Plan':
        Res.append(PlanYr)
    # Lon and Lat
    Res.append(line[2])
    Res.append(line[3])
    #Vc
    Res.append(-99)
    #Vc/Vt
    Res.append(-99)
    M.append(Res)

#save
OutFile = open(ofn,"w")
for i in M:
    OutFile.write(str(i[0])+'\t'+str(i[1])+'\t'+str(i[2])+'\t'+str(int(i[3]))+'\t'+str(i[4])+'\t'+str(i[5])+'\t'+str(i[6])+'\t'+str(i[7])+'\n')
#np.savetxt(ofn,M,delimiter='\t')
OutMetaFile = open(meta,"w")
OutMetaFile.write("The factor you've used last is: "+str(factor))
