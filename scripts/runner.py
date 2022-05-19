#!/usr/bin/env python

import time
from pmbus import PMBus

print("Initializing PMBUS... \n")

DRQ = PMBus(0x47,1) #New pmbus object with device address 0x12

# time.sleep(1)

# DRQ.setVinUVLimit(36.0)
# DRQ.regOff(hard=True)
# time.sleep(3)

# DRQ.regOn()
# time.sleep(3)
# DRQ.clearFaults()
# time.sleep(3)

print("PM Bus Version: ", hex(DRQ.getPmbusRev()))
# DRQ.setIoutFaultResponse(0x00)
# time.sleep(3)
# print("Response",DRQ.getIoutFaultResponse())


def config_curve(val):
    return config_param(DRQ.setCurveConfig, DRQ.getCurveConfig, val)

def config_ichg(val):
    return config_param(DRQ.setCurve_ICHG, DRQ.getCurve_ICHG, val)

def config_vbst(val):
    return config_param(DRQ.setCurve_vbst, DRQ.getCurve_vbst, val)

def config_vfloat(val):
    return config_param(DRQ.setCurve_vfloat, DRQ.getCurve_vfloat, val)

def config_cc_timeout(val):
    return config_param(DRQ.set_ccTimeout, DRQ.get_ccTimeout, val)

def config_cv_timeout(val):
    return config_param(DRQ.set_cvTimeout, DRQ.get_cvTimeout, val)

def config_float_timeout(val):
    return config_param(DRQ.set_floatTimeout, DRQ.get_floatTimeout, val)


def config_param(setter,getter,val):
    time.sleep(3)
    setter(val)
    print("val = ", val)
    time.sleep(3)
    ret_val = getter()
    print("ret_val = ", ret_val)
    if (ret_val == val):
        return True
    return False


def read_charge_status():
    charge_status = DRQ.get_chg_status()
    print("charge_status = ", charge_status)
    status = {
            "Fully Charged" :                           bool(charge_status & (0b1<<0)),
            "Constant Current Mode Status" :            bool(charge_status & (0b1<<1)),
            "Constant Voltage Mode Status" :            bool(charge_status & (0b1<<2)),
            "Float Mode Status" :                       bool(charge_status & (0b1<<3)),
            "EEPROM Charge Parameter Error" :           bool(charge_status & (0b1<<8)),
            "Temperature Compensation Status" :         bool(charge_status & (0b1<<10)),
            "Battery Detection" :                       bool(charge_status & (0b1<<11)),
            "Time-out Flag of Constant Current Mode" :  bool(charge_status & (0b1<<13)),
            "Time-out Flag of Constant Voltage Mode" :  bool(charge_status & (0b1<<14)),
            "Time-out Flag of Float Mode" :             bool(charge_status & (0b1<<15)),
        }
    print(status)

def read_status_cml():
    com_status = DRQ.get_status_cml()
    print("com_status = ", com_status)


while True:

    print(DRQ.getStatusSummary())

    print("FW version = ", "".join([chr(x) for x in DRQ.getMfrRevision()]))

    if (config_curve(0)):
        print("config_curve was sccessful")
    else:
        print("Failed to set config_curve")

    read_status_cml()
    if (config_ichg(25)):
        print("curve ichg was sccessful")
    else:
        print("Failed to set ichg")


    if (config_vbst(28)):
        print("curve vbst was sccessful")
    else:
        print("Failed to set vbst")

    if (config_vfloat(26)):
        print("curve vfloat was sccessful")
    else:
        print("Failed to set vfloat")

    read_status_cml()

    if (config_cc_timeout(70)):
        print("cc_timeout was sccessful")
    else:
        print("Failed to set cc_timeout")

    if (config_cv_timeout(75)):
        print("cv_timeout was sccessful")
    else:
        print("Failed to set cv_timeout")

    if (config_float_timeout(75)):
        print("float_timeout was sccessful")
    else:
        print("Failed to set float_timeout")


    read_charge_status()


    # print("Tempurature: " + str(DRQ.getTempurature()))
    # print("Input Voltage: " + str(DRQ.getVoltageIn()))
    # print("Output Voltage: " + str(DRQ.getVoltageOut()))
    # print("Output Current: " + str(DRQ.getCurrent()))
    # print("Output Power: " + str(DRQ.getPowerOut(False)) + "\n\n") #False is caclulated from given values of current and voltage while True gets values from DRQ1250

    #DRQ.encodePMBus(34.0)

    time.sleep(1)
