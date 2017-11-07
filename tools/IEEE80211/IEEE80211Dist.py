# -*- coding: utf-8 -*-
import time
import math

from IEEE80211scan import unique_wifi_scan

def wifi_dist(WFinterface, WFaddr, repeticao):

    n = 3  # Path loss exponent(n) = 1.5
    c = 10  # Environment constant(C) = 10
    A0 = float(-24)  # Average RSSI value at d0
    sum_distance = 0
    count = 0
    avg_distance = 0

    for i in range(repeticao):
        rssi_wf = float(unique_wifi_scan(WFinterface, WFaddr))
        if (rssi_wf != 0):  # Evita contabilizar valores ZERO em certas interfaces de rede
            count = count + 1
            x = float((rssi_wf - A0) / (-10 * n))  # Log Normal Shadowing Model considering d0 =1m where
            distance = (math.pow(10, x) * 100) + c
            sum_distance = sum_distance + distance
            avg_distance = sum_distance / count
        time.sleep(1)
    return avg_distance