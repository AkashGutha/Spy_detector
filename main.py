import threading
import asyncio
import io
import glob
import os
import sys
import time
import uuid
import requests
import json
import select
import datetime
import subprocess
from urllib.parse import urlparse
from io import BytesIO
from PIL import Image, ImageDraw

import numpy as np
import cv2
from dotenv import load_dotenv, find_dotenv
from record_spies import Spy, SpyImageProcessor

# load your dot env file
load_dotenv(find_dotenv())

# Global variables
flip_video = False
key_input = ''
terminate_program = False
spies = []

# video capture from open cv2
capture = cv2.VideoCapture(0)

fps = capture.get(cv2.CAP_PROP_FPS)
print("fps: ", fps)

face_cascade = cv2.CascadeClassifier(
    "/Users/akash/Desktop/hackio2019/haarcascade_frontalface_default.xml")

path = os.path.join(
    os.getcwd(),
    "temp_spy_data/",
    datetime.datetime.now().strftime('%Y%m%d_%H%M%S')
)
try:
    os.mkdir(path)
except OSError:
    print("Creation of the directory %s failed" % path)
else:
    print("Successfully created the directory %s " % path)


spy_images_processor = SpyImageProcessor(path)

def main():
    spy_face_counter = 0
    while(True):
        #  read if any input
        input = select.select([sys.stdin], [], [], 0.8)[0]
        if input:
            line = sys.stdin.readline().rstrip()
            if (line == 'q'):
                spy_images_processor.save_data()
                print("terminating the program")
                break
        else:
            # Capture frame-by-frame
            ret, frame = capture.read()
            # processed_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

            # Look for faces in the image using the loaded cascade file
            faces = face_cascade.detectMultiScale(frame, 1.1, 5)

            print("Found "+str(len(faces))+" face(s)")

            # Draw a rectangle around every found face
            for (x, y, w, h) in faces:
                # print("area: " + str(w*h))
                if (w*h > 15000):
                    spy_face_counter = spy_face_counter + 1
                    img_path = path + '/spy_img_' + \
                        str(spy_face_counter) + '.jpg'
                    # print(path)
                    # cv2.rectangle(frame, (x, y),
                    #               (x+w, y+h), (255, 255, 0), 2)
                    cv2.imwrite(img_path, frame)
                    spy_images_processor.add_image_path(img_path)
                    # subprocess.call(
                    #     'echo \'tell application "Finder" to sleep\' | osascript', shell=True)
                    break

            # Display the resulting frame
            # cv2.imshow('capture frame', frame)
            # cv2.waitKey(5000)

    # output spies captured
    # for image in spy_images_processor.images:
    #     print(image)

    # When everything done, release the capture
    print("spy face counter: ", spy_face_counter)
    capture.release()
    cv2.destroyAllWindows()


if __name__ == '__main__':
    main()
    pass
