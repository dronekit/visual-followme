import cv2
import time
import os.path
import os

from file_utils import Logger
from polyphemus import process_stream

mustarm = False

def get_vehicle():
    api = local_connect()  # @UndefinedVariable
    v = api.get_vehicles()[0]
    return v

def wait_for_arm(v):
    print "Waiting for arming"
    while not v.armed:
        time.sleep(0.001)
    print "ARMED"


def open_camera():
    # yuck - opencv has no way to count # of cameras, so do this hack of looking for /dev/video*
    numCameras = len(filter(lambda s: s.startswith("video"), os.listdir("/dev")))

    c = cv2.VideoCapture()
    # We start our search with higher numbered (likely external) cameras
    for cnum in range(0, numCameras):
        c.open(numCameras - cnum - 1)
        if c.isOpened():
            return c

    raise Exception('No cameras found')

print "DroneScript - Visual-Follow Running"
v = get_vehicle()

while True:
    if mustarm:
        wait_for_arm(v)    
    
    video_in = open_camera()
    homedir = os.path.expanduser("~")
    logger = Logger(path= homedir + "/Videos/")
    
    process_stream(video_in, logger, vehicle=v, require_arming=mustarm)
