# -*- coding: utf-8 -*-
import argparse
import time

from navio2 import conecta, uavstate
# from tools.Multilateration import multilateration
# from dronekit import VehicleMode, LocationGlobalRelative
from tools import sensores
# from tools import sensores, camera                      # para habilitar o suporte a cameras
from tools.IEEE80211 import IEEE80211Dist
from tools.bluetooth import BTDist, BTscanpaired, BLEscan, BLEDist
from navio2 import uavstate
from tools.IEEE80211 import IEEE80211scan


##################### Código para OBSERVAR o voo controlado externamente por uma missão #############################


parser = argparse.ArgumentParser(description='Comanda o drone em uma rota de voo estabelecida e executa o sensoriamento.')

parser.add_argument('--connect',
                    help=" Interface de conexão com o veículo. Se não for definida, a porta 1450 local será automaticamente usada. Padrão: 127.0.0.1:14550")
parser.add_argument('--loop',
                    help=" Define quantas vezes os dados dos sensores serão coletados em cada waypoint. Padrão: 3")
parser.add_argument('--WFinterface',
                    help=" Define qual interface de rede será usada. Padrão: wlp3s0")
parser.add_argument('--BTinterface',
                    help=" Define qual interface bluettoth será usada. Padrão: 1")
parser.add_argument('--WFaddr',
                    help=" Define qual endereco WIFI será verificado. Padrão:")
parser.add_argument('--BTaddr',
                    help=" Define qual endereco Bluetooth será verificado. Padrão: 00:02:72:D5:6E:5D")
parser.add_argument('--BTstandard',
                    help=" Define qual o padão bluetooth a ser usado (BT ou BLE). Padrão: BLE")
parser.add_argument('--output',
                    help=" Define qual o tipo de saída a ser usada (screen, file ou SQL). Padrão: screen")

args = parser.parse_args()

connection_string = args.connect
repeticao = args.loop
WFinterface = args.WFinterface
BTinterface = args.BTinterface
WFaddr = args.WFaddr
BTaddr = args.BTaddr
BTstandard = args.BTstandard
output = args.output

# Valores padroes se nao forem especificados
if not connection_string:
    connection_string = "127.0.0.1:14550"
if not repeticao:
    repeticao = 20
if not WFinterface:
    WFinterface = "wlx20e7170213df"
if not BTinterface:
    BTinterface = 0
if not WFaddr:
#    WFaddr = 'C0:3F:0E:D0:D8:15' # igorlandia
#    WFaddr = 'B8:5A:73:A4:E8:9E' # Galaxy Duos
    WFaddr = '84:C9:B2:69:97:B2' # Netgear
if not BTaddr:
#    BTaddr = '00:02:72:D5:6E:5D' # rc-control???B8:5A:73:A4:E8:9D
#    BTaddr = 'B8:5A:73:A4:E8:9D'  # Galaxy Duos
#    BTaddr = 'f4:f5:d8:fc:57:a5'  # BLE vizinho
    BTaddr = '68:C4:4D:81:6D:02'  # XT1650
if not BTstandard:
    BTstandard = "BT"
if not output:
    output = "file"

# Executa a conexao an aeronave e recebe a classe vehicle devolta
veiculo = conecta.conexao(connection_string)

# Listagem dos parametros de status do veiculo e modo de voo
print " GPS: %s" % veiculo.gps_0
print " Global Location (relative altitude): %s" % veiculo.location.global_relative_frame
uavstate.uavversion(veiculo)

# Grava os sensores em arquivo
with open('uavsensors.dump', "a") as f:
    f.write("Posição: {}\n".format(veiculo.location.global_relative_frame))
    f.write("Coleta realizada no Tempo: {}\n".format(time.ctime()))
    f.close()
uavlocal = uavstate.uavsensors(veiculo, repeticao, output)

print "A posição do sensor é: {}".format(veiculo.location.global_relative_frame)

# Registra o inicio do arquivo para não perder a referencia do ponto de coleta de WIFI, executa o rastreamento ambiental de sinais WIFI e estimativa de distância de WIFI
with open('wifiscan.dump', "a") as f:
    f.write("Posição: {}\n".format(veiculo.location.global_relative_frame))
    f.write("Coleta realizada no Tempo: {}\n".format(time.ctime()))
    f.close()
full_wifi_scan = IEEE80211scan.scan_wifi(repeticao, WFinterface, output)
print "Terminou de coletar dados WIFI. Agora, calculando a distância"
dist_wf_avg = (IEEE80211Dist.wifi_dist(WFaddr, full_wifi_scan))
with open('wifidist.dump', "a") as f:
    f.write("Posição: {}\n".format(veiculo.location.global_relative_frame))
    f.write("Coleta realizada no Tempo: {}\n".format(time.ctime()))
    f.write("Distância WIFI do alvo é: {}cm".format(dist_wf_avg))
    f.close()

print "Distância WIFI do alvo é: {}cm".format(dist_wf_avg)

# Registra o inicio do arquivo para não perder a referencia do ponto de estimativa de distância de Bluetooth e executa o rastreamento ambiental de dispositivos pariados

if BTstandard == "BLE":
    with open('blescan.dump', "a") as f:
        f.write("Posição: {}\n".format(veiculo.location.global_relative_frame))
        f.write("Coleta realizada no Tempo: {}\n".format(time.ctime()))
        f.close()
    full_ble_scan = BLEscan.scan_ble(repeticao, output, BTinterface)
    print "Terminou de coletar dados BLE. Agora, calculando a distância"
    dist_bt_avg = BLEDist.ble_dist(BTaddr,full_ble_scan)
    with open('bledist.dump', "a") as f:
        f.write("Posição: {}\n".format(veiculo.location.global_relative_frame))
        f.write("Coleta realizada no Tempo: {}\n".format(time.ctime()))
        f.write("Distância Bluetooth BLE do alvo é: {}cm".format(dist_bt_avg))
        f.close()

elif BTstandard == "BT":
    with open('btscan.dump', "a") as f:
        f.write("Posição: {}\n".format(veiculo.location.global_relative_frame))
        f.write("Coleta realizada no Tempo: {}\n".format(time.ctime()))
        f.close()
    full_bt_scan = BTscanpaired.scan_bluetooth(repeticao, BTaddr, output)
    print "Terminou de coletar dados Bluetooth. Agora, calculando a distância"
    dist_bt_avg = BTDist.bt_dist_paired(BTaddr, full_bt_scan)
    with open('btdist.dump', "a") as f:
        f.write("Posição: {}\n".format(veiculo.location.global_relative_frame))
        f.write("Coleta realizada no Tempo: {}\n".format(time.ctime()))
        f.write("Distância Bluetooth do alvo é: {}cm".format(dist_bt_avg))
        f.close()

print "Distância bluetooth do alvo é: {}cm".format(dist_bt_avg)

# Fecha o objeto veiculo antes de terminar o script
print("Desconectando do Veículo")
veiculo.close()