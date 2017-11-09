# -*- coding: utf-8 -*-
import picamera

from time import sleep

def camera_gimbal (vehicle, mode, wayPointNum):
    camera = picamera.PiCamera()
    print "Gimbal status: %s" % vehicle.gimbal
    if not mode:
        mode = "ground"

    # Tira foto do chão
    if mode == "ground":
        vehicle.gimbal.rotate(-90, 0, 0)
        camera.capture('imageGround%03i.jpg' % wayPointNum)
        sleep(10)

    # Tira foto do ponto de decolagem
    if mode == "home":
        # Set the camera to track the current home position.
        vehicle.gimbal.target_location(vehicle.home_location)
        camera.capture('imageHome%03i.jpg' % wayPointNum)
        sleep(10)

# Rotacao da imagem
#    camera.hflip = True
#    camera.vflip = True


# Video recording
#   if mode == "video":
    #   camera.start_recording('video.h264')
    #   sleep(5)
    #   camera.stop_recording()