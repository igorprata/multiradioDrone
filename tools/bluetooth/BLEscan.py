# -*- coding: utf-8 -*-

# test BLE Scanning software
# jcs 6/8/2014

import BLEScanLib
import sys
import bluetooth._bluetooth as bluez
import time


##################### Código para OBSERVAR RSSI de dispositivos bluetooth BLE #############################


def scan_ble(repeticao, output, bt_dev_id):
    if output == "screen":
        print "Exibição dos resultados Bluetooth BLE somente em tela"
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

    if output == "file":
        with open('blescan.dump', "a") as f:
            print "Exibicao dos resultados Bluetooth BLE somente no arquivo: {}".format(f.name)
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
                f.write ("n. de repetições: {}, Timestamp: {}, Endereço: {}, RSSI: {}\n".format(repeticao,time.time(),beacon[0],beacon[3]))
            BLEScanLib.hci_disable_le_scan(sock)
            sock.close()
            f.close()

    return returnedList

def unique_ble_scan(BTaddr, bt_dev_id, repeticao):
    try:
        sock = bluez.hci_open_dev(bt_dev_id)
        print "Thread de busca por dispositivos BLE iniciada"

    except:
        print "erro ao acessar dispositivo bluetooth..."
        sys.exit(1)

    BLEScanLib.hci_le_set_scan_parameters(sock)
    BLEScanLib.hci_enable_le_scan(sock)

    ble_rssi = 0
    returnedList = BLEScanLib.parse_events(sock, repeticao)

    for beacon in returnedList:
        if beacon[0].lower() == BTaddr.lower():
            ble_rssi = beacon[3]
            print "Timestamp: {}, Endereco: {}, RSSI: {}".format(time.time(), beacon[0], ble_rssi)
    BLEScanLib.hci_disable_le_scan(sock)
    sock.close()
    return ble_rssi
#
# def main():
#      bt_dev_id = 0
#      BTaddr = "f4:f5:d8:fc:57:a5"
#      output = "screen"
#      repeticao = 20
#      target = scan_ble(repeticao, output, bt_dev_id)
#      print target
#
# if __name__ == '__main__':
#      main()
