import tkinter as tk
from detection import App

from gui import GUI

if __name__ == "__main__":
    root = tk.Tk()
    app = App()
    gui = GUI(root, app)
    root.mainloop()
