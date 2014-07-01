import cv2


def render_crosshairs(frame, target):
    if target != None:
        green = 20, 255, 60
                
        cx, cy = target
        cv2.circle(frame, (cx, cy), 4, green, 5)
        cv2.line(frame, (0, cy), (frame.shape[1], cy), green, 1)
        cv2.line(frame, (cx, 0), (cx, frame.shape[0]), green, 1)
            
        cv2.putText(frame,'Y:%d'%cy,(0,25), cv2.FONT_HERSHEY_SIMPLEX, 1,(0,0,0),2)
        