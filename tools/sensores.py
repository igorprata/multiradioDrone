# -*- coding: utf-8 -*-
from navio2 import uavstate
from tools.IEEE80211 import IEEE80211scan
from tools.bluetooth import BTrssi


def sensors(vehicle, repeticao, WFinterface, BTaddr, output):
    uavstate.uavstatus(vehicle, output)
    uavstate.uavsensors(vehicle, repeticao, output)
    IEEE80211scan.scan_wifi(repeticao, WFinterface, output)
    BTrssi.scan_bluetooth(repeticao, BTaddr, output)


#   print '\033[1m' + "PARA DEIXAR EM NEGRITO"
#   print '\033[0m'