#! /bin/python3

import numpy as np
import h5py
import time
import serial
from time import sleep
import sys
import subprocess
from subprocess import PIPE

fc = int(145e6)
fs = int(2e6)
NFFT = int(4096) 
t_int = int(2)
gain = int(254)

timestr = time.strftime("%Y%m%d-%H%M%S")
h5_file = str(timestr)+"_fftw.h5"

print ("Writing to",h5_file)
hf = h5py.File(h5_file, 'w')

timestamp = time.time()
dummy_data = np.zeros(NFFT, dtype=np.float32)

data_group = hf.create_group('data')
data_group.attrs["fc"] = fc
data_group.attrs["fs"] = fs
data_group.attrs["NFFT"] = NFFT
data_group.attrs["gain"] = gain
data_group.attrs["t_int"] = t_int

data_group.create_dataset('timestamps', data=np.array([timestamp]), maxshape=(None,))
data_group.create_dataset('temperature', data=np.array([0.0]), maxshape=(None,))
data_group.create_dataset('obssource', data=np.array([-1]), maxshape=(None,))
data_group.create_dataset('radio', data=np.array([dummy_data]), maxshape=(None,None))

source_index = 0
ser = serial.Serial(port='/dev/ttyUSB0', baudrate=115200, timeout=.1)

for dv in range(10):
    ser.write(bytes("A", 'ascii'))
    sleep(1)
    temperature = ser.readline().decode('ascii').strip()
    print (temperature)

while True:
    try:
        len_old_data = data_group['timestamps'].shape[0]

        hf['data/obssource'].resize((len_old_data + 1), axis=0)
        hf['data/obssource'][-1:] = np.array([source_index])

        if source_index == 0:
            ser.write(bytes("A", 'ascii'))
            print ("Antenna")
        elif source_index == 1:
            ser.write(bytes("C", 'ascii'))
            print ("Cold")
        else:
            ser.write(bytes("H", 'ascii'))
            print ("Hot")

        hf['data/timestamps'].resize((len_old_data + 1), axis=0)
        hf['data/timestamps'][-1:] = time.time()

        p = subprocess.Popen(["rtl_power_fftw_estimate","-f",str(fc),"-b",str(NFFT),"-g",str(gain),"-l","-r",str(fs),"-t",str(t_int),"-m","/tmp/spectra"], stdout=PIPE, stderr=PIPE)
        stdout, stderr = p.communicate()
        spectrum = np.fromfile("/tmp/spectra.bin", dtype=np.float32)

        temperature = ser.readline().decode('ascii').strip()
        print (temperature)
        hf['data/temperature'].resize((len_old_data + 1), axis=0)
        hf['data/temperature'][-1:] = float(temperature)

        hf['data/radio'].resize((len_old_data + 1), axis=0)
        hf['data/radio'][-1:] = np.array(spectrum)

        source_index = int((source_index+1)%3)

    except KeyboardInterrupt:
        print ("Exiting gracefully !")
        ser.write(bytes("A", 'ascii'))
        hf.close()
        ser.close() 
        sys.exit()






