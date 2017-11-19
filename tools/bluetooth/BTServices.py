# -*- coding: utf-8 -*-
# file: sdp-browse.py
# auth: Albert Huang <albert@csail.mit.edu>
# desc: displays services being advertised on a specified bluetooth device
# $Id: BTServices.py 393 2006-02-24 20:30:15Z albert $

import sys
import bluetooth


##################### Código para OBSERVAR todos os serviços Bluetooth visíveis de um MAC Address específico #############################


#Verifica os argumentos. Desabilite para um único alvo específico para fins de teste.
if len(sys.argv) < 2:
    print("utilizar: BTServices.py <addr>")
    print(" O parâmetro addr pode ser um endereço bluetooth específico, \"localhost\", ou \"all\"")
    sys.exit(2)
target = sys.argv[1]
if target == "all": target = None

# Definição de um alvo específico (para testes).
#target = "68:C4:4D:81:6D:02"

services = bluetooth.find_service(address=target)

if len(services) > 0:
    print("Encontrado(s) %d serviço(s) no alvo de endereço: %s" % (len(services), target))
    print("")
else:
    print("Nenhum serviço encontrado")

for svc in services:
    print("Nome do Serviço: %s"    % svc["name"])
    print("    Host:        %s" % svc["host"])
    print("    Descrição: %s" % svc["description"])
    print("    Provided By: %s" % svc["provider"])
    print("    Protocol:    %s" % svc["protocol"])
    print("    channel/PSM: %s" % svc["port"])
    print("    svc classes: %s "% svc["service-classes"])
    print("    profiles:    %s "% svc["profiles"])
    print("    service id:  %s "% svc["service-id"])
    print("")
