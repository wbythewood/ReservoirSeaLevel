#!/usr/bin/env python3.7

import sys
import math

# this file will make a cpt file for fingerprints 
# there are 6 colors on either side of 0
# need to make the boundaries close together at the far 
# end of the spectrum, and farther apart as the numbers
# are increasingly larger. 

# usage:
if len(sys.argv) < 2:
    print("\nThis code will create a color scale based on GMT Panoply.\n")
    print("There are 6 colors on either side of 0.")
    print("On the extreme negative side of the scale, the transitions")
    print("are closer together, while with increasing values, the")
    print("transitions are farther apart. This color scale is based")
    print("on a user-supplied input.")
    print("\nUsage:")
    print(sys.argv[0]+" GridMin\n")
    print("  where GridMin represents the largest sea level fall.\n")
    sys.exit()

ofn = "ImloaRev.cpt"

# get the min value as float
GridMinFloat = float(sys.argv[1])
print(GridMinFloat)

# using rounding and stuff... convert this to being between 10 and 100
factor = 10
if -10 < GridMinFloat <= -1:
    factor = 100
elif -1 < GridMinFloat <= -0.1:
    factor = 1000
elif -0.1 < GridMinFloat <= -0.01:
    factor = 10000
elif -0.01 < GridMinFloat:
    print("\nColor scale may be too small... aborting.\n")
    sys.exit()
GridMinFloat = GridMinFloat * factor

# now figure out relative values
GridMin = math.floor(GridMinFloat)
#GridMin18 = GridMin - round(GridMin/50)
#GridMin17 = GridMin18 - round(GridMin/50)
#GridMin16 = GridMin17 - round(GridMin/50)
GridMin15 = GridMin - round(GridMin/50)
GridMin14 = GridMin15 - round(GridMin/50)
GridMin13 = GridMin14 - round(GridMin/50)
GridMin12 = GridMin13 - round(GridMin/50)
GridMin11 = GridMin12 - round(GridMin/40)
GridMin10 = GridMin11 - round(GridMin/40)
GridMin9 = GridMin10 - round(GridMin/40)
GridMin8 = GridMin9 - round(GridMin/30)
GridMin7 = GridMin8 - round(GridMin/30)
GridMin6 = GridMin7 - round(GridMin/30)
GridMin5 = GridMin6 - round(GridMin/20)
GridMin4 = GridMin5 - round(GridMin/20)
GridMin3 = GridMin4 - round(GridMin/10)
GridMin2 = GridMin3 - round(GridMin/10)
GridMin1 = GridMin2 - round(GridMin/5)
Grid0 = 0

# save those to a list

print(GridMin5)
#values = [GridMin, GridMin18, GridMin17, GridMin16, GridMin15, GridMin14, GridMin13, GridMin12, GridMin11, GridMin10, GridMin9, GridMin8, GridMin7, GridMin6, GridMin5, GridMin4, GridMin3, GridMin2, GridMin1, Grid0]
values = [GridMin, GridMin15, GridMin14, GridMin13, GridMin12, GridMin11, GridMin10, GridMin9, GridMin8, GridMin7, GridMin6, GridMin5, GridMin4, GridMin3, GridMin2, GridMin1, Grid0]

print(values[16])
# and return them to match the values in the grd file
precision = round(math.log(factor,10))
values = [round(float(i)*(1/factor),precision) for i in values]
if factor == 1000:
    Min = values[0]
    Min = Min - 0.01
    values = [round(i,2) for i in values]
#    values[0] = Min

# and make them end in either 0 or 5?
#values = [(1/factor)*0.5*round(i*factor*2,0) for i in values]

print(values)
# write cpt file

with open(ofn,'w') as f:
    f.write(str(values[0])+"\t238.06/249.03/102\t"+str(values[1])+"\t238.06/249.03/102\n")
    f.write(str(values[1])+"\t205.19/237.09/102\t"+str(values[2])+"\t205.19/237.09/102\n")
    f.write(str(values[2])+"\t175.16/222.16/104.84\t"+str(values[3])+"\t175.16/222.16/104.84\n")
    f.write(str(values[3])+"\t153.44/204.22/108.78\t"+str(values[4])+"\t153.44/204.22/108.78\n")
    f.write(str(values[4])+"\t136.28/187.28/113\t"+str(values[5])+"\t136.28/187.28/113\n")
    f.write(str(values[5])+"\t120.34/171.34/117\t"+str(values[6])+"\t120.34/171.34/117\n")
    f.write(str(values[6])+"\t104.41/155.41/121\t"+str(values[7])+"\t104.41/155.41/121\n")
    f.write(str(values[7])+"\t90.469/140.47/125\t"+str(values[8])+"\t90.469/140.47/125\n")
    f.write(str(values[8])+"\t77.531/127.53/130\t"+str(values[9])+"\t77.531/127.53/130\n")
    f.write(str(values[9])+"\t67.594/117.59/138\t"+str(values[10])+"\t67.594/117.59/138\n")
    f.write(str(values[10])+"\t58.656/108/146.34\t"+str(values[11])+"\t58.656/108/146.34\n")
    f.write(str(values[11])+"\t51/98.719/154\t"+str(values[12])+"\t51/98.719/154\n")
    f.write(str(values[12])+"\t45/88.781/160\t"+str(values[13])+"\t45/88.781/160\n")
    f.write(str(values[13])+"\t40/78/165\t"+str(values[14])+"\t40/78/165\n")
    f.write(str(values[14])+"\t34.906/67.906/170.09\t"+str(values[15])+"\t34.906/67.906/170.09\n")
    f.write(str(values[15])+"\t29/56.969/176\t"+str(values[16])+"\t29/56.969/176\n")
    f.write("B\t255 255 102\n")
    #f.write("F\tlightgoldenrod\n")
    f.write("F\tdarkviolet\n")
    f.write("N\twhite")

