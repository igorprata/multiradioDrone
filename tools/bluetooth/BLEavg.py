# -*- coding: utf-8 -*-
import math
import BLEScanLib
import sys
import bluetooth._bluetooth as bluez
import time
import os

from optparse import OptionParser, make_option


########################### Ferramenta standalone que verifica o RSSI e distância média de dispositivos Bluetooth BLE ###########################

# Responsável por disparar as coletas BLE:
def scan_ble(repeticao, bt_dev_id):
    try:
        sock = bluez.hci_open_dev(bt_dev_id)
        print "Thread de busca por dispositivos BLE iniciada"

    except:
        print "erro ao acessar dispositivo bluetooth..."
        sys.exit(1)

    BLEScanLib.hci_le_set_scan_parameters(sock)
    BLEScanLib.hci_enable_le_scan(sock)

    returnedList = BLEScanLib.parse_events(sock, repeticao)
    for beacon in returnedList:
        print "Amostra numero: {}, Timestamp: {}, Endereco: {}, RSSI: {}".format(repeticao,time.time(),beacon[0],beacon[3])
    BLEScanLib.hci_disable_le_scan(sock)
    sock.close()
    return returnedList

def ble_sinalmedio(BLEaddr, BTinterface):

    sum_rssi_ble = 0
    count = 0
    avg_rssi_ble = 0

    full_ble_scan = scan_ble(repeticao, BTinterface)

    for ble_ap in full_ble_scan:
        if ble_ap[0].lower() == BLEaddr.lower():
            rssi_ble = float(ble_ap[3])
            if (rssi_ble != 0):                    #reduces initial false values of RSSI using initial delay of 10sec
                count = count + 1
                sum_rssi_ble = sum_rssi_ble + rssi_ble
                avg_rssi_ble = sum_rssi_ble / count
    return avg_rssi_ble


def ble_distmedia(BLEaddr, BTinterface):

    n = 3  #Path loss exponent(n) = 1.5
    c = 10   #Environment constant(C) = 10
    A0 = float(-82)   #Average RSSI value at d0
    sum_error = 0
    count = 0
    avg_error = 0

    full_ble_scan = scan_ble(repeticao, BTinterface)

    for ble_ap in full_ble_scan:
        if ble_ap[0].lower() == BLEaddr.lower():
            rssi_ble = float(ble_ap[3])
            if (rssi_ble != 0):                    #reduces initial false values of RSSI using initial delay of 10sec
                count = count + 1
                x = float((rssi_ble-A0)/(-10*n))         #Log Normal Shadowing Model considering d0 =1m where
                distance = (math.pow(10,x) * 100) + c
                error = abs(actual_dist - distance)
                sum_error = sum_error + error
                avg_error = sum_error / count
                print "Average Error=  " + str(avg_error)
                print "Error=  " + str(error)
                print "Approximate Distance:" + str(distance)
                print "RSSI: " + str(rssi_ble)
                print "Count: " + str(count)
                print " "
    return avg_error

###########################

if __name__ == '__main__':

#Faz o parser a entrada de comando de terminal:
    option_list = [make_option("-i", "--interface", action="store", type="string", dest="BTinterface", help="Define a interface de rede utilizada. Default=0"),
                   make_option("-a", "--address", action="store", type="string", dest="BLEaddr", help="Define o endereço MAC a ser verificado. Default="),
                   make_option("-s", "--ssid", action="store", type="string", dest="SSID", help="Define o endereço o SSID da rede Wifi a ser verificada. Default="),
                   make_option("-l", "--loop", action="store", type="string", dest="repeticao", help="Define o número de interações. Default="),
                   make_option("-m", "--actual_dist", action="store", type="string", dest="actual_dist", help="Define a distância d0 a ser usada com o RSSI médio A0 na calibração (em cm). Default="),
                   make_option("-u", "--rssi_medio", action="store", type="string", dest="A0", help="Define o RSSI médio na distância d0. Default="),
                   make_option("-r", "--rssi", action="store_true", dest="avgrssi", help="Ativa a verificação do RSSI médio (PADRÃO)"),
                   make_option("-d", "--distance", action="store_true", dest="dist", help="Ativa a análise de distância por RSSI médio na distância A0"),
				    ]

    parser = OptionParser(option_list=option_list)
    (options, args) = parser.parse_args()

# Define valores padrão:
    if not options.BLEaddr:
        BLEaddr = "B8:5A:73:A4:E8:9D" #Samsung Galaxy Duos
    if not options.SSID:
        SSID = "IGORLANDIA"
    if not options.BTinterface:
        BTinterface = 1
    if not options.repeticao:
        repeticao = 60
    if not options.A0:
        A0 = float(2)  # Valor de RSSI médio na distância d0 =1m
    if not options.actual_dist:
        actual_dist = 100  # Distância estática entre transmissor e receptor em cm
    options.dist = True

# Checa permissões de Root:
    if not os.geteuid() == 0:
        sys.exit("Esse script só pode ser executado com privilégios de root")


# Define quais das duas operações serão feitas dependendo da entrada:
    if options.dist and not options.avgrssi:
        erro_medio = ble_distmedia(BLEaddr, BTinterface)
        print "o erro aproximado a {}cm de distância é de {}".format(actual_dist, erro_medio)
    else:
        resultado = ble_sinalmedio(BLEaddr, BTinterface)
        print "o resultado do RSSI médio é: %s dbm" % (resultado)
