import torch
from facenet_pytorch import MTCNN
import cv2


class FastMTCNN(object):
    def __init__(self, stride, size=1, *args, **kwargs):
        self.stride = stride
        self.size = size
        self.mtcnn = MTCNN(*args, **kwargs)

    def __call__(self, frames):
        faces = []
        if self.size != 1:
            frames = [cv2.resize(f, (int(f.shape[1] * self.size), int(f.shape[0] * self.size))) for f in frames]

        boxes, probs = self.mtcnn.detect(frames[::self.stride])

        for i, frame in enumerate(frames):
            box_ind = int(i / self.size)
            if boxes[box_ind] is None:
                continue
            for box in boxes[box_ind]:
                box = [int(b) for b in box]
                start = (box[0], box[1])
                end = (box[2], box[3])
                cv2.rectangle(frame, start, end, (0, 255, 0))
                faces.append(frame)
                # faces.append(frame[box[1]:box[3], box[0]:box[2]])

        return faces

    def __str__(self):
        return self.__class__.__name__


if __name__ == '__main__':
    FastMTCNN()
