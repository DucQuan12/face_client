import time
import os
import logging
import imutils
import server_pb2
import grpc
import server_pb2_grpc
from utils.data_task import DataTask
from imutils.video import FPS
from imutils.video import WebcamVideoStream
from src.processor_model import Model
from facenet_pytorch import MTCNN
from grpc_client import Grpc
from NeatLogger import Log
from utils.utils import Util
import cv2
import configparser

cfg = configparser.ConfigParser()
cfg.read('config.ini')

log = Log()
logger = log.get_logger()


class FaceClient(object):
    def __init__(self):
        self.__path = cfg.get('DEFAULT', 'path')
        self._size = cfg.getint('PARAMETER', 'size_w')
        self._stride = cfg.getfloat('PARAMETER', 'stride')
        self.__camera_url = cfg.get('DEFAULT', 'camera_url')
        self._batch_size = cfg.getint('PARAMETER', 'batch_size')
        self.__key_server = cfg.get('DEFAULT', 'key_server')
        self.__port = cfg.get('DEFAULT', 'port')
        self.__host = cfg.get('DEFAULT', 'host')
        self.__util = Util()
        self.__data = DataTask()
        self.__person_id = 1
        self._frames_list = []

    def __str__(self):
        return self.__class__.__name__

    def run(self):
        logger.info('Start App')
        private_key = self.__util.read_key(self.__key_server)
        credentials = grpc.ssl_channel_credentials(root_certificates=private_key)
        channel = grpc.secure_channel('localhost:50070', credentials)
        stub = server_pb2_grpc.FaceServiceStub(channel)

        cap = cv2.VideoCapture(0)
        while True:
            try:
                _, frame = cap.read()
                self._frames_list.append(frame)

                if _ != 1:
                    continue

                # if len(self._frames_list) == self._batch_size:
                #     faces_list = model.detect(self._frames_list)
                #     # faces_list = Model.modelmtcnn(frames_list=self._frames_list)
                #     self._frames_list = []
                #     # print(faces_list)
                #     # for frame in faces:
                #     # if faces_list is not None:
                response = stub.getStream(Grpc.request_client(frame))
                for res in response:
                    logger.info(("{}").format(res))

            except grpc.RpcError as e:
                logger.error("E")


if __name__ == "__main__":
    app = FaceClient()
    logging.info('Start App')
    app.run()
