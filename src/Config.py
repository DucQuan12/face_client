import time
import os
import configparser


class ConfigApp(object):
    @staticmethod
    def config_app():
        cfg = configparser.ConfigParser()
        cfg = cfg.read('config.ini')
        return cfg
