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