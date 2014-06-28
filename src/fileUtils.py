import cv2
import datetime
import glob


def get_new_file_name(path):
    video_counter = len(glob.glob1(path, "*.avi"))
    filename = "demo_%03d"%video_counter
    return path+timeStamped(filename)+ ".avi"

def timeStamped(fname, fmt='{fname}_%Y-%m-%d-%H-%M-%S'):
    return datetime.datetime.now().strftime(fmt).format(fname=fname)


def getLoggers(path = "../vids/"):
    filename = get_new_file_name(path)
    videoWriter = cv2.VideoWriter(filename=filename, # Provide a file to write the video to
        fourcc=cv2.cv.CV_FOURCC('P', 'I', 'M', '1'), # bring up codec dialog box
        fps=30, 
        frameSize=(640, 480))
    logFile = open(filename[:-3] + "csv", "w")
    return (videoWriter, logFile)




def closeloggers(loggers):
    loggers[0].release()
    loggers[1].close()