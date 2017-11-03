import argparse
import time

from navegacao import simplegoto, takeoff
from navio2 import conecta
from tools import sensores

##################### Codigo para Voo controlado #############################
# String de conexao com o veiculo
parser = argparse.ArgumentParser(description='Commanda o drone em uma rota de voo estabelecida e executa o sensoriamento.')

parser.add_argument('--connect',
                    help=" Interface de conexao com o veiculo. Se nao for definida, a porta 1450 local sera automaticamente usada.")
parser.add_argument('--loop',
                    help=" Define quantas vezes os dados dos sensores serao coletados em cada waypoint.")
parser.add_argument('--interface',
                    help=" Define qual interface de rede sera usada.")
parser.add_argument('--output',
                    help=" Define qual o tipo de saida a ser usada (tela, arquivo ou SQL).")

args = parser.parse_args()

connection_string = args.connect
repeticao = args.loop
interface = args.interface
output = args.output

# Conecta em localhost se nenhuma connection string for especificada
if not connection_string:
    connection_string = "127.0.0.1:14550"
print "Conectando no veiculo pelo canal: %s" % connection_string
# Executa a conexao an aeronave e recebe a classe vehicle devolta
veiculo = conecta.conexao(connection_string)

# Listagem dos parametros de status do veiculo e modo de voo
sensores.sensors(veiculo, repeticao, interface, output)

# Dispara a Funcao de Decolagem
takeoff.armandtakeoff(10, veiculo)

# espera alguns segundos para verificar a estabilidade
time.sleep(10)

# Dispara a Funcao de navegacao ponto a ponto
simplegoto.pontoaponto(veiculo, repeticao, interface, output)

# Fecha o objeto veiculo antes de termianr o script
print("Desconectando do Veiculo")
veiculo.close()