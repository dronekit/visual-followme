#!/usr/bin/python

import sys

import cv2
import glob
import numpy as np

def main():
    video_in = None
    if len(sys.argv) >= 2 and sys.argv[1][:8] == "--input=":
        video_in = cv2.VideoCapture(sys.argv[1][8:])
        print sys.argv[1][8:]
    else:
        video_in = cv2.VideoCapture(0)
        
    hist = np.array([[255.], [0.], [0.], [0.], [0.], [0.], [0.], [0.], [0.], [0.], [0.], [0.], [0.], [0.], [0.], [255.]])
    hist = hist.astype(np.float32, copy=False)
    while True:
        frame = get_frame(video_in)
        if record:
            print "recording"
            writer.write(frame)
        biggest_contour = detect_target(cv2, hist, np, frame)
        render_crosshairs(cv2, frame, biggest_contour)
        cv2.imshow("frame", frame)
        ch = 0xFF & cv2.waitKey(5)
        if ch == 27:
            return

def get_frame(input):
    _, frame = input.read()
    return frame

def detect_target(cv2, hist, np, frame):
    prob = filter_red_pixels(cv2, hist, np, frame)
    binary_img = clean_up_with_morphology(cv2, prob)
    biggest_contour = detect_biggest_polygon(cv2, binary_img)
    return biggest_contour

def filter_red_pixels(cv2, hist, np, frame):
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    unsaturated_pixels = discard_saturated_pixels(cv2, np, hsv)  
    red_pixels = filter_by_color(cv2, hist, hsv)
    red_pixels &= unsaturated_pixels
    return red_pixels

def discard_saturated_pixels(cv2, np, hsv):
    mask = cv2.inRange(hsv, np.array((0., 150., 0.)), np.array((180., 255., 255.)))
    return mask

def filter_by_color(cv2, hist, hsv):
    prob = cv2.calcBackProject([hsv], [0], hist, [0, 180], 1)
    return prob

def clean_up_with_morphology(cv2, prob):
    erode = cv2.erode(prob, None, iterations=1)
    dilated = cv2.dilate(erode, None, iterations=2)
    binary_img = cv2.erode(dilated, None, iterations=1)
    return binary_img

def detect_biggest_polygon(cv2, binary_img):
    binary_img_to_process = binary_img.copy()  # contour detection will mess up the image
    contours, hierarchy = cv2.findContours(binary_img_to_process, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
    biggest_contour = None
    if contours != []:
        biggest_contour_index = 0
        for i in range(1, len(contours)):
            if cv2.contourArea(contours[i]) > cv2.contourArea(contours[biggest_contour_index]):
                biggest_contour_index = i
        
        biggest_contour = contours[biggest_contour_index]
    return biggest_contour

def render_crosshairs(cv2, frame, biggest_contour):
    if biggest_contour != None:
        green = 20, 255, 60
        contour_centroid = cv2.moments(biggest_contour)
        
        try:
            cx, cy = int(contour_centroid['m10'] / contour_centroid['m00']), int(contour_centroid['m01'] / contour_centroid['m00'])
            cv2.circle(frame, (cx, cy), 4, green, 5)
            cv2.line(frame, (0, cy), (frame.shape[1], cy), green, 1)
            cv2.line(frame, (cx, 0), (cx, frame.shape[0]), green, 1)
        except ZeroDivisionError:
            pass

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
        
