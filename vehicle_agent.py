# -*- coding: utf-8 -*-
from dronekit import connect

import time
import socket
import exceptions

##################### Código Base do Luis e Fábio #############################

# String de conexao local com o veiculo
connection_string = "127.0.0.1:14550"

print "Conectando no veiculo pelo canal: %s" % connection_string

# abrir conexao com o veiculo no dispositivo local

##vehicle = connect(connection_string, wait_ready=True)

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
        print 'Algum erro imprevisto aconteceu!'

    time.sleep(1)
    
# listagem dos parametros de status do veiculo e modo de voo

while True:

    print " System status: %s" % vehicle.system_status.state
    print " Mode: %s" % vehicle.mode.name
    print " Battery: %s" % vehicle.battery
    print " GPS: %s" % vehicle.gps_0
    print " Global Location (relative altitude): %s" % vehicle.location.global_relative_frame

    time.sleep(1)
    
# finalizar a conexao com o veiculo
vehicle.close()

print "Conexao Fechada"
