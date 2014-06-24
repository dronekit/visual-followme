#!/usr/bin/python

import numpy as np
import cv2

cam = cv2.VideoCapture(0)
hist = np.array([[255.],[0.],[0.],[0.],[0.],[0.],[0.],[0.],[0.],[0.],[0.],[0.],[0.],[0.],[0.],[255.]])
hist = hist.astype(np.float32, copy=False)

while True:
    _, frame = cam.read()
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    mask = cv2.inRange(hsv, np.array((0., 150., 0.)), np.array((180., 255., 255.)))#ignore pixels that are black or gray
    prob = cv2.calcBackProject([hsv], [0], hist, [0, 180], 1)
    #prob is a binary image with all red pixels represented as 1's
    prob &= mask
    
    #clean it up with some morphology
    erode = cv2.erode(prob,None,iterations = 1)
    dilated = cv2.dilate(erode,None,iterations = 2)
    binary_img = cv2.erode(dilated,None,iterations = 1) 
    
    #detect biggest polygon
    binary_img_to_process = binary_img.copy()#contour detection will mess up the image
    contours,hierarchy = cv2.findContours(binary_img_to_process,cv2.RETR_LIST,cv2.CHAIN_APPROX_SIMPLE)
    biggest_contour=None
    if contours != []:
        biggest_contour_index = 0
        for i in range(1,len(contours)):       
            if cv2.contourArea(contours[i])>cv2.contourArea(contours[biggest_contour_index]):
                biggest_contour_index = i
        biggest_contour=contours[biggest_contour_index]
    
    #draw some stuff out of a bad spy movie
    if biggest_contour != None:
        ball_centroid=cv2.moments(biggest_contour)
        cx,cy = int(ball_centroid['m10']/ball_centroid['m00']), int(ball_centroid['m01']/ball_centroid['m00'])
        cv2.circle(frame,(cx,cy),4,(200,110,255),3)
    
    cv2.imshow("frame",frame)
    ch = 0xFF & cv2.waitKey(5)
    if ch == 27:
        break