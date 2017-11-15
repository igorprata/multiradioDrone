# -*- coding: utf-8 -*-
import argparse
import time

from navio2 import conecta, uavstate
# from tools.Multilateration import multilateration
# from dronekit import VehicleMode, LocationGlobalRelative
from tools import sensores
# from tools import sensores, camera                      # para habilitar o suporte a cameras
from tools.IEEE80211 import IEEE80211Dist
from tools.bluetooth import BTDist, BTscanpaired
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
parser.add_argument('--WFaddr',
                    help=" Define qual endereco WIFI será verificado. Padrão:")
parser.add_argument('--BTaddr',
                    help=" Define qual endereco Bluetooth será verificado. Padrão: 00:02:72:D5:6E:5D")
parser.add_argument('--output',
                    help=" Define qual o tipo de saída a ser usada (screen, file ou SQL). Padrão: screen")

args = parser.parse_args()

connection_string = args.connect
repeticao = args.loop
WFinterface = args.WFinterface
WFaddr = args.WFaddr
BTaddr = args.BTaddr
output = args.output

# Valores padroes se nao forem especificados
if not connection_string:
    connection_string = "127.0.0.1:14550"
if not repeticao:
    repeticao = 30
if not WFinterface:
    WFinterface = "wlp3s0"
if not WFaddr:
#    WFaddr = 'C0:3F:0E:D0:D8:15' # igorlandia
    WFaddr = 'B8:5A:73:A4:E8:9E' # Galaxy Duos
if not BTaddr:
#    BTaddr = '00:02:72:D5:6E:5D' # rc-control???B8:5A:73:A4:E8:9D
    BTaddr = 'B8:5A:73:A4:E8:9D'  # Galaxy Duos
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

# Registra o inicio do arquivo para não perder a referencia do ponto de coleta de WIFI, executa o rastreamento ambiental de sinais WIFI e estimativa de distância de WIFI
with open('wifiscan.dump', "a") as f:
    f.write("Posição: {}\n".format(veiculo.location.global_relative_frame))
    f.write("Coleta realizada no Tempo: {}\n".format(time.ctime()))
    f.close()
IEEE80211scan.scan_wifi(repeticao, WFinterface, output)

dist_wf_avg = (IEEE80211Dist.wifi_dist(WFinterface, WFaddr, repeticao))
with open('wifidist.dump', "a") as f:
    f.write("Posição: {}\n".format(veiculo.location.global_relative_frame))
    f.write("Coleta realizada no Tempo: {}\n".format(time.ctime()))
    f.write("Distância WIFI do alvo é: {}cm".format(dist_wf_avg))
    f.close()

# Registra o inicio do arquivo para não perder a referencia do ponto de estimativa de distância de Bluetooth e executa o rastreamento ambiental de dispositivos pariados
with open('btscan.dump', "a") as f:
    f.write("Posição: {}\n".format(veiculo.location.global_relative_frame))
    f.write("Coleta realizada no Tempo: {}\n".format(time.ctime()))
    f.close()
BTscanpaired.scan_bluetooth(repeticao, BTaddr, output)

dist_bt_avg = BTDist.bt_dist_paired(BTaddr, repeticao)
with open('btdist.dump', "a") as f:
    f.write("Posição: {}\n".format(veiculo.location.global_relative_frame))
    f.write("Coleta realizada no Tempo: {}\n".format(time.ctime()))
    f.write("Distância Bluetooth do alvo é: {}cm".format(dist_bt_avg))
    f.close()

print "A posição do sensor é: {}".format(veiculo.location.global_relative_frame)
print "Distância WIFI do alvo é: {}cm".format(dist_wf_avg)

time.sleep(10)

# Fecha o objeto veiculo antes de terminar o script
print("Desconectando do Veículo")
veiculo.close()