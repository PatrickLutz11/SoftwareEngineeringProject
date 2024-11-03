"""GUI module for the Object Pattern Recognizer application."""


import tkinter as tk
from tkinter import filedialog, ttk
from typing import Any, List, Optional, Tuple

import cv2
from PIL import Image, ImageTk

from controller import DetectionController
from handling_configurations import ConfigReader, ConfigWriter


class ObjectPatternRecognizerGUI:
    """GUI class for the Object Pattern Recognizer application.

    This class implements the graphical user interface for the object pattern
    recognition application. It provides controls for switching between camera and
    image modes, starting/stopping detection, and displaying detected patterns.

    Attributes:
        master: The root tkinter window.
        mode: StringVar controlling camera/image mode selection.
        image_path: StringVar storing the selected image folder path.
        controller: DetectionController instance managing the detection process.
        original_img_pil_list: List of processed images and their paths.
        current_image_index: Index of currently displayed image.
    """

    def __init__(self, master: tk.Tk) -> None:
        """_summary_

        Args:
            master (tk.Tk): _description_
        """
        """Initialize the GUI."""
        self.master = master
        self.master.title("Object Pattern Recognizer")

        # Configure grid layout
        self.master.rowconfigure(5, weight=1)  # Image frame gets all extra space
        self.master.columnconfigure(0, weight=1)

        # Initialize config handling
        self.config_reader = ConfigReader("config.json")
        self.config_writer = ConfigWriter("config.json")

        # Initialize instance variables
        self.mode = tk.StringVar(value="CAMERA")
        self.image_path = tk.StringVar()

        # Load last path if exists
        last_path = self.config_reader.get_value('last_image_folder_path', "")
        if last_path:
            self.mode.set("IMAGE")
            self.image_path.set(last_path)

        self.original_img_pil_list: List[Tuple[Image.Image, str]] = []
        self.current_image_index: int = 0
        self.img_tk: Optional[ImageTk.PhotoImage] = None
        self.image_names: List[str] = []  # Liste für Bildnamen

        # Create UI elements
        self._create_mode_frame()
        self._create_path_frame()
        self._create_control_frame()
        self._create_status_label()
        self._create_image_frame()

        # Initialize controller
        self.controller = DetectionController(
            mode=self.mode,
            image_path=self.image_path,
            show_image_callback=self.collect_images,
            update_status_callback=self.update_status
        )

        # Initialize widget states
        self.update_button_state()

        # Bind window resize event
        self.master.bind('<Configure>', self.on_window_resize)

    def _create_mode_frame(self) -> None:
        """Create the mode selection frame."""
        mode_frame = ttk.LabelFrame(self.master, text="Mode")
        mode_frame.grid(row=0, column=0, padx=10, pady=5, sticky="ew")

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

    def _create_path_frame(self) -> None:
        """Create the image path selection frame."""
        self.path_frame = ttk.LabelFrame(self.master, text="Image Path")
        self.path_entry = ttk.Entry(
            self.path_frame,
            textvariable=self.image_path
        )
        self.path_entry.pack(side=tk.LEFT, expand=True, fill="x", padx=5, pady=5)

        self.browse_button = ttk.Button(
            self.path_frame,
            text="Browse",
            command=self.browse_image
        )
        self.browse_button.pack(side=tk.LEFT, padx=5, pady=5)

    def _create_control_frame(self) -> None:
        """Create the frame containing the start/stop button."""
        control_frame = ttk.Frame(self.master)
        control_frame.grid(row=2, column=0, padx=10, pady=5, sticky="ew")

        self.toggle_button = ttk.Button(
            control_frame,
            text="Start Detection",
            command=self.toggle_detection
        )
        self.toggle_button.pack(side=tk.LEFT, padx=5)

    def _create_status_label(self) -> None:
        """Create the status label."""
        self.status_label = ttk.Label(
            self.master,
            text="Status: Ready"
        )
        self.status_label.grid(
            row=4,
            column=0,
            padx=10,
            pady=5,
            sticky="ew"
        )

    def _create_image_frame(self) -> None:
        """Create the frame for displaying images."""
        # Main container for image and navigation
        main_container = ttk.Frame(self.master)
        main_container.grid(row=5, column=0, sticky="nsew")
        main_container.rowconfigure(0, weight=1)
        main_container.columnconfigure(0, weight=1)

        # Image frame (gets all extra space)
        self.image_frame = ttk.Frame(main_container)
        self.image_frame.grid(row=0, column=0, sticky="nsew")
        self.image_frame.rowconfigure(0, weight=1)
        self.image_frame.columnconfigure(0, weight=1)

        # Create canvas and scrollbars
        self.canvas = tk.Canvas(self.image_frame, bg="grey")
        self.canvas.grid(row=0, column=0, sticky="nsew")

        self.v_scrollbar = ttk.Scrollbar(
            self.image_frame,
            orient=tk.VERTICAL,
            command=self.canvas.yview
        )
        self.v_scrollbar.grid(row=0, column=1, sticky='ns')

        self.h_scrollbar = ttk.Scrollbar(
            self.image_frame,
            orient=tk.HORIZONTAL,
            command=self.canvas.xview
        )
        self.h_scrollbar.grid(row=1, column=0, sticky='ew')

        self.canvas.configure(
            yscrollcommand=self.v_scrollbar.set,
            xscrollcommand=self.h_scrollbar.set
        )

        # Navigation frame (fixed at bottom)
        self.navigation_frame = ttk.Frame(main_container)
        self.navigation_frame.grid(row=1, column=0, sticky="ew", pady=5)
        self.navigation_frame.grid_remove()  # Initially hidden

        # Create button frame inside navigation frame
        button_frame = ttk.Frame(self.navigation_frame)
        button_frame.pack(fill="x", pady=5)

        # Add Previous and Next buttons with image label between them
        self.prev_button = ttk.Button(
            button_frame,
            text="Previous",
            command=self.show_previous_image
        )
        self.prev_button.pack(side=tk.LEFT, padx=5)

        self.image_name_label = ttk.Label(
            button_frame,
            text="",
            anchor="center"
        )
        self.image_name_label.pack(side=tk.LEFT, expand=True)

        self.next_button = ttk.Button(
            button_frame,
            text="Next",
            command=self.show_next_image
        )
        self.next_button.pack(side=tk.LEFT, padx=5)

        # Create slider frame inside navigation frame
        slider_frame = ttk.Frame(self.navigation_frame)
        slider_frame.pack(fill="x", pady=5)

        self.image_slider = ttk.Scale(
            slider_frame,
            from_=0,
            to=0,
            orient=tk.HORIZONTAL,
            command=self.on_slider_change
        )
        self.image_slider.pack(fill="x", padx=5)

    def update_button_state(self) -> None:
        """Update widget states based on current mode."""
        if self.mode.get() == "IMAGE":
            self.path_frame.grid(row=1, column=0, padx=10, pady=5, sticky="ew")
            self.path_frame.columnconfigure(0, weight=1)
        else:
            self.path_frame.grid_remove()

        self.toggle_button.config(text="Start Detection")
        self.toggle_button.state(['!disabled'])

    def browse_image(self) -> None:
        """Open file dialog for selecting image folder and save the path."""
        filepath = filedialog.askdirectory(title='Select Image Folder')
        if filepath:
            self.image_path.set(filepath)
            # Save the path directly in GUI
            self.config_writer.save_value('last_image_folder_path', filepath)

    def toggle_detection(self) -> None:
        """Toggle detection process on/off."""
        if not self.controller.running:
            self.start_detection()
        else:
            self.stop_detection()

    def start_detection(self) -> None:
        """Start the detection process."""
        if self.mode.get() == "IMAGE" and not self.image_path.get():
            self.update_status("Please select an image folder.")
            return

        # Reset GUI state
        self.original_img_pil_list.clear()
        self.current_image_index = 0
        self.canvas.delete("all")
        self.image_name_label.config(text="")
        self.navigation_frame.grid_remove()

        # Start detection with controller
        self.controller.start_detection()
        
        # Get image names if in IMAGE mode
        if self.mode.get() == "IMAGE":
            self.image_names = self.controller.get_image_names()

        # Update button states
        self.toggle_button.config(text="Stop Detection")
        if self.mode.get() == "IMAGE":
            self.toggle_button.state(['disabled'])

    def stop_detection(self) -> None:
        """Stop the detection process."""
        if self.controller and self.controller.running:
            self.controller.stop_detection()
            self.toggle_button.config(text="Start Detection")
            self.toggle_button.state(['!disabled'])

    def collect_images(self, img: cv2.typing.MatLike, image_path: str = "") -> None:
        """_summary_

        Args:
            img (cv2.typing.MatLike): _description_
            image_path (str, optional): _description_. Defaults to "".
        """
        """Queue image collection for GUI thread.

        Args:
            img: The image to be collected.
            image_path: Path of the image file.
        """
        self.master.after(0, self._collect_images, img, image_path)

    def _collect_images(self, img: cv2.typing.MatLike, image_path: str = "") -> None:
        """_summary_

        Args:
            img (cv2.typing.MatLike): _description_
            image_path (str, optional): _description_. Defaults to "".
        """
        """Process and store collected images.

        Args:
            img: The image to be processed.
            image_path: Path of the image file.
        """
        try:
            img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
            pil_image = Image.fromarray(img_rgb)

            # Speichere das Bild mit seinem Namen
            self.original_img_pil_list.append((pil_image, image_path))

            # Show navigation frame if we have images
            if len(self.original_img_pil_list) > 0:
                self.navigation_frame.grid()

            # Update the slider range
            self.image_slider.config(to=len(self.original_img_pil_list) - 1)

            # Update display for first image or if viewing latest
            if (len(self.original_img_pil_list) == 1 or
                self.current_image_index == len(self.original_img_pil_list) - 2):
                self.current_image_index = len(self.original_img_pil_list) - 1
                self.update_displayed_image()

        except Exception as e:
            self.update_status(f"Error in collect_images: {e}")
            print(f"Error in collect_images: {e}")

    def on_slider_change(self, event: Any) -> None:
        """_summary_

        Args:
            event (Any): _description_
        """
        """Handle slider value changes."""
        new_index = int(float(self.image_slider.get()))
        if new_index != self.current_image_index:
            self.current_image_index = new_index
            self.update_displayed_image()

    def show_previous_image(self) -> None:
        """Display the previous image in the list."""
        if self.current_image_index > 0:
            self.current_image_index -= 1
            self.update_displayed_image()

    def show_next_image(self) -> None:
        """Display the next image in the list."""
        if self.current_image_index < len(self.original_img_pil_list) - 1:
            self.current_image_index += 1
            self.update_displayed_image()

    def update_displayed_image(self) -> None:
        """Update the image display and counter."""
        if not self.original_img_pil_list:
            return
        if self.current_image_index >= len(self.original_img_pil_list):
            return
    
        image_to_show, image_name = self.original_img_pil_list[
            self.current_image_index
        ]
        total_images = len(self.original_img_pil_list)
    
        # Update image name and counter with both number and name
        if self.mode.get() == "IMAGE":
            counter_text = (f"Image {self.current_image_index + 1}/{total_images}"
                           f" - {image_name}")
        else:
            counter_text = f"Frame {self.current_image_index + 1}"
            
        self.image_name_label.config(text=counter_text)
    
        # Check canvas initialization
        canvas_width = self.canvas.winfo_width()
        canvas_height = self.canvas.winfo_height()
        if canvas_width <= 1 or canvas_height <= 1:
            self.master.after(100, self.update_displayed_image)
            return
    
        # Calculate new image size
        img_width, img_height = image_to_show.size
        ratio = min(canvas_width / img_width, canvas_height / img_height)
        new_size = (int(img_width * ratio), int(img_height * ratio))
    
        # Update canvas with resized image
        resized_img = image_to_show.resize(new_size, Image.Resampling.LANCZOS)
        self.img_tk = ImageTk.PhotoImage(resized_img)
        self.canvas.delete("all")
        self.canvas.create_image(
            canvas_width//2,
            canvas_height//2,
            image=self.img_tk,
            anchor="center"
        )
        self.canvas.config(scrollregion=self.canvas.bbox(tk.ALL))
    
        # Update the slider value
        self.image_slider.set(self.current_image_index)

    def on_window_resize(self, event: tk.Event) -> None:
        """_summary_

        Args:
            event (tk.Event): _description_
        """
        """Handle window resize events.

        Args:
            event: The resize event.
        """
        self.update_displayed_image()

    def update_status(self, message: str) -> None:
        """_summary_

        Args:
            message (str): _description_
        """
        """Update the status label text.

        Args:
            message: The status message to display.
        """
        self.status_label.config(text=message)

        # Re-enable toggle button when detection is completed or stopped
        if any(keyword in message.lower() for keyword in ["completed", "stopped"]):
            self.toggle_button.config(text="Start Detection")
            self.toggle_button.state(['!disabled'])


if __name__ == "__main__":
    root = tk.Tk()
    app = ObjectPatternRecognizerGUI(master=root)
    root.mainloop()