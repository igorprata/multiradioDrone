# -*- coding: utf-8 -*-
from navio2 import uavstate
from tools.IEEE80211 import IEEE80211scan
from tools.bluetooth import BTscanpaired


########################### Biblioteca que dispara os métodos de todos os sensores utilizados pelo VANT ###########################


def sensors(vehicle, repeticao, WFinterface, BTaddr, output):
    uavstate.uavstatus(vehicle, output)
    uavlocal = uavstate.uavsensors(vehicle, repeticao, output)
    IEEE80211scan.scan_wifi(repeticao, WFinterface, output)
    BTscanpaired.scan_bluetooth(repeticao, BTaddr, output)
    return uavlocal
