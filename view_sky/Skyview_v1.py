from datetime import datetime
import numpy as np
import matplotlib.pyplot as plt
import ephem
from matplotlib import animation
import healpy as hp
#hp.disable_warnings()

plt.rc('font', family='serif')
plt.rcParams.update({'font.size': 18})

'''
Uses info from https://geohack.toolforge.org/geohack.php?pagename=Murchison_Radio-astronomy_Observatory&params=26.70312_S_116.670575_E_
as well as https://rhodesmill.org/pyephem/quick.html
'''
MRO_observer = ephem.Observer()
MRO_observer.lon = '115.8613' 
MRO_observer.lat = '-31.9523'
MRO_observer.elevation = 0
MRO_observer.date = datetime.utcnow()
ra_rad, dec_rad = MRO_observer.radec_of(0, np.pi/2)
print ("LST =",ra_rad*12/np.pi, "hrs")


sky_map = hp.ud_grade(hp.read_map("/home/jishnu/SKY_MAPS/lambda_haslam408_nofilt.fits", dtype=np.float64), nside_out=64)
#sky_map = hp.ud_grade(hp.read_map("/Users/jishnu/Dropbox/CRB/MAPS/haslam408_ds_Remazeilles2014.fits", dtype=np.float64), nside_out=64)


lst_hrs = ra_rad*12/np.pi
ra_deg  = lst_hrs*360/24.0
dec_deg = -31.9523

r_map = hp.Rotator(rot=[ra_deg, dec_deg], coord=['G', 'C'])    
sky_val = r_map.rotate_map_alms(sky_map, use_pixel_weights=False)
map_here = np.log2(hp.orthview(sky_val, half_sky=True, return_projected_map=True))
plt.close()

fig, ax_sky = plt.subplots(1, 1, figsize=(10,10))
fig.canvas.manager.set_window_title('Sky view') 
ax_sky.axis('off')

im = ax_sky.imshow(map_here, aspect='auto', cmap='rainbow')
ax_sky.set_title("LST = {:.5f} hours".format(ra_rad*12/np.pi))

def animate_func(i):

    MRO_observer.date = datetime(2022, 4, 13, (i%24), 10) #Year, month, date, hrs, mins - UTC
    # MRO_observer.date = datetime.utcnow()
    ra_rad, dec_rad = MRO_observer.radec_of(0, np.pi/2)
    print ("LST =",ra_rad*12/np.pi, "hrs")

    lst_hrs = ra_rad*12/np.pi
    ra_deg  = lst_hrs*360/24.0
    dec_deg = -31.9523
    r_map = hp.Rotator(rot=[ra_deg, dec_deg], coord=['G', 'C'])    
    sky_val = r_map.rotate_map_alms(sky_map, use_pixel_weights=False)

    map_here = np.log2(hp.orthview(sky_val, half_sky=True, return_projected_map=True))

    im.set_array(map_here)
    ax_sky.set_title("LST = {:.5f} hours".format(ra_rad*12/np.pi))

    return [im]

anim = animation.FuncAnimation(fig, animate_func, frames = None, interval=1000)
                               
plt.show() 
