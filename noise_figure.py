import numpy as np
import matplotlib.pyplot as plt
import scipy.constants as cst

kB = cst.Boltzmann
B = 1

ns_off_dbm = -133.37
ns_on_dbm = -126.3

ns_off_lin = (10.00**(ns_off_dbm/10.0))/1000.0
ns_on_lin = (10.00**(ns_on_dbm/10.0))/1000.0

T_DUT_on = ns_on_lin/(kB*B)
T_DUT_off = ns_off_lin/(kB*B)

#print T_DUT_off,T_DUT_on
#
#T_off = 300
#T_on = 8800
#
#print T_DUT_off
#print T_DUT_on
#
#T = np.array([T_off,T_on])
#T_DUT = np.array([T_DUT_off,T_DUT_on]) 
#
#p_coeff = np.polyfit(T,T_DUT,1)
#po = np.poly1d(p_coeff)
#
#T_fit = np.linspace(-10000,1000,1000)
#
#plt.plot(T,T_DUT)
#plt.plot(T_fit,po(T_fit))
#plt.show()

print T_DUT_off*8000/(T_DUT_on-T_DUT_off)
