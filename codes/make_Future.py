#!/usr/bin/env python3.7

import sys
import os
from res_subr import databases as DB
from res_subr import read_res_fp as rf
import numpy as np
import config

# the three databases
cdb,a,b = DB("C")
pdb,a,b = DB("P")
fdb,a,b = DB("F")

# the three FP directories
cfpDir = config.FPDir+cdb+'/'
pfpDir = config.FPDir+pdb+'/'
ffpDir = config.FPDir+'/'

# read the Const and Plan FPs
cfp = rf(cfpDir, "All")
pfp = rf(pfpDir, "All")

# add them together
fp = np.add(cfp,pfp)

# define path
ofn = ffpDir+"seagl_grid_Future.txt"

# save file
np.savetxt(ofn, fp, delimiter = '\t')
