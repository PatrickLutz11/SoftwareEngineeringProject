import tkinter as tk
from tkinter import ttk, filedialog
import threading

class ObjectPatternRecognizerGUI:
    def __init__(self, master):
        self.master = master
        self.master.title("Object Pattern Recognizer")

        self.mode = tk.StringVar(value="CAMERA")
        mode_frame = ttk.LabelFrame(master, text="Betriebsart")
        mode_frame.pack(padx=10, pady=10, fill="x")

        ttk.Radiobutton(mode_frame, text="CAMERA", variable=self.mode, value="CAMERA").pack(anchor=tk.W)
        ttk.Radiobutton(mode_frame, text="IMAGE", variable=self.mode, value="IMAGE").pack(anchor=tk.W)

        self.folder_path = tk.StringVar()
        path_frame = ttk.LabelFrame(master, text="Bilderordner Pfad")
        path_frame.pack(padx=10, pady=10, fill="x")

        ttk.Entry(path_frame, textvariable=self.folder_path).pack(side=tk.LEFT, expand=True, fill="x", padx=5, pady=5)
        ttk.Button(path_frame, text="Durchsuchen", command=self.browse_folder).pack(side=tk.LEFT, padx=5, pady=5)

        button_frame = ttk.Frame(master)
        button_frame.pack(padx=10, pady=10)

        self.start_button = ttk.Button(button_frame, text="Erkennung starten", command=self.start_detection)
        self.start_button.pack(side=tk.LEFT, padx=5)

        self.stop_button = ttk.Button(button_frame, text="Erkennung stoppen", command=self.stop_detection, state=tk.DISABLED)
        self.stop_button.pack(side=tk.LEFT, padx=5)

        self.status_label = ttk.Label(master, text="Status: Bereit")
        self.status_label.pack(padx=10, pady=10)

        self.detection_thread = None
        self.running = False

    def browse_folder(self):
        directory = filedialog.askdirectory()
        if directory:
            self.folder_path.set(directory)

    def start_detection(self):
        if not self.running:
            self.running = True
            self.start_button.config(state=tk.DISABLED)
            self.stop_button.config(state=tk.NORMAL)
            self.status_label.config(text="Status: Erkennung läuft...")
            self.detection_thread = threading.Thread(target=self.run_detection)
            self.detection_thread.start()

    def stop_detection(self):
        if self.running:
            self.running = False
            self.status_label.config(text="Status: Erkennung wird gestoppt...")

    def run_detection(self):
        mode = self.mode.get()
        if mode == "CAMERA":
            self.detect_from_camera()
        elif mode == "IMAGE":
            folder = self.folder_path.get()
            if folder:
                self.detect_from_images(folder)
            else:
                self.status_label.config(text="Status: Bitte einen gültigen Ordnerpfad angeben.")
        self.running = False
        self.start_button.config(state=tk.NORMAL)
        self.stop_button.config(state=tk.DISABLED)
        self.status_label.config(text="Status: Erkennung abgeschlossen.")

    def detect_from_camera(self):
        while self.running:
            pass
        self.status_label.config(text="Status: Kameraerkennung gestoppt.")

    def detect_from_images(self, folder):
        import time
        import os

        image_files = [f for f in os.listdir(folder) if f.endswith(('.png', '.jpg', '.jpeg'))]
        for image_file in image_files:
            if not self.running:
                break
            image_path = os.path.join(folder, image_file)
            time.sleep(1)
        if self.running:
            self.status_label.config(text="Status: Bilderkennung abgeschlossen.")
        else:
            self.status_label.config(text="Status: Bilderkennung gestoppt.")

if __name__ == "__main__":
    root = tk.Tk()
    app = ObjectPatternRecognizerGUI(root)
    root.mainloop()
