import numpy as np
import matplotlib.pyplot as plt
from pylab import *
import serial
from time import sleep
ser = serial.Serial(port='/dev/ttyUSB0', baudrate=9600, timeout=.1)

i = 1
while i != 0:
    ser.write(bytes("A", 'ascii'))
    sleep(2)
    temperature = ser.readline().decode('ascii').strip()

    print (temperature)

ser.close() 

