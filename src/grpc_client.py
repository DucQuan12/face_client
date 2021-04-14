import server_pb2
import server_pb2_grpc
# from utils.camera_url import CameraUrl
from utils import utils
import grpc
import base64
import cv2
import imutils
# import Config
import configparser
from NeatLogger import Log

cfg = configparser.ConfigParser()
cfg.read('config.ini')
log = Log()
logger = log.get_logger()


class Grpc(object):
    def __init__(self):
        self._size = cfg.getint('PARAMETER', 'size_w')
        self._stride = cfg.getfloat('PARAMETER', 'stride')
        self.__camera_url = cfg.get('DEFAULT', 'camera_url')
        self._batch_size = cfg.getint('PARAMETER', 'batch_size')
        self.__key_server = cfg.get('DEFAULT', 'key_server')
        self.__port = cfg.get('DEFAULT', 'port')
        self.__host = cfg.get('DEFAULT', 'host')
        self.__utils = utils.Util()
        self.__frames_list = []

    def _run(self):
        private_key = self.__utils.read_key(self.__key_server)
        credentials = grpc.ssl_channel_credentials(root_certificates=private_key)
        # channel = grpc.secure_channel('{}:{}'.format(self.__host, self.__port), credentials)
        channel = grpc.insecure_channel("localhost:50070")
        stub = server_pb2_grpc.FaceServiceStub(channel)
        cap = cv2.VideoCapture(0)
        while True:
            try:
                _, frame = cap.read()
                # self._frames_list.append(frame)
                if _ != 1:
                    continue
                # if len(self._frames_list) == self._batch_size:
                #     faces_list = model.detect(self._frames_list)
                #     # faces_list = Model.modelmtcnn(frames_list=self._frames_list)
                #     self._frames_list = []
                #     # print(faces_list)
                #     # for frame in faces:
                #     # if faces_list is not None:
                response = stub.getStream(self.__utils.request_client(frame))
                
                for res in response:
                    logger.info("{}".format(res))
                    
            except grpc.RpcError as e:
                logger.error(e.details())
