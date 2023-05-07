#! /bin/python3

import numpy as np
import h5py
import time
import serial
from time import sleep
import sys
import subprocess
from subprocess import PIPE
import argparse

parser = argparse.ArgumentParser(description='Acquire data from three state radiometer')
parser.add_argument('-f', metavar='freq_c', help='List of centre frequencies, comma separated (Hz)', nargs='?', default="78e6", type=str)
parser.add_argument('-s', metavar='freq_s', help='Sampling frequency (Hz)', nargs='?', default=2e6, type=float)
parser.add_argument('-g', metavar='gain',  help='SDR gain (dB)', nargs='?', default=25.4, type=float)
parser.add_argument('-i', metavar='t_int', help='Integration time (s)', nargs='?', default=2, type=int)
parser.add_argument('-N', metavar='NFFT', help='NFFT', nargs='?', default=4096, type=int)

args = parser.parse_args()

freq_list_str = args.f.strip().split(",")
N_freqs = len(freq_list_str)
freq_list_float = np.zeros([N_freqs], dtype=np.float32)
for i in range(N_freqs):
    freq_list_float[i] = float(freq_list_str[i])

fs = int(args.s)
NFFT = int(args.N) 
t_int = int(args.i)
gain = int(args.g)*10

print("Acq params")
print("Nfreqs="+str(N_freqs))
print("fs="+str(fs/1e6)+" MHz")
print("NFFT="+str(NFFT))
print("Gain="+str(gain))
print("t_int="+str(t_int)+" s")
timestr = time.strftime("%Y%m%d-%H%M%S")
h5_file = str(timestr)+"_fftw.h5"

print ("Writing to",h5_file)
hf = h5py.File(h5_file, 'w')

timestamp = time.time()
dummy_data = np.zeros(NFFT, dtype=np.float32)

data_group = hf.create_group('data')
data_group.attrs["Nfreqs"] = N_freqs
data_group.attrs["fs"] = fs
data_group.attrs["NFFT"] = NFFT
data_group.attrs["gain"] = gain
data_group.attrs["t_int"] = t_int

data_group.create_dataset('timestamps', data=np.array([timestamp]), maxshape=(None,))
data_group.create_dataset('temperature', data=np.array([0.0]), maxshape=(None,))
data_group.create_dataset('fc', data=np.array([0.0]), maxshape=(None,))
data_group.create_dataset('obssource', data=np.array([-1]), maxshape=(None,))
data_group.create_dataset('radio', data=np.array([dummy_data]), maxshape=(None,None))

source_index = 0
freq_index = -1
ser = serial.Serial(port='/dev/ttyUSB0', baudrate=115200, timeout=.1)
ser.flushInput()
ser.flushOutput()

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
            freq_index = int((freq_index+1)%N_freqs)
            print ("Antenna, Freq =", str(freq_list_float[freq_index]/1e6), "MHz")
        elif source_index == 1:
            ser.write(bytes("C", 'ascii'))
            print ("Cold, Freq =", str(freq_list_float[freq_index]/1e6), "MHz")
        else:
            ser.write(bytes("H", 'ascii'))
            print ("Hot, Freq =", str(freq_list_float[freq_index]/1e6), "MHz")

        fc = freq_list_float[freq_index]
        hf['data/fc'].resize((len_old_data + 1), axis=0)
        hf['data/fc'][-1:] = fc

        hf['data/timestamps'].resize((len_old_data + 1), axis=0)
        hf['data/timestamps'][-1:] = time.time()

        p = subprocess.Popen(["rtl_power_fftw_estimate","-f",str(fc),"-b",str(NFFT),"-g",str(gain),"-l","-r",str(fs),"-t",str(t_int),"-m","/tmp/spectra"], stdout=PIPE, stderr=PIPE)
        stdout, stderr = p.communicate()
        spectrum = np.fromfile("/tmp/spectra.bin", dtype=np.float32)

        temperature = ser.readline().decode('ascii').strip()
        hf['data/temperature'].resize((len_old_data + 1), axis=0)
        hf['data/temperature'][-1:] = float(temperature)
        # print (temperature)

        hf['data/radio'].resize((len_old_data + 1), axis=0)
        hf['data/radio'][-1:] = np.array(spectrum)

        source_index = int((source_index+1)%3)

    except KeyboardInterrupt:
        print ("Exiting gracefully !")
        ser.write(bytes("A", 'ascii'))
        hf.close()
        ser.close() 
        sys.exit()






