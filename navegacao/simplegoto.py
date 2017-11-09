# -*- coding: utf-8 -*-
import time

from dronekit import VehicleMode, LocationGlobalRelative
from tools import sensores
# from tools import sensores, camera                      # para habilitar o suporte a cameras
from tools.IEEE80211 import IEEE80211Dist
from tools.bluetooth import BTDist


########################### Simples biblioteca que realiza navegação a pontos LAT, LON, ALT preestabelecidos no array COORDENADAS e dispara coletas em cada ponto ###########################


def pontoaponto(aparelho, repeticao, WFinterface, WFaddr, BTaddr, output):
    print("Definindo como padrão a velocidade aérea de 3 metros por segundo")
    aparelho.airspeed = 3
    time.sleep(1)

    coordenadas = [(-22.6065254211425781, -43.4078941345214844, 8),(-22.6065349578857422, -43.407806396484375, 8),(-22.6064414978027344, -43.4078102111816406, 8),(-22.6064109802246094, -43.407989501953125, 8),(-22.6065559387207031, -43.4079933166503906, 8),(-22.6066148915314784, -43.407880961894989, 8)]
    dist_wf = []
    dist_bt = []
    uavlocal = []
    wayPointNum = 0

    # Voa até o ponto X
    for coordenada in coordenadas:
        uavlocal.append(sensores.sensors(aparelho, repeticao, WFinterface, BTaddr, output))
        time.sleep(repeticao)
        dist_wf.append(IEEE80211Dist.wifi_dist(WFinterface, WFaddr, repeticao))
        dist_bt.append(BTDist.bt_dist_paired(BTaddr,repeticao))
#        camera.camera_gimbal(aparelho, "ground", wayPointNum) # Tira uma foto do solo
#        camera.camera_gimbal(aparelho, "home", wayPointNum) # Tira uma foto do alvo
        time.sleep(repeticao)
        print "Distância WIFI do alvo ao ponto {}: {}cm".format(wayPointNum, dist_wf[wayPointNum])
        print "Distância Bluetooth do alvo ao ponto {}: {}cm".format(wayPointNum, dist_bt[wayPointNum])
        wayPointNum += 1
        print "Voando até o ponto {}".format(wayPointNum)
        point = LocationGlobalRelative(coordenada[0],coordenada[1],coordenada[2])
        aparelho.simple_goto(point)
        time.sleep(10)


    # Retorna a aeronave ao ponto de decolagem
    uavlocal.append(sensores.sensors(aparelho, repeticao, WFinterface, BTaddr, output))
    time.sleep(repeticao)
    dist_wf.append(IEEE80211Dist.wifi_dist(WFinterface, WFaddr, repeticao))
    dist_bt.append(BTDist.bt_dist_paired(BTaddr, repeticao))
#    camera.camera_gimbal(aparelho, "ground", wayPointNum)  # Tira uma foto do solo
#    camera.camera_gimbal(aparelho, "home", wayPointNum)  # Tira uma foto do alvo
    time.sleep(repeticao)
    print "Distância WIFI do alvo ao ponto {}: {}cm".format(wayPointNum, dist_wf[wayPointNum])
    print "Distância Bluetooth do alvo ao ponto {}: {}cm".format(wayPointNum, dist_bt[wayPointNum])
    wayPointNum += 1
    print "Retornando ao ponto de Decolagem"
    aparelho.mode = VehicleMode("RTL")
    
    return (dist_wf,dist_bt,uavlocal)