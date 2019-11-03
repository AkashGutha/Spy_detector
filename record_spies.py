from queue import Queue


class Spy():
    name = ""
    images = []

    def set_name(self, name):
        self.name = name

    def add_image(self, image):
        self.images.append(image)


class SpyImageProcessor():
    images = []

    def add_image(self, image):
        self.images.append(image)
