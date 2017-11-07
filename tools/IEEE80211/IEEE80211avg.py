# -*- coding: utf-8 -*-
import time
import math
from IEEE80211scan import unique_wifi_scan

# Mede o RSSI Médio a um metro de distância de um alvo

WFaddr = "C0:3F:0E:D0:D8:15"
SSID = "IGORLANDIA"
WFinterface = "wlp3s0"
repeticao = 100
"""
count = 0
sum_rssi_wf = 0

for i in range(repeticao):
    rssi_wf = float(unique_wifi_scan(WFinterface, WFaddr))
    if (rssi_wf != 0 and i > 3):  # reduz a possibilidade de valores iniciais falsos de RSSI esperando por 9 seg e elimina valores 0
        count = count + 1
        sum_rssi_wf = sum_rssi_wf + rssi_wf
        avg_rssi_wf = sum_rssi_wf / count
        print "Sinal médio:  " + str(avg_rssi_wf)
        print "RSSI: " + str(rssi_wf)
        print "Amostra número: " + str(count)
        print " "
    time.sleep(2) # para aguardar por uma variação maior por parte do IWLIST

"""
n = 3  # Path loss exponent(n) = 1.5
c = 10  # Environment constant(C) = 10
A0 = float(-26)  # Average RSSI value at d0
actual_dist = 100  # Static distance between transmitter and Receiver in cm
sum_error = 0
count = 0
avg_distance = 0

for i in range(repeticao):
    rssi_wf = float(unique_wifi_scan(WFinterface, WFaddr))
    if (rssi_wf != 0 and i > 10):  # reduces initial false values of RSSI using initial delay of 10sec
        count = count + 1
        x = float((rssi_wf - A0) / (-10 * n))  # Log Normal Shadowing Model considering d0 =1m where
        distance = (math.pow(10, x) * 100) + c
        error = abs(actual_dist - distance)
        sum_error = sum_error + error
        avg_error = sum_error / count
        print "Average Error=  " + str(avg_error)
        print "Error=  " + str(error)
        print "Approximate Distance:" + str(distance)
        print "RSSI: " + str(rssi_wf)
        print "Count: " + str(count)
        print " "
    time.sleep(1)
