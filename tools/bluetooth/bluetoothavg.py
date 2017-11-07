# -*- coding: utf-8 -*-
import time
import math

from optparse import OptionParser, make_option
#from BTscan import unique_bt_scan
from bt_proximity import BluetoothRSSI


########################### Ferramenta standalone que verifica o RSSI e distância média de dispositivos Bluetooth pareados ou não ###########################


# Valores iniciais. Pode-se pensar em descartar para reduzir linhas de código.
BTaddr = "B8:5A:73:A4:E8:9D" #Samsung Galaxy Duos
SSID = "IGORLANDIA"
BTinterface = "hci1"
repeticao = 30
A0 = float(2)  # Valor de RSSI médio na distância d0 =1m
actual_dist = 100  # Distância estática entre transmissor e receptor em cm

# Mede o RSSI Médio a um metro de distância de um alvo
def bt_sinalmedio_paired(BTaddr, repeticao):
    count = 0
    sum_rssi_bt = 0
    avg_rssi_bt = 0
    btrssi = BluetoothRSSI(addr=BTaddr)

    for i in range(repeticao):
        rssi_bt = float(btrssi.get_rssi())
        if (rssi_bt != 0 and i > 10):  # reduz a possibilidade de valores iniciais falsos de RSSI esperando por x seg e elimina valores 0
            count = count + 1
            sum_rssi_bt = sum_rssi_bt + rssi_bt
            avg_rssi_bt = sum_rssi_bt / count
            print "Sinal médio:  " + str(avg_rssi_bt)
            print "RSSI: " + str(rssi_bt)
            print "Amostra número: " + str(count)
            print " "
        time.sleep(1) # para aguardar por uma variação maior por parte do IWLIST
    return avg_rssi_bt

# Mede o flutuações na distância a partir do RSSI Médio e compara o erro proporcional a uma distância fixa
def bt_distmedia_paired(BTaddr, repeticao, A0, actual_dist):
    n = 1.5  # Path loss exponent(n) = 1.5
    c = 10  # Constante ambiental(C) = 10
    sum_error = 0
    count = 0
    avg_error = 0
    btrssi = BluetoothRSSI(addr=BTaddr)

    for i in range(repeticao):
        rssi_bt = float(btrssi.get_rssi())
        if (rssi_bt != 0 and i > 10):  # reduces initial false values of RSSI using initial delay of 10sec
            count = count + 1
            x = float((rssi_bt - A0) / (-10 * n))  # Log Normal Shadowing Model considering d0 =1m where
            distance = (math.pow(10, x) * 100) + c
            error = abs(actual_dist - distance)
            sum_error = sum_error + error
            avg_error = sum_error / count
            print "Average Error=  " + str(avg_error)
            print "Error=  " + str(error)
            print "Approximate Distance:" + str(distance)
            print "RSSI: " + str(rssi_bt)
            print "Count: " + str(count)
            print " "
        time.sleep(1)
    return avg_error


###########################

if __name__ == '__main__':

#Faz o parser a entrada de comando de terminal:
    option_list = [make_option("-i", "--interface", action="store", type="string", dest="BTinterface", help="Define a interface de rede utilizada. Default= %s" % (BTinterface)),
                   make_option("-a", "--address", action="store", type="string", dest="BTaddr", help="Define o endereço MAC a ser verificado. Default="),
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
    if not options.BTaddr:
        BTaddr = "B8:5A:73:A4:E8:9D" #Samsung Galaxy Duos
    if not options.SSID:
        SSID = "IGORLANDIA"
    if not options.BTinterface:
        BTinterface = "hci1"
    if not options.repeticao:
        repeticao = 30
    if not options.A0:
        A0 = float(2)  # Valor de RSSI médio na distância d0 =1m
    if not options.actual_dist:
        actual_dist = 100  # Distância estática entre transmissor e receptor em cm
    options.dist = True

# Define quais das duas operações serão feitas dependendo da entrada:
    if options.dist and not options.avgrssi:
        erro_medio = bt_distmedia_paired(BTaddr, repeticao, A0, actual_dist)
        print "o erro aproximado a {}cm de distância é de {}".format(actual_dist, erro_medio)
    else:
        resultado = bt_sinalmedio_paired(BTaddr, repeticao)
        print "o resultado do RSSI médio é: %s dbm" % (resultado)
