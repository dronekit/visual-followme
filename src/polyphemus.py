import cv2
import datetime
import sys

from file_utils import close_loggers
from gui import render_crosshairs
import numpy as np
from red_blob_detection import detect_target



def move_camera(vehicle, pwm):
    msg = vehicle.message_factory.rc_channels_override_encode(1, 1, 0, 0, 0, 0, 0, pwm, 0, 0)
    vehicle.send_mavlink(msg)
    vehicle.flush()

def process_stream(video_in, loggers, vehicle=None):
    if not video_in.isOpened():
        print "Could not open Video Stream.  Bad filename name or missing camera."
        sys.exit(-1)
    
    hist = np.array([[255.], [0.], [0.], [0.], [0.], [0.], [0.], [0.], [0.], [0.], [0.], [0.], [0.], [0.], [0.], [255.]])
    hist = hist.astype(np.float32, copy=False)
    frame_number = 0       
    
    if loggers:
        write_header(loggers)
        
    while True:
        frame = get_frame(video_in)
        
        process_frame(loggers, hist, frame_number, frame, vehicle)
        frame_number = frame_number + 1
        
        pwm = 1300 + (frame_number % 500)
        move_camera(vehicle, pwm)

        
        if vehicle:
            if not vehicle.armed:
                break
        ch = 0xFF & cv2.waitKey(5)
        if ch == 27:
            break        
    
    if loggers:
        close_loggers(loggers)
    cv2.destroyAllWindows()
    video_in.release()
    

def write_header(loggers):
    loggers[1].write("frame,datetime,pitch,roll,yaw,lat,lon,alt,is_relative;\n")

def get_attitude_string(vehicle):
    return str(vehicle.attitude.pitch)+","+str(vehicle.attitude.roll)+","+str(vehicle.attitude.yaw)


def get_location_string(vehicle):
    return str(vehicle.location.lat)+","+str(vehicle.location.lon)+","+str(vehicle.location.alt)+","+str(vehicle.location.is_relative)

def process_frame(loggers, hist, frame_number, frame, vehicle):
    if loggers:
        loggers[0].write(frame)
        if vehicle:
            loggers[1].write(str(frame_number) + "," + str(datetime.datetime.today()) + ","+get_attitude_string(vehicle)+ ","+get_location_string(vehicle)+";\n")
        else:
            loggers[1].write(str(frame_number) + "," + str(datetime.datetime.today()) + ";\n")
    target = detect_target(hist, frame)
    render_crosshairs(frame, target)
    cv2.imshow("frame", frame)

def get_frame(videoInput):
    gotNewFrame, frame = videoInput.read()
    if not gotNewFrame:
        print "Reached EOF or webcam disconnected"
        sys.exit(0) 
    return frame