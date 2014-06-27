#!/usr/bin/python

import argparse
import datetime
import sys

import cv2
import numpy as np

from gui import render_crosshairs
from redBlobDetection import detect_target
from fileUtils import getLoggers, closeloggers




def main(loggers):
    if not video_in.isOpened():
        print "Could not open Video Stream.  Bad filename name or missing camera."
        sys.exit(-1)
    hist = np.array([[255.], [0.], [0.], [0.], [0.], [0.], [0.], [0.], [0.], [0.], [0.], [0.], [0.], [0.], [0.], [255.]])
    hist = hist.astype(np.float32, copy=False)
    frame_number=0       
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

if __name__ == '__main__':
    parser=argparse.ArgumentParser(description="Track a red blob and adjust camera gimbal to follow")
    parser.add_argument('-r','--record', action="store_true", default=False, help='record the output of the program to ../vids/demo_X.avi')
    parser.add_argument('-i','--input', action="store", help='use a video filename as an input instead of a webcam')
    args = parser.parse_args()
    
    video_in = cv2.VideoCapture()
    
    if args.input != None:
        video_in.open(args.input)
    else:
        video_in.open(0)
    
    if args.record:
        loggers = getLoggers()
    else:
        loggers = None  
    try:
        main(loggers)
    except KeyboardInterrupt:
        print "KeyboardInterrupt detected."
    cv2.destroyAllWindows()
    if args.record:
        closeloggers(loggers)
        
