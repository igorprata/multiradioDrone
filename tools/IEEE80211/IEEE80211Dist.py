# -*- coding: utf-8 -*-
import math


########################### Biblioteca que verifica a distância média de um dispositivo Wifi ###########################


def wifi_dist(WFaddr, full_wifi_scan):

    n = 3  # Path loss exponent(n) = 1.5
    c = 10  # Environment constant(C) = 10
    A0 = float(-24)  # Average RSSI value at d0
    sum_distance = 0
    count = 0
    avg_distance = 0

    for scan_repetition in full_wifi_scan:
        for wifi_ap in scan_repetition:
            if wifi_ap[0] == WFaddr:
                rssi_wf = wifi_ap[1]
                if (rssi_wf != 0):  # Evita contabilizar valores ZERO em certas interfaces de rede
                    count = count + 1
                    x = float((rssi_wf - A0) / (-10 * n))  # Log Normal Shadowing Model considering d0 =1m where
                    distance = (math.pow(10, x) * 100) + c
                    sum_distance = sum_distance + distance
                    avg_distance = sum_distance / count
    return avg_distance