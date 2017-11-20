# -*- coding: utf-8 -*-
import fcntl
import struct
import array
import bluetooth
import bluetooth._bluetooth as bt
import time

from bt_proximity import BluetoothRSSI


##################### Código para OBSERVAR dispositovps bluetooth pareados #############################


def bluetooth_rssi(addr):
    # Open hci socket
    hci_sock = bt.hci_open_dev()
    hci_fd = hci_sock.fileno()

    # Connect to device (to whatever you like)
    bt_sock = bluetooth.BluetoothSocket(bluetooth.L2CAP)
    bt_sock.settimeout(10)
    result = bt_sock.connect((addr, 1))	# PSM 1 - Service Discovery

    try:
        # Get ConnInfo
        reqstr = struct.pack("6sB17s", bt.str2ba(addr), bt.ACL_LINK, "\0" * 17)
        request = array.array("c", reqstr )
        handle = fcntl.ioctl(hci_fd, bt.HCIGETCONNINFO, request, 1)
        handle = struct.unpack("8xH14x", request.tostring())[0]
        # Get RSSI
        cmd_pkt=struct.pack('H', handle)
        rssi = bt.hci_send_req(hci_sock, bt.OGF_STATUS_PARAM, bt.OCF_READ_RSSI, bt.EVT_CMD_COMPLETE, 4, cmd_pkt)
        rssi = struct.unpack('b', rssi[3])[0]
        # Close sockets
        bt_sock.close()
        hci_sock.close()
        return rssi
    except:
        return None

def unique_bt_scan(BTaddr):
    b = BluetoothRSSI(BTaddr)
    bt_rssi = b.get_rssi()
    print "addr: {}, rssi: {}".format(BTaddr, bt_rssi)
    if bt_rssi is None:
        time.sleep(1)
        print "Falha na coleta"
    return bt_rssi

def scan_bluetooth(repeticao, BTaddr, output):
    bt_rssi = []
    if output == "screen":
        print "Exibicao dos resultados Bluetooth para o endereco {} em tela:".format(BTaddr)
        for n in range(repeticao):
            # get rssi reading for address
            rssi = bluetooth_rssi(BTaddr)
            print "Amostra numero: {}, Timestamp: {}, Endereco: {}, RSSI: {}".format(n + 1, time.time(), BTaddr, rssi)
            time.sleep(1)
            bt_rssi.append(rssi)
        return bt_rssi

    if output == "file":
        with open('btscan.dump', "a") as f:
            print "Exibicao dos resultados Bluetooth para o endereco {} somente no arquivo: {}".format(BTaddr, f.name)
            for n in range(repeticao):
                rssi = bluetooth_rssi(BTaddr)
                f.write("Amostra numero: {}, Timestamp: {}, Endereco: {}, RSSI: {}\n".format(n + 1, time.time(), BTaddr, rssi))
                time.sleep(1)
                bt_rssi.append(rssi)
            f.close()
            return bt_rssi
        f.closed
