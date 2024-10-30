import tkinter as tk
from tkinter import ttk, filedialog
import threading
import cv2
import sys
import os

# Add the path to your modules
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), 'src')))

from Detection import *
from PictureModifications import *

class ObjectPatternRecognizerGUI:
    def __init__(self, master):
        self.master = master
        self.master.title("Object Pattern Recognizer")

        # Mode selection (CAMERA or IMAGE)
        self.mode = tk.StringVar(value="CAMERA")
        mode_frame = ttk.LabelFrame(master, text="Mode")
        mode_frame.pack(padx=10, pady=10, fill="x")

        # Radiobuttons to select mode
        ttk.Radiobutton(mode_frame, text="CAMERA", variable=self.mode, value="CAMERA", command=self.update_path_state).pack(anchor=tk.W)
        ttk.Radiobutton(mode_frame, text="IMAGE", variable=self.mode, value="IMAGE", command=self.update_path_state).pack(anchor=tk.W)

        # Image path widgets (only shown in IMAGE mode)
        self.image_path = tk.StringVar()
        self.path_frame = ttk.LabelFrame(master, text="Image Path")

        self.path_entry = ttk.Entry(self.path_frame, textvariable=self.image_path)
        self.path_entry.pack(side=tk.LEFT, expand=True, fill="x", padx=5, pady=5)

        self.browse_button = ttk.Button(self.path_frame, text="Browse", command=self.browse_image)
        self.browse_button.pack(side=tk.LEFT, padx=5, pady=5)

        # Start and Stop buttons
        button_frame = ttk.Frame(master)
        button_frame.pack(padx=10, pady=10)

        self.start_button = ttk.Button(button_frame, text="Start Detection", command=self.start_detection)
        self.start_button.pack(side=tk.LEFT, padx=5)

        self.stop_button = ttk.Button(button_frame, text="Stop Detection", command=self.stop_detection, state=tk.DISABLED)
        self.stop_button.pack(side=tk.LEFT, padx=5)

        # Status label
        self.status_label = ttk.Label(master, text="Status: Ready")
        self.status_label.pack(padx=10, pady=10)

        # Label to display images
        self.image_label = ttk.Label(master)
        self.image_label.pack()

        self.detection_thread = None
        self.running = False

        # Initialize the state of path widgets
        self.update_path_state()

    def update_path_state(self):
        mode = self.mode.get()
        if mode == "IMAGE":
            # Show the path widgets
            self.path_frame.pack(padx=10, pady=10, fill="x")
        else:
            # Hide the path widgets and clear the path
            self.path_frame.forget()
            self.image_path.set("")

    def browse_image(self):
        filetypes = (('Image files', '*.png;*.jpg;*.jpeg;*.bmp;*.tiff;*.gif'), ('All files', '*.*'))
        filepath = filedialog.askopenfilename(title='Select Image', filetypes=filetypes)
        if filepath:
            self.image_path.set(filepath)

    def start_detection(self):
        if not self.running:
            self.running = True
            self.start_button.config(state=tk.DISABLED)
            self.stop_button.config(state=tk.NORMAL)
            self.status_label.config(text="Status: Detection running...")
            self.detection_thread = threading.Thread(target=self.run_detection)
            self.detection_thread.start()

    def stop_detection(self):
        if self.running:
            self.running = False
            self.status_label.config(text="Status: Stopping detection...")

    def run_detection(self):
        mode = self.mode.get()
        if mode == "CAMERA":
            self.detect_from_camera()
        elif mode == "IMAGE":
            image_path = self.image_path.get()
            if image_path:
                self.detect_from_image(image_path)
            else:
                self.status_label.config(text="Status: Please provide a valid image path.")
                self.running = False
                self.start_button.config(state=tk.NORMAL)
                self.stop_button.config(state=tk.DISABLED)
                return
        self.running = False
        self.start_button.config(state=tk.NORMAL)
        self.stop_button.config(state=tk.DISABLED)

    def detect_from_camera(self):
        try:
            cap = cv2.VideoCapture(0)
            if not cap.isOpened():
                self.status_label.config(text="Error: Cannot open camera.")
                self.running = False
                return
            while self.running:
                ret, img = cap.read()
                if not ret:
                    break

                # Perform shape detection and recognition
                searching_for_shapes = Detection.shape_detection(img)
                Detection.shape_recognition(searching_for_shapes, img)

                # Resize image
                img = PictureModifications.resize_the_picture(img)

                # Display image in GUI
                self.show_image_in_gui(img)

            cap.release()
            if self.running:
                self.status_label.config(text="Status: Camera detection completed.")
            else:
                self.status_label.config(text="Status: Camera detection stopped.")
        except Exception as e:
            self.status_label.config(text=f"Error: {e}")
            self.running = False

    def detect_from_image(self, image_path):
        try:
            if not os.path.isfile(image_path):
                self.status_label.config(text=f"Error: File {image_path} does not exist.")
                self.running = False
                return

            img = cv2.imread(image_path)
            if img is None:
                self.status_label.config(text=f"Error: Cannot load image from {image_path}")
                self.running = False
                return

            # Perform shape detection and recognition
            searching_for_shapes = Detection.shape_detection(img)
            Detection.shape_recognition(searching_for_shapes, img)

            # Resize image
            img = PictureModifications.resize_the_picture(img)

            # Display image in GUI
            self.show_image_in_gui(img)

            self.status_label.config(text="Status: Image detection completed.")
        except Exception as e:
            self.status_label.config(text=f"Error: {e}")
            self.running = False

    def show_image_in_gui(self, img):
        from PIL import Image, ImageTk

        # Convert image to RGB and then to PIL format
        img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        img_pil = Image.fromarray(img_rgb)
        img_tk = ImageTk.PhotoImage(img_pil)

        # Update the image label
        self.image_label.configure(image=img_tk)
        self.image_label.image = img_tk  # Keep a reference to prevent garbage collection

if __name__ == "__main__":
    root = tk.Tk()
    app = ObjectPatternRecognizerGUI(root)
    root.mainloop()
