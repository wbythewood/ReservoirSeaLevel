#!/usr/bin/env python3.7

import sys
import math
import numpy as np
import config
from matplotlib import pyplot as plt

# usage
if len(sys.argv) != 2:
    print("\nThis code will plot three figures for a supplied tide gauge number")
    print(" One showing the tide gauge observations,")
    print(" One showing the tide gauge predictions on the same scale, and")
    print(" One showing the tide gauge predictions zoomed in.")
    print(" For certain tide gauges, it will show compare also to the corrected")
    print("  TG records from Pieguch et al (2019). Those tide gauges are:")
    print("  97, 138, 179, 1049, 1218, 1592, 2112")
    print("\nUsage:")
    print(sys.argv[0]+" [Tide Gauge No.]\n")
    sys.exit()

# some constants
# Grand
begin = 1900
end = 2011
# 1950 - 2000
begin2 = 1950
end2 = 2000
# Sweden
#begin2 = 1900
#end2 = 2011

# set up paths
figPath = config.BaseDir+'figures/TG_Observations/'
tgPath = config.BaseDir+'data/TideGauge/'
rlrPath = tgPath+'rlr_annual/data/'
predPath = tgPath+'TideGaugePredictions/'
PiecuchPath = tgPath+'Piecuch/'

# argument
TGNo = int(sys.argv[1])

DataFN = rlrPath+str(TGNo)+'.rlrdata'
PredFN = predPath+str(TGNo)+'.rlrpred.txt'
NOAAFN = PiecuchPath+str(TGNo)+'.NOAA.rlr_corr.txt'
ERAFN = PiecuchPath+str(TGNo)+'.ERA.rlr_corr.txt'

Pred = np.loadtxt(PredFN,delimiter=';')

# make the vectors for predicted
year = []
hPred = []

for i in Pred:
    year.append(i[0])
    hPred.append(i[1]*1000)

# plot the predicted
ja = 0
if ja == 1:
    plt.plot(year,hPred)
    plt.xlim(begin,end)
    plt.xlabel('Year')
    plt.ylabel('Sea Level Change (mm)')
    plt.title('Predicted Sea Level Curve for Baie Comeau, Canada')
    #plt.show()
    aFN = figPath+'Pred.pdf'
    fig = plt.gcf()
    fig.set_size_inches(8,4.5)
    fig.savefig(aFN)
    #plt.savefig(aFN)
    plt.close()

# make vectors for observed
Data = np.loadtxt(DataFN,delimiter=';',usecols=(0,1))
yeard = []
hObs1 = []

for i in Data:
    yeard.append(i[0])
    if i[1] > -1000:
        hObs1.append(i[1])
    else:
        hObs1.append(np.nan)

# find a way to center on zero
Max = max(hObs1)+5
Min = min(hObs1)-5
MaxP = (Max - Min)/2
MinP = 0 - MaxP

hObs2 = hObs1 - (Max - MaxP)

# make vectors for Piecuch sea level predictions
NOAA = np.loadtxt(NOAAFN,delimiter=',')
ERA = np.loadtxt(ERAFN,delimiter=',')

# monthly ERA ocean height
yearERA = []
hERA = []
for i in ERA:
    yi = i[0]+((i[1]-1)/12)
    yearERA.append(yi)
    hERA.append(i[2])

# yearly ERA ocean height
yearEFloor = np.floor(yearERA)
yearE = []
hAnnERA = []
hy = []
for i,y in enumerate(yearEFloor):
    if i+1 == len(yearEFloor):
        hAnnERA.append(np.average(hy))
        yearE.append(y)
        continue
    if yearEFloor[i] == yearEFloor[i+1]:
        hy.append(hERA[i])
    else:
        hAnnERA.append(np.average(hy))
        hy = []
        hy.append(hERA[i])
        yearE.append(y)

# monthly NOAA ocean height
yearNOAA = []
hNOAA = []
for i in NOAA:
    yi = i[0]+((i[1]-1)/12)
    yearNOAA.append(yi)
    hNOAA.append(i[2])

# yearly NOAA ocean height
yearNFloor = np.floor(yearNOAA)
yearN = []
hAnnNOAA = []
hy = []
for i,y in enumerate(yearNFloor):
    if i+1 == len(yearNFloor):
        hAnnNOAA.append(np.average(hy))
        yearN.append(y)
        continue
    if yearNFloor[i] == yearNFloor[i+1]:
        hy.append(hNOAA[i])
    else:
        hAnnNOAA.append(np.average(hy))
        hy = []
        hy.append(hNOAA[i])
        yearN.append(y)

# monthly MEAN ocean height
yearMEAN = yearNOAA
hMEAN = []
for i,hN in enumerate(hNOAA):
    try: 
        j = yearERA.index(yearNOAA[i])
        hE = hERA[j]
        hM = (hN+hE)/2
    except:
        hM = hN
    hMEAN.append(hM)

# yearly MEAN ocean height
yearM = yearN
hAnnMEAN = []
for i,hN in enumerate(hAnnNOAA):
    try:
        j = yearE.index(yearN[i])
        hE = hAnnERA[j]
        hM = (hN+hE)/2
    except:
        hM = hN
    hAnnMEAN.append(hM)

# Correct TG record for the above SL predictions
hCorrERA = []
hCorrNOAA = []
hCorrMEAN = []

for i,y in enumerate(yeard):
    hO = hObs2[i]
    try:
        iERA = yearE.index(y)
        hE = hO - hAnnERA[iERA]
    except:
        hE = np.nan
    try:
        iNOAA = yearN.index(y)
        hN = hO - hAnnNOAA[iNOAA]
    except:
        hN = np.nan
    try:
        iMEAN = yearM.index(y)
        hM = hO - hAnnMEAN[iMEAN]
    except:
        nM = np.nan
    hCorrERA.append(hE)
    hCorrNOAA.append(hN)
    hCorrMEAN.append(hM)


# plot observed
jb = 0
if jb == 1:
    plt.plot(yeard,hObs1,marker ='o')
    plt.xlim(begin,end)
    plt.xlabel('Year')
    plt.ylabel('Sea Level Change (mm)')
    plt.title('Observed Sea Level at Baie Comeau, Canada')
    #plt.show()
    bFN = figPath+'ObsRLR.pdf'
    fig = plt.gcf()
    fig.set_size_inches(8,4.5)
    fig.savefig(bFN)
    #plt.savefig(bFN)
    plt.close()


# plot centered on zero
jc = 0
if jc == 1:
    plt.plot(yeard,hObs2,marker ='o')
    plt.xlim(begin2,end2)
    plt.ylim(MinP,MaxP)
    plt.xlabel('Year')
    plt.ylabel('Sea Level Change (mm)')
    plt.title('Observed Sea Level at Baie Comeau, Canada')
    #plt.show()
    cFN = figPath+'ObsZero.pdf'
    fig = plt.gcf()
    fig.set_size_inches(8,4.5)
    fig.savefig(cFN)
    #plt.savefig(cFN)
    plt.close()


# prediction plot at scale
jd = 0
if jd == 1:
    plt.plot(year,hPred)
    plt.xlim(begin2,end2)
    plt.ylim(MinP,MaxP)
    plt.xlabel('Year')
    plt.ylabel('Sea Level Change (mm)')
    plt.title('Predicted Sea Level Curve for Baie Comeau, Canada')
    #plt.show()
    dFN = figPath+'PredScaled.pdf'
    fig = plt.gcf()
    fig.set_size_inches(8,4.5)
    fig.savefig(dFN)
    #plt.savefig(dFN)
    plt.close()

# 
je = 1
if je == 1:
    plt.plot(yeard, hObs2, 'k', marker = 'o', label = 'Observed')
    plt.plot(year, hPred, 'b',label = 'Predicted')
    plt.xlim(begin2, end2)
    plt.ylim(MinP,MaxP)
    plt.xlabel('Year')
    plt.ylabel('Sea Level Change (mm)')
    plt.title('Sea Level change for '+str(TGNo))
    plt.legend(loc=2)
    #plt.show()
    eFN = figPath+'TG_Obs.'+str(TGNo)+'.pdf'
    fig = plt.gcf()
    fig.set_size_inches(8,4.5)
    fig.savefig(eFN)
    plt.close()

jcorr = 1
for BaroModel in ['MEAN', 'ERA', 'NOAA']: 
    if jcorr == 1:
        if BaroModel == 'MEAN':
            #plt.plot(yearMEAN,hMEAN, color='lightpink', linewidth=0.8, marker='.', markersize=4, label='Mean Corrected, monthly')
            #plt.plot(yearP,hAnnMEAN, color='firebrick', linewidth=1, marker='o', label='Mean Corrected, yearly')
            plt.plot(yeard,hCorrMEAN, color='firebrick', linewidth=2, marker='.', markersize=8, label='ERA & NOAA Corrected')
        elif BaroModel == 'ERA':
            #plt.plot(yearERA,hERA, color='lightpink', linewidth=0.8, marker='.', markersize=4, label='ERA Corrected, monthly')
            #plt.plot(yearE,hAnnERA, color='firebrick', linewidth=1, marker='o', label='ERA Corrected, yearly')
            plt.plot(yeard,hCorrERA, color='firebrick', linewidth=2, marker='.', markersize=8, label='ERA Corrected')
        elif BaroModel == 'NOAA':
            #plt.plot(yearNOAA,hNOAA, color='lightpink', linewidth=0.8, marker='.', markersize=4, label='NOAA Corrected, monthly')
            #plt.plot(yearN,hAnnNOAA, color='firebrick', linewidth=1, marker='o', label='NOAA Corrected, yearly')
            plt.plot(yeard,hCorrNOAA, color='firebrick', linewidth=2, marker='.', markersize=8, label='NOAA Corrected')
        plt.plot(yeard,hObs2,'k',linewidth=1,marker='.',markersize=8,label='Uncorrected')
        plt.plot(year,hPred,'b',label='Predicted')
        plt.xlim(begin2,end2)
        plt.xlabel('Year')
        plt.ylabel('Sea Level Change (mm)')
        plt.title('Sea Level change for '+str(TGNo))
        plt.legend(loc=3)
        #plt.show()
        corrFN = figPath+'TG_Obs.'+str(TGNo)+'.'+BaroModel+'.pdf'
        fig = plt.gcf()
        fig.set_size_inches(8,4.5)
        fig.savefig(corrFN)
        plt.close()

