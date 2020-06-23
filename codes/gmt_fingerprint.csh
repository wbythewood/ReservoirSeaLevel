#!/bin/csh

#######################################################
#  This script plots the fingerprint of the example
#  file in Jerry's sea level code.
#  William B Hawley, April 2013
#######################################################

# GENERAL NAME - name of fingerprint, to be followed by extensions to 
# 	denote file type
set File =  gridinp.txt

# INPUT FILE - the fingerprint to be mapped
set FP = $File.gmt

# Intermediate Grid File
set GRD = grd.dat
rm $GRD
set GRDI = grd.interp.dat
rm $GRDI

# Grid file for determining max value for color scale for Manicouagan
set VGRD = vgrd.dat
rm $VGRD

#set TSTI = test.xyz
#rm $TSTI

# OUTPUT FILE
set OFN = Fingerprint.ps
set GRegion = "-R0/360/-90/90"

# MAP INFO
# WORLD
set Region = "-R0/360/-90/90"
set Projection = "-JW0/23c"
set Tick = "-Bf30a30WseN"
set TitleLoc = "-R-10/10/-9/10"
set ScaleLoc = "-R-10/10/-10/10"

# SE ASIA
set AsiaLat1 = 75
set AsiaLat2 = 115
set AsiaLon1 = 5
set AsiaLon2 = 35
####### Uncomment Below to zoom in on SE Asia #######
set Region = "-R$AsiaLat1/$AsiaLat2/$AsiaLon1/$AsiaLon2"
set Projection = "-JM16"
set Tick = "-Bf5a10WseN"
set TitleLoc = "-R-10/10/-18/20"
set ScaleLoc = "-R-10/10/-9.5/5"

# S AMERICA
set SALat1 = 270
set SALat2 = 330
set SALon1 = -30
set SALon2 = 15
####### Uncomment Below to zoom in on S America #######
#set Region = "-R$SALat1/$SALat2/$SALon1/$SALon2"
#set Projection = "-JM16"
#set Tick = "-Bf10a10WseN"
#set TitleLoc = "-R-10/10/-18/20"
#set ScaleLoc = "-R-10/10/-9.5/5"

# MANICOUAGAN
#######  Uncomment Below to zoom in on Manicouagan #######
#set Region = "-R280/310/40/55"
#set Projection = "-JM16"
#set Tick = "-Bf5a5WseN"
#set TitleLoc = "-R-10/10/-18/20"
#set ScaleLoc = "-R-10/10/-9.5/5"
#set ValsRegion = "-R290/300/40/49.5"

# F is the scale for smoothing to get rid of ringing... g is gaussian, no is degree width
set F = "-Fg2"
set Form = "--FORMAT_FLOAT_OUT=%3.0f"
set Shift = "-Yr7c -Xc-1"
#SEAsia and SAm
####### Uncomment below for SE Asia and S America #######
set Shift = "-Yr4c -Xc-1"

# Set Basemap
gmt psbasemap $Region $Projection $Tick $Shift $Form -K >! $OFN

# change xyz input file to a grd
gmt xyz2grd $File -G$GRD $Region -I0.36 -V #-ZT
# Manicouagan
####### Uncomment below for Manicouagan #######
#gmt xyz2grd $File -G$VGRD $ValsRegion -I0.36 -V

# sample down to get rid of ringing... F sets scale. g=gaussian; no is degree width
# make cpt from grid
# put grid onto the map
# add contour for hinge line
# get grid info for color scale
# one for each GRD and GRDI

set GRDI = $GRD
####### Uncomment the following line to filter the image #######
gmt grdfilter $GRD -D0 -G$GRDI $F $Region -V

# get min value
set min = `gmt grdinfo $GRDI -Cn --FORMAT_FLOAT_OUT=%.2f | awk '{print $5}'`
echo $min

## make color file
####### Uncomment one below for global maps #######
#set CPT = ImloaRev.cpt
#make_cpt_imloa_rev.py $min
####### Uncomment below for SE Asia or S America #######
set CPT = Inset.cpt
gmt grd2cpt $GRDI -Cpanoply $Region -V -T- -E13 > $CPT
####### Uncomment below for Manicouagan #######
#set max = `gmt grdinfo $VGRD -Cn --FORMAT_FLOAT_OUT=%.2f | awk '{print $6}'`
#echo $max
#gmt makecpt -Clajolla -T0/20/2 -V > $CPT

## BEGIN PLOTTING
# Set Basemap
gmt psbasemap $Region $Projection $Tick $Shift $Form -K >! $OFN
# plot fingerprint
gmt grdimage $GRDI $Region $Projection $Form -C$CPT -O -K -V >> $OFN
gmt grdcontour $GRDI $Region $Projection -C0.5 -L-0.2/0.2 -O -K -V >> $OFN
#Manicouagan -- line at 10 mm
####### Uncomment below for Manicouagan #######
#gmt grdcontour $GRDI $Region $Projection -C10 -L5/15 -O -K -V >> $OFN

#gmt grdinfo $GRDI -Cn
#Manicouagan
####### Uncomment Below for Manicouagan #######
#set VMax = `gmt grdinfo $VGRD -Cn | awk '{print $6}'`
#gmt grdinfo $VGRD -Cn


#####

#Use These
# clip land:
####### Uncomment below for all but Manicouagan #######
gmt pscoast $Region $Projection $Tick $Form -O -Ggrey -Dl -A7800 -W1/0.5 -W2/0.5 -K >> $OFN
#Manicouagan
####### Uncomment below for Manicouagan #######
#gmt pscoast $Region $Projection $Tick $Form -O -Ggrey -Di -A1000 -W1/0.2 -W2/0.2 -W3/0.2 -N1/0.2 -N2/0.2,- -K >> $OFN

#scale et al
####### Uncomment below for all but Manicouagan #######
#echo "-5 -10.8 $min mm" | gmt pstext $Projection $ScaleLoc -N -O -K -V >> $OFN
####### Uncomment below for Manicouagan #######
#echo "-3 -10.8 $VMax m" | gmt pstext $Projection $ScaleLoc -N -O -K -V >> $OFN

## Box for the future regions
# SE Asia
#gmt psxy $Region $Projection -W1,0/0/0 -Am -K -O << END >> $OFN
#$AsiaLat1 $AsiaLon1
#$AsiaLat1 $AsiaLon2
#$AsiaLat2 $AsiaLon2
#$AsiaLat2 $AsiaLon1
#$AsiaLat1 $AsiaLon1
#END
# South America
#gmt psxy $Region $Projection -W1,0/0/0 -Am -K -O << END >> $OFN
#$SALat1 $SALon1
#$SALat1 $SALon2
#$SALat2 $SALon2
#$SALat2 $SALon1
#$SALat1 $SALon1
#END

## Title
gmt pstext "gmtTitle.txt" $Projection $TitleLoc -F-f16p -N -O -K -V >> $OFN

## play around with scale location... 
#psscale -D is location, --D_FORMAT is output syntax -B
#gmt psscale -C$CPT -D3.15/-0.4/6/0.3h --FORMAT_FLOAT_OUT=%3.0f -B10:"Change in Relative Sea Level": -O -Xc0 -E >> $OFN
# horizontal scale:
#gmt psscale -C$CPT $Region $Projection -DJBC+e+w16/0.5 -Bx+l"Change in Relative Sea Level (mm)" -Np -O -K -Xc-1 >> $OFN
# vertical scale
gmt psscale -C$CPT $Region $Projection -DJMR+ef+w10/0.5 -Bx+l"Change in Relative Sea Level (mm)" -Np -O -K -Xc-1 >> $OFN
# second horizontal one
#gmt psscale -C$CPT $Region $Projection --FORMAT_FLOAT_OUT=%3.2f -DJBC+e+w16/0.5 -Bx+l"Change in Relative Sea Level (mm)" -Np -O -L -Xc-1 -Yc-0 >> $OFN
# vertical scale
#psscale -C$CPT -D1.15/-0.2/6/0.3h --FORMAT_FLOAT_OUT=%3.0f -O -Xc0 -E >> $OFN

#grdview $GRD $Region $Projection -C$CPT -O -V >> $OFN
ps2pdf $OFN

#clean up
rm $OFN

