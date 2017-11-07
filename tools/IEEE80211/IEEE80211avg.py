# -*- coding: utf-8 -*-
import time
import math

from optparse import OptionParser, make_option
from IEEE80211scan import unique_wifi_scan

# Valores iniciais. Pode pensar em descartar para reduzir linhas de código.
WFaddr = "C0:3F:0E:D0:D8:15"
SSID = "IGORLANDIA"
WFinterface = "wlp3s0"
repeticao = 10
A0 = float(-26)  # Valor de RSSI médio na distância d0 =1m
actual_dist = 100  # Distância estática entre transmissor e receptor em cm

# Mede o RSSI Médio a um metro de distância de um alvo
def wifi_sinalmedio(WFinterface, WFaddr, repeticao, SSID):
    count = 0
    sum_rssi_wf = 0
    avg_rssi_wf = 0

    for i in range(repeticao):
        rssi_wf = float(unique_wifi_scan(WFinterface, WFaddr))
        if (rssi_wf != 0 and i > 3):  # reduz a possibilidade de valores iniciais falsos de RSSI esperando por x seg e elimina valores 0
            count = count + 1
            sum_rssi_wf = sum_rssi_wf + rssi_wf
            avg_rssi_wf = sum_rssi_wf / count
            print "Sinal médio:  " + str(avg_rssi_wf)
            print "RSSI: " + str(rssi_wf)
            print "Amostra número: " + str(count)
            print " "
        time.sleep(2) # para aguardar por uma variação maior por parte do IWLIST
    return avg_rssi_wf

# Mede o flutuações na distância a partir do RSSI Médio e compara o erro proporcional a uma distância fixa
def wifi_distmedia(WFinterface, WFaddr, repeticao, A0, actual_dist):
    n = 3  # Path loss exponent(n) = 1.5
    c = 10  # Constante ambiental(C) = 10
    sum_error = 0
    count = 0

    for i in range(repeticao):
        rssi_wf = float(unique_wifi_scan(WFinterface, WFaddr))
        if (rssi_wf != 0 and i > 5):  # reduz a possibilidade de valores iniciais falsos de RSSI esperando por x seg e elimina valores 0
            count = count + 1
            x = float((rssi_wf - A0) / (-10 * n))  # Log Normal Shadowing Model considering d0 =1m where
            distance = (math.pow(10, x) * 100) + c
            error = abs(actual_dist - distance)
            sum_error = sum_error + error
            avg_error = sum_error / count
            print "Erro médio =  " + str(avg_error)
            print "Erro =  " + str(error)
            print "Distância aproximada:" + str(distance)
            print "RSSI: " + str(rssi_wf)
            print "Contador: " + str(count)
            print " "
        time.sleep(1)
    return avg_error


###########################

if __name__ == '__main__':

#Faz o parser a entrada de comando de terminal:
    option_list = [make_option("-i", "--interface", action="store", type="string", dest="WFinterface", help="Define a interface de rede utilizada. Default= %s" % (WFinterface)),
                   make_option("-a", "--address", action="store", type="string", dest="WFaddr", help="Define o endereço MAC a ser verificado. Default=C0:3F:0E:D0:D8:15"),
                   make_option("-s", "--ssid", action="store", type="string", dest="SSID", help="Define o endereço o SSID da rede Wifi a ser verificada. Default="),
                   make_option("-l", "--loop", action="store", type="string", dest="repeticao", help="Define o número de interações. Default="),
                   make_option("-m", "--actual_dist", action="store", type="string", dest="actual_dist", help="Define a distância d0 a ser usada com o RSSI médio A0 na calibração (em cm). Default="),
                   make_option("-u", "--rssi_medio", action="store", type="string", dest="A0", help="Define o RSSI médio na distância d0. Default="),
                   make_option("-r", "--rssi", action="store_true", dest="avgrssi", help="Ativa a verificação do RSSI médio (PADRÃO)"),
                   make_option("-d", "--distance", action="store_true", dest="dist", help="Ativa a análise de distância por RSSI médio na distância A0"),
				    ]

    parser = OptionParser(option_list=option_list)
    (options, args) = parser.parse_args()
    repeticao = options.repeticao
    SSID = options.SSID
    WFaddr = options.WFaddr
    WFinterface = options.WFinterface
    A0 = options.A0
    actual_dist = options.actual_dist

# Define valores padrão:
    if not WFaddr:
        WFaddr = "C0:3F:0E:D0:D8:15"
    if not SSID:
        SSID = "IGORLANDIA"
    if not WFinterface:
        WFinterface = "wlp3s0"
    if not repeticao:
        repeticao = 10
    if not A0:
        A0 = float(-26)  # Valor de RSSI médio na distância d0 =1m
    if not actual_dist:
        actual_dist = 100  # Distância estática entre transmissor e receptor em cm

# Define quais das duas operações serão feitas dependendo da entrada:
    if options.dist and not options.avgrssi:
        erro_medio = wifi_distmedia(WFinterface, WFaddr, repeticao, A0, actual_dist)
        print "o erro aproximado a {}cm de distância é de {}".format(actual_dist, erro_medio)
    else:
        resultado = wifi_sinalmedio(WFinterface, WFaddr, repeticao, SSID)
        print "o resultado do RSSI médio é: %s dbm" % (resultado)
