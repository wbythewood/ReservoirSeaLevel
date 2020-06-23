#!/usr/bin/env python3.7

# Thic script will take the file I received from Ben Chao and put it in a format
# consistent with other datasets. 

# Input file format:
# [year] [cumulative volume, km**3]

# Output file format:
# [resNo] [Vol] [area] [year] [lat] [lon] [Vol_cumulative] [percent_vol_c]
#  xxxx          xxxx          xxx   xxx                    xxx  <-- Chao won't need these params

# william b hawley
# whawley@seismo.berkeley.edu

import numpy as np

ifn = "Reservoir_TS.txt"
ofn = "../Res.Chao.txt"

InFile = open(ifn)

MatOut = []

# for reservoir number
VolLast = 0
for line in InFile:
    year = int(line.split()[0])
    CumVol = float(line.split()[1]) * 1000 # make same units, 10**6 m**3
    Vol = CumVol - VolLast

    row = [-99,Vol,-99,year,-99,-99,CumVol,-99]
    MatOut.append(row)
    VolLast = CumVol

InFile.close()
np.savetxt(ofn,MatOut,fmt='%2i \t %.6f \t %2i \t %4i \t %2i \t %2i \t %.6f \t %2i')
 
