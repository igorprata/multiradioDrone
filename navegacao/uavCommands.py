# -*- coding: utf-8 -*-
import time

from dronekit import VehicleMode


####################### Reúne os métodos mais básicos para operação do veículo ###########################

### Coloca o veículo em modo GUIDED para operação controlada
def mode_guided(vehicle):

    vehicle.mode = VehicleMode("GUIDED")

    while not vehicle.mode.name == 'GUIDED':
        print " Aguardando o modo GUIDED"
        time.sleep(1)

    print " Modo de voo: %s" % vehicle.mode.name


### Arma os rotores do veículo
def arm_vehicle(vehicle):

    # Copter should arm in GUIDED mode
    mode_guided(vehicle)

    print "Basic pre-arm checks"

    # Evitar armar o veículo antes da checagem do autopilot
    while not vehicle.is_armable:
        print "Aguardando o veículo iniciar..."
        time.sleep(1)

    print "Armando motores"

    vehicle.armed = True

    # Confirma se o veículo está armado antes de tentar decolar
    while not vehicle.armed:
        print " Aguardando os rotores armarem..."
        time.sleep(1)

    print "Motores armados"


### Decola para uma altitude predeterminada
def takeoff_vehicle(altitude, vehicle):

    if not vehicle.armed:
        print " Os rotores não estão armados!"
        time.sleep(1)
        arm_vehicle(vehicle)

    # Decola até uma altitude desejada
    vehicle.simple_takeoff(altitude)
    print "DECOLANDO..."

    # Aguarda alcançar a altitude desejada:
    print " Altitude: ",
    while True:
        print " %s" % vehicle.location.global_relative_frame.alt,
        #Criterio de aceitação para a altitude desejada.
        if vehicle.location.global_relative_frame.alt >= altitude * 0.95:
            print "\nAlcançou a altitude desejada"
            break
        time.sleep(1)


### Pousa o veículo na posição atual
def land_vehicle(vehicle):

    print "Pousando o veículo..."

    vehicle.mode = VehicleMode("LAND")

    print " Altitude: ",
    while True:
        print " %s" % vehicle.location.global_relative_frame.alt,
        if vehicle.location.global_relative_frame.alt <=  0.20:
            print "\nVeículo no solo"
            break
        time.sleep(1)

    time.sleep(2)
    vehicle.armed = False

    while vehicle.armed:
        print " Aguardando o veículo desarmar..."
        time.sleep(1)

    print "Motores desarmados"

    vehicle.mode = VehicleMode("STABILIZE")
    print " Modo de voo: %s" % vehicle.mode.name

# mantem a busca por uma posição home:
def check_for_home(vehicle):
    while not vehicle.home_location:
        cmds1 = vehicle.commands
        cmds1.download()
        cmds1.wait_ready()
        if not vehicle.home_location:
            print " Aguardando por um home location ..."

    # Se tivermos uma posição HOME:
    print "\n Home location: %s \n" % vehicle.home_location