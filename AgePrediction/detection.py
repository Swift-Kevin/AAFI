import cv2
from PIL import Image, ImageTk
import numpy as np

face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_frontalface_default.xml")
age_net = cv2.dnn.readNetFromCaffe("age_deploy.prototxt", "age_net.caffemodel")
AGE_LIST = ['(0-2)', '(4-6)', '(8-12)', '(15-20)',
            '(25-32)', '(38-43)', '(48-53)', '(60-100)']

DISPLAY_WIDTH = 640
DISPLAY_HEIGHT = 480

class App:
    def __init__(self):
        self.cap = None
        self.running = True
        self.current_frame = None
        self.cap = cv2.VideoCapture(0)

    def detect_age(self, face):
        blob = cv2.dnn.blobFromImage(face, 1.0, (227,227), (78.4,87.1,114.0), swapRB=False)
        age_net.setInput(blob)
        preds = age_net.forward()
        return AGE_LIST[np.argmax(preds)]

    def process_frame(self, frame):
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces = face_cascade.detectMultiScale(gray, 1.1, 5)
        for (x, y, w, h) in faces:
            face = frame[y:y+h, x:x+w]
            age = self.detect_age(face)
            cv2.rectangle(frame, (x, y), (x+w, y+h), (0,255,0), 2)
            cv2.putText(frame, f"Age: {age}", (x, y-10),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0,255,0), 2)
        return frame

    def start_webcam(self):
        if self.cap:
            self.cap.release()
        self.cap = cv2.VideoCapture(0)
        self.running = True

    def stop_webcam(self):
        self.running = False
        if self.cap:
            self.cap.release()
            self.cap = None

    def read_webcam_frame(self):
        if self.cap and self.running:
            ret, frame = self.cap.read()
            if ret:
                self.current_frame = self.process_frame(frame)
                return self.current_frame
        return None

    def load_image(self, path):
        self.stop_webcam()
        frame = cv2.imread(path)
        if frame is not None:
            self.current_frame = self.process_frame(frame)
        return self.current_frame

    def get_tk_frame(self):
        if self.current_frame is None:
            return None

        scale = 0.7
        h, w = self.current_frame.shape[:2]
        new_w = int(w * scale)
        new_h = int(h * scale)

        resized = cv2.resize(self.current_frame, (new_w, new_h), interpolation=cv2.INTER_AREA)
        rgb = cv2.cvtColor(resized, cv2.COLOR_BGR2RGB)
        return ImageTk.PhotoImage(Image.fromarray(rgb))
