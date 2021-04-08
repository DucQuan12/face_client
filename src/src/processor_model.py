# from .FaceDetect.FASTMTCNN import FastMTCNN
from face_recognition import face_locations
from facenet_pytorch import MTCNN
from NeatLogger import Log
import imutils
import torch

log = Log()
logger = log.get_logger()


class Model(object):
    def __init__(self, stride=0.2, size=400, model_name = 'hog'):
        self.names = ['hog', 'mtcnn']
        self.model_name = model_name
        if model_name in self.names:
            if model_name == 'mtcnn':
                self.stride = stride
                self.size = size
                self.device = 'cuda' if torch.cuda.is_available() else 'cpu'
                self.keep = True
                self.factor = 0.6
                self.margin = 14
                self.keep_all = True
                self.mtcnn_model = MTCNN(keep_all=True, device='cuda' if torch.cuda.is_available() else 'cpu')

    # def fast_mtcnn(self):
    #     return FastMTCNN(stride=self.stride, size=self.size,
    #                     margin=self.margin, factor=self.factor,
    #                     keep_all=self.keep_all, device=self.device)

    # @staticmethod
    # def modelmtcnn(frames_list):
    #     faces = []
    #     model_mtcnn = MTCNN(keep_all=True, device='cuda' if torch.cuda.is_available() else 'cpu')
    #     for frame in frames_list:
    #         boxes, _ = model_mtcnn.detect(frame)
    #         try:
    #             for box in boxes:
    #                 img = frame[box[1]:box[3], box[0]:box[2]]
    #                 img = imutils.resize(img, 224)
    #                 faces.append(img)
    #             yield faces
    #         except:
    #             log.error()
    
    def detect(self, frames_list):
        faces = []
        for frame in frames_list:
            if self.model_name == 'mtcnn':
                # l t r b
                boxes, _ = self.mtcnn_model.detect(frame)
            else:
                # t r b l
                boxes = face_locations(frame, number_of_times_to_upsample=0, model="hog")
                boxes = list([x[3], x[0], x[1], x[2]] for x in boxes)
            if boxes is not None:
                try:
                    for box in boxes:
                        img = frame[int(box[1]):int(box[3]), int(box[0]):int(box[2])]
                        img = imutils.resize(img, 224)
                        faces.append(img)
                    return faces
                except Exception as e:
                    print(e)
                    # log.error()

if __name__ == '__main__':
    import cv2
    cap = cv2.VideoCapture(0)
    model = Model(model_name='hog')

    while True:
        r, frame = cap.read()
        faces = []
        if r:
            faces = model.detect([frame])
            if faces is not None:
                if len(faces) > 0:
                    cv2.imshow('face', faces[0])

        cv2.imshow('frame', frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    
    cap.release()
    cv2.destroyAllWindows()

