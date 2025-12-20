import os

import cv2
import numpy as np

cascPath = os.path.dirname(cv2.__file__) + "/data/haarcascade_frontalface_default.xml"
faceCascade = cv2.CascadeClassifier(cascPath)

proto = "MobileNetSSD_deploy.prototxt"
model = "MobileNetSSD_deploy.caffemodel"
net = cv2.dnn.readNetFromCaffe(proto, model)
DETECT_KEYWORDS = [
    ("background", (50, 50, 50)),
    ("aeroplane", (0, 255, 0)),
    ("bicycle", (255, 0, 0)),
    ("bird", (0, 255, 255)),
    ("boat", (255, 255, 0)),
    ("bottle", (255, 0, 255)),
    ("bus", (0, 128, 255)),
    ("car", (128, 0, 255)),
    ("cat", (255, 128, 0)),
    ("chair", (0, 128, 128)),
    ("cow", (128, 128, 0)),
    ("diningtable", (128, 0, 128)),
    ("dog", (255, 100, 100)),
    ("horse", (100, 255, 100)),
    ("motorbike", (100, 100, 255)),
    ("person", (0, 200, 0)),
    ("pottedplant", (0, 150, 150)),
    ("sheep", (150, 150, 0)),
    ("sofa", (150, 0, 150)),
    ("train", (255, 255, 150)),
    ("tvmonitor", (150, 255, 255)),
]

FACE_COLOR = (128, 255, 0)
VEHICLE_COLOR = (255, 255, 0)
FONT = cv2.FONT_HERSHEY_SIMPLEX
FONT_SCALE = 1
THICKNESS = 2

class Detector:

    def detect_faces(self, frame):
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces = faceCascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5)
        return faces

    def detect_objects(self, frame):
        h, w = frame.shape[:2]
        blob = cv2.dnn.blobFromImage(cv2.resize(frame, (300, 300)), 0.007843, (300, 300), 127.5)
        net.setInput(blob)
        detections = net.forward()
        results = []

        label = "unknown"
        color = (0, 0, 0)

        for i in range(detections.shape[2]):
            conf = detections[0, 0, i, 2]

            class_id = int(detections[0, 0, i, 1])
            if 0 < class_id < len(DETECT_KEYWORDS):
                label, color = DETECT_KEYWORDS[class_id]

            x1, y1, x2, y2 = (detections[0, 0, i, 3:7] * np.array([w, h, w, h])).astype(int)
            results.append((label, color, conf, x1, y1, x2, y2))

        return results

    @staticmethod
    def annotate_frame(frame, faces, vehicles):
        for (x, y, w, h) in faces:
            cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), THICKNESS)
            cv2.putText(frame, "Face", (x, y - 5), FONT, FONT_SCALE, (0, 255, 0), THICKNESS)

        for label, color, conf, x1, y1, x2, y2 in vehicles:
            cv2.rectangle(frame, (x1, y1), (x2, y2), color, THICKNESS)
            cv2.putText(frame, f"{label} ({conf * 100:.1f}%)", (x1, y1 - 5), FONT, FONT_SCALE, color, THICKNESS)

        return frame
