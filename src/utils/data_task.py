import os
import time
import json
import base64
import logging

logging.basicConfig()


class DataTask(object):
    def __init__(self):
        self.image = 1
        self.list_sender = []

    def _convert_data(self, image_array, path, person_id):
        for image in image_array:
            name = str(time.timezone)
            image_encode = base64.b64encode(image)
            image_json = json.dumps(image_encode)
            try:
                if isinstance(person_id, int):
                    with open(path + str(time.timezone) + '_' + str(int(person_id)) + '.jon', 'w') as f:
                        json.dumps(image_json, f)
                    self.list_sender.append(image_json)
                else:
                    logging.error("Person_id no type int")
            except FileExistsError:
                logging.error("File not exist")
