
import datetime
import glob

def get_new_file_name():
    video_counter = len(glob.glob1("../vids", "*.avi"))
    filename = "demo_" + str(video_counter)
    path = "../vids/"
    return path+timeStamped(filename)+ ".avi"

def timeStamped(fname, fmt='{fname}_%Y-%m-%d-%H-%M-%S'):
    return datetime.datetime.now().strftime(fmt).format(fname=fname)