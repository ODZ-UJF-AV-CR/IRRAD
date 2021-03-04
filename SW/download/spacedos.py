#!/usr/bin/python3
#
# Logger for KID dosimeter
# 

import time
import serial

#port = '/dev/ttyACM0'
port = '/dev/ttyUSB2'

#baud = 115200
baud = 9600

ser = serial.Serial(port, baud, timeout=1)

def handle_data(data):
  print (data,end='')
  datafname = "spacedos.csv"
  with open(datafname, "a") as nbf:
    nbf.write(data)
  nbf.close()

while True:
	reading = ser.readline() #.rstrip()
	if (len(reading) > 0):
	  handle_data(str(int(round(time.time(),0))) + ',' + reading.decode())


