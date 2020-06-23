#!/usr/bin/env python3.7

import sys
import os
import math
import numpy as np
import scipy.optimize as opt
from scipy import special
from matplotlib import pyplot as plt

import config
from res_subr import databases as DB

# file names
tsDir = config.BaseDir+'time_series/'
#chaofn = config.BaseDir+'data/Chao/Hist.Chao.txt'
chaofn = tsDir+'Hist.Chao.txt'
chaoFuturefn = tsDir+'Hist.ChaoF.txt'
grandfn = tsDir+'Hist.Grand.txt'
allfn = tsDir+'Hist.All_2040.txt'
allfn = tsDir+'Hist.All.txt'
popfn = config.BaseDir+'data/Population/TotalPop.txt'
figDir = config.BaseDir+'figures/Population/'
if os.path.isdir(figDir) == False:
    os.mkdir(figDir)

# easy to change start and end
start = 1950
end = 2010
years = np.arange(start,end+1)

eus_fac = (3.409*10**5)**-1

# for sigmoid fitting
startFit = 1950
endFit = 2010
YearC = 2030
YearP = 2040

# read in volume data

#chao
TotalTest = 0
Chao = []
VolC = 0
VolT = 0
InFile = open(chaofn)
for line in InFile:
    year = int(float(line.split()[0]))
    VolY = float(line.split()[2])
    VolSy = float(line.split()[3])
    VolC += VolY
    VolT += VolY + VolSy
    TotalTest += VolT

    Chao.append([year,VolC,VolT])

InFile.close()
# save as np array
Chao = np.asarray(Chao)

#Chao with Zarfl future
ChaoF = []
VolC = 0
VolT = 0
InFile = open(chaoFuturefn)
for line in InFile:
    year = int(float(line.split()[0]))
    VolY = float(line.split()[2])
    VolSy = float(line.split()[3])
    VolC += VolY
    VolT += VolY + VolSy

    ChaoF.append([year,VolC,VolT])

InFile.close()
# save as np array
ChaoF = np.asarray(ChaoF)

#grand
Grand = []
TotalGTest = 0
VolC = 0
VolT = 0
InFile = open(grandfn)
for line in InFile:
    year = int(float(line.split()[0]))
    VolY = float(line.split()[2])
    VolSy = float(line.split()[3])
    VolC += VolY
    VolT += VolY + VolSy
    TotalGTest += VolT
    
    Grand.append([year,VolC,VolT])

InFile.close()
Grand = np.asarray(Grand)

#all
All = []
VolC = 0
VolT = 0
InFile = open(allfn)
for line in InFile:
    year = int(float(line.split()[0]))
    VolY = float(line.split()[2])
    VolSy = float(line.split()[3])
    VolC += VolY
    VolT += VolY + VolSy

    All.append([year,VolC,VolT])

InFile.close()
All = np.asarray(All)

# read in pop data
Pop = []
InFile = open(popfn)
for line in InFile:
    year = int(float(line.split()[0]))
    pop = int(line.split()[1])*(10**-6)

    Pop.append([year,pop])

InFile.close()
PopA = np.asarray(Pop)
# keep a vector that contains pop to 2100 for plotting
PopAll = PopA[:,1]

#######
# Make vectors to plot
#######

ChaoN = []
ChaoS = []
ChaoFN = []
ChaoFS = []
GrandN = []
GrandS = []
AllN = []
AllS = []
Pop = []
years = np.arange(start,end+1)
for year in years:
    if year not in Chao[:,0]:
        ChaoN.append(np.nan)
        print(" uh oh using nans")
        ChaoS.append(np.nan)
        #print year
        continue
    for line in Chao:
        if year == line[0]:
            #print year,line[0],line[1]
            ChaoN.append(line[1]*eus_fac)
            ChaoS.append(line[2]*eus_fac)
for year in years:
    if year not in ChaoF[:,0]:
        ChaoFN.append(np.nan)
        print(" uh oh using nans")
        ChaoFS.append(np.nan)
        #print year
        continue
    for line in ChaoF:
        if year == line[0]:
            #print year,line[0],line[1]
            ChaoFN.append(line[1]*eus_fac)
            ChaoFS.append(line[2]*eus_fac)
for year in years:
    if year not in Grand[:,0]:
        print(" uh oh using nans")
        GrandN.append(np.nan)
        GrandS.append(np.nan)
        continue
    for line in Grand:
        if year == line[0]:
            #print year,line[0],line[1]
            GrandN.append(line[1]*eus_fac)
            GrandS.append(line[2]*eus_fac)
for year in years:
    if year not in Grand[:,0]:
        if year not in All[:,0]:
            print(" uh oh using nans")
            AllN.append(np.nan)
            AllS.append(np.nan)
            continue
        for line in All:
            if year == line[0]:
                AllN.append(line[1]*eus_fac)
                AllS.append(line[2]*eus_fac)
    for line in Grand:
        if year == line[0]:
            AllN.append(line[1]*eus_fac)
            AllS.append(line[2]*eus_fac)

for year in years:
    if year not in PopA[:,0]:
        print(" uh oh using nans")
        Pop.append(np.nan)
        continue
    for line in PopA:
        if year == line[0]:
            Pop.append(line[1])

# add two years for const and plan
PopFuture = list(Pop)
for line in PopA:
    if YearC == line[0]:
        PopFuture.append(line[1])
    if YearP == line[0]:
        PopFuture.append(line[1])
for line in All:
    if YearC == line[0]:
        AllN.append(line[1]*eus_fac)
        AllS.append(line[2]*eus_fac)
    if YearP == line[0]:
        AllN.append(line[1]*eus_fac)
        AllS.append(line[2]*eus_fac)
for line in ChaoF:
    if YearC == line[0]:
        ChaoFN.append(line[1]*eus_fac)
        ChaoFS.append(line[2]*eus_fac)
    if YearP == line[0]:
        ChaoFN.append(line[1]*eus_fac)
        ChaoFS.append(line[2]*eus_fac)

#######
# fit curves
#######

def sigmoid(P,t1,t2,t3,t4):
    return t1 * special.erf((P-t2)/t3)+t4

ChaoSopt,ChaoScov = opt.curve_fit(sigmoid,Pop,ChaoS)
GrandSopt,GrandScov = opt.curve_fit(sigmoid,Pop,GrandS)

#######
# plot
#######

plt.plot(Pop,ChaoN)
plt.xlim(1,8)
plt.ylim(0,40)
plt.xlabel('Population (billions)')
plt.ylabel('Impoundment (mm esl)')
plt.title('Using Chao Without Seepage from '+str(start))
ofn = figDir+'ChaoN_'+str(start)+'.pdf'
fig=plt.gcf()
fig.set_size_inches(6,4.5)
fig.savefig(ofn)
plt.close()

plt.scatter(Pop,ChaoS,s=12,c='k')
plt.plot(Pop,sigmoid(Pop,*ChaoSopt),'r--',linewidth=1)
plt.xlim(2,8)
plt.ylim(0,40)
plt.xlabel('Population (billions)')
plt.ylabel('Impoundment (mm esl)')
#plt.title('Using Chao With Seepage from '+str(start))
plt.title("Impoundment vs. Population from Kopp et al., 2014")
ofn = figDir+'ChaoS_'+str(start)+'.pdf'
fig=plt.gcf()
fig.set_size_inches(6,4.5)
fig.savefig(ofn)
plt.close()

plt.plot(Pop,GrandN)
plt.xlim(1,8)
plt.ylim(0,40)
plt.xlabel('Population (billions)')
plt.ylabel('Impoundment (mm esl)')
plt.title('Using Grand Without Seepage from '+str(start))
ofn = figDir+'GrandN_'+str(start)+'.pdf'
fig=plt.gcf()
fig.set_size_inches(6,4.5)
fig.savefig(ofn)
plt.close()

plt.plot(Pop,GrandS)
plt.xlim(1,8)
plt.ylim(0,40)
plt.xlabel('Population (billions)')
plt.ylabel('Impoundment (mm esl)')
plt.title('Using Grand With Seepage from '+str(start))
ofn = figDir+'GrandS_'+str(start)+'.pdf'
fig=plt.gcf()
fig.set_size_inches(6,4.5)
fig.savefig(ofn)
plt.close()

#plt.plot(PopFuture,AllN)
#plt.scatter(PopFuture,AllN,s=12)
plt.xlim(1,10)
plt.ylim(0,40)
plt.xlabel('Population (billions)')
plt.ylabel('Impoundment (mm esl)')
plt.title('Using All Without Seepage from '+str(start))
ofn = figDir+'AllN_'+str(start)+'.pdf'
fig=plt.gcf()
fig.set_size_inches(6,4.5)
fig.savefig(ofn)
plt.close()

#plt.plot(PopFuture,AllS)
plt.xlim(1,10)
plt.ylim(0,40)
plt.xlabel('Population (billions)')
plt.ylabel('Impoundment (mm esl)')
plt.title('Using All With Seepage from '+str(start))
ofn = figDir+'AllS_'+str(start)+'.pdf'
fig=plt.gcf()
fig.set_size_inches(6,4.5)
fig.savefig(ofn)
plt.close()

# finally chao future for Bob
#plt.scatter(Pop,GrandN,s=12,c='b')
plt.scatter(Pop,GrandS,s=12,c='r',label='This Study (GRanD)')
#plt.scatter(Pop,ChaoN,s=12,c='darkblue')
plt.scatter(PopFuture,ChaoFS,s=12,c='indigo',label='Zarfl $\it{et}$ $\it{al}$. (2015)')
plt.scatter(Pop,ChaoS,s=12,c='k',label='Chao $\it{et}$ $\it{al}$. (2008)')
#plt.plot(PopFuture,sigmoid(PopFuture,*ChaoSopt),'r--',linewidth=1)
plt.plot(PopFuture,sigmoid(PopFuture,*ChaoSopt),'b--',linewidth=1,label='Extrapolation ($\it{c.f.}$, Kopp $\it{et}$ $\it{al}$., 2014)')
plt.xlim(1,11)
plt.ylim(0,45)
plt.xlabel('Population (billions)')
plt.ylabel('Impoundment (mm esl)')
plt.legend(loc=4)
plt.title("Extrapolation based on population")
ofn = figDir+'Chao+Zarfl.pdf'
fig = plt.gcf()
fig.set_size_inches(6,4.5)
fig.savefig(ofn)
plt.show()
plt.close()

