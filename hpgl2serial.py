#!/usr/bin/env python
import sys
import time
import serial

if "help" in sys.argv[1]:
	print("Usage: hpgl2serial.py file.hpgl tty speed format center scale")
	print("speed: 0-200")
	print("format: A3 or A4")
	print("center: center on page?")
	print("scale: scaling. 100% = fill page")
	print("E.g.: hpgl2serial.py  ~/Pictures/drawing.hpgl /dev/ttyUSB0 100 A4 center 70%")
	exit(0)

fIn = open(sys.argv[1],"r")
serial = serial.Serial(port = sys.argv[2], baudrate = 9600, parity = serial.PARITY_NONE, stopbits = serial.STOPBITS_ONE, bytesize = serial.EIGHTBITS, xonxoff = True)

try:
	speed = sys.argv[3]
except:
	speed = 2

try:
	arg1 = sys.argv[4]
except:
	arg1 = ""
try:
	arg2 = sys.argv[5]
except:
	arg2 = ""
try:
	arg3 = sys.argv[6]
except:
	arg3 = ""

if "A4" in arg1 or "A4" in arg2 or "A4" in arg3:
	format = "A4"
else:
	format = "A3"

if "center" in arg1 or "center" in arg2 or "center" in arg3:
	print("Plotting centered on landscape " + format)
	center = True
else:
	print("Plotting bottom-left on landscape " + format)
	center = False

if "%" in arg1:
	scale = int(arg1.replace("%", ""))
	print("Scale to " + str(scale) + "%")
elif "%" in arg2:
	scale = int(arg2.replace("%", ""))
	print("Scale to " + str(scale) + "%")
elif "%" in arg3:
	scale = int(arg3.replace("%", ""))
	print("Scale to " + str(scale) + "%")
else:
	scale = 0
	print("No scaling")


line = fIn.read().splitlines()
commands = []
for l in line:
	for c in l.replace(' ', ';').split(';'):
		if c != '':
			commands.append(c)
commandsMissing = []

serial.flush()

# Max Size: 4050 x 2900

# DIN A3: 0,0 to 4000x2900 with 10mm border

xmaxA3 = 4050
ymaxA3 = 2900

xmaxA4 = 2030
ymaxA4 = 2835


xoffset = 0
yoffset = 0

xfilemin = 100000
xfilemax = 0

yfilemin = 100000
yfilemax = 0

for index,c in enumerate(commands[:len(commands)-1]):
	if c[:2] == "PD":
		list = c[2:len(c)].split (",")
		li = []
		for i in list:
			li.append(int(i))
		cnt = 0
		for i in li:
			if cnt % 2 == 0:
				if i < xfilemin:
					xfilemin = i
				if i > xfilemax:
					xfilemax = i
			else:
				if i < yfilemin:
					yfilemin = i
				if i > yfilemax:
					yfilemax = i
			cnt += 1

scalingfactor = 1.0

if format == "A3":
	if scale == 0 and (xfilemax > xmaxA3 or yfilemax > ymaxA3):
		print("File too big for selected format. Try again with scaling.")
		exit(0)
	elif scale <= 100:
		if ((xfilemax - xfilemin) / xmaxA3) > ((yfilemax - yfilemin) / ymaxA3):
			scalingfactor = (xmaxA3 / (xfilemax - xfilemin)) * (scale / 100)
		else:
			scalingfactor = (ymaxA3 / (yfilemax - yfilemin)) * (scale / 100)

	if center == True:
		xoffset = (xmaxA3 - ((xfilemax - xfilemin) * scalingfactor)) / 2
		yoffset = (ymaxA3 - ((yfilemax - yfilemin) * scalingfactor)) / 2


if format == "A4":
	if scale == 0 and (xfilemax > xmaxA4 or yfilemax > ymaxA4):
		print("File too big for selected format. Try again with scaling.")
		exit(0)
	elif scale <= 100:
		if ((xfilemax - xfilemin) / xmaxA4) > ((yfilemax - yfilemin) / ymaxA4):
			scalingfactor = (xmaxA4 / (xfilemax - xfilemin)) * (scale / 100)
		else:
			scalingfactor = (ymaxA4 / (yfilemax - yfilemin)) * (scale / 100)

	if center == True:
		xoffset = (xmaxA4 - ((xfilemax - xfilemin) * scalingfactor)) / 2
		yoffset = (ymaxA4 - ((yfilemax - yfilemin) * scalingfactor)) / 2
#exit(0)



for index,c in enumerate(commands[:len(commands)-1]):
	if c[:2] == "IN":
		serial.write('\x1B\x03'.encode())
		serial.write("FU3564,5268\x03".encode())
		#serial.write("FU564,268\x03".encode())
		serial.write("FM1\x03".encode())
		serial.write("TB50,1\x03".encode())
		serial.write("FO3564\x03".encode())
		serial.write("&100,100,100,\\0,0,Z5588,4064,L0,!{}.0\x03".format(speed).encode())
		serial.write("FX8,0\x03".encode())

		#serial.write("M200,200\x03".encode())
		#serial.write("SO\x03".encode())
	elif c[:2] == "PD":
		serial.write("D".encode())

		list = c[2:len(c)].split (",")
		li = []
		for i in list:
			li.append(int(i))
		cmd = ""
		cnt = 0
		for i in li:
			if cnt % 2 == 0:
				cmd += str(int(i*scalingfactor+xoffset)) + ","
			elif cnt == len(li)-1:
				cmd += str(int(i*scalingfactor+yoffset))
			else:
				cmd += str(int(i*scalingfactor+yoffset)) + ","
			cnt += 1

			if cnt % 512 == 0: # split up very long commands
				serial.write(cmd.encode())
				cmd = ""
				serial.write('\x03'.encode())
				resp = 0
				while resp != 1344:
					serial.write("V".encode())
					serial.write('\x03'.encode())
					resp = int(serial.readline())
					time.sleep(0.1)
				serial.write("D".encode())

		serial.write(cmd.encode())
		#print(cmd)
		serial.write('\x03'.encode())

		resp = 0
		while resp != 1344:
			serial.write("V".encode())
			serial.write('\x03'.encode())
			resp = int(serial.readline())
			time.sleep(0.1)
			#print(resp)


	elif c[:2] == "PA": # Never used?
		serial.write("M".encode())
		for sc in c[2:len(c)]:
			list = c[2:len(c)].split (",")
			li = []
			for i in list:
				li.append(int(i))
			cmd = ""
			cnt = 0
			for i in li:
				if cnt % 2 == 0:
					cmd += str(int(i*scalingfactor+xoffset)) + ","
				else:
					cmd += str(int(i*scalingfactor+yoffset)) + ","
				cnt += 1
		serial.write(cmd.encode())
		#print(cmd)
		serial.write('\x03'.encode())
	elif c[:2] == "PU":
		serial.write("M".encode())
		list = c[2:len(c)].split (",")
		li = []
		for i in list:
			li.append(int(i))
		cmd = str(int(li[0]*scalingfactor + xoffset)) + "," + str(int(li[1]*scalingfactor + yoffset))
		serial.write(cmd.encode())
		#print(cmd)
		serial.write('\x03'.encode())
	elif c[:2] == "SP":
		serial.write("j".encode())
		serial.write(c[2:len(c[2:])-1].encode())
		print(c[2:len(c[2:])-1])
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
