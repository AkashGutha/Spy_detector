
from azure_face_api import find_similar_faces, detect_face
from multiprocessing import Process, Queue, Array, Manager, Lock
import time


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
    face_ids_copy = {}
    processing_thread = None

    def add_image_path(self, image):
        self.image_paths.put(image)

    def create_and_attach_thread(self):
        # create and start the process
        p = Process(target=main, args=[self.image_paths,
                                       self.face_ids])

        p.daemon = True
        p.start()
        self.processing_thread = p
    
    def save_data(self):
        print(self.face_ids)
        

    def __init__(self):
        self.create_and_attach_thread()

    def __del__(self):
        #  save the data and sync the thread
        self.processing_thread.join()


def dummy(a, b):
    pass


def main(image_paths, face_ids):
    while True:
        if(not image_paths.empty()):
            image_path_to_process = image_paths.get()
            is_similar = False
            face_id = 0
            if (len(face_ids) > 0):
                # similarity test
                is_similar, face_id = find_similar_faces(
                    image_path_to_process, face_ids.keys())
                if (is_similar):
                    print("is similar")
                    continue
                else:
                    print("sent to detection 1 ")
                    face_id = detect_face(image_path_to_process)
                    face_ids[str(face_id)] = 0
            else:
                # detect face
                print("sent to detection 2 ")
                face_id = detect_face(image_path_to_process)
                face_ids[str(face_id)] = 0

            # increase the face id count
            face_ids[str(face_id)] += 1
            
            print("ietms:", face_ids.items())
