#you can run test-visa.py first to find out correct GPIB interface
#then edit it in table.py
#emrea, Feb 2019

import table

tbl = table.Table() #init turn table device

if not table.isCorrectDev():
    print("CO2000 controller not found or wrong device selected, exiting!!!")
    tbl.close()
    sys.exit(1)

print("Current angle of table")
print(tbl.getAngle())

#Table go to angle
tbl.goAngle(130)

tbl.close()
