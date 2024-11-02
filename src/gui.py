import os
import tkinter as tk
from tkinter import filedialog, ttk
from typing import Any, Optional, List, Tuple

import cv2
from PIL import Image, ImageTk

from controller import DetectionController


class ObjectPatternRecognizerGUI:
    """GUI for the Object Pattern Recognizer application."""

    def __init__(self, master: tk.Tk) -> None:
        self.master = master
        self.master.title("Object Pattern Recognizer")

        # Configure grid layout
        self.master.rowconfigure(5, weight=1)
        self.master.columnconfigure(0, weight=1)

        # Mode selection (CAMERA or IMAGE)
        self.mode = tk.StringVar(value="CAMERA")
        mode_frame = ttk.LabelFrame(master, text="Mode")
        mode_frame.grid(row=0, column=0, padx=10, pady=5, sticky="ew")

        # Radiobuttons to select mode
        ttk.Radiobutton(
            mode_frame,
            text="CAMERA",
            variable=self.mode,
            value="CAMERA",
            command=self.update_button_state
        ).pack(side=tk.LEFT, padx=5, pady=5)
        ttk.Radiobutton(
            mode_frame,
            text="IMAGE",
            variable=self.mode,
            value="IMAGE",
            command=self.update_button_state
        ).pack(side=tk.LEFT, padx=5, pady=5)

        # Image path widgets (only shown in IMAGE mode)
        self.image_path = tk.StringVar()
        self.path_frame = ttk.LabelFrame(master, text="Image Path")
        self.path_entry = ttk.Entry(self.path_frame, textvariable=self.image_path)
        self.path_entry.pack(side=tk.LEFT, expand=True, fill="x", padx=5, pady=5)
        self.browse_button = ttk.Button(self.path_frame, text="Browse", command=self.browse_image)
        self.browse_button.pack(side=tk.LEFT, padx=5, pady=5)

        # Buttons
        button_frame = ttk.Frame(master)
        button_frame.grid(row=2, column=0, padx=10, pady=5, sticky="ew")
        self.toggle_button = ttk.Button(button_frame, text="Start Detection", command=self.toggle_detection)
        self.toggle_button.pack(side=tk.LEFT, padx=5)

        # Navigation buttons (initially hidden)
        self.prev_button = ttk.Button(button_frame, text="Previous", command=self.show_previous_image)
        self.next_button = ttk.Button(button_frame, text="Next", command=self.show_next_image)
        self.prev_button.pack(side=tk.LEFT, padx=5)
        self.next_button.pack(side=tk.LEFT, padx=5)
        self.prev_button.pack_forget()
        self.next_button.pack_forget()

        # Image name label
        self.image_name_label = ttk.Label(master, text="", anchor="center")
        self.image_name_label.grid(row=3, column=0, padx=10, pady=5, sticky="ew")

        # Status label
        self.status_label = ttk.Label(master, text="Status: Ready")
        self.status_label.grid(row=4, column=0, padx=10, pady=5, sticky="ew")

        # Frame to display images
        self.image_frame = ttk.Frame(master)
        self.image_frame.grid(row=5, column=0, sticky="nsew")
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

        self.controller: Optional[DetectionController] = None
        self.original_img_pil_list: List[Tuple[Image.Image, str]] = []
        self.current_image_index: int = 0

        # Initialize the state of path widgets
        self.update_button_state()

        # Bind the configure event to handle window resizing
        self.master.bind('<Configure>', self.on_window_resize)

    def update_button_state(self) -> None:
        """Updates the state of the toggle button and image path widgets based on the selected mode."""
        if self.mode.get() == "IMAGE":
            self.path_frame.grid(row=1, column=0, padx=10, pady=5, sticky="ew")
            self.path_frame.columnconfigure(0, weight=1)
            self.toggle_button.config(text="Start Detection")
            self.toggle_button.state(['!disabled'])
        else:
            self.path_frame.grid_remove()
            self.image_path.set("")
            self.toggle_button.config(text="Start Detection")
            self.toggle_button.state(['!disabled'])

    def browse_image(self) -> None:
        """Opens a dialog to browse and select an image folder."""
        filepath = filedialog.askdirectory(title='Select Image Folder')
        if filepath:
            self.image_path.set(filepath)

    def toggle_detection(self) -> None:
        """Starts or stops the detection process based on the current state."""
        if not self.controller or not self.controller.running:
            self.start_detection()
        else:
            self.stop_detection()

    def start_detection(self) -> None:
        """Starts the detection process."""
        if self.mode.get() == "IMAGE" and not self.image_path.get():
            self.update_status("Please select an image folder.")
            return

        self.original_img_pil_list.clear()
        self.current_image_index = 0
        self.canvas.delete("all")
        self.image_name_label.config(text="")
        self.prev_button.pack_forget()
        self.next_button.pack_forget()

        self.controller = DetectionController(
            mode=self.mode,
            image_path=self.image_path,
            show_image_callback=self.collect_images,
            update_status_callback=self.update_status
        )
        self.controller.start_detection()

        self.toggle_button.config(text="Stop Detection")
        if self.mode.get() == "IMAGE":
            self.toggle_button.state(['disabled'])

    def stop_detection(self) -> None:
        """Stops the ongoing detection process."""
        if self.controller and self.controller.running:
            self.controller.stop_detection()
            self.toggle_button.config(text="Start Detection")
            self.toggle_button.state(['!disabled'])
            self.controller = None

    def collect_images(self, img: Any, image_path: str = "") -> None:
        """Collects processed images and updates the GUI.

        Args:
            img (Any): The processed image.
            image_path (str, optional): Path to the image. Defaults to "".
        """
        self.master.after(0, self._collect_images, img, image_path)

    def _collect_images(self, img: Any, image_path: str = "") -> None:
        """Handles the collection and display of images in the GUI.

        Args:
            img (Any): The processed image.
            image_path (str, optional): Path to the image. Defaults to "".
        """
        try:
            img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
            pil_image = Image.fromarray(img_rgb)
            self.original_img_pil_list.append((pil_image, image_path))
            if len(self.original_img_pil_list) == 1:
                self.update_displayed_image()

            if len(self.original_img_pil_list) > 1:
                self.prev_button.pack(side=tk.LEFT, padx=5)
                self.next_button.pack(side=tk.LEFT, padx=5)
        except Exception as e:
            self.update_status(f"Error in collect_images: {e}")
            print(f"Error in collect_images: {e}")

    def show_previous_image(self) -> None:
        """Displays the previous image in the list."""
        if self.current_image_index > 0:
            self.current_image_index -= 1
            self.update_displayed_image()

    def show_next_image(self) -> None:
        """Displays the next image in the list."""
        if self.current_image_index < len(self.original_img_pil_list) - 1:
            self.current_image_index += 1
            self.update_displayed_image()

    def update_displayed_image(self) -> None:
        """Updates the image displayed on the canvas."""
        if not self.original_img_pil_list or self.current_image_index >= len(self.original_img_pil_list):
            return

        image_to_show, image_path = self.original_img_pil_list[self.current_image_index]
        image_name = os.path.basename(image_path) if image_path else f"Image {self.current_image_index + 1}"
        self.image_name_label.config(text=f"Current Image: {image_name} ({self.current_image_index + 1}/{len(self.original_img_pil_list)})")

        canvas_width = self.canvas.winfo_width()
        canvas_height = self.canvas.winfo_height()
        if canvas_width <= 1 or canvas_height <= 1:
            self.master.after(100, self.update_displayed_image)
            return

        img_width, img_height = image_to_show.size
        ratio = min(canvas_width / img_width, canvas_height / img_height)
        new_size = (int(img_width * ratio), int(img_height * ratio))

        resized_img = image_to_show.resize(new_size, Image.Resampling.LANCZOS)
        self.img_tk = ImageTk.PhotoImage(resized_img)
        self.canvas.delete("all")
        self.canvas.create_image(0, 0, anchor=tk.NW, image=self.img_tk)
        self.canvas.config(scrollregion=self.canvas.bbox(tk.ALL))

    def on_window_resize(self, event: tk.Event) -> None:
        """Handles window resize events to adjust the displayed image."""
        self.update_displayed_image()

    def update_status(self, message: str) -> None:
        """Updates the status label in the GUI.

        Args:
            message (str): The status message to display.
        """
        self.master.after(0, self.status_label.config, {'text': message})

        # Enable the toggle button when detection is completed or stopped, regardless of mode
        if any(keyword in message.lower() for keyword in ["completed", "stopped"]):
            self.toggle_button.config(text="Start Detection")
            self.toggle_button.state(['!disabled'])


def main() -> None:
    root = tk.Tk()
    app = ObjectPatternRecognizerGUI(master=root)
    root.mainloop()


if __name__ == "__main__":
    main()
