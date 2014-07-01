import cv2
import sys

from gui import render_crosshairs
import numpy as np
from red_blob_detection import detect_target
from pid import Pid, print_graph


controller = Pid(kp=0.36, ki=0.05, kd=2.4)


def move_camera(vehicle, pwm):
    if vehicle:
        msg = vehicle.message_factory.rc_channels_override_encode(1, 1, 0, 0, 0, 0, 0, pwm, 0, 0)
        vehicle.send_mavlink(msg)
        vehicle.flush()

def process_stream(video_in, logger, vehicle=None):
    if not video_in.isOpened():
        print "Could not open Video Stream.  Bad filename name or missing camera."
        sys.exit(-1)
    
    hist = np.array([[255.], [0.], [0.], [0.], [0.], [0.], [0.], [0.], [0.], [0.], [0.], [0.], [0.], [0.], [0.], [255.]])
    hist = hist.astype(np.float32, copy=False) 
    
    if logger:
        logger.write_header()

    while True:
        frame = get_frame(video_in)
        
        process_frame(logger, hist,  frame, vehicle)
        
        # if vehicle:
        #    if not vehicle.armed:
        #        break
        ch = 0xFF & cv2.waitKey(5)
        if ch == 27:
            break        
    
    if logger:
        logger.close()
    cv2.destroyAllWindows()
    video_in.release()


def camera_pid(target, vehicle):
    if target != None:
        contour_centroid = cv2.moments(target)
        try:
            _, cy = int(contour_centroid['m10'] / contour_centroid['m00']), int(contour_centroid['m01'] / contour_centroid['m00'])
            
            control = controller.compute(cy, 240)
            pwm = control+1500
            move_camera(vehicle, pwm)

            print_graph(cy,pwm)
        except ZeroDivisionError:
            pass    


def process_frame(logger, hist, frame, vehicle):
    if logger:
        logger.log(frame,vehicle)
        
    target = detect_target(hist, frame)
    
    camera_pid(target, vehicle)
    
    render_crosshairs(frame, target)
    cv2.imshow("frame", frame)

def get_frame(videoInput):
    gotNewFrame, frame = videoInput.read()
    if not gotNewFrame:
        print "Reached EOF or webcam disconnected"
        sys.exit(0) 
    return frame
