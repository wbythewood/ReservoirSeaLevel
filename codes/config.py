# this file will allow the user to configure paths and global variables
# that can be accessed easily by importing config

# william b hawley

# global paths
BaseDir = '/Users/wbhawley/Research/Reservoirs/'
BackDir = '/Volumes/WilliamExtra/school/Research/Reservoirs/'
FPDir = '/Users/wbhawley/Research/Reservoirs/fingerprints/'
MapsDir = '/Users/wbhawley/data/maps/'
FigDir = BaseDir+'figures/'

# global variables
nr = 513
nc = 1025

# factor to multiply V by to find eustatic term
# area of oceans = 3.409E14 m^2
# reported vol in 10^6 m^3
# V*10^6 m^3 = 3.409*10^14 m^2 * h [m]
# h = V * (3.409*10^8)^-1

eus = (-3.409*10**8)**-1

