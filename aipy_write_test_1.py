import aipy as a
import numpy as np
import time

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
uv['nspect'] = 512
uv['obsdec'] = 0.0 
uv['vsource'] = 0.0
uv['ischan'] = 0
uv['operator'] = 'J'
uv['nants'] = 1
uv['baseline'] = 0.0
uv['sfreq'] = 0.05 
uv['inttime'] = 1.0
uv['source'] = 'SKY'
uv['epoch'] = 2000.0
uv['version'] = 'A'
uv['ra'] = 0.0
uv['restfreq'] = 0.0
uv['nschan'] = 512
uv['sdf'] = 0.05/512.0
uv['corr'] = 0.0 
uv['freq'] = 0.0
uv['longitu'] = 77.516667*np.pi/180.0
uv['nchan'] = 512
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

freq = np.linspace(50,100,512)
sky = np.array(4000*(freq/50.0)**-2.7)
data_mask = np.zeros(512)

uvw = np.array([1,2,3], dtype=np.double)
preamble = (uvw, time.time(), (0,1))
data = np.ma.array(sky, mask=data_mask, dtype=np.complex64)
uv.write(preamble,data)
del(uv)
