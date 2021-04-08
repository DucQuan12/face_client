from PIL import ImageDraw, Image
import cv2
import os


class Util(object):
    @staticmethod
    def read_key(path_file):
        with open(path_file, 'rb') as f:
            key_sever = f.read()
        return key_sever

    @staticmethod
    def draw_image(image, boxes):
        draw = ImageDraw.Draw(image)
        draw.line()
        return image

    def __str__(self):
        return self.__class__.__name__
