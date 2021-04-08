from NeatLogger import Log
import cv2
import os

log = Log()
logger = log.get_logger()


class CameraUrl(object):
    def __init__(self):
        self._frames_list = []

    def camera_url(self, batch_size):
        cap = cv2.VideoCapture(0)
        while True:
            _, frame = cap.read()
            logger.error('No input')
            if _ != 1:
                continue
            self._frames_list.append(frame)
            if self._frames_list == batch_size:
                yield self._frames_list
                self._frames_list = []