# -*- coding: utf-8 -*-
import argparse
import time
import sys
import os

from navio2 import conecta, uavstate
from tools.Multilateration import multilateration
# from dronekit import VehicleMode, LocationGlobalRelative
from tools import sensores
# from tools import sensores, camera                      # para habilitar o suporte a cameras
from tools.IEEE80211 import IEEE80211Dist, IEEE80211scan
from tools.bluetooth import BTDist, BTscanpaired, BLEscan, BLEDist


##################### Código para OBSERVAR o voo controlado externamente por uma missão #############################


parser = argparse.ArgumentParser(description='Comanda o drone em uma rota de voo estabelecida e executa o sensoriamento.')

parser.add_argument('--connect',
                    help=" Interface de conexão com o veículo. Se não for definida, a porta 1450 local será automaticamente usada. Padrão: 127.0.0.1:14550")
parser.add_argument('--loop',
                    help=" Define quantas vezes os dados dos sensores serão coletados em cada waypoint. Padrão: 3")
parser.add_argument('--WFinterface',
                    help=" Define qual interface de rede será usada. Padrão: wlp3s0")
parser.add_argument('--BTinterface',
                    help=" Define qual interface bluettoth será usada. Padrão: 0")
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
    WFaddr = 'B8:5A:73:A4:E8:9E' # Galaxy Duos
#    WFaddr = '84:C9:B2:69:97:B2' # Netgear
if not BTaddr:
#    BTaddr = '00:02:72:D5:6E:5D' # rc-control???B8:5A:73:A4:E8:9D
    BTaddr = 'B8:5A:73:A4:E8:9D'  # Galaxy Duos
#    BTaddr = 'f4:f5:d8:fc:57:a5'  # BLE vizinho
#    BTaddr = '68:C4:4D:81:6D:02'  # XT1650
if not BTstandard:
    BTstandard = "BLE"
if not output:
    output = "file"

# Verifica privilégios de ROOT para executar consultas BLE
if BTstandard == "BLE" and not os.geteuid() == 0:
    sys.exit("Esse script só pode ser executado com privilégios de root")

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
uavlocal = uavstate.uavsensors(veiculo, output)

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
    f.write("Distância WIFI do alvo é: {}cm\n".format(dist_wf_avg))
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
        f.write("Distância Bluetooth BLE do alvo é: {}cm\n".format(dist_bt_avg))
        f.close()
        print "Distância bluetooth do alvo é: {}cm".format(dist_bt_avg)

elif BTstandard == "BT":
    with open('btscan.dump', "a") as f:
        f.write("Posição: {}\n".format(veiculo.location.global_relative_frame))
        f.write("Coleta realizada no Tempo: {}\n".format(time.ctime()))
        f.close()
    full_bt_scan = BTscanpaired.scan_bluetooth(repeticao, BTaddr, output)
    print "Terminou de coletar dados Bluetooth. Agora, calculando a distância"
    dist_bt_avg = BTDist.bt_dist_paired(full_bt_scan)
    with open('btdist.dump', "a") as f:
        f.write("Posição: {}\n".format(veiculo.location.global_relative_frame))
        f.write("Coleta realizada no Tempo: {}\n".format(time.ctime()))
        f.write("Distância Bluetooth do alvo é: {}cm\n".format(dist_bt_avg))
        f.close()
    print "Distância bluetooth do alvo é: {}cm".format(dist_bt_avg)



# Amostras Estáticas previamente tiradas
# latlon = [(-22.86985120,-43.1051227),(-22.86983310,-43.1051285),(-22.86984080,-43.1051355),(-22.86983130,-43.1051311),(-22.86984440,-43.1051408),(-22.86987940,-43.1051325),(-22.86986800,-43.1051353),(-22.86986740,-43.1051099),(-22.86982530,-43.1051313),(-22.86986990,-43.1051268),(-22.86987800,-43.1051076),(-22.86984740,-43.1051061),(-22.86984480,-43.1051351),(-22.86984460,-43.1051185),(-22.86986010,-43.1051341),(-22.86987300,-43.1051315),(-22.86985720,-43.1051022),(-22.86986560,-43.1051251),(-22.86986950,-43.1051279),(-22.86987230,-43.1051344),(-22.86984940,-43.1051007),(-22.86984500,-43.1051201),(-22.86992110,-43.1050613),(-22.86984650,-43.1050980),(-22.86997450,-43.1050409),(-22.86984980,-43.1050972),(-22.86989680,-43.1050272),(-22.86984260,-43.1050673),(-22.86982940,-43.1050112),(-22.86996080,-43.1050254)]
# dist_wf = (0.000251189,0.000271227,0.000292864,0.000316228,0.000316228,0.000398107,0.000398107,0.000398107,0.000398107,0.000429866,0.000429866,0.000464159,0.000464159,0.000501187,0.000681292,0.000735642,0.000926119,0.001000000,0.001079775,0.001165914,0.001165914,0.001847850,0.001847850,0.002712273,0.002712273,0.002928645,0.002928645,0.003162278,0.003981072,0.005843414)

# # Voo de 17 de Nov de 2017
# latlon = [(-20.7463786,-41.2290764),(-20.7465702,-41.2290774),(-20.7465712,-41.2293447),(-20.7463795,-41.2293439)]
# dist_wf = (0.0130352714943,0.0163173436884,0.00627227441873,0.0041974967925)

#latlon = [(-20.7463768,-41.2290752),(-20.746569,-41.2290756),(-20.7465713,-41.2293429),(-20.7463788,-41.2293451)]
#dist_bt = (0.0162113117382,0.0369645139601,0.025944144831,0.0191378229595)

# Dispara método de multilateração final com todos os resultados finais e distâncias WIFI
#multilateration.multilateration(latlon, dist_bt)


# Fecha o objeto veiculo antes de terminar o script
print("Desconectando do Veículo")
veiculo.close()