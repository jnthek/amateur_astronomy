import numpy as np
import matplotlib.pyplot as plt
import subprocess
# rtl_power -f 200M:1.7G:1M -g 50 -i 1m -1 noise4.csv
# p = subprocess.Popen(["rtl_power", "-f", "200M:1.7G:1M","-g","50","-i","1m","-1"], stdout=subprocess.PIPE)

f_low = '24M'
f_high = '1700M'
f_step = '1M'
f_string = f_low+':'+f_high+':'+f_step

p = subprocess.Popen(["rtl_power","-f",f_string,"-g","50","-i","1m","-1"], stdout=subprocess.PIPE)

vaal = p.communicate()
freq_array = np.array([])
power_dBm_array= np.array([])

vaal = vaal[0]
for line in vaal.split('\n'):
	if line:
		line = line.split(',')
		freq = (float(line[2])+float(line[3]))/2.0
		freq_array = np.append(freq_array, freq)
		power_dBm = float(line[6])
		power_dBm_array = np.append(power_dBm_array, power_dBm)

plt.figure()
plt.plot(freq_array/1e6, power_dBm_array)
plt.grid()
plt.show()
