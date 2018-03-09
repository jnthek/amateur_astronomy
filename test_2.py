# -*- coding: utf-8 -*-
"""
Created on Thu Mar  8 18:54:44 2018

@author: jishnu
"""

import astropy as ap
from astropy.coordinates import SkyCoord
from astropy import units as u
c = SkyCoord(l=10.68458, b=41.26917, unit=(u.degree, u.degree), frame='galactic')
print c.galactic
print c.galactic.l.radian
print c.galactic.b.radian

