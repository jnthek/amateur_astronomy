import numpy as np
import matplotlib.pyplot as plt
from matplotlib import animation
#from pylab import *
from rtlsdr import *
import time 
from scipy import signal

# configure the rtlsdr
sdr = RtlSdr()
sdr.sample_rate = 2.4e6  # Hz
sdr.center_freq = 94.7e6  # Hz
sdr.gain = 'auto'

samples = sdr.read_samples(128*1024)

#f, Pxx_den = signal.periodogram(samples, sdr.sample_rate, nfft=1024)
Pxx, freq = plt.psd(samples, NFFT=1024, Fs=sdr.sample_rate/1e6, Fc=sdr.center_freq/1e6)

plt.figure()
plt.semilogy(freq, Pxx)
plt.show()
sdr.close()

