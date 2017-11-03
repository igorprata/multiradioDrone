import time

from dronekit import VehicleMode


def armandtakeoff(aTargetAltitude,veiculo):

    #Arma o veiculo e voa ate uma altitude definida.
    print "Basic pre-arm checks"
    # Nao arma o veiculo enquanto o piloto automatico nao estiver pronto
    while not veiculo.is_armable:
        print "Aguardando o veiculo inicializar..."
        if v.mode.name == "INITIALISING":
            print "Aguardando o veiculo iniciar"
            time.sleep(1)
        if veiculo.gps_0.fix_type < 2:
            print "aguardando estabilidade de conexao com o GPS...:", veiculo.gps_0.fix_type
            time.sleep(1)
        time.sleep(1)
    print "Armando os motores"
    # ArduCopter deve ficar no modo GUIDED
    veiculo.mode    = VehicleMode("GUIDED")
    veiculo.armed   = True
    # Confirma se o veiculo esta armado antes de tentar Decolar: EKF ready, and the vehicle has GPS lock
    while not veiculo.armed:
        print "Aguardando o acionamento dos motores..."
        time.sleep(3)
    print "DECOLANDO!"
    veiculo.simple_takeoff(aTargetAltitude) # DECOLA ate a altitude desejada
    # Wait until the vehicle reaches a safe height before processing the goto (otherwise the command
    #  after Vehicle.simple_takeoff will execute immediately).
    while True:
        print " Altitude: ", veiculo.location.global_relative_frame.alt
        #Break and return from function just below target altitude.
        if veiculo.location.global_relative_frame.alt>=aTargetAltitude*0.95:
            print "Alcancou a altitude desejada"
            break
        time.sleep(1)
