import tkinter as tk
from tkinter import filedialog

import cv2
from PIL import Image, ImageTk


class GUI:
    def __init__(self, root, app):
        self.root = root
        self.app = app
        self.root.title("Detector - Startup")

        frame = tk.Frame(root)
        frame.pack(padx=10, pady=10)
        tk.Button(frame, text="Open Image", command=self.open_image).pack(side=tk.LEFT, padx=5)
        tk.Button(frame, text="Webcam Mode", command=self.webcam_mode).pack(side=tk.LEFT, padx=5)
        tk.Button(frame, text="Quit", command=self.quit_app).pack(side=tk.LEFT, padx=5)

        self.video_label = tk.Label(root)
        self.video_label.pack(padx=10, pady=10)
        self.update_frame()
        self.root.protocol("WM_DELETE_WINDOW", self.quit_app)

    def open_image(self):
        path = filedialog.askopenfilename(filetypes=[("Image Files","*.jpg *.png *.jpeg")])
        if path:
            self.app.load_image(path)

    def webcam_mode(self):
        self.app.use_webcam()

    def quit_app(self):
        self.app.stop_app()
        self.root.destroy()

    def update_frame(self):
        if not self.app.running:
            return

        frame = self.app.get_frame()
        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        img = Image.fromarray(frame_rgb)
        imgtk = ImageTk.PhotoImage(image=img)
        self.video_label.imgtk = imgtk
        self.video_label.configure(image=imgtk)
        self.root.title(f"Detector - {self.app.mode}")

        self.root.after(30, self.update_frame)
