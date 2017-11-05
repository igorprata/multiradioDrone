# -*- coding: utf-8 -*-
import time

from dronekit import VehicleMode, LocationGlobalRelative
from tools import sensores
from tools.IEEE80211 import IEEE80211Dist

def pontoaponto(aparelho, repeticao, WFinterface, WFaddr, BTaddr, output):
    print("Definindo como padrao a velocidade aerea de 3 metros por segundo")
    aparelho.airspeed = 3
    time.sleep(1)

    # Voa até o ponto 1
    sensores.sensors(aparelho, repeticao, WFinterface, BTaddr, output)
    time.sleep(repeticao)
    dist = IEEE80211Dist.wifi_dist(WFinterface, WFaddr, repeticao)
    time.sleep(repeticao)
    print "Distância até o ponto 0: {}cm".format(dist)
    print "Voando até o ponto 1"
    point1 = LocationGlobalRelative(-22.6065254211425781, -43.4078941345214844, 8)
    aparelho.simple_goto(point1)
    time.sleep(10)

    # Voa até o ponto 2
    sensores.sensors(aparelho, repeticao, WFinterface, BTaddr, output)
    time.sleep(repeticao)
    dist = IEEE80211Dist.wifi_dist(WFinterface, WFaddr, repeticao)
    time.sleep(repeticao)
    print "Distância até o ponto 1: {}cm".format(dist)
    print "Voando até o ponto 2"
    point2 = LocationGlobalRelative(-22.6065349578857422, -43.407806396484375, 8)
    aparelho.simple_goto(point2)
    time.sleep(9)

    # Voa até o ponto 3
    sensores.sensors(aparelho, repeticao, WFinterface, BTaddr, output)
    time.sleep(repeticao)
    dist = IEEE80211Dist.wifi_dist(WFinterface, WFaddr, repeticao)
    time.sleep(repeticao)
    print "Distância até o ponto 2: {}cm".format(dist)
    print "Voando até o ponto 3"
    point3 = LocationGlobalRelative(-22.6064414978027344, -43.4078102111816406, 8)
    aparelho.simple_goto(point3)
    time.sleep(9)

    # Voa até o ponto 4
    sensores.sensors(aparelho, repeticao, WFinterface, BTaddr, output)
    time.sleep(repeticao)
    dist = IEEE80211Dist.wifi_dist(WFinterface, WFaddr, repeticao)
    time.sleep(repeticao)
    print "Distância até o ponto 3: {}cm".format(dist)
    print "Voando até o ponto 4"
    point4 = LocationGlobalRelative(-22.6064109802246094, -43.407989501953125, 8)
    aparelho.simple_goto(point4)
    time.sleep(9)

    # Voa até o ponto 5
    sensores.sensors(aparelho, repeticao, WFinterface, BTaddr, output)
    time.sleep(repeticao)
    dist = IEEE80211Dist.wifi_dist(WFinterface, WFaddr, repeticao)
    time.sleep(repeticao)
    print "Distância até o ponto 4: {}cm".format(dist)
    print "Voando até o ponto 5"
    point5 = LocationGlobalRelative(-22.6065559387207031, -43.4079933166503906, 8)
    aparelho.simple_goto(point5)
    time.sleep(9)

    # Voa até o ponto 6
    sensores.sensors(aparelho, repeticao, WFinterface, BTaddr, output)
    time.sleep(repeticao)
    dist = IEEE80211Dist.wifi_dist(WFinterface, WFaddr, repeticao)
    time.sleep(repeticao)
    print "Distância até o ponto 5: {}cm".format(dist)
    print "Voando até o ponto 6"
    point6 = LocationGlobalRelative(-22.6066148915314784, -43.407880961894989, 8)
    aparelho.simple_goto(point6)
    time.sleep(9)

    # Retorna a aeronave ao ponto de decolagem
    sensores.sensors(aparelho, repeticao, WFinterface, BTaddr, output)
    time.sleep(repeticao)
    dist = IEEE80211Dist.wifi_dist(WFinterface, WFaddr, repeticao)
    time.sleep(repeticao)
    print "Distância até o ponto 6: {}cm".format(dist)
    print("Retornando ao ponto de Decolagem")
    aparelho.mode = VehicleMode("RTL")