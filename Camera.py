#!/usr/bin/python3

import picamera
import datetime

def init():
    camera = picamera.PiCamera()
    camera.resolution = (320, 180)
    return camera

def getPhoto(camera, directory):
    now = datetime.datetime.now()
    name = "cam_%04d%02d%02d_%02d%02d%02d.jpg" % (now.year, now.month, now.day, now.hour, now.minute, now.second)
    fullPath = "%s%s" % (directory, name)
    camera.capture(fullPath)
    return fullPath

if __name__ == '__main__':
    folder = "./camera/"

    name = getPhoto(folder)
    print(name)
