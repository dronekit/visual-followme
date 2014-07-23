import cv2
import time
import os.path
import os

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


def open_camera():
    # yuck - opencv has no way to count # of cameras, so do this hack of looking for /dev/video*
    numCameras = len(filter(lambda s: s.startswith("video"), os.listdir("/dev")))

    c = cv2.VideoCapture()
    for cnum in range(0, numCameras):
        c.open(0)
        if c.isOpened():
            return c

    raise Exception('No cameras found')

print "DroneScript - Visual-Follow Running"
v = get_vehicle()

while True:
    wait_for_arm(v)    

    video_in = open_camera()
    
    homedir = os.path.expanduser("~")
    logger = Logger(path= homedir + "/Videos/")
    
    process_stream(video_in, logger, vehicle=v)
