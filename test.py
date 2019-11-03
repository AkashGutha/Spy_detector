import copy
import os

from azure.cognitiveservices.vision.face import FaceClient
from dotenv import find_dotenv, load_dotenv
from msrest.authentication import CognitiveServicesCredentials
from multiprocessing import Process, Queue, Array, Manager, Lock

# load your dot env file
load_dotenv(find_dotenv())

KEY = os.environ['FACE_SUBSCRIPTION_KEY']
FACE_ENDPOINT = os.environ['FACE_ENDPOINT']
DETECT_FACE_ENDPOINT = os.environ['DETECT_FACE_ENDPOINT']
FIND_SIMILAR_ENDPOINT_EXT = os.environ['FIND_SIMILAR_ENDPOINT_EXT']


def main(image_path):

    face_client = FaceClient(FACE_ENDPOINT,
                             CognitiveServicesCredentials(KEY))

    print(image_path)

    with open(image_path, "rb", buffering=0) as stream:
        print("open file")
        result = face_client.face.detect_with_stream(
            stream,
            return_face_attributes=[
                'age', 'gender', 'headPose', 'smile', 'facialHair', 'glasses', 'emotion', 'hair', 'makeup', 'occlusion', 'accessories', 'blur', 'exposure', 'noise'
            ],
            recognition_model='recognition_01'
        )

        print(result)
        print("-------------------------------------------")
        print("done with file")
        print("-------------------------------------------")
        detected_face = result[0]
        print(detected_face)
        return detected_face.face_id, detected_face


p = Process(target=main, args=[
            "/Users/akash/Desktop/hackio2019/temp_spy_data/20191103_075128/spy_img_1.jpg"])
p.daemon = True
p.start()
p.join()

# # Call grouping, the grouping result is a group collection, each group contains similar faces.
# group_result = face_client.face.group(face_ids)
# print(group_result)
# # Face groups containing faces that are similar.
# for i, group in enumerate(group_result.groups):
#     print("Found face group {}: {}.".format(
#         i + 1,
#         " ".join([faces[face_id] for face_id in group])
#     ))
