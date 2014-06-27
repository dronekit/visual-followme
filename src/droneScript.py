import cv2
from droneapi.lib import VehicleMode
from pymavlink import mavutil
import time

from fileUtils import getLoggers
from polyphemus import process_stream


def getVehicle():
    # First get an instance of the API endpoint
    api = local_connect()  # @UndefinedVariable
    # get our vehicle - when running with mavproxy it only knows about one vehicle (for now)
    v = api.get_vehicles()[0]
    return v

def waitForArm(v):
# wait for vehicle to arm
    while not v.armed:
        time.sleep(0.001)
    print "ARMED"



print "DroneScript - Visual-Follow Running"

v = getVehicle()

while True:
    waitForArm(v)
    
    video_in = cv2.VideoCapture()
    video_in.open(0)
    
    loggers = getLoggers(path="/home/odroid/Videos/")
    
    process_stream(video_in, loggers, vehicle=v)



