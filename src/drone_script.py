import cv2
import time

from file_utils import get_loggers
from polyphemus import process_stream


def get_vehicle():
    # First get an instance of the API endpoint
    api = local_connect()  # @UndefinedVariable
    # get our vehicle - when running with mavproxy it only knows about one vehicle (for now)
    v = api.get_vehicles()[0]
    return v

def wait_for_arm(v):
# wait for vehicle to arm
    while not v.armed:
        time.sleep(0.001)
    print "ARMED"


print "DroneScript - Visual-Follow Running"
v = get_vehicle()

wait_for_arm(v)
while True:
    
    video_in = cv2.VideoCapture()
    video_in.open(0)
    
    loggers = get_loggers(path="/home/odroid/Videos/")
    
    process_stream(video_in, loggers, vehicle=v)
