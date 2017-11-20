# -*- coding: utf-8 -*-
import time
from wifi import Cell

def scan_wifi(repeticao, WFinterface, output):
    full_wifi_scan = []
    if output == "screen":
        print "Exibicao dos resultados WIFI da interface {} somente em tela".format(WFinterface)
        for n in range(repeticao):
            wifi_scan = []
            for cell in Cell.all(WFinterface):
                cell_scan = []
                timestamp = time.time()
                print "Amostra numero: {}".format(n+1)
                print("Timestamp: {}, MAC: {}, Frequencia: {}, Sinal {}, Canal: {}, Nome: {}, Qualidade: {}".format(timestamp, cell.address, cell.frequency, cell.signal, cell.channel, cell.ssid, cell.quality))
                cell_scan.append(cell.address)
                cell_scan.append(cell.signal)
                wifi_scan.append(cell_scan)
            time.sleep(1)
            full_wifi_scan.append(wifi_scan)

    if output == "file":
        with open('wifiscan.dump', "a") as f:
            print "Exibicao dos resultados WIFI de interface {} somente no arquivo: {}".format(WFinterface,f.name)
            for n in range(repeticao):
                wifi_scan = []
                for cell in Cell.all(WFinterface):
                    cell_scan = []
                    timestamp = time.time()
                    f.write("Amostra numero: {}, ".format(n+1))
                    f.write("Timestamp: {}, MAC: {}, Frequencia: {}, Sinal {}, Canal: {}, Nome: {}, Qualidade: {}\n".format(
                        timestamp, cell.address, cell.frequency, cell.signal, cell.channel, cell.ssid, cell.quality))
                    cell_scan.append(cell.address)
                    cell_scan.append(cell.signal)
                    wifi_scan.append(cell_scan)
                time.sleep(1)
                full_wifi_scan.append(wifi_scan)
            f.close()
    return full_wifi_scan

def unique_wifi_scan (WFinterface, WFaddr):
#    for cell in Cell.all(WFinterface):
#        if cell.address == WFaddr:
#             return cell.ssid
#    return False
    cell = Cell.where(WFinterface, lambda cell: cell.address.lower() == WFaddr.lower())
    for c in cell:
        return c.signal
    return False