#!/usr/bin/env python

import time
from pmbus import PMBus

print("Initializing PMBUS... \n")

DRQ = PMBus(0x47,8) #New pmbus object with device address 0x12

# time.sleep(1)

# DRQ.setVinUVLimit(36.0)

time.sleep(1)

while True:

    # DRQ.setCurve_ICHG(53)
    # print("Curve_ICHG: " + str(DRQ.getCurve_ICHG()))

    for i in range (11,55):
        DRQ.setCurve_ICHG(i)
        time.sleep(2)
        ICHG = DRQ.getCurve_ICHG()
        print("Curve_ICHG: " + str(ICHG))
        print("--------->> sent: ",i)
        print("--------->> got: ",str(ICHG))

        if (i == ICHG):
            print("Success")
        else:
            print("----------------------------------->> Fail <<--------")
        time.sleep(2)


    # print("Tempurature: " + str(DRQ.getTempurature()))
    # print("Input Voltage: " + str(DRQ.getVoltageIn()))
    # print("Output Voltage: " + str(DRQ.getVoltageOut()))
    # print("Output Current: " + str(DRQ.getCurrent()))
    # print("Output Power: " + str(DRQ.getPowerOut(False)) + "\n\n") #False is caclulated from given values of current and voltage while True gets values from DRQ1250

    #DRQ.encodePMBus(34.0)

    time.sleep(1)
