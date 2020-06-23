#!/usr/bin/env python3.7

# this script will make individual files for each of the tide gauges
# included in the two csv files Chris Piecuch sent me.

# william b hawley  --  march 2020
# whawley@ldeo.columbia.edu

import sys
import numpy as np

for mod in ['NOAA','ERA']:
    ifn = 'BarotropicModel'+mod+'.csv'

    data = np.loadtxt(ifn,delimiter=',',skiprows=1)
    year = data[:,0]
    month = data[:,1]
    for n,tgid in enumerate([97, 138, 179, 1049, 1218, 1592, 2112]):
        col = n+2
        h = data[:,col]
        ofn = str(tgid)+'.'+mod+'.rlr_corr.txt'
        final = np.transpose(np.array([year,month,h]))
        np.savetxt(ofn,final,delimiter=',')
