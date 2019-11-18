import os
from azure.cognitiveservices.vision.face import FaceClient
from msrest.authentication import CognitiveServicesCredentials
from dotenv import load_dotenv, find_dotenv
from azure.cognitiveservices.vision.face.models import FaceAttributeType, HairColorType, TrainingStatusType, Person


def group_processing(face_ids):
    # return False, 0
    # load your dot env file
    load_dotenv(find_dotenv())

    KEY = os.environ['FACE_SUBSCRIPTION_KEY']
    FACE_ENDPOINT = os.environ['FACE_ENDPOINT']

    # print("grouping")
    face_client = FaceClient(
        FACE_ENDPOINT,
        CognitiveServicesCredentials(KEY)
    )

    # Call grouping, the grouping result is a group collection, each group contains similar faces.
    group_result = face_client.face.group(face_ids)
    # print(group_result)

    return group_result


def detect_face(image_path):
    # load your dot env file
    load_dotenv(find_dotenv())

    KEY = os.environ['FACE_SUBSCRIPTION_KEY']
    FACE_ENDPOINT = os.environ['FACE_ENDPOINT']

    face_client = FaceClient(FACE_ENDPOINT,
                             CognitiveServicesCredentials(KEY))

    # print(image_path)

    with open(image_path, "rb", buffering=0) as face_fd:
        # print("open file")
        result = face_client.face.detect_with_stream(
            face_fd,
            return_face_attributes=[
                'age', 'gender', 'headPose', 'emotion', 'hair', 'makeup', 'occlusion', 'accessories', 'blur', 'exposure', 'noise'
            ],
            recognition_model='recognition_02',
            detection_model='detection_01',
        )

        return result[0]
