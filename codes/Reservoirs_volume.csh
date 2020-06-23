#!/bin/csh

# plot on a map the reservoirs according to size, year
# user supplies the two filenames

if ( $#argv != 2) then
	echo ""
	echo "call: Reservoirs_volume.csh [GRanD fn] [Zarfl fn]"
	echo "these filenames are the names of the .pdf figure files"
	echo ""
	exit
endif

set GrandFN = $1
set ZarflFN = $2

# params for both maps
set ResDir = "GMT_files/"
set cpt = "ResColor.cpt"
set Rm = "-Rg"
set Jm = "-JKf0/23"

##### For the GRanD database #####

set ifn = $ResDir"Res.Grand.xyzm"
set ofn = "ReservoirMapGrand.ps"
set TMin = 1900
set TMax = 2011


# plot coastlines
gmt pscoast -A1000 -N1/0.2 -W1/0.25 -W2/0.1 -Y5 $Rm $Jm -Slightgray -Dl -K -Ba90f30/a30f15 > $ofn

# make color scale
gmt makecpt -Ccool -I -A50 -T$TMin/$TMax -N > $cpt

# plot reservoirs
gmt psxy $ifn $Rm $Jm -Sc -C$cpt -W0.2 -K -O >> $ofn

# plot scale
gmt psscale -D11.5/-2/12/0.8h -B50 -C$cpt -E -O >> $ofn


ps2pdf $ofn $GrandFN
rm $ofn
#open $GrandFN

##### For the Zarfl Database #####

set ifn = $ResDir"Res.Zarfl.xyzm"
set ofn = "ReservoirMapZarfl.ps"
set TMin = 2025
set TMax = 2035

# plot coastlines
gmt pscoast -A1000 -N1/0.2 -W1/0.25 -W2/0.1 -Y5 $Rm $Jm -Slightgray -Dl -K -Ba90f30/a30f15 > $ofn

# make color scale
gmt makecpt -Csplit -I -A50 -T$TMin/$TMax -N > $cpt

# plot reservoirs
gmt psxy $ifn $Rm $Jm -Sc -C$cpt -W0.2 -K -O >> $ofn

# plot scale
gmt psscale -D11.5/-2/12/0.8h -B50 -C$cpt -E -O >> $ofn

ps2pdf $ofn $ZarflFN
rm $ofn
#open $ZarflFN
