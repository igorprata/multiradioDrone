# -*- coding: utf-8 -*-
import argparse
import time

from navegacao import simplegoto, takeoff
from navio2 import conecta, uavstate
from tools.Multilateration import multilateration


##################### Código para realizar um Voo controlado #############################


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
    # WFaddr = 'C0:3F:0E:D0:D8:15' # igorlandia
    WFaddr = 'B8:5A:73:A4:E8:9E' # Galaxy Duos
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

# Dispara a Funcao de navegacao ponto a ponto e recebe um array de distancias (WF e BT) e lat, lon, alt para cada ponto de coleta:
results = simplegoto.pontoaponto(veiculo, repeticao, WFinterface, WFaddr, BTaddr, output)

# Faz o parse dos resultados em variáveis especificas por atributo em cada ponto
dist_wf = results[0]
dist_bt = results[1]
latlon = []
alt = []

for x in results[2]:
    latlon.append(x[0])
    alt.append(x[1])

# Amostras do Fabio Costa
#latlon = [(-22.86985120,-43.1051227),(-22.86983310,-43.1051285),(-22.86984080,-43.1051355),(-22.86983130,-43.1051311),(-22.86984440,-43.1051408),(-22.86987940,-43.1051325),(-22.86986800,-43.1051353),(-22.86986740,-43.1051099),(-22.86982530,-43.1051313),(-22.86986990,-43.1051268),(-22.86987800,-43.1051076),(-22.86984740,-43.1051061),(-22.86984480,-43.1051351),(-22.86984460,-43.1051185),(-22.86986010,-43.1051341),(-22.86987300,-43.1051315),(-22.86985720,-43.1051022),(-22.86986560,-43.1051251),(-22.86986950,-43.1051279),(-22.86987230,-43.1051344),(-22.86984940,-43.1051007),(-22.86984500,-43.1051201),(-22.86992110,-43.1050613),(-22.86984650,-43.1050980),(-22.86997450,-43.1050409),(-22.86984980,-43.1050972),(-22.86989680,-43.1050272),(-22.86984260,-43.1050673),(-22.86982940,-43.1050112),(-22.86996080,-43.1050254)]
#dist_wf = (0.000251189,0.000271227,0.000292864,0.000316228,0.000316228,0.000398107,0.000398107,0.000398107,0.000398107,0.000429866,0.000429866,0.000464159,0.000464159,0.000501187,0.000681292,0.000735642,0.000926119,0.001000000,0.001079775,0.001165914,0.001165914,0.001847850,0.001847850,0.002712273,0.002712273,0.002928645,0.002928645,0.003162278,0.003981072,0.005843414)

# Dispara método de multilateração final com todos os resultados finais e distâncias WIFI
multilateration.multilateration(latlon, dist_wf)


# Fecha o objeto veiculo antes de termianr o script
print("Desconectando do Veículo")
veiculo.close()