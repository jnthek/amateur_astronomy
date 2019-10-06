# -*- coding: utf-8 -*-
"""
Created on Thu Mar  8 18:54:44 2018

@author: jishnu
"""

import astropy as ap
from astropy.coordinates import SkyCoord
from astropy import units as u
c = SkyCoord(ra=5.933807, dec=-1.178487, unit=(u.radian, u.radian), frame='icrs')
#print c.galactic
print c.galactic.l.radian
print c.galactic.b.radian

