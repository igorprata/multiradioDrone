# -*- coding: utf-8 -*-
from bt_proximity import BluetoothRSSI
# from BTScan import unique_bt_scan
import math


########################### Biblioteca que verifica a distância média de um dispositivo Bluetooth (pareados ou não) ###########################


def bt_dist_paired(full_bt_scan):

    n = 1.5  #Path loss exponent(n) = 1.5
    c = 10   #Environment constant(C) = 10
    A0 = 2   #Average RSSI value at d0
    count = 0
    sum_distance = 0
    avg_distance = 0

    for i in full_bt_scan:
        rssi_bt = float(i)
#        if(rssi_bt!=0 and i>10):
        if (rssi_bt != 0):                    #reduces initial false values of RSSI using initial delay of 10sec
            count=count+1
            x = float((rssi_bt-A0)/(-10*n))         #Log Normal Shadowing Model considering d0 =1m where
            distance = (math.pow(10,x) * 100) + c
            sum_distance = sum_distance + distance
            avg_distance = sum_distance / count
    return avg_distance


