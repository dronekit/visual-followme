import cv2
import time

from file_utils import Logger
from polyphemus import process_stream

def get_vehicle():
    api = local_connect()  # @UndefinedVariable
    v = api.get_vehicles()[0]
    return v

def wait_for_arm(v):
    while not v.armed:
        time.sleep(0.001)
    print "ARMED"


print "DroneScript - Visual-Follow Running"
v = get_vehicle()

while True:
    wait_for_arm(v)    

    video_in = cv2.VideoCapture()
    video_in.open(0)
    
    logger = Logger(path="/home/odroid/Videos/")
    
    process_stream(video_in, logger, vehicle=v)
