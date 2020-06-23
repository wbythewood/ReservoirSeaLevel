#!/usr/bin/env python3.7

# This program will make a histogram of the supplied dataset
# It is wired to run the Zarfl datasets, though there is not
# currently any year information for them. If any becomes 
# available, this code could be modified to use them.

# william b hawley
# whawley@seismo.berkeley.edu

import sys
import numpy as np
from matplotlib import pyplot as plt
from mpl_toolkits.axes_grid1.inset_locator import inset_axes
import pylab

import config
from res_subr import databases as DB

#This code will make a histogram of the supplied dataset. 

# usage
if len(sys.argv) != 4:
    print("\nThis program will make a histogram of the supplied dataset.\n")
    print("Usage:")
    print(sys.argv[0]+" DB_Name R|V C|Y\n")
    print("DB_names are: \nG = GRanD\nC = under Construction\nP = Planned")
    print("Choose R for number of reservoirs on vertical axis; choose V for volume.")
    print("C for cumulative change, Y for yearly change")
    sys.exit()

if sys.argv[2] != 'R' and sys.argv[2] != 'V':
    print(sys.argv[2]+" is invalid. Please choose R for number of reservoirs or ")
    print("V for volume to be displayed on the vertical axis.")
    sys.exit()

if sys.argv[3] != 'C' and sys.argv[3] != 'Y':
    print(sys.argv[2]+" is invalid. Please choose C for cumulative data or")
    print("Y for yearly data to be displayed on the vertical axis.")
    sys.exit()

rv = sys.argv[2]
cy = sys.argv[3]

factor = 1000
# location of timeseries data:
ts_path = config.BaseDir+'time_series/'
# where to save the figure:
fig_path = config.BaseDir+'figures/'

#get db name
db,start,end = DB(sys.argv[1])
dbA,startA,endA = DB("A")

# set up filenames
ifn = ts_path+"Hist."+db+".txt"
ifnAll = ts_path+"Hist.All.txt"
ofn = fig_path+"Hist."+db+"."+rv+"."+cy+".pdf"

# we already know the horizontal axis is time
time = np.arange(start,end)
timeA = np.arange(1830,endA,10)
No = []
NoA = []
Vol = []
VolA = []
Seep = []
SeepA = []

##############
# Extract data
##############

# to get the data we open this file
#InFile = np.loadtxt(ifn)

# get the info saved to a matrix
YearList = []
InFile = open(ifn)
for line in InFile:
    YearList.append(line.split())
InFile.close()

# Get the data
for line in YearList:
    No.append(float(line[1]))
    Vol.append(float(line[2])/factor)
    Seep.append(float(line[3])/factor)

TitleTimeStr = " Per Year"
Ocy = ".yr"
# if cumulative, add each to the year prior
if cy == 'C':
    TitleTimeStr = " Cumulative"
    Ocy = ".cumul"
    for data in [No,Vol,Seep]:
        for i,d in enumerate(data):
            if i > 0:
                data[i] += data[i-1]


# Do the same for all (for the inset)
#InFileAll = np.loadtxt(ifnAll)
# get the info saved to a matrix
YearListAll = []
InFileAll = open(ifnAll)
for line in InFileAll:
    YearListAll.append(line.split())
InFileAll.close()

# Get the data
for line in YearListAll:
    NoA.append(float(line[1]))
    VolA.append(float(line[2])/factor)
    SeepA.append(float(line[3])/factor)

# if cumulative, add each to the year prior
if cy == 'C':
    for data in [NoA,VolA,SeepA]:
        for i,d in enumerate(data):
            if i > 0:
                data[i] += data[i-1]


#######
# Plot
#######

fig,ax1 = plt.subplots()

if rv == 'R':
    Title = "Reservoirs -"+TitleTimeStr
    Orv = ".res"
    YLabel = "Number of Reservoirs"
    pRes = ax1.bar(time, No, color = 'k')

if rv == 'V':
    ax2 = ax1.twinx()
    Title = "Volume Impounded -"+TitleTimeStr
    Orv = ".vol"
    YLabel = "Impoundment in km$^3$"
    ax2.set_ylabel("Equivalent sea level fall in mm")
    pVol = ax1.bar(time, Vol, color = 'b')
    pSeep = ax1.bar(time, Seep, color = 'r', bottom = Vol)
    v2 = [i/360 for i in Vol]
    s2 = [i/360 for i in Seep]
    pVol2 = ax2.bar(time,v2,color = 'b')
    pSeep2 = ax2.bar(time,s2,color = 'r',bottom=v2)

plt.title(Title)
# uncomment below to change the time range for the histogram
ax1.set_xlim([1900,end]); print("overriding x-axis bounds...")

ax1.set_xlabel("Year")
ax1.set_ylabel(YLabel)

# inset subplot
axInset = inset_axes(ax1, width=2.5, height=1.5, loc=2)
#axInset.tick_params(labelleft=False, labelbottom=False, labelright=True)

if rv == 'R':
    pResI = axInset.bar(timeA, NoA, color = 'k', width=9)

if rv == 'V':
    SeepI = np.add(SeepA,VolA)
    #print(SeepI)
    #print(timeA)
    #pSeepI = axInset.scatter(timeA, SeepI, color = 'r', s = 0.5)
    #pVolI = axInset.scatter(timeA, VolA, color = 'b', s = 0.5)
    pVolI = axInset.bar(timeA, VolA, color = 'b', width=9)
    pSeepIA = axInset.bar(timeA, SeepA, color = 'r', bottom = VolA, width=9)

#plt.show()
ofn = fig_path+"Hist."+db+Orv+Ocy+".pdf"
plt.savefig(ofn)

