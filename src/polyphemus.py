#!/usr/bin/python

import sys

import cv2
import glob
import numpy as np

from gui import render_crosshairs
from redBlobDetection import detect_target

def main():
    cam = cv2.VideoCapture(0)
    hist = np.array([[255.], [0.], [0.], [0.], [0.], [0.], [0.], [0.], [0.], [0.], [0.], [0.], [0.], [0.], [0.], [255.]])
    hist = hist.astype(np.float32, copy=False)
    while True:
        frame = get_frame(cam)
        if record:
            print "recording"
            writer.write(frame)
        biggest_contour = detect_target(cv2, hist, np, frame)
        render_crosshairs(cv2, frame, biggest_contour)
        cv2.imshow("frame", frame)
        ch = 0xFF & cv2.waitKey(5)
        if ch == 27:
            return

def get_frame(cam):
    _, frame = cam.read()
    return frame

if __name__ == '__main__':
    record = len(sys.argv) >= 2 and sys.argv[1] == "--record"
    video_counter = len(glob.glob1("./vids","*.avi"))
    file = "./vids/demo_" + str(video_counter) + ".avi"
    if record:
        writer = cv2.VideoWriter(filename=file,  #Provide a file to write the video to
                             fourcc=cv2.cv.CV_FOURCC('P','I','M','1'),            #bring up codec dialog box
                             fps=30,
                             frameSize=(640, 480))
    try:
        main()
    except KeyboardInterrupt:
        print "KeyboardInterrupt detected."
    cv2.destroyAllWindows()
    if record:
        writer.release()
        
