# -*- coding: utf-8 -*-
"""
Created on Thu Mar  8 18:14:48 2018

@author: jishnu
"""

import healpy as hp
import matplotlib.pyplot as plt
import numpy as np
import astropy as ap
import astropy.units as u
from astropy.time import Time
from astropy.coordinates import SkyCoord, EarthLocation, AltAz

def antenna_function(theta,phi):
    return (np.cos(theta))**2

Obs_loc = EarthLocation(lat=41.3*u.deg, lon=-74*u.deg, height=390*u.m)
utcoffset = -4*u.hour  # Eastern Daylight Time
time = Time('2012-7-12 23:00:00') - utcoffset

gal_lat_coordinate = np.array([])
gal_lon_coordinate = np.array([])
pixel_list_file = open("PIXEL_LISTING_NESTED_R4_GALACTIC.txt",'r')
for line in pixel_list_file:
    line = line.strip()
    line = line.split()
    if line[0] != "LONGITUDE":
        gal_lon_coordinate = np.append(gal_lon_coordinate,float(line[0]))
        gal_lat_coordinate = np.append(gal_lat_coordinate,float(line[1]))
    
file_150 = open("map_150_r4_5deg_nested_galactic_Kelvin.txt",'r')
map_150 = np.array([])
for line in file_150:
    line = line.strip()
    line = line.split()
    map_150 = np.append(map_150,float(line[0]))

T_a = 0.0
for i in range(3072):
    sky_loc_gal = SkyCoord(l=gal_lon_coordinate[i], b=gal_lat_coordinate[i], unit=(u.degree, u.degree), frame='galactic')
    sky_val = map_150[i]    
    sky_loc_altaz = sky_loc_gal.transform_to(AltAz(obstime=time,location=Obs_loc))
    phi = sky_loc_altaz.az.radian
    theta = sky_loc_altaz.alt.radian
    T_a = T_a + sky_val*antenna_function(theta,phi)
    #print sky_loc_altaz
    #print("M33's Altitude = {0.alt:.2}".format(sky_loc_altaz))
print T_a    
hp.mollview(map_150, norm='hist', nest=True)
plt.show()
