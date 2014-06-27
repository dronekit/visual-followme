#!/usr/bin/python

import cv2
import datetime
import sys

from gui import render_crosshairs
import numpy as np
from redBlobDetection import detect_target


def main(video_in, loggers):
    if not video_in.isOpened():
        print "Could not open Video Stream.  Bad filename name or missing camera."
        sys.exit(-1)
    hist = np.array([[255.], [0.], [0.], [0.], [0.], [0.], [0.], [0.], [0.], [0.], [0.], [0.], [0.], [0.], [0.], [255.]])
    hist = hist.astype(np.float32, copy=False)
    frame_number = 0       
    while True:
        frame = get_frame(video_in)
        if loggers:
            loggers[0].write(frame)
            loggers[1].write(str(frame_number) + "," + str(datetime.datetime.today()) + ";\n")
            frame_number = frame_number + 1
        target = detect_target(hist, frame)
        render_crosshairs(frame, target)
        cv2.imshow("frame", frame)
        ch = 0xFF & cv2.waitKey(5)
        if ch == 27:
            return

def get_frame(videoInput):
    gotNewFrame, frame = videoInput.read()
    if not gotNewFrame:
        print "Reached EOF or webcam disconnected"
        sys.exit(0) 
    return frame

        
