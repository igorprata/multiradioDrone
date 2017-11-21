# -*- coding: utf-8 -*-
import argparse
import time
import sys
import os

from navio2 import conecta, uavstate
from tools.Multilateration import multilateration
from dronekit import VehicleMode, LocationGlobalRelative
from tools import sensores
# from tools import sensores, camera                      # para habilitar o suporte a cameras
from tools.IEEE80211 import IEEE80211Dist, IEEE80211scan
from tools.bluetooth import BTDist, BTscanpaired, BLEscan, BLEDist
from navegacao import missionManager, uavCommands, takeoff


##################### Código para OBSERVAR o voo controlado externamente por uma missão #############################


parser = argparse.ArgumentParser(description='Comanda o drone em uma rota de voo estabelecida e executa o sensoriamento.')

parser.add_argument('--connect',
                    help=" Interface de conexão com o veículo. Se não for definida, a porta 1450 local será automaticamente usada. Padrão: 127.0.0.1:14550")
parser.add_argument('--loop',
                    help=" Define quantas vezes os dados dos sensores serão coletados em cada waypoint. Padrão: 3")
parser.add_argument('--WFinterface',
                    help=" Define qual interface de rede será usada. Padrão: wlp3s0")
parser.add_argument('--WFaddr',
                    help=" Define qual endereco WIFI será verificado. Padrão:")
parser.add_argument('--BTaddr',
                    help=" Define qual endereco Bluetooth será verificado. Padrão: 00:02:72:D5:6E:5D")
parser.add_argument('--BTstandard',
                    help=" Define qual o padão bluetooth a ser usado (BT ou BLE). Padrão: BLE")
parser.add_argument('--BTinterface',
                    help=" Define qual interface bluettoth será usada. Padrão: 0")
parser.add_argument('--output',
                    help=" Define qual o tipo de saída a ser usada (screen, file ou SQL). Padrão: screen")
parser.add_argument('--mission_plan',
                    help=" Define qual o arquivo de missão de voo será utilizado. Padrão: mission.txt")

args = parser.parse_args()

connection_string = args.connect
repeticao = args.loop
WFinterface = args.WFinterface
WFaddr = args.WFaddr
BTaddr = args.BTaddr
BTstandard = args.BTstandard
BTinterface = args.BTinterface
output = args.output
mission_plan = args.mission_plan

# Define valores padroes se nao forem especificados
if not connection_string:
    connection_string = "127.0.0.1:14550"
if not repeticao:
    repeticao = 1
if not WFinterface:
    WFinterface = "wlp3s0"
if not WFaddr:
#    WFaddr = 'C0:3F:0E:D0:D8:15' # igorlandia
#    WFaddr = 'B8:5A:73:A4:E8:9E' # Galaxy Duos
    WFaddr = '84:C9:B2:69:97:B2'  # Netgear
if not BTaddr:
#    BTaddr = '00:02:72:D5:6E:5D' # rc-control???B8:5A:73:A4:E8:9D
#    BTaddr = 'B8:5A:73:A4:E8:9D'  # Galaxy Duos
#    BTaddr = 'f4:f5:d8:fc:57:a5'  # BLE vizinho
    BTaddr = '68:C4:4D:81:6D:02'  # XT1650
if not BTinterface:
    BTinterface = 0
if not BTstandard:
    BTstandard = "B"
if not output:
    output = "file"
if not mission_plan:
    mission_file = "mission.txt"

# Verifica privilégios de ROOT para executar consultas BLE
if BTstandard == "BLE" and not os.geteuid() == 0:
    sys.exit("Esse script só pode ser executado com privilégios de root")

# Executa a conexão com a aeronave e recebe a classe vehicle devolta
veiculo = conecta.conexao(connection_string)

# Listagem dos parametros de status do veiculo e modo de voo
uavstate.uavversion(veiculo)

# Espera alguns segundos para verificar a estabilidade
time.sleep(10)

######### !!!!! Área de controle opicional da aeronave (útil para iniciar os testes em ambientes simulados)!!!!! #########

# Carrega uma missão de voo:
missionManager.upload_mission(mission_file, veiculo)

# Dispara a Funcao de Decolagem
takeoff.armandtakeoff(8, veiculo)
time.sleep(5)
# Faz o vaículo entrar no modo automático e iniciar a missão
veiculo.mode = VehicleMode("AUTO")
time.sleep(5)

##########################################################################################################################


# listagem dos parametros de status do veiculo e modo de voo

veiculo.wait_ready('autopilot_version')
print "Altitude relative to home_location: %s" % veiculo.location.global_relative_frame.alt
print " Modo de voo: %s" % veiculo.mode.name

if veiculo.mode.name != "AUTO":
    print "não está em AUTO, aguardando"
    time.sleep(30)
else:
    print "O veículo está em AUTO, prosseguindo"

# Verifica parâmetros de Throttle
uavstate.uav_throttle(veiculo)

# Verifica se há posição de home no veículo
uavCommands.check_for_home(veiculo)

# Baixa a missão par aum array
missionlist = missionManager.download_mission(veiculo)
print "O número de pontos programados para essa missão de voo é: {}".format(veiculo.commands.count)


uavlocal = []   # Vetor de coordenadas onde foram realizadas as coletas
latlon = []     # Vetor de coordenadas Latitude e Londitude (apenas) onde foram realizadas as coletas
alt = []        # Vetor de altitudes (apenas) onde foram realizadas as coletas
dist_wf = []    # Em cm, como retornado pelo aloritmo de distância
dist_wf_km = [] # Em kilômetros para o algoritimo de multlateração
dist_bt = []    # Em cm, como retornado pelo aloritmo de distância
dist_bt_km =[]  # Em kilômetros para o algoritimo de multlateração
wayPointNum = 0 # Contador de Número de coletas realizadas


def actions(wayPointNum):
        print "Coleta realizada no Tempo: {}\n".format(time.ctime())
        print "Voando até o ponto: currentwaypoint {} ".format(veiculo._current_waypoint)
        print " Estado do Sistema: %s" % veiculo.system_status.state
        print " Bateria: %s" % veiculo.battery
        print " GPS: %s" % veiculo.gps_0
        print " Global Location (relative altitude): %s" % veiculo.location.global_relative_frame

#Prepara cabeçalho nos arquivos
        with open('uavsensors.dump', "a") as f:
            f.write("Posição: {}\n".format(veiculo.location.global_relative_frame))
            f.write("Coleta realizada no Tempo: {}\n".format(time.ctime()))
            f.close()
        with open('wifiscan.dump', "a") as f:
            f.write("Posição: {}\n".format(veiculo.location.global_relative_frame))
            f.write("Coleta realizada no Tempo: {}\n".format(time.ctime()))
            f.close()
        with open('btscan.dump', "a") as f:
            f.write("Posição: {}\n".format(veiculo.location.global_relative_frame))
            f.write("Coleta realizada no Tempo: {}\n".format(time.ctime()))
            f.close()
        with open('blescan.dump', "a") as f:
            f.write("Posição: {}\n".format(veiculo.location.global_relative_frame))
            f.write("Coleta realizada no Tempo: {}\n".format(time.ctime()))
            f.close()

# Coleta pontos onde as coletas foram executadas
        uavlocal.append(sensores.sensors(veiculo, repeticao, WFinterface, BTaddr, output))

# Dispara Rotinas WIFI
        full_wifi_scan = IEEE80211scan.scan_wifi(repeticao, WFinterface, output)
        print "Terminou de coletar dados WIFI. Agora, calculando a distância"
        dist_wf_avg = (IEEE80211Dist.wifi_dist(WFaddr, full_wifi_scan))
        dist_wf.append(dist_wf_avg)
        dist_wf_km.append(dist_wf_avg / 100000)
        print "Distância WIFI do alvo ao ponto {}: {}cm".format(wayPointNum, dist_wf_avg)

        with open('wifidist.dump', "a") as f:
            f.write("Posição: {}\n".format(veiculo.location.global_relative_frame))
            f.write("Coleta realizada no Tempo: {}\n".format(time.ctime()))
            f.write("Distância WIFI do alvo é: {}cm\n".format(dist_wf_avg))
            f.close()

# Dispara Rotinas BT
        if BTstandard == "BT":
            full_bt_scan = BTscanpaired.scan_bluetooth(repeticao, BTaddr, output)
            print "Terminou de coletar dados Bluetooth. Agora, calculando a distância"
            dist_bt_avg = BTDist.bt_dist_paired(BTaddr, full_bt_scan)
            dist_bt.append(dist_bt_avg)
            dist_bt_km.append(dist_bt_avg / 100000)
            with open('btdist.dump', "a") as f:
                f.write("Posição: {}\n".format(veiculo.location.global_relative_frame))
                f.write("Coleta realizada no Tempo: {}\n".format(time.ctime()))
                f.write("Distância Bluetooth do alvo é: {}cm\n".format(dist_bt_avg))
                f.close()
            print "Distância Bluetooth do alvo ao ponto {}: {}cm".format(wayPointNum, dist_bt_avg)

# Dispara Rotinas BLE
        elif BTstandard == "BLE":
            full_ble_scan = BLEscan.scan_ble(repeticao, output, BTinterface)
            print "Terminou de coletar dados BLE. Agora, calculando a distância"
            dist_bt_avg = BLEDist.ble_dist(BTaddr, full_ble_scan)
            dist_bt.append(dist_bt_avg)
            dist_bt_km.append(dist_bt_avg / 100000)
            with open('bledist.dump', "a") as f:
                f.write("Posição: {}\n".format(veiculo.location.global_relative_frame))
                f.write("Coleta realizada no Tempo: {}\n".format(time.ctime()))
                f.write("Distância Bluetooth BLE do alvo é: {}cm\n".format(dist_bt_avg))
                f.close()
            print "Distância BLE do alvo ao ponto {}: {}cm".format(wayPointNum, dist_bt_avg)

# Dispara Fotos
    #    camera.camera_gimbal(aparelho, "ground", wayPointNum) # Tira uma foto do solo
    #    camera.camera_gimbal(aparelho, "home", wayPointNum) # Tira uma foto do alvo

# Dispara multilateração a cada waypoint a partir de uma certa quantidade de pontos coletados
        if len(uavlocal) >= 3:
            for x in uavlocal:
                latlon.append(x[0])
                alt.append(x[1])
            multilateration.multilateration(latlon, dist_wf_km)  # mudar para a distância medida pela fusão de sensores

        wayPointNum = veiculo._current_waypoint
        return wayPointNum


while veiculo.mode == VehicleMode("AUTO"):
    if veiculo._current_waypoint in (3 ,5, 7, 9, 11, 13) and veiculo._current_waypoint>wayPointNum:
        wayPointNum = actions(veiculo._current_waypoint)
        print "Executada coleta no ponto wayPointNum {}".format(wayPointNum)
    if veiculo._current_waypoint == veiculo.commands.count:
        print "Alcançou o último ponto da missão"
        break
    else:
        print "Coleta não executada. Ainda não chegou no ponto certo!"
        time.sleep(3)

# Fecha o objeto veiculo antes de terminar o script
print("Desconectando do Veículo")
veiculo.close()


