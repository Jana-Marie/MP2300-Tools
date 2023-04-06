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

mode = 0 # 0 = absolute, 1 = relative
out = "" # output string, written to file

for index,c in enumerate(commands[:len(commands)-1]):
	if c[:2] == "IN": # init
		out += '\x1B'
		out += '\x03'
		out += "FU3564,5268"
		out += '\x03'
		out += "FM1"
		out += '\x03'
		out += "TB50,1"
		out += '\x03'
		out += "FO3564"
		out += '\x03'
		out += "&100,100,100,\0,0,Z5588,4064,L0,!{}.0".format(speed)	
		out += '\x03'
		out += "FX8,0"
		out += '\x03'
	elif c[:2] == "PD": # pen down → draw
		if mode == 0: # draw in relative 
			out += "D"
		else:
			out += "E"
		for sc in c[2:]:
			out += sc
		out += '\x03'
	elif c[:2] == "PA": # plot absolute
		mode = 0 # switch to absolute mode
		if len(c) > 2:
			out += "M"
			for sc in c[2:]:
				out += sc
			out += '\x03'
	elif c[:2] == "PU":
		if mode == 0:
			out += "M"
		else:
			out += "O"
		out += c[2:]
		out += '\x03'
	elif c[:2] == "SP":
		out += "j"
		out += c[2:]
		out += '\x03'
	elif c[:2] == "VS":
		out += "!"
		out += c[2:]
		out += '\x03'
	elif c[:2] == "PR": # switch to relative movement
		mode = 1
		if len(c) > 2:
			out += "O"
			for sc in c[2:]:
				out += sc
			out += '\x03'
	else:
		commandsMissing.append(c)
		pass

	print("{}%".format((int)(((index+1)/(len(commands)-1))*100)), end='\r', flush=True)
out += "&1,1,1,TB50,0\x03"
out += "FO0\x03"    # feed the page out
out += "H,"         # halt


fOut.write(out)
print()
print("Written file: {}".format(sys.argv[2]))

if len(commandsMissing) > 0:
	print("The following commands where missing")
	print(commandsMissing)

exit(0)
