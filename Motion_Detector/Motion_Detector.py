import cv2
import numpy as np

class FrameMotionDetector():
    def __init__(self, accumulated_weight):
        self.accumulated_weight = accumulated_weight
        self.background = None

    def update(self, image):
        if self.background is None:
            self.background = image.copy().astype('float')
            return
        cv2.accumulateWeighted(image, self.background, self.accumulated_weight)

    def detect(self, image, threshold_val=25):
        delta = cv2.absdiff(self.background.astype("uint8"), image)
        thresh = cv2.threshold(delta, threshold_val, 255, cv2.THRESH_BINARY)[1]
        thresh = cv2.erode(thresh, None, iterations=2)
        thresh = cv2.dilate(thresh, None, iterations=2)
        contours = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        if len(contours) == 0:
            return None
        return (thresh)
