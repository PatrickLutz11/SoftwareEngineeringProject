# src/controller.py

import os
import threading
from typing import Callable, Optional

import cv2

from Detection import Detection
from PictureModifications import PictureModifications


class DetectionController:
    """Controller for managing image and camera detection."""

    def __init__(
        self,
        mode,
        image_path,
        show_image_callback: Callable[[any], None],
        update_status_callback: Callable[[str], None],
    ) -> None:
        """
        Initializes the controller.

        Args:
            mode: Current mode with a `get()` method that returns "CAMERA" or "IMAGE".
            image_path: Object with a `get()` method that returns the path to the image file (only in IMAGE mode).
            show_image_callback: Callback function to display the image.
            update_status_callback: Callback function to update the status.
        """
        self.mode = mode
        self.image_path = image_path
        self.show_image_callback = show_image_callback
        self.update_status_callback = update_status_callback
        self.running = False
        self.detection_thread: Optional[threading.Thread] = None

    def start_detection(self) -> None:
        """Starts object detection in a separate thread."""
        if not self.running:
            self.running = True
            self.update_status_callback("Status: Detection running...")
            self.detection_thread = threading.Thread(
                target=self.run_detection, daemon=True
            )
            self.detection_thread.start()

    def stop_detection(self) -> None:
        """Stops the ongoing object detection."""
        if self.running:
            self.running = False
            self.update_status_callback("Status: Stopping detection...")

    def run_detection(self) -> None:
        """Performs object detection based on the current mode."""
        try:
            current_mode = self.mode.get()
            if current_mode == "CAMERA":
                self.detect_from_camera()
            elif current_mode == "IMAGE":
                image_path = self.image_path.get()
                if image_path:
                    self.detect_from_image(image_path)
                else:
                    self.update_status_callback(
                        "Status: Please provide a valid image path."
                    )
                    self.running = False
            else:
                self.update_status_callback(
                    f"Status: Unknown mode '{current_mode}'."
                )
        except Exception as e:
            self.update_status_callback(f"Error: {e}")
        finally:
            self.running = False
            self.update_status_callback("Status: Detection stopped.")

    def detect_from_camera(self) -> None:
        """Performs object detection using the camera."""
        cap = cv2.VideoCapture(0)
        if not cap.isOpened():
            self.update_status_callback("Error: Cannot open camera.")
            self.running = False
            return

        self.update_status_callback("Status: Camera detection started.")
        while self.running:
            ret, img = cap.read()
            if not ret:
                self.update_status_callback("Error: No frame received from camera.")
                break

            # Perform shape detection and recognition
            searching_for_shapes = Detection.shape_detection(img)
            Detection.shape_recognition(searching_for_shapes, img)

            # Resize image
            img = PictureModifications.resize_the_picture(img)

            # Update the GUI with the processed image
            self.show_image_callback(img)

        cap.release()
        if self.running:
            self.update_status_callback("Status: Camera detection completed.")
        else:
            self.update_status_callback("Status: Camera detection stopped.")

    def detect_from_image(self, image_path: str) -> None:
        """Performs object detection on a static image.

        Args:
            image_path: Path to the image file.
        """
        if not os.path.isfile(image_path):
            self.update_status_callback(
                f"Error: File {image_path} does not exist."
            )
            return

        img = cv2.imread(image_path)
        if img is None:
            self.update_status_callback(
                f"Error: Cannot load image from {image_path}"
            )
            return

        # Perform shape detection and recognition
        searching_for_shapes = Detection.shape_detection(img)
        Detection.shape_recognition(searching_for_shapes, img)

        # Resize image
        img = PictureModifications.resize_the_picture(img)

        # Update the GUI with the processed image
        self.show_image_callback(img)

        self.update_status_callback("Status: Image detection completed.")
