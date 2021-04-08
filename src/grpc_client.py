from concurrent import futures
import server_pb2
import server_pb2_grpc
from utils.camera_url import CameraUrl
from utils import utils
import grpc
import time
import base64
import os
import cv2
import sys
import Config
from NeatLogger import Log

cfg = Config.ConfigApp()
log = Log()
logger = log.get_logger()


class Grpc(object):
    def __init__(self):
        self.__key_server = cfg.get('DEFAULT', 'key_server')
        self.__utils = utils.Util()
        self.__host = cfg.get('DEFAULT', 'host')
        self.__port = cfg.get('DEFAULT', 'port')

    def request_client(self, frame):
        if frame is not None:
            ret, image = cv2.imencode('.jpg', frame)
            image64 = base64.b64encode(image)

            yield server_pb2.Request(datas=image64)

    def client(self, func):
        private_key = self.__utils.read_key(self.__key_server)
        credentials = grpc.ssl_channel_credentials(root_certificates=private_key)
        channel = grpc.secure_channel('{}:{}'.format(self.__host, self.__port), credentials)
        stub = server_pb2_grpc.FaceServiceStub(channel)
        list_frame = CameraUrl.camera_url()
        response = map(stub.getStream(self.request_client), list_frame)
        for res in response:
            logger.info("response from {}: {}".format(self.__host, res))
