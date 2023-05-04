import numpy as np
import matplotlib.pyplot as plt
from matplotlib import animation
import time 
import subprocess

# rtl_power_fftw -f 145e6 -b 4096 -g 100 -l -r 2000000 -t 1


# p = subprocess.Popen(["rtl_power_fftw","-f","145e6","-b","4096","-g","100","-l","-r","2000000","-t","0.1"], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
# stdout, stderr = p.communicate()

# data = str(stdout.strip())
# # print (data)

# data = data.split("\\n")
# # print (data)
# for line in data[-4096:]:
#     line = line.strip()
#     datum = line.split(' ')
#     print (datum)

spectrum = np.array(np.fromfile("myscanfilename.bin", dtype=np.float32))
print (spectrum.shape)
plt.figure()
plt.semilogy(spectrum)
plt.show()