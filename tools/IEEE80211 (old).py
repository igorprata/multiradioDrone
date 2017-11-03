#!/usr/bin/env python

# import os
# import sys
import time
from wifi import Cell, Scheme

# orig_stdout = sys.stdout
# f = open('wifilog.dump', 'w')
# sys.stdout = f

#    def check_root():
#        if not os.geteuid() == 0:
#            print __file__ + " requires root permissions."
#            exit(1)
def scan_wifi(repeticao, interface):
    output = None
    if not repeticao:
        repeticao = 1
    if not interface:
        interface = "wlp3s0"
    if not output:
        output = "file"

    if output == "screen":
        print "Exibicao dos resultados somente em tela"
        for n in range(repeticao):
            for cell in Cell.all(interface):
                timestamp = int(time.time())
                print "Amostra numero: {}".format(n+1)
                print("Timestamp: {}, MAC: {}, Frequencia: {}, Sinal {}, Canal: {}, Nome {}, Qualidade{}".format(timestamp, cell.address, cell.frequency, cell.signal, cell.channel, cell.ssid, cell.quality))

    if output == "file":
        with open('wifiscan.dump', "a") as f:
            print "Exibicao dos resultados somente em arquivo: {}".format(f.name)
            for n in range(repeticao):
                for cell in Cell.all(interface):
                    timestamp = int(time.time())
                    f.write("Amostra numero: {}".format(n+1))
                    f.write("Timestamp: {}, MAC: {}, Frequencia: {}, Sinal {}, Canal: {}, Nome {}, Qualidade{}\n".format(
                        timestamp, cell.address, cell.frequency, cell.signal, cell.channel, cell.ssid, cell.quality))
            f.close()
        f.closed
#    sys.stdout = orig_stdout
#    f.close()
