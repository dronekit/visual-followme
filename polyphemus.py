#!/usr/bin/python

import numpy as np
import cv2

cam = cv2.VideoCapture(0)

while True:
    _, frame = cam.read()
    cv2.imshow("frame",frame)
    ch = 0xFF & cv2.waitKey(5)
    if ch == 27:
        break