import cv2
import datetime
import glob
import os

def get_new_file_name(path):
    video_counter = len(glob.glob1(path, "*.avi"))
    filename = "demo_%03d" % video_counter
    return path + time_stamped(filename) + ".avi"

def time_stamped(fname, fmt='{fname}_%Y-%m-%d-%H-%M-%S'):
    return datetime.datetime.now().strftime(fmt).format(fname=fname)


def make_path(path):
    if not os.path.exists(path):
        os.makedirs(path)

def get_attitude_string(vehicle):
    return str(vehicle.attitude.pitch) + "," + str(vehicle.attitude.roll) + "," + str(vehicle.attitude.yaw)

def get_location_string(vehicle):
    return str(vehicle.location.lat) + "," + str(vehicle.location.lon) + "," + str(vehicle.location.alt) + "," + str(vehicle.location.is_relative)


class Logger:
    frame_number = 0
    
    def __init__(self, path="../vids/"):
        make_path(path)
        
        filename = get_new_file_name(path)
        self.videoWriter = cv2.VideoWriter(filename=filename,  # Provide a file to write the video to
            fourcc=cv2.cv.CV_FOURCC('P', 'I', 'M', '1'),  # bring up codec dialog box
            fps=30,
            frameSize=(640, 480))
        self.logFile = open(filename[:-3] + "csv", "w")
        self.write_header()
        
    def write_header(self):
        self.logFile.write("frame,datetime,pitch,roll,yaw,lat,lon,alt,is_relative;\n")
    
    def log(self, frame, vehicle):
        self.frame_number = self.frame_number + 1
        self.videoWriter.write(frame)
        if vehicle:
            self.logFile.write(str(self.frame_number) + "," + str(datetime.datetime.today()) + "," + get_attitude_string(vehicle) + "," + get_location_string(vehicle) + ";\n")
        else:
            self.logFile.write(str(self.frame_number) + "," + str(datetime.datetime.today()) + ";\n")
        
    def close(self):
        self.videoWriter.release()
        self.logFile.close()
