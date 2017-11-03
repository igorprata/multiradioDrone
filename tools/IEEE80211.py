import time
from wifi import Cell, Scheme

def scan_wifi(repeticao, interface, output):
    if not repeticao:
        repeticao = 1
    if not interface:
        interface = "wlp3s0"
    if not output:
        output = "screen"

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
                    f.write("Amostra numero: {}, ".format(n+1))
                    f.write("Timestamp: {}, MAC: {}, Frequencia: {}, Sinal {}, Canal: {}, Nome {}, Qualidade{}\n".format(
                        timestamp, cell.address, cell.frequency, cell.signal, cell.channel, cell.ssid, cell.quality))
            f.close()
        f.closed
