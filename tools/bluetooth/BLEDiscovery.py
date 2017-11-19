# -*- coding: utf-8 -*-
import sys
import os
import struct
import errno

from ctypes import (CDLL, get_errno)
from ctypes.util import find_library
from socket import (
    socket,
    AF_BLUETOOTH,
    SOCK_RAW,
    BTPROTO_HCI,
    SOL_HCI,
    HCI_FILTER,
)


########################### Ferramenta standalone que verifica o MAC Address dos dispositivos Bluetooth BLE ao redor ###########################


if not os.geteuid() == 0:
    sys.exit("Esse script só pode ser executado com privilégios de root")

btlib = find_library("bluetooth")
if not btlib:
    raise Exception(
        "Não foram encontradas as bibliotecas bluetooth requeridas"
        " (necessário instalar o pacote bluez)"
    )
bluez = CDLL(btlib, use_errno=True)

dev_id = bluez.hci_get_route(None)

sock = socket(AF_BLUETOOTH, SOCK_RAW, BTPROTO_HCI)
sock.bind((dev_id,))

err = bluez.hci_le_set_scan_parameters(sock.fileno(), 0, 0x10, 0x10, 0, 0, 1000);
if err < 0:
    raise Exception("Falha ao configurar os parâmetros de scan")
    # occurs when scanning is still enabled from previous call

# allows LE advertising events
hci_filter = struct.pack(
    "<IQH",
    0x00000010,
    0x4000000000000000,
    0
)
sock.setsockopt(SOL_HCI, HCI_FILTER, hci_filter)

err = bluez.hci_le_set_scan_enable(
    sock.fileno(),
    1,  # 1 - turn on;  0 - turn off
    0, # 0-filtering disabled, 1-filter out duplicates
    1000  # timeout
)
if err < 0:
    errnum = get_errno()
    raise Exception("{} {}".format(
        errno.errorcode[errnum],
        os.strerror(errnum)
    ))

for i in range (3):
    data = sock.recv(1024)
    # print bluetooth address from LE Advert. packet
    print(':'.join("{0:02x}".format(ord(x)) for x in data[12:6:-1]))
