import aipy as a
import time
import astropy
import numpy as np
import matplotlib.pyplot as plt
from datetime import datetime
from astropy.time import Time
from scipy import signal
import subprocess

f_low = 50e6
f_high = 1700e6
f_step = 1e6
f_string = str(f_low)+':'+str(f_high)+':'+str(f_step)

SAMP_RATE_GHz = f_step/1e9
FREQ_GHz = f_low/1e9
NFFT = int((f_high-f_low)/f_step)
sdf = f_step/1e9

my_time = time.gmtime(time.time())
file_name = str(my_time.tm_year)+'_'+str(my_time.tm_mon).zfill(2)+'_'+str(my_time.tm_mday).zfill(2)+'-'+str(my_time.tm_hour).zfill(2)+str(my_time.tm_min).zfill(2)+str(my_time.tm_sec).zfill(2)+".dat"

uv = a.miriad.UV(file_name, 'new')
uv['history'] = 'test file\n'

uv.add_var('latitud','d')
uv.add_var('npol','i')
uv.add_var('nspect', 'i')
uv.add_var('obsdec', 'd')
uv.add_var('vsource', 'r')
uv.add_var('ischan', 'i')
uv.add_var('operator', 'a')
uv.add_var('nants', 'i')
uv.add_var('baseline', 'r')
uv.add_var('sfreq', 'd')
uv.add_var('inttime', 'r')
uv.add_var('source', 'a')
uv.add_var('epoch', 'r')
uv.add_var('version', 'a')
uv.add_var('ra', 'd')
uv.add_var('restfreq', 'd')
uv.add_var('nschan', 'i')
uv.add_var('sdf', 'd')
uv.add_var('corr', 'r')
uv.add_var('freq', 'd')
uv.add_var('longitu', 'd')
uv.add_var('nchan', 'i')
uv.add_var('tscale', 'r')
uv.add_var('antpos', 'd')
uv.add_var('telescop', 'a')
uv.add_var('pol', 'i')
uv.add_var('coord', 'd')
uv.add_var('veldop', 'r')
uv.add_var('lst', 'd')
uv.add_var('time', 'd')
uv.add_var('dec', 'd')
uv.add_var('obsra', 'd')

uv['latitud'] = 13.611111*np.pi/180.0
uv['npol'] = 1
uv['nspect'] = 1
uv['obsdec'] = 0.0 
uv['vsource'] = 0.0
uv['ischan'] = 0
uv['operator'] = 'J'
uv['nants'] = 1
uv['baseline'] = 0.0
uv['sfreq'] = FREQ_GHz 
uv['inttime'] = 1.0
uv['source'] = 'SKY'
uv['epoch'] = 2000.0
uv['version'] = 'A'
uv['ra'] = 0.0
uv['restfreq'] = 0.0
uv['nschan'] = NFFT
uv['sdf'] = sdf
uv['corr'] = 0.0 
uv['freq'] = 0.0
uv['longitu'] = 77.516667*np.pi/180.0
uv['nchan'] = NFFT
uv['tscale'] = 0.0
uv['antpos'] = 0.0
uv['telescop'] = 'J'
uv['pol'] = 1
uv['coord'] = 0.0
uv['veldop'] = 0.0
uv['lst'] = 0.0
uv['time'] = 0.0
uv['dec'] = 0.0
uv['obsra'] = 0.0

p = subprocess.Popen(["rtl_power","-f",f_string,"-g","50","-1"], stdout=subprocess.PIPE) #"-i","1m",

vaal = p.communicate()
freq_array = np.array([])
power_array= np.array([])

vaal = vaal[0]
for line in vaal.split('\n'):
	if line:
		line = line.split(',')
		freq = (float(line[2])+float(line[3]))/2.0
		freq_array = np.append(freq_array, freq)
		power_dBm = float(line[6])
		power_array = np.append(power_array, 10**(power_dBm/10.0))

data_mask = np.zeros(NFFT)

uvw = np.array([1,2,3], dtype=np.double)
ut = Time(datetime.utcnow(), scale='utc')
preamble = (uvw, ut.jd, (0,1))
data = np.ma.array(power_array, mask=data_mask, dtype=np.complex64)
uv.write(preamble,data)

del(uv)

