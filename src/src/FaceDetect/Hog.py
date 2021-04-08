from face_recognition import face_locations
import logging
import time
from datetime import datetime, timezone
import os
import sys
import cv2
import imutils

class FaceDetect(object):
    def __init__(self, resize_w=400, resize_h=None, save_img=True):
        self.url = '/logs/image/'
        self.resize_w = resize_w 
        self.resize_h = resize_h
        self.save_img = save_img

    def detect_face(self, img):
        small_img = imutils.resize(img, width=self.resize_w)
        small_bbs = face_locations(img=small_img)

        bbs = []
        face_img = []
        if len(small_bbs) > 0:
            w_ratio = img.shape[1]/small_img.shape[1]
            h_ratio = img.shape[0]/small_img.shape[0]

            for bb in small_bbs:
                top, right, bottom, left = bb
                real_bb = [0,0,0,0]
                real_bb[0] = round(top * h_ratio)
                real_bb[1] = round(right * w_ratio)
                real_bb[2] = round(bottom * h_ratio)
                real_bb[3] = round(left * w_ratio)
                face_img = img[real_bb[0]:real_bb[2], real_bb[3]:real_bb[1]].copy()

                # Save face image
                if self.save_img:
                    time = datetime.now().replace(tzinfo=timezone.utc).timestamp()
                    cv2.imwrite(f'{self.url}{time}.png', face_img)

                bbs.append(real_bb)
        return bbs


def main():
    detector = FaceDetect(save_img=False)

    cap = cv2.VideoCapture(0)
    while True:
        s, frame = cap.read()
        if s :
            face_locs =  detector.detect_face(frame)
            if len(face_locs) > 0:
                for loc in face_locs:
                    t, r, b, l = loc

                    cv2.rectangle(frame, (l, t), (r, b), (0,255,0), 2)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break 
        cv2.imshow('test', frame)



if __name__ == '__main__':
    main()
    