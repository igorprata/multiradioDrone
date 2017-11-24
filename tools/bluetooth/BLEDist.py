# -*- coding: utf-8 -*-
import math


########################### Biblioteca que verifica a distância média de um dispositivo Bluetooth BLE ###########################


def ble_dist(BLEaddr, full_ble_scan):

    n = 1.5  #Path loss exponent(n) = 1.5
    c = 10   #Environment constant(C) = 10
    A0 = 2   #Average RSSI value at d0
    sum_distance = 0
    count = 0
    avg_distance = 0

    for ble_ap in full_ble_scan:
        if ble_ap[0].lower() == BLEaddr.lower():
            rssi_ble = float(ble_ap[3])
            if (rssi_ble != 0):                    #reduces initial false values of RSSI using initial delay of 10sec
                count = count + 1
                x = float((rssi_ble-A0)/(-10*n))         #Log Normal Shadowing Model considering d0 =1m where
                distance = (math.pow(10,x) * 100) + c
                sum_distance = sum_distance + distance
                avg_distance = sum_distance / count
    return avg_distance


