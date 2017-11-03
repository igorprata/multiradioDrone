from tools import IEEE80211
from navio2 import uavstate

def sensors(vehicle, repeticao, interface, output):
    uavstate.uavstatus(vehicle)
    uavstate.uavsensors(vehicle)
    print '\033[1m' + " Sinal WIFI:"
    IEEE80211.scan_wifi(repeticao, interface, output)
    print '\033[0m'