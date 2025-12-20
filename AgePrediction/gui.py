import tkinter as tk
from tkinter import filedialog

class GUI:
    def __init__(self, root, app):
        self.root = root
        self.app = app
        self.root.title("Age Detector")

        # Top menu frame
        top = tk.Frame(root)
        top.pack(pady=5)
        tk.Button(top, text="Open Image", command=self.open_image).pack(side=tk.LEFT, padx=5)
        tk.Button(top, text="Webcam Mode", command=self.webcam_mode).pack(side=tk.LEFT, padx=5)

        # Video frame
        self.video_label = tk.Label(root)
        self.video_label.pack(padx=10, pady=10)

        self.root.protocol("WM_DELETE_WINDOW", self.on_close)
        self.update_frame()

    def open_image(self):
        path = filedialog.askopenfilename(filetypes=[("Image Files", "*.jpg *.png *.jpeg")])
        if path:
            self.app.load_image(path)

    def webcam_mode(self):
        self.app.start_webcam()

    def update_frame(self):
        if self.app.running:
            self.app.read_webcam_frame()

        tk_frame = self.app.get_tk_frame()
        if tk_frame:
            self.video_label.imgtk = tk_frame
            self.video_label.configure(image=tk_frame)

        self.root.after(30, self.update_frame)

    def on_close(self):
        self.app.stop_webcam()
        self.root.destroy()
