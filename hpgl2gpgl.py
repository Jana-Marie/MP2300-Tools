#!/usr/bin/env python
import sys
import time

fIn = open(sys.argv[1],"r")
fOut = open(sys.argv[2],"w")

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

print("Reading file: {}".format(sys.argv[1]))
print("Now processing {} lines of HPGL to GPGL".format(len(commands)-1))

for index,c in enumerate(commands[:len(commands)-1]):
	if c[:2] == "IN":
		fOut.write('\x1B')
		fOut.write('\x03')		
		fOut.write("FU3564,5268")	
		fOut.write('\x03')	
		fOut.write("FM1")	
		fOut.write('\x03')			
		fOut.write("TB50,1")	
		fOut.write('\x03')			
		fOut.write("FO3564")	
		fOut.write('\x03')
		fOut.write("&100,100,100,\0,0,Z5588,4064,L0,!{}.0".format(speed))	
		fOut.write('\x03')	
		fOut.write("FX8,0")	
		fOut.write('\x03')
	elif c[:2] == "PD":
		fOut.write("D")
		for sc in c[2:len(c[2:])-1]:
			fOut.write(sc)
			time.sleep(0.01)
		fOut.write('\x03')	
	elif c[:2] == "PA":
		fOut.write("M")
		for sc in c[2:len(c[2:])-1]:
			fOut.write(sc)
			time.sleep(0.01)
		fOut.write('\x03')
	elif c[:2] == "PU":
		fOut.write("M")
		fOut.write(c[2:len(c[2:])-1])
		fOut.write('\x03')	
	elif c[:2] == "SP":
		fOut.write("j")
		fOut.write(c[2:len(c[2:])-1])
		fOut.write('\x03')
	else:
		#print("{} is missing. Payload: {}".format(c[:2],c[2:]))
		commandsMissing.append(c)
		pass
	time.sleep(1)

	print("{}%".format((int)(((index+1)/(len(commands)-1))*100)), end='\r', flush=True)
fOut.write("&1,1,1,TB50,0\x03")
fOut.write("FO0\x03")    # feed the page out
fOut.write("H,")         # halt?

print()
print("Written file: {}".format(sys.argv[2]))

if len(commandsMissing) > 0:
	print("The following commands where missing")
	print(commandsMissing)

exit(0)
