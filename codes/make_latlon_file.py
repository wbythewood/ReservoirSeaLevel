#!/usr/bin/env python3.7

import sys
import math
from res_subr import GetLatLon as gl
import numpy as np

ofn = "LatLon.xy"

nLat = 513
nLon = 1025

lat,lon = gl(nLat,nLon)

nr = len(lat)*len(lon)

vector = []

for i in range(nr):
    iLat = int(math.floor(i/nLon))
    iLon = i % nLon
    vector.append([lat[iLat], lon[iLon]])

np.savetxt(ofn,vector,delimiter='\t')
