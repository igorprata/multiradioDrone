#!/usr/bin/python
# -*- coding: utf-8 -*-
from bt_proximity import BluetoothRSSI
import time
import sys


########################### Verifica o RSSI de dispositivos Bluetooth pareados ###########################


# crie uma lista separada por vírgulas dos endereços MAC dos dispositivos Bluetooth que deseja verificar
BTaddr = 'B8:5A:73:A4:E8:9D'
repeticao = 10


def unique_bt_scan(BTaddr):
    b = BluetoothRSSI(BTaddr)
    bt_rssi = b.get_rssi()
    print "addr: {}, rssi: {}".format(BTaddr, bt_rssi)
    if bt_rssi is None:
        time.sleep(1)
        print "Falha na coleta"
    return bt_rssi

def main():
    if not BTaddr:
        print "Por favor, adicione um endereço na variável BTaddr"
        sys.exit(1)
    target = unique_bt_scan(BTaddr)
    print target


if __name__ == '__main__':
    main()
