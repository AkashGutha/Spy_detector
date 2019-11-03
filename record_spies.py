
from azure_face_api import find_similar_faces, detect_face
from multiprocessing import Process, Queue, Array, Manager, Lock
import time
import os


class Spy():
    name = ""
    images = []

    def set_name(self, name):
        self.name = name

    def add_image(self, image):
        self.images.append(image)


class SpyImageProcessor():
    process_manager = Manager()
    image_paths = Queue()
    face_ids = process_manager.dict()
    faces = process_manager.dict()
    spy_groups = process_manager.dict()
    spy_detetction_threads = []
    spy_grouping_thread = None

    def add_image_path(self, image_path):
        print("new image added")
        self.image_paths.put(image_path)
        p = Process(target=spy_detection_pipeline, args=[self.image_paths,
                                                         self.face_ids, self.faces])
        p.daemon = True
        p.start()
        self.spy_detetction_threads.append(p)

    def create_and_attach_thread(self, images_folder_path):
        # create and start the process

        p1 = Process(target=spy_grouping_pipeline, args=[
                     images_folder_path, self.spy_groups])
        p1.daemon = True
        p1.start()
        self.spy_grouping_thread = p1

    def save_data(self):
        print(dict(self.face_ids).keys())
        for face in self.faces:
            print(face)

    def __init__(self, path):
        self.create_and_attach_thread(path)

    def __del__(self):
        #  save the data and sync the thread
        self.spy_grouping_thread.join()
        for thread in self.spy_detetction_threads:
            thread.join()


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
            find_similar_faces(folder_path, {})
            n_processed_batches = n_processed_batches + 1
            print("-------------------------------------------")
            print("Faces length : ", len(faces))
            print("Images length : ", n_images)
            print("n_processed_batches : ", n_processed_batches)
            print("-------------------------------------------")

        if n_processed_batches > 19:
            return 0

    return 1