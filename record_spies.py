
from azure_face_api import group_processing, detect_face
from queue import Queue
import time
import os
import json


class Spy():
    name = ""
    images = []

    def set_name(self, name):
        self.name = name

    def add_image(self, image):
        self.images.append(image)


class SpyImageProcessor():
    image_paths = Queue()
    face_ids = []
    faces = []
    combined_data = {}

    def add_image_path(self, image_path):
        # print("new image added")
        self.image_paths.put(image_path)
        face = detect_face(image_path)
        # print(face)
        self.combined_data[face.face_id] = image_path
        self.face_ids.append(face.face_id)

    def save_data(self):
        group_result = group_processing(self.face_ids)
        spy_grouped_data = {
            "groups": group_result.groups,
            "messy_groups": group_result.messy_group
        }

        with open('spy_data.json', 'w') as outfile:
            json.dump(self.combined_data, outfile)

        with open('./ui/src/spy_grouped_data.json', 'w') as outfile:
            json.dump(spy_grouped_data, outfile)

        with open('./ui/src/spy_data.json', 'w') as outfile:
            json.dump(self.combined_data, outfile)

        with open('spy_grouped_data.json', 'w') as outfile:
            json.dump(spy_grouped_data, outfile)

    def __init__(self, path):
        self.folder_path = path

    def __del__(self):
        pass


def spy_detection_pipeline(image_paths, face_ids, faces):
    # while True:
    #     if(not image_paths.empty()):
    image_path_to_process = image_paths.get()
    face_id, detected_face = detect_face(image_path_to_process)
    # face_ids[face_id] = 0
    # faces[face_id] = detected_face
    return


def spy_grouping_pipeline(folder_path, faces):
    n_processed_batches = 0
    n_batch_size = 5

    while True:

        n_images = len(os.listdir(folder_path))

        if n_images > n_batch_size * (n_processed_batches + 1):
            group_processing(folder_path, {})
            n_processed_batches = n_processed_batches + 1
            print("-------------------------------------------")
            print("Faces length : ", len(faces))
            print("Images length : ", n_images)
            print("n_processed_batches : ", n_processed_batches)
            print("-------------------------------------------")

        if n_processed_batches > 19:
            return 0

    return 1
