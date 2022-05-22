#!/usr/bin/env python

import time
from pmbus import PMBus

print("Initializing PMBUS... \n")

DRQ = PMBus(0x47,1) #New pmbus object with device address 0x12

# time.sleep(1)

# DRQ.setVinUVLimit(36.0)
# DRQ.regOff(hard=True)
# time.sleep(3)

DRQ.regOn()
time.sleep(3)


print("PM Bus Version: ", hex(DRQ.getPmbusRev()))

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

def config_iout(val):
    return config_param(DRQ.setIoutOCLimit, DRQ.getIoutOCLimit, val)

def config_vout_trim(val):
    return config_param(DRQ.setVoutTrim, DRQ.getVoutTrim, val)


def config_param(setter,getter,val):
    time.sleep(2)
    setter(val)
    print("val = ", val)
    time.sleep(2)
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


def initial_settings():

    try:
        DRQ.regOff(hard=True)
        time.sleep(3)
        if (config_iout(20)):
            print("config_iout was sccessful")
        else:
            print("--->>>Failed to set config_iout <<<--- ")

        if (config_vout_trim(3)):
            print("config_vout_trim was sccessful")
        else:
            print("--->>>Failed to set config_vout_trim <<<--- ")
        DRQ.regOn()
        time.sleep(3)
    except:
        initial_settings()



def reading_status():
    iout = 0
    vout_trim = 0
    # print(DRQ.getStatusSummary())
    # print("FW version = ", "".join([chr(x) for x in DRQ.getMfrRevision()]))
    # print("OC Response",hex(DRQ.getIoutFaultResponse()))
    print("Vout = ", DRQ.getVoltageOut())
    time.sleep(1)
    print("Vin = ",DRQ.getVoltageIn())
    time.sleep(1)
    iout = DRQ.getCurrent()
    print("Iout = ",iout)
    time.sleep(1)
    # if (iout < 15.0):
    #     vout_trim = DRQ.getVoutTrim()
    #     time.sleep(1)
    #     config_vout_trim(int(vout_trim) + 1)
    #     print("new vout trim = ", vout_trim +1 )
    print("")
    print("")
    time.sleep(3)

DOCKING_IND = 1

while True:
    if (DOCKING_IND):
            initial_settings()

    while True:
        try:
            reading_status()
        except:
            continue


    time.sleep(1)



    # DRQ.setIoutOCLimit(20)
    # time.sleep(3)
    # print("OC limit = " ,DRQ.getIoutOCLimit())

    # DRQ.setVoutTrim(3)
    # time.sleep(3)
    # print("vout trim = ", DRQ.getVoutTrim())



    # if (config_curve(25)):
    #     print("config_curve was sccessful")
    # else:
    #     print("Failed to set config_curve")

    # read_status_cml()
    # if (config_ichg(25)):
    #     print("curve ichg was sccessful")
    # else:
    #     print("Failed to set ichg")

    # if (config_vfloat(26)):
    #     print("curve vfloat was sccessful")
    # else:
    #     print("Failed to set vfloat")

    # if (config_vbst(28)):
    #     print("curve vbst was sccessful")
    # else:
    #     print("Failed to set vbst")




    # read_status_cml()

    # if (config_cc_timeout(70)):
    #     print("cc_timeout was sccessful")
    # else:
    #     print("Failed to set cc_timeout")

    # if (config_cv_timeout(75)):
    #     print("cv_timeout was sccessful")
    # else:
    #     print("Failed to set cv_timeout")

    # if (config_float_timeout(75)):
    #     print("float_timeout was sccessful")
    # else:
    #     print("Failed to set float_timeout")


    # read_charge_status()

    # time.sleep(1)
