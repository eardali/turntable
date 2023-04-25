#!/usr/bin/python3

#---------README---------
#turn table operations for Innco CO2000
#emrea, Feb 2019

import visa
import time
import settings
import logging
import sys

#instrument name, get this by a simple script printing all devices
instName = 'GPIB0::7::INSTR'

#device IDN to check
idn = 'CO2000'

#position check interval
waitpos = 1 #sec

#disable pyvisa logging
logging.getLogger('pyvisa').setLevel(logging.WARNING)

class Table(object):
    
    #constructor for table object
    def __init__(self):
        self.rm = visa.ResourceManager()
        self.rm.list_resources()
        self.inst = self.rm.open_resource(instName)
        logging.debug(self.rm.list_resources())
    
    #check if correct GPIB device is opened or not, since there may be many other devices on bus
    def isCorrectDev(self):
        q = self.inst.query("*IDN?")
        if idn in q:
            return True
        else:
            return False

    #return float
    def getAngle(self):
        self.inst.write("LD 1 DV") #select turn table, 0 is antenna mast
        self.inst.write("CP")
        deg = self.inst.read() #.1f precision, such as 160.0
        logging.debug("Table position: %s", deg.strip('\n'))
        return float(deg)
    
    #check if table is still turning or not
    def isBusy(self):
        self.inst.write("LD 1 DV")
        self.inst.write("BU")
        val = self.inst.read()
        if int(val) == 1:
            return True
        elif int(val) == 0:
            return False
        else: 
            return None #shouldn't happen

    def goAngle(self, angle):
        if not (angle >= 0) and (angle <=360):
            print("Exiting script, turn table angle parameter is not in valid range [0,360]!!!")
            self.close()
            sys.exit(1)
        strAngle = '{:.1f}'.format(angle) #convert to string, one digit after point, ie 60.0
        command = "LD " + strAngle + " DG NP GO"
        logging.debug("Turn table goto command: %s", command)
        self.inst.write("LD 1 DV")
        self.inst.write(command)
        logging.debug("Turn table goto angle %s", str(angle))
        time.sleep(waitpos) #wait a bit before check motor status
        while (self.isBusy()):
            time.sleep(waitpos) #wait till motor stops
        
        time.sleep(waitpos)
        #self.isBusy()
        if not (self.getAngle() == angle):
            print("Exiting script, turn table is not at desired angle!!!")
            self.close()
            sys.exit(1)
            
        return True

    def close(self):
        self.inst.close()
        self.rm.close()
        del self.inst
