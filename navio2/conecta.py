# -*- coding: utf-8 -*-
import exceptions
import socket
import time

from dronekit import connect

def conexao (connection_string):
    # abrir conexao com o veiculo no dispositivoespecificado
    conn = False
    vehicle = None
    print "Conectando no veiculo pelo canal: %s" % connection_string
    while not conn:
        try:
            vehicle = connect(connection_string, wait_ready=True)
            print "Veiculo conectado!"
            conn = True

        # Falha na conexao TCP
        except socket.error:
            print 'O Servidor nao existe!'

        # Falha na conexao TTY
        except exceptions.OSError as e:
            print 'Nenhuma conexao serial!'

        # Outros erros
        except:
            print 'Um erro imprevisto aconteceu!'

        time.sleep(1)
    return vehicle

