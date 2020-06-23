#!/bin/csh

###########################################################
# This code will plot the tide gauge locations, and color
# them accoring to the maximum yearly sea level change 
# observed at that site. 
###########################################################

# filenames
set TGFile = "TGMaxChange.txt"
set TGMaxFile = "LargestTGMaxChange.txt"
set ofn = "TGMaxChange.ps"
set pdfn = "TGMaxChange.pdf"
set cpt = "TGColor.cpt"
set hmin = 0
set hmax = 0.007


#map params
set Rm = "-Rg"
set Jm = "-JKf0/23"

#plot coastlines
#pscoast -A1000 -N1/0.2 -W1/0.25 -W2/0.1 -Y5 $Rm $Jm -Slightgrey -Df -K -Ba90f30/a30f15 > $ofn
pscoast -A1000 -N1/0.2 -W1/0.25 -W2/0.1 -Y5 $Rm $Jm -Df -K -Ba90f30/a30f15 > $ofn

# make color scale
makecpt -Ccool -I -T$hmin/$hmax -N > $cpt

# write first all the TGs
cat $TGFile | awk '{print $3, $2, $4}' | psxy -Sc0.10 -W0.1  -C$cpt $Jm $Rm -O -K >> $ofn
# now write the largest ones, larger size
cat $TGMaxFile | awk '{print $3, $2, $4}' | psxy -Sc0.20 -W0.1  -C$cpt $Jm $Rm -O -K >> $ofn

psscale -C$cpt -D2.15/-1.0/6/0.3h --FORMAT_FLOAT_OUT=%3.0f -B10:"Maximum yearly change": -O -K -Xc0 -E >> $ofn



echo 0 0 | psxy -Sc0.0001 -G255 $Jm $Rm -O >> $ofn

ps2pdf $ofn $pdfn
rm $ofn
open $pdfn

