# -*- coding: utf-8 -*-
import time

from dronekit import VehicleMode, LocationGlobalRelative
from tools import sensores
from tools.IEEE80211 import IEEE80211Dist
from tools.bluetooth import BTDist

def pontoaponto(aparelho, repeticao, WFinterface, WFaddr, BTaddr, output):
    print("Definindo como padrão a velocidade aérea de 3 metros por segundo")
    aparelho.airspeed = 3
    time.sleep(1)

    coordenadas = [(-22.6065254211425781, -43.4078941345214844, 8),(-22.6065349578857422, -43.407806396484375, 8),(-22.6064414978027344, -43.4078102111816406, 8),(-22.6064109802246094, -43.407989501953125, 8),(-22.6065559387207031, -43.4079933166503906, 8),(-22.6066148915314784, -43.407880961894989, 8)]
    dist_wf = []
    dist_bt = []
    uavlocal = []
    count = 0

    # Voa até o ponto X
    for coordenada in coordenadas:
        uavlocal.append(sensores.sensors(aparelho, repeticao, WFinterface, BTaddr, output))
        time.sleep(repeticao)
        dist_wf.append(IEEE80211Dist.wifi_dist(WFinterface, WFaddr, repeticao))
        dist_bt.append(BTDist.bt_dist_paired(BTaddr,repeticao))
        time.sleep(repeticao)
        print "Distância WIFI do alvo ao ponto {}: {}cm".format(count, dist_wf[count])
        print "Distância Bluetooth do alvo ao ponto {}: {}cm".format(count, dist_bt[count])
        count += 1
        print "Voando até o ponto {}".format(count)
        point = LocationGlobalRelative(coordenada[0],coordenada[1],coordenada[2])
        aparelho.simple_goto(point)
        time.sleep(10)


    # Retorna a aeronave ao ponto de decolagem
    uavlocal.append(sensores.sensors(aparelho, repeticao, WFinterface, BTaddr, output))
    time.sleep(repeticao)
    dist_wf.append(IEEE80211Dist.wifi_dist(WFinterface, WFaddr, repeticao))
    dist_bt.append(BTDist.bt_dist_paired(BTaddr, repeticao))
    time.sleep(repeticao)
    print "Distância WIFI do alvo ao ponto {}: {}cm".format(count, dist_wf[count])
    print "Distância Bluetooth do alvo ao ponto {}: {}cm".format(count, dist_bt[count])
    count += 1
    print "Retornando ao ponto de Decolagem"
    aparelho.mode = VehicleMode("RTL")
    
    return (dist_wf,dist_bt,uavlocal)