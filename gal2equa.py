import astropy as ap
import numpy as np
from astropy import units as u
from astropy.coordinates import SkyCoord

gal_lat=np.array([])
gal_lon=np.array([])
f = open("PIXEL_LISTING_NESTED_R4_GALACTIC.txt",'r')
f2 = open("Converted.txt",'w')
f.readline()
for line in f:
    line = line.strip()
    line = line.split()
    gal_lat = np.append(gal_lat,line[0])
    gal_lon = np.append(gal_lon,line[1])
    
for i in range(len(gal_lat)):
    c = SkyCoord(gal_lat[i], gal_lon[i], frame='galactic', unit='deg')
    some_val = c.transform_to('icrs')
    some_val = some_val.to_string('decimal')
    #print some_val
    f2.writelines(some_val+"\n")

f.close()
f2.close()
