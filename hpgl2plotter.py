#!/usr/bin/env python
import sys
import time

fIn = open(sys.argv[1],"r")

try:
	speed = sys.argv[2]
except:
	speed = 2

line = fIn.read().splitlines()
commands = []
for l in line:
	for c in l.replace(' ', ';').split(';'):
		if c != '':
			commands.append(c)
commandsMissing = []

for index,c in enumerate(commands[:len(commands)-1]):
	if c[:2] == "IN":
		sys.stdout.write('\x1B')
		sys.stdout.write('\x03')		
		sys.stdout.write("FU3564,5268")	
		sys.stdout.write('\x03')	
		sys.stdout.write("FM1")	
		sys.stdout.write('\x03')			
		sys.stdout.write("TB50,1")	
		sys.stdout.write('\x03')			
		sys.stdout.write("FO3564")	
		sys.stdout.write('\x03')
		sys.stdout.write("&100,100,100,\0,0,Z5588,4064,L0,!{}.0".format(speed))	
		sys.stdout.write('\x03')	
		sys.stdout.write("FX8,0")	
		sys.stdout.write('\x03')
	elif c[:2] == "PD":
		sys.stdout.write("D")
		for sc in c[2:len(c)]:
			sys.stdout.write(sc)
			sys.stdout.flush()
			time.sleep(0.005)		
		sys.stdout.write('\x03')	
	elif c[:2] == "PA":
		sys.stdout.write("M")
		for sc in c[2:len(c)]:
			sys.stdout.write(sc)
			sys.stdout.flush()
			time.sleep(0.005)		
		sys.stdout.write('\x03')
	elif c[:2] == "PU":
		sys.stdout.write("M")
		sys.stdout.write(c[2:len(c)])
		sys.stdout.write('\x03')	
	elif c[:2] == "SP":
		sys.stdout.write("j")
		sys.stdout.write(c[2:len(c[2:])-1])
		sys.stdout.write('\x03')
	else:
		#sys.stdout.write("{} is missing. Payload: {}".format(c[:2],c[2:]))
		commandsMissing.append(c)
		pass
	time.sleep(0.05);
	sys.stdout.flush()
#time.sleep(0.02)
sys.stdout.write("&1,1,1,TB50,0\x03")
sys.stdout.write("FO0\x03")    # feed the page out
sys.stdout.write("H,")         # halt?

if len(commandsMissing) > 0:
	sys.stdout.write("The following commands where missing")
	sys.stdout.write(commandsMissing)

exit(0)
