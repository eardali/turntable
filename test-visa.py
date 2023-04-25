#find GPIB interface and edit it accordingly
#emrea, Feb 2019

import visa
import time

rm = visa.ResourceManager()
print(rm.list_resources())
#it will appear a list like below
#('ASRL1::INSTR', 'ASRL2::INSTR', 'GPIB0::7::INSTR')
#this device is addressed as GPIBxxx
#open device and query IDN to find your device
inst = rm.open_resource('GPIB0::7::INSTR')
print(inst.query("*IDN?"))
#returns something like
#innco GmbH,CO2000,6011210,1.24

#below some raw command examples, you can read these details from device manual
#using table.py is more handy, check test-table.py

#current pos
#select device and send command
inst.write("LD 1 DV")
inst.write("CP")
val =  inst.read()
print("Table position %s" % val)

#goto
print("Going to angle")
inst.write("LD 1 DV")
inst.write("LD 70.0 DG NP GO")

time.sleep(1)

#read motor status, 1 on, 0 off
inst.write("LD 1 DV")
inst.write("BU")
val =  inst.read()
print("Motor status %s" % val)

time.sleep(10)
#read pos
inst.write("LD 1 DV")
inst.write("CP")
val =  inst.read()
print("Table position %s" % val)

#read motor status, assume it reached angle and stopped
inst.write("LD 1 DV")
inst.write("BU")
val =  inst.read()
print("Motor status %s" % val)
