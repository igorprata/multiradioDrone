# -*- coding: utf-8 -*-
import fcntl
import struct
import array
import tools.bluetooth
import tools.bluetooth._bluetooth as bt
import time

if not os.geteuid() == 0:
    sys.exit("Execute como root")

btlib = find_library("bluetooth")
if not btlib:
    raise Exception(
        "Can't find required bluetooth libraries"
        " (need to install bluez)"
    )

def bluetooth_rssi(addr):
    # Open hci socket
    hci_sock = bt.hci_open_dev()
    hci_fd = hci_sock.fileno()

    # Connect to device (to whatever you like)
    bt_sock = tools.bluetooth.BluetoothSocket(tools.bluetooth.L2CAP)
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

# addr = '00:02:72:D5:6E:5D'
# RC_Control = '00:02:72:D5:6E:5D'
# XT1650_addr = '68:C4:4D:81:6D:02'
# HP1_addr = '00:24:7E:50:33:A2'
# repeticao = 1
# output = "screen"

def scan_bluetooth(repeticao, BTaddr, output):
    output = "screen"
    if output == "screen":
        print "Exibicao dos resultados Bluetooth para o endereco {} em tela:".format(BTaddr)
        for n in range(repeticao):
            # get rssi reading for address
            rssi = bluetooth_rssi(BTaddr)
            print "Amostra numero: {}, Timestamp: {}, Endereco: {}, RSSI: {}".format(n + 1, int(time.time()), BTaddr, rssi)

    if output == "file":
        with open('btscan.dump', "a") as f:
            print "Exibicao dos resultados Bluetooth para o endereco {} somente no arquivo: {}".format(BTaddr, f.name)
            for n in range(repeticao):
                rssi = bluetooth_rssi(BTaddr)
                f.write("Amostra numero: {}, Timestamp: {}, Endereco: {}, RSSI: {}\n".format(n + 1, int(time.time()), BTaddr, rssi))
            f.close()
        f.closed