import aipy as a
import numpy as np
import time

file_name = str(time.time())+".dat"

uv = a.miriad.UV(file_name, 'new')
uv['history'] = 'Made this file from scratch.\n'
uv.add_var('nchan', 'i')
uv.add_var('pol', 'i')
uv['nchan'] = 512
uv['pol'] = -5

freq = np.linspace(50,100,512)
sky = np.array(4000*(freq/50.0)**-2.7)
data_mask = np.zeros(512)

uvw = np.array([1,2,3], dtype=np.double)
preamble = (uvw, time.time(), (0,1))
data = np.ma.array(sky, mask=data_mask, dtype=np.complex64)
uv.write(preamble,data)
del(uv)
uv = a.miriad.UV(file_name)
for p, d in uv.all():
    print p, uv['pol']
    print d
