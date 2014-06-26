#!/usr/bin/python

import sys

import cv2
import glob
import numpy as np

from gui import render_crosshairs
from redBlobDetection import detect_target

def main():
    video_in = cv2.VideoCapture()
    if len(sys.argv) >= 2 and sys.argv[1][:8] == "--input=":
        video_in.open(sys.argv[1][8:])
        print sys.argv[1][8:]
    else:
        video_in.open(0)
        
    hist = np.array([[255.], [0.], [0.], [0.], [0.], [0.], [0.], [0.], [0.], [0.], [0.], [0.], [0.], [0.], [0.], [255.]])
    hist = hist.astype(np.float32, copy=False)
    while True:
        frame = get_frame(video_in)
        if record:
            writer.write(frame)
        cv2.imshow("frame", frame)
        target = detect_target(hist, frame)
        render_crosshairs(frame, target)
        ch = 0xFF & cv2.waitKey(5)
        if ch == 27:
            return

def get_frame(input):
    _, frame = input.read()
    return frame

if __name__ == '__main__':
    record = len(sys.argv) >= 2 and sys.argv[1] == "--record"
    video_counter = len(glob.glob1("./vids", "*.avi"))
    file = "./vids/demo_" + str(video_counter) + ".avi"
    if record:
        writer = cv2.VideoWriter(filename=file,  # Provide a file to write the video to
                             fourcc=cv2.cv.CV_FOURCC('P', 'I', 'M', '1'),  # bring up codec dialog box
                             fps=30,
                             frameSize=(640, 480))
    try:
        main()
    except KeyboardInterrupt:
        print "KeyboardInterrupt detected."
    cv2.destroyAllWindows()
    if record:
        writer.release()
        
