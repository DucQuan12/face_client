from __future__ import absolute_import

import logging
import time
from utils.data_task import DataTask
from grpc_client import Grpc
from NeatLogger import Log
from utils.utils import Util
import configparser

cfg = configparser.ConfigParser()
cfg.read('config.ini')

log = Log()
logger = log.get_logger()


class FaceClient(object):
    def __init__(self):
        self.__util = Util()
        self.__data = DataTask()
        self.__person_id = 1
        self._frames_list = []

    def __str__(self):
        return self.__class__.__name__

    def run(self):
        start = time.time()
        print(2)
        app_client = Grpc()
        print(1)
        app_client._run()
        logger.info("Total time:{}".format(time.time() - start))


if __name__ == "__main__":
    app = FaceClient()
    logging.info('Start App')
    app.run()
