import tkinter as tk
from tkinter import ttk, filedialog
import threading
import cv2
import sys
import os

# Add the path to your modules
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), 'src')))

from shape_detection import *
from modificators_image import *

# Import Image and ImageTk at the top
from PIL import Image, ImageTk

class ObjectPatternRecognizerGUI:
    def __init__(self, master):
        self.master = master
        self.master.title("Object Pattern Recognizer")

        # Configure grid layout
        self.master.rowconfigure(4, weight=1)  # Row 4 (image display area) expands
        self.master.columnconfigure(0, weight=1)  # Column 0 expands

        # Mode selection (CAMERA or IMAGE)
        self.mode = tk.StringVar(value="CAMERA")
        mode_frame = ttk.LabelFrame(master, text="Mode")
        mode_frame.grid(row=0, column=0, padx=10, pady=5, sticky="ew")

        # Radiobuttons to select mode
        ttk.Radiobutton(mode_frame, text="CAMERA", variable=self.mode, value="CAMERA",
                        command=self.update_path_state).pack(side=tk.LEFT, padx=5, pady=5)
        ttk.Radiobutton(mode_frame, text="IMAGE", variable=self.mode, value="IMAGE",
                        command=self.update_path_state).pack(side=tk.LEFT, padx=5, pady=5)

        # Image path widgets (only shown in IMAGE mode)
        self.image_path = tk.StringVar()
        self.path_frame = ttk.LabelFrame(master, text="Image Path")
        self.path_entry = ttk.Entry(self.path_frame, textvariable=self.image_path)
        self.path_entry.pack(side=tk.LEFT, expand=True, fill="x", padx=5, pady=5)
        self.browse_button = ttk.Button(self.path_frame, text="Browse", command=self.browse_image)
        self.browse_button.pack(side=tk.LEFT, padx=5, pady=5)

        # Start and Stop buttons
        button_frame = ttk.Frame(master)
        button_frame.grid(row=2, column=0, padx=10, pady=5, sticky="ew")
        self.start_button = ttk.Button(button_frame, text="Start Detection", command=self.start_detection)
        self.start_button.pack(side=tk.LEFT, padx=5)
        self.stop_button = ttk.Button(button_frame, text="Stop Detection", command=self.stop_detection,
                                      state=tk.DISABLED)
        self.stop_button.pack(side=tk.LEFT, padx=5)

        # Status label
        self.status_label = ttk.Label(master, text="Status: Ready")
        self.status_label.grid(row=3, column=0, padx=10, pady=5, sticky="ew")

        # Frame to display images
        self.image_frame = ttk.Frame(master)
        self.image_frame.grid(row=4, column=0, sticky="nsew")
        self.image_frame.rowconfigure(0, weight=1)
        self.image_frame.columnconfigure(0, weight=1)

        # Canvas to display images
        self.canvas = tk.Canvas(self.image_frame, bg="grey")
        self.canvas.grid(row=0, column=0, sticky="nsew")

        # Add scrollbars to the canvas
        self.v_scrollbar = ttk.Scrollbar(self.image_frame, orient=tk.VERTICAL, command=self.canvas.yview)
        self.v_scrollbar.grid(row=0, column=1, sticky='ns')
        self.h_scrollbar = ttk.Scrollbar(self.image_frame, orient=tk.HORIZONTAL, command=self.canvas.xview)
        self.h_scrollbar.grid(row=1, column=0, sticky='ew')
        self.canvas.configure(yscrollcommand=self.v_scrollbar.set, xscrollcommand=self.h_scrollbar.set)

        self.detection_thread = None
        self.running = False

        # Initialize the state of path widgets
        self.update_path_state()

        # Initialize variable to store the original image
        self.original_img_pil = None

        # Bind the configure event to handle window resizing
        self.master.bind('<Configure>', self.on_window_resize)

    def update_path_state(self):
        mode = self.mode.get()
        if mode == "IMAGE":
            # Show the path widgets
            self.path_frame.grid(row=1, column=0, padx=10, pady=5, sticky="ew")
            self.path_frame.columnconfigure(0, weight=1)
        else:
            # Hide the path widgets and clear the path
            self.path_frame.grid_remove()
            self.image_path.set("")

    def browse_image(self):
        filetypes = (('Image files', '*.png;*.jpg;*.jpeg;*.bmp;*.tiff;*.gif'),
                     ('All files', '*.*'))
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
                self.update_status("Status: Please provide a valid image path.")
                self.running = False
                self.master.after(0, self.start_button.config, {'state': tk.NORMAL})
                self.master.after(0, self.stop_button.config, {'state': tk.DISABLED})
                return
        self.running = False
        self.master.after(0, self.start_button.config, {'state': tk.NORMAL})
        self.master.after(0, self.stop_button.config, {'state': tk.DISABLED})

    def detect_from_camera(self):
        try:
            cap = cv2.VideoCapture(0)
            if not cap.isOpened():
                self.update_status("Error: Cannot open camera.")
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

                # Schedule GUI update in the main thread
                self.master.after(0, self.show_image_in_gui, img)

            cap.release()
            if self.running:
                self.update_status("Status: Camera detection completed.")
            else:
                self.update_status("Status: Camera detection stopped.")
        except Exception as e:
            self.update_status(f"Error: {e}")
            self.running = False

    def detect_from_image(self, image_path):
        try:
            if not os.path.isfile(image_path):
                self.update_status(f"Error: File {image_path} does not exist.")
                self.running = False
                return

            img = cv2.imread(image_path)
            if img is None:
                self.update_status(f"Error: Cannot load image from {image_path}")
                self.running = False
                return

            # Perform shape detection and recognition
            searching_for_shapes = Detection.shape_detection(img)
            Detection.shape_recognition(searching_for_shapes, img)

            # Resize image
            img = PictureModifications.resize_the_picture(img)

            # Schedule GUI update in the main thread
            self.master.after(0, self.show_image_in_gui, img)

            self.update_status("Status: Image detection completed.")
        except Exception as e:
            self.update_status(f"Error: {e}")
            self.running = False

    def show_image_in_gui(self, img):
        # Convert image to RGB and then to PIL format
        img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        self.original_img_pil = Image.fromarray(img_rgb)

        # Resize and display the image
        self.update_displayed_image()

    def update_displayed_image(self):
        if self.original_img_pil is None:
            return

        # Get canvas size
        canvas_width = self.canvas.winfo_width()
        canvas_height = self.canvas.winfo_height()

        if canvas_width <= 1 or canvas_height <= 1:
            # Canvas not yet properly sized
            self.master.after(100, self.update_displayed_image)
            return

        # Resize image while maintaining aspect ratio
        img_width, img_height = self.original_img_pil.size
        ratio = min(canvas_width / img_width, canvas_height / img_height)
        new_size = (int(img_width * ratio), int(img_height * ratio))

        resized_img = self.original_img_pil.resize(new_size, Image.ANTIALIAS)

        # Convert to PhotoImage and display
        self.img_tk = ImageTk.PhotoImage(resized_img)
        self.canvas.delete("all")
        self.canvas.create_image(0, 0, anchor=tk.NW, image=self.img_tk)
        self.canvas.config(scrollregion=self.canvas.bbox(tk.ALL))

    def on_window_resize(self, event):
        # Update the displayed image when the window is resized
        self.update_displayed_image()

    def update_status(self, message):
        # Schedule status update in the main thread
        self.master.after(0, self.status_label.config, {'text': message})

if __name__ == "__main__":
    root = tk.Tk()
    app = ObjectPatternRecognizerGUI(root)
    root.mainloop()
