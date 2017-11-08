# -*- coding: utf-8 -*-
import argparse
import time

from navegacao import simplegoto, takeoff
from navio2 import conecta, uavstate

##################### Codigo para Voo controlado #############################
parser = argparse.ArgumentParser(description='Comanda o drone em uma rota de voo estabelecida e executa o sensoriamento.')

parser.add_argument('--connect',
                    help=" Interface de conexão com o veículo. Se não for definida, a porta 1450 local será automaticamente usada. Padrão: 127.0.0.1:14550")
parser.add_argument('--loop',
                    help=" Define quantas vezes os dados dos sensores serão coletados em cada waypoint. Padrão: 3")
parser.add_argument('--WFinterface',
                    help=" Define qual interface de rede será usada. Padrão: wlp3s0")
parser.add_argument('--WFaddr',
                    help=" Define qual endereco WIFI será verificado. Padrão:")
parser.add_argument('--BTaddr',
                    help=" Define qual endereco Bluetooth será verificado. Padrão: 00:02:72:D5:6E:5D")
parser.add_argument('--output',
                    help=" Define qual o tipo de saída a ser usada (screen, file ou SQL). Padrão: screen")

args = parser.parse_args()

connection_string = args.connect
repeticao = args.loop
WFinterface = args.WFinterface
WFaddr = args.WFaddr
BTaddr = args.BTaddr
output = args.output

# Valores padroes se nao forem especificados
if not connection_string:
    connection_string = "127.0.0.1:14550"
if not repeticao:
    repeticao = 1
if not WFinterface:
    WFinterface = "wlp3s0"
if not WFaddr:
    WFaddr = 'C0:3F:0E:D0:D8:15' # igorlandia
if not BTaddr:
#    BTaddr = '00:02:72:D5:6E:5D' # rc-control???B8:5A:73:A4:E8:9D
    BTaddr = 'B8:5A:73:A4:E8:9D'  # Galaxy Duos
if not output:
    output = "file"


# Executa a conexao an aeronave e recebe a classe vehicle devolta
veiculo = conecta.conexao(connection_string)

# Listagem dos parametros de status do veiculo e modo de voo
uavstate.uavversion(veiculo)

# Dispara a Funcao de Decolagem
takeoff.armandtakeoff(8, veiculo)

# espera alguns segundos para verificar a estabilidade
time.sleep(10)

# Dispara a Funcao de navegacao ponto a ponto e recebe array de distancias
results = simplegoto.pontoaponto(veiculo, repeticao, WFinterface, WFaddr, BTaddr, output)

print results

# Fecha o objeto veiculo antes de termianr o script
print("Desconectando do Veículo")
veiculo.close()