import tkinter as tk
import cv2
import numpy as np
from detection import Detector
from gui import GUI

MAX_WIDTH = 640
MAX_HEIGHT = 480

class APP:
    def __init__(self):
        self.detector = Detector()
        self.use_image = False
        self.image = None
        self.video_capture = cv2.VideoCapture(0)
        self.running = True
        self.mode = "Webcam Mode"

    def load_image(self, path):
        img = cv2.imread(path)
        if img is not None:
            self.image = self.resize_frame(img)
            self.use_image = True
            self.mode = f"Image Mode ({path.split('/')[-1]})"

    def use_webcam(self):
        self.use_image = False
        self.mode = "Webcam Mode"

    def stop_app(self):
        self.running = False
        if self.video_capture.isOpened():
            self.video_capture.release()

    def resize_frame(self, frame):
        h, w = frame.shape[:2]
        scale = min(MAX_WIDTH / w, MAX_HEIGHT / h, 1.0)
        new_w, new_h = int(w * scale), int(h * scale)
        return cv2.resize(frame, (new_w, new_h))

    def get_frame(self):
        if not self.use_image:
            ret, frame = self.video_capture.read()
            if not ret:
                frame = np.ones((MAX_HEIGHT, MAX_WIDTH, 3), dtype=np.uint8) * 255
            else:
                frame = self.resize_frame(frame)
        else:
            if self.image is None:
                frame = np.ones((MAX_HEIGHT, MAX_WIDTH, 3), dtype=np.uint8) * 255
            else:
                frame = self.image.copy()

        faces = self.detector.detect_faces(frame)
        d_objects = self.detector.detect_objects(frame)
        frame = self.detector.annotate_frame(frame, faces, d_objects)
        return frame


if __name__ == "__main__":
    app = APP()
    root = tk.Tk()
    gui = GUI(root, app)
    root.mainloop()
