#!/usr/bin/env python
import sys
import time
import serial

fIn = open(sys.argv[1],"r")
serial = serial.Serial(port = sys.argv[2], baudrate = 9600, parity = serial.PARITY_NONE, stopbits = serial.STOPBITS_ONE, bytesize = serial.EIGHTBITS, xonxoff = True)

try:
	speed = sys.argv[3]
except:
	speed = 2

line = fIn.read().splitlines()
commands = []
for l in line:
	for c in l.replace(' ', ';').split(';'):
		if c != '':
			commands.append(c)
commandsMissing = []

serial.flush()

for index,c in enumerate(commands[:len(commands)-1]):
	if c[:2] == "IN":
		serial.write('\x1B\x03'.encode())
		serial.write("FU3564,5268\x03".encode())	
		serial.write("FM1\x03".encode())	
		serial.write("TB50,1\x03".encode())	
		serial.write("FO3564\x03".encode())	
		serial.write("&100,100,100,\0,0,Z5588,4064,L0,!{}.0\x03".format(speed).encode())	
		serial.write("FX8,0\x03".encode())	
	elif c[:2] == "PD":
		serial.write("D".encode())
		for sc in c[2:len(c)]:
			serial.write(sc.encode())
		serial.write('\x03'.encode())	
	elif c[:2] == "PA":
		serial.write("M".encode())
		for sc in c[2:len(c)]:
			serial.write(sc.encode())
		serial.write('\x03'.encode())
	elif c[:2] == "PU":
		serial.write("M".encode())
		serial.write(c[2:len(c)].encode())
		serial.write('\x03'.encode())	
	elif c[:2] == "SP":
		serial.write("j".encode())
		serial.write(c[2:len(c[2:])-1].encode())
		serial.write('\x03'.encode())
	else:
		commandsMissing.append(c)
		pass

serial.write("&1,1,1,TB50,0\x03".encode())
serial.write("FO0\x03".encode())    
serial.write("H,\x03".encode())
serial.flush()

time.sleep(10) #wait for the serial buffer to be flushed

if len(commandsMissing) > 0:
	serial.write("The following commands where missing")
	serial.write(commandsMissing)

exit(0)
