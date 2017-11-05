# -*- coding: utf-8 -*-
import picamera
from time import sleep

def cameraGimbal (vehicle, mode):
    camera = picamera.PiCamera()
    if not mode:
        mode = "photo"
    print "Gimbal status: %s" % vehicle.gimbal

    # Point the gimbal straight down
    if mode == "photo":
        vehicle.gimbal.rotate(-90, 0, 0)

        camera.capture('imageGround{counter:03d}.jpg')
        sleep(10)

        # Set the camera to track the current home position.
        vehicle.gimbal.target_location(vehicle.home_location)
        camera.capture('imageHome.jpg')
        sleep(10)

# Rotacao
#    camera.hflip = True
#    camera.vflip = True


# Video recording
#   if mode == "video":
    #   camera.start_recording('video.h264')
    #   sleep(5)
    #   camera.stop_recording()