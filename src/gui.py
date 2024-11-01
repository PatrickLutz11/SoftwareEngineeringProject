# src/gui.py

import os
import sys
import tkinter as tk
from tkinter import filedialog, ttk
from typing import Optional

import cv2

from PIL import Image, ImageTk

from controller import DetectionController


class ObjectPatternRecognizerGUI:
    """GUI for the Object Pattern Recognizer application."""

    def __init__(self, master: tk.Tk) -> None:
        """
        Initializes the GUI components.

        Args:
            master: The root Tkinter window.
        """
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
        ttk.Radiobutton(
            mode_frame,
            text="CAMERA",
            variable=self.mode,
            value="CAMERA",
            command=self.update_path_state
        ).pack(side=tk.LEFT, padx=5, pady=5)
        ttk.Radiobutton(
            mode_frame,
            text="IMAGE",
            variable=self.mode,
            value="IMAGE",
            command=self.update_path_state
        ).pack(side=tk.LEFT, padx=5, pady=5)

        # Image path widgets (only shown in IMAGE mode)
        self.image_path = tk.StringVar()
        self.path_frame = ttk.LabelFrame(master, text="Image Path")
        self.path_entry = ttk.Entry(
            self.path_frame, textvariable=self.image_path
        )
        self.path_entry.pack(side=tk.LEFT, expand=True, fill="x", padx=5, pady=5)
        self.browse_button = ttk.Button(
            self.path_frame, text="Browse", command=self.browse_image
        )
        self.browse_button.pack(side=tk.LEFT, padx=5, pady=5)

        # Start and Stop buttons
        button_frame = ttk.Frame(master)
        button_frame.grid(row=2, column=0, padx=10, pady=5, sticky="ew")
        self.start_button = ttk.Button(
            button_frame, text="Start Detection", command=self.start_detection
        )
        self.start_button.pack(side=tk.LEFT, padx=5)
        self.stop_button = ttk.Button(
            button_frame,
            text="Stop Detection",
            command=self.stop_detection,
            state=tk.DISABLED
        )
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
        self.v_scrollbar = ttk.Scrollbar(
            self.image_frame, orient=tk.VERTICAL, command=self.canvas.yview
        )
        self.v_scrollbar.grid(row=0, column=1, sticky='ns')
        self.h_scrollbar = ttk.Scrollbar(
            self.image_frame, orient=tk.HORIZONTAL, command=self.canvas.xview
        )
        self.h_scrollbar.grid(row=1, column=0, sticky='ew')
        self.canvas.configure(
            yscrollcommand=self.v_scrollbar.set, xscrollcommand=self.h_scrollbar.set
        )

        self.controller: Optional[DetectionController] = None
        self.original_img_pil: Optional[Image.Image] = None

        # Initialize the state of path widgets
        self.update_path_state()

        # Bind the configure event to handle window resizing
        self.master.bind('<Configure>', self.on_window_resize)

    def update_path_state(self) -> None:
        """Updates the visibility of the image path widgets based on the selected mode."""
        mode = self.mode.get()
        if mode == "IMAGE":
            # Show the path widgets
            self.path_frame.grid(row=1, column=0, padx=10, pady=5, sticky="ew")
            self.path_frame.columnconfigure(0, weight=1)
        else:
            # Hide the path widgets and clear the path
            self.path_frame.grid_remove()
            self.image_path.set("")

    def browse_image(self) -> None:
        """Opens a file dialog to select an image and updates the image path."""
        filetypes = (
            ('Image files', '*.png;*.jpg;*.jpeg;*.bmp;*.tiff;*.gif'),
            ('All files', '*.*')
        )
        filepath = filedialog.askopenfilename(
            title='Select Image', filetypes=filetypes
        )
        if filepath:
            self.image_path.set(filepath)

    def start_detection(self) -> None:
        """Starts the object detection process."""
        if not self.controller or not self.controller.running:
            # Initialize the controller
            self.controller = DetectionController(
                mode=self.mode,
                image_path=self.image_path,
                show_image_callback=self.show_image_in_gui,
                update_status_callback=self.update_status
            )
            self.controller.start_detection()
            self.start_button.config(state=tk.DISABLED)
            self.stop_button.config(state=tk.NORMAL)

    def stop_detection(self) -> None:
        """Stops the ongoing object detection process."""
        if self.controller and self.controller.running:
            self.controller.stop_detection()
            self.stop_button.config(state=tk.DISABLED)

    def show_image_in_gui(self, img: any) -> None:
        """
        Converts the processed image and displays it in the GUI.

        Args:
            img: The processed image in BGR format.
        """
        # Convert image from BGR to RGB and then to PIL format
        img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        self.original_img_pil = Image.fromarray(img_rgb)

        # Resize and display the image
        self.update_displayed_image()

    def update_displayed_image(self) -> None:
        """Resizes and updates the image displayed on the canvas."""
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

    def on_window_resize(self, event: tk.Event) -> None:
        """Handles window resize events to update the displayed image."""
        self.update_displayed_image()

    def update_status(self, message: str) -> None:
        """
        Updates the status label with the provided message.

        Args:
            message: The status message to display.
        """
        self.status_label.config(text=message)


def main() -> None:
    """Entry point for the GUI application."""
    root = tk.Tk()
    app = ObjectPatternRecognizerGUI(master=root)
    root.mainloop()


if __name__ == "__main__":
    main()
