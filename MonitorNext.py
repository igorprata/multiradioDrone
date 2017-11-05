# -*- coding: utf-8 -*-
# Set up option parsing to get connection string
import argparse
import exceptions
import socket

from dronekit import connect

from tools.IEEE80211.IEEE80211scan import *

# String de conexao local com o veiculo
parser = argparse.ArgumentParser(description='Commands vehicle using vehicle.simple_goto.')
parser.add_argument('--connect',
                    help="Vehicle connection target string. If not specified, SITL automatically started and used.")
args = parser.parse_args()

connection_string = args.connect

# Conecta em localhost se nenhuma connection string for especificada
if not connection_string:
    connection_string = "127.0.0.1:14550"

print "Conectando no veiculo pelo canal: %s" % connection_string

# abrir conexao com o veiculo no dispositivo local
## vehicle = connect(connection_string, wait_ready=True)

vehicle = None

conn = False

while not conn:

    try:
        vehicle = connect(connection_string, wait_ready=True)

        print "Veiculo conectado!"
        conn = True

    # Bad TCP connection
    except socket.error:
        print 'O Servidor nao existe!'

    # Bad TTY connection
    except exceptions.OSError as e:
        print 'Nenhuma conexao serial!'

    # Other error
    except:
        print 'Um erro imprevisto aconteceu!'

    time.sleep(1)

# Listagem dos parametros de status do veiculo e modo de voo

semfio = IEEE80211()

while vehicle.commands.next<14:
    print " Estado do Sistema: %s" % vehicle.system_status.state
    print " Modo de voo: %s" % vehicle.mode.name
    print " Bateria: %s" % vehicle.battery
    print " GPS: %s" % vehicle.gps_0
    print " Global Location (relative altitude): %s" % vehicle.location.global_relative_frame
    semfio.scan_wifi()
    print '\033[1m' + " Ponto da missao: %s" % vehicle.commands.next
    print '\033[0m'

    time.sleep(20)

# Close vehicle object before exiting script
print("Desconectando do Veiculo")
vehicle.close()

# Desliga o Simulador se ligado.
#if sitl:
#    sitl.stop()
#    print("Simulador SITL desligado")


