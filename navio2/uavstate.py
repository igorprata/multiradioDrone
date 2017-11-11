# -*- coding: utf-8 -*-
import time

def uavversion (vehicle):
    print " Autopilot Firmware version: %s" % vehicle.version
    print " Estado do Sistema: %s" % vehicle.system_status.state
    print " EKF OK?: %s" % vehicle.ekf_ok
    print " Modo de voo: %s" % vehicle.mode.name
    print " Is Armable?: %s" % vehicle.is_armable
    print " Armed: %s" % vehicle.armed

def uavstatus (vehicle, output):
    if output == "screen":
        print " Estado do Sistema: %s" % vehicle.system_status.state
        print " Modo de voo: %s" % vehicle.mode.name
        print " Bateria: %s" % vehicle.battery
        print " Last Heartbeat: %s" % vehicle.last_heartbeat
        print " Airspeed: %s" % vehicle.airspeed
        print " Velocity: %s" % vehicle.velocity
        print " Groundspeed: %s" % vehicle.groundspeed
        print " Heading: %s" % vehicle.heading
        print " Orientacao: %s" % vehicle.attitude
        print " Satelites: %s" % vehicle.gps_0

    if output == "file":
        with open('uavstatus.dump', "a") as f:
            print "Exibicao das informacoes do VANT somente em arquivo: {}".format(f.name)
            timestamp = int(time.time())
            f.write("Timestamp: {}, ".format(timestamp))
            f.write("Estado do Sistema: %s, " % vehicle.system_status.state)
            f.write("Modo de voo: %s, " % vehicle.mode.name)
            f.write("Bateria: %s, " % vehicle.battery)
            f.write("Last Heartbeat: %s, " % vehicle.last_heartbeat)
            f.write("Airspeed: %s, " % vehicle.airspeed)
            f.write("Velocity: %s, " % vehicle.velocity)
            f.write("Groundspeed: %s, " % vehicle.groundspeed)
            f.write("Heading: %s, " % vehicle.heading)
            f.write("Orientacao: %s, " % vehicle.attitude)
            f.write("Satelites: %s\n" % vehicle.gps_0)
        f.close()

def uavsensors (vehicle, repeticao, output):

    latlon = []
    alt = []

    if output == "screen":
        print " Localizacao Global: %s" % vehicle.location.global_frame
        print " Rangefinder distance: %s" % vehicle.rangefinder.distance
        print " Orientacao Local: %s" % vehicle.location.local_frame    #NED
        print " Altitude (relativa): %s" % vehicle.location.global_relative_frame.alt
        alt.append(vehicle.location.global_relative_frame.alt)
        latlon.append(vehicle.location.global_frame.lat)
        latlon.append(vehicle.location.global_frame.lon)

    if output == "file":
        with open('uavsensors.dump', "a") as f:
            print "Exibicao dos sensores do VANT somente em arquivo: {}".format(f.name)
            for n in range(repeticao):
                timestamp = int(time.time())
                f.write(" Amostra numero: {}, ".format(n + 1))
                f.write(" Timestamp: {}, ".format(timestamp))
                f.write(" Localizacao Global: %s, " % vehicle.location.global_frame)
                f.write(" Rangefinder distance: %s, " % vehicle.rangefinder.distance)
                f.write(" Orientacao Local: %s, " % vehicle.location.local_frame)  # NED
                f.write(" Altitude (relativa): %s\n" % vehicle.location.global_relative_frame.alt)
                alt.append(vehicle.location.global_relative_frame.alt)
                latlon.append(vehicle.location.global_frame.lat)
                latlon.append(vehicle.location.global_frame.lon)
            f.close()
        f.closed
    return (latlon,alt)

    """
    # vehicle is an instance of the Vehicle class
    print "Autopilot Firmware version: %s" % vehicle.version
    print "Autopilot capabilities (supports ftp): %s" % vehicle.capabilities.ftp
    print "Global Location (absolute altitude): %s" % vehicle.location.global_frame
    print "Global Location (relative altitude): %s" % vehicle.location.global_relative_frame
    print "Local Location: %s" % vehicle.location.local_frame    #NED
    print "Attitude: %s" % vehicle.attitude
    print "Velocity: %s" % vehicle.velocity
    print "GPS: %s" % vehicle.gps_0
    print "Groundspeed: %s" % vehicle.groundspeed
    print "Airspeed: %s" % vehicle.airspeed
    print "Gimbal status: %s" % vehicle.gimbal
    print "Battery: %s" % vehicle.battery
    print "EKF OK?: %s" % vehicle.ekf_ok
    print "Last Heartbeat: %s" % vehicle.last_heartbeat
    print "Rangefinder: %s" % vehicle.rangefinder
    print "Rangefinder distance: %s" % vehicle.rangefinder.distance
    print "Rangefinder voltage: %s" % vehicle.rangefinder.voltage
    print "Heading: %s" % vehicle.heading
    print "Is Armable?: %s" % vehicle.is_armable
    print "System status: %s" % vehicle.system_status.state
    print "Mode: %s" % vehicle.mode.name    # settable
    print "Armed: %s" % vehicle.armed    # settable
    """