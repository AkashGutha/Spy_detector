import os
from azure.cognitiveservices.vision.face import FaceClient
from msrest.authentication import CognitiveServicesCredentials
from dotenv import load_dotenv, find_dotenv
from azure.cognitiveservices.vision.face.models import FaceAttributeType, HairColorType, TrainingStatusType, Person


def find_similar_faces(images_path, faces={}):
    # return False, 0
    # load your dot env file
    load_dotenv(find_dotenv())

    KEY = os.environ['FACE_SUBSCRIPTION_KEY']
    FACE_ENDPOINT = os.environ['FACE_ENDPOINT']

    print("grouping")
    face_client = FaceClient(
        FACE_ENDPOINT,
        CognitiveServicesCredentials(KEY)
    )

    # Call grouping, the grouping result is a group collection, each group contains similar faces.
    group_result = face_client.face.group(face_ids=list(faces.keys()))
    # Face groups containing faces that are similar.
    for i, group in enumerate(group_result.groups):
        print("Found face group {}: {}.".format(
            i + 1,
            " ".join([faces[face_id] for face_id in group])
        ))

    return False, 0


def detect_face(image_path):
    # load your dot env file
    load_dotenv(find_dotenv())

    KEY = os.environ['FACE_SUBSCRIPTION_KEY']
    FACE_ENDPOINT = os.environ['FACE_ENDPOINT']

    face_client = FaceClient(FACE_ENDPOINT,
                             CognitiveServicesCredentials(KEY))

    print(image_path)

    with open(image_path, "r+b", buffering=0) as face_fd:
        print("open file")
        result = face_client.face.detect_with_stream(
            face_fd,
            return_face_attributes=[
                'age', 'gender', 'headPose', 'emotion', 'hair', 'makeup', 'occlusion', 'accessories', 'blur', 'exposure', 'noise'
            ],
            recognition_model='recognition_02',
            detection_model='detection_01',
        )

        print(result)
        print("-------------------------------------------")
        print("done with file")
        print("-------------------------------------------")
        detected_face = result[0]
        print(detected_face)
        return detected_face.face_id, detected_face
