import threading
import asyncio
import io
import glob
import os
import sys
import time
import uuid
import requests
import select
from urllib.parse import urlparse
from io import BytesIO
from PIL import Image, ImageDraw
from azure.cognitiveservices.vision.face import FaceClient
from msrest.authentication import CognitiveServicesCredentials
from azure.cognitiveservices.vision.face.models import TrainingStatusType, Person, SnapshotObjectType, OperationStatusType

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
spy_images_processor = SpyImageProcessor()

# video capture from open cv2
capture = cv2.VideoCapture(0)
# capture.set(cv2.CAP_PROP_FRAME_WIDTH,640)
# capture.set(cv2.CAP_PROP_FRAME_HEIGHT,480)

# Set the FACE_SUBSCRIPTION_KEY environment variable with your key as the value.
# This key will serve all examples in this document.
KEY = os.environ['FACE_SUBSCRIPTION_KEY']

# Set the FACE_ENDPOINT environment variable with the endpoint from your Face service in Azure.
# This endpoint will be used in all examples in this quickstart.
ENDPOINT = os.environ['FACE_ENDPOINT']

# print(KEY, ENDPOINT)

fps = capture.get(cv2.CAP_PROP_FPS)
print("fps: ", fps)

face_cascade = cv2.CascadeClassifier(
    "/Users/akash/Desktop/hackio2019/haarcascade_frontalface_default.xml")


def main():
    spy_face_counter = 0
    while(True):
        #  read if any input
        input = select.select([sys.stdin], [], [], 0)[0]
        if input:
            line = sys.stdin.readline().rstrip()
            if (line == 'q'):
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
                print("area: " + str(w*h))
                if (w*h > 15000):
                    spy_face_counter = spy_face_counter + 1
                    path = './temp_spy_data/spy_face_'+str(spy_face_counter)+'.jpg'
                    print(path)
                    spy_images_processor.add_image(cv2.imwrite(path, frame))
                    cv2.rectangle(frame, (x, y),
                                  (x+w, y+h), (255, 255, 0), 2)
                    break

            # Display the resulting frame
            cv2.imshow('capture frame', frame)
            cv2.waitKey(5000)

    # When everything done, release the capture
    capture.release()
    cv2.destroyAllWindows()


if __name__ == '__main__':
    main()
    pass
