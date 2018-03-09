# -*- coding: utf-8 -*-
"""
Created on Tue May 16 09:00:20 2017

@author: jishnu
"""

import healpy as hp
import matplotlib.pyplot as plt
import numpy as np

map_1420_full=hp.fitsfunc.read_map('1420_1D_R8.FITS',field=0)
map_1420_full = map_1420_full-2.725
hp.mollview(map_1420_full, norm='hist')
plt.show()