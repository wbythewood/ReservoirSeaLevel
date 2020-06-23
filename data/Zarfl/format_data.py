#!/usr/bin/env python2.7

# NOTE that this script is in Python 2.7. There are character encoding 
# errors in Python 3 that would take too much time to overcome.

# this script will read in the csv file supplied by C. Zarfl
# containing data of estimated reservoirs to be constructed.

# it will make two files, one for reservoirs in the planning
# phase, and another for those under construction. 

# The capacity in this section is the power generation capacity
# It is NOT the volume of the reservoir. A different code,
#  make_zarfl_slope.py
# will convert the MW to m**3.

# Output format:
# [resNo] [cap_MW] [lat] [lon]

# william b hawley
# whawley@seismo.berkeley.edu

ifn = open("17_0116_future_dams_update_final_v2.csv")

plan = open("../Plan.txt",'w')
const = open("../Const.txt",'w')


status_list = []
i_p = 0
i_u = 0


skip_header = 0
for line in ifn:
    if skip_header == 0:
        skip_header = 1
        continue
    cap = line.split(',')[7]
    lat = line.split(',')[9]
    lon = line.split(',')[10]
    status = line.split(',')[11]
    
    lat = "%.2f" %float(lat)
    lon = "%.2f" %float(lon)

    if status not in status_list:
        status_list.append(status)

    if status == 'P':
        i_p += 1
        plan.write(str(i_p)+'\t'+str(cap)+'\t'+str(lat)+'\t'+str(lon)+'\n')
    
    if status == 'U':
        i_u += 1
        const.write(str(i_u)+'\t'+str(cap)+'\t'+str(lat)+'\t'+str(lon)+'\n')

print("list of possible status:")
print(status_list)
