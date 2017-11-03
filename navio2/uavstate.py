
def uavstatus (vehicle):
    print " Estado do Sistema: %s" % vehicle.system_status.state
    print " Modo de voo: %s" % vehicle.mode.name
    print " Bateria: %s" % vehicle.battery


def uavsensors (vehicle):
    print " GPS: %s" % vehicle.gps_0
    print " Localizacao Global (altitude relativa): %s" % vehicle.location.global_relative_frame