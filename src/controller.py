# src/controller.py

import os
import threading
from typing import Callable, Optional, Any, Dict

import cv2

from Detection import Detection
from PictureModifications import PictureModifications
from logger import Log  # Import the Log class from logger.py


class DetectionController:
    """Controller for managing image and camera detection."""

    def __init__(
        self,
        mode,
        image_path,
        show_image_callback: Callable[[Any], None],
        update_status_callback: Callable[[str], None],
        log_file_path: str = 'log.csv'  # Default path for the log file
    ) -> None:
        """
        Initializes the controller.

        Args:
            mode: Current mode with a `get()` method that returns "CAMERA" or "IMAGE".
            image_path: Object with a `get()` method that returns the path to the image file (only in IMAGE mode).
            show_image_callback: Callback function to display the image.
            update_status_callback: Callback function to update the status.
            log_file_path: Path to the CSV log file. Defaults to 'log.csv'.
        """
        self.mode = mode
        self.image_path = image_path
        self.show_image_callback = show_image_callback
        self.update_status_callback = update_status_callback
        self.running = False
        self.detection_thread: Optional[threading.Thread] = None
        self.logger = Log(file_path=log_file_path)  # Initialize the logger
        print(f"Logger initialized with file path: {log_file_path}")

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
            print(f"Current mode: {current_mode}")
            if current_mode == "CAMERA":
                self.detect_from_camera()
            elif current_mode == "IMAGE":
                image_path = self.image_path.get()
                print(f"Image path: {image_path}")
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
            print(f"Error in run_detection: {e}")
        finally:
            self.running = False
            self.update_status_callback("Status: Detection stopped.")

    def detect_from_camera(self) -> None:
        """Performs object detection using the camera."""
        cap = cv2.VideoCapture(0)
        if not cap.isOpened():
            self.update_status_callback("Error: Cannot open camera.")
            print("Error: Cannot open camera.")
            self.running = False
            return

        self.update_status_callback("Status: Camera detection started.")
        frame_count = 0  # To keep track of frame numbers
        while self.running:
            ret, img = cap.read()
            if not ret:
                self.update_status_callback("Error: No frame received from camera.")
                print("Error: No frame received from camera.")
                break

            frame_count += 1

            # Perform shape detection and recognition
            searching_for_shapes = Detection.shape_detection(img)
            recognized_shapes = Detection.shape_recognition(searching_for_shapes, img)
            print(f"Frame {frame_count}: Recognized shapes: {recognized_shapes}")

            # Resize image
            img = PictureModifications.resize_the_picture(img)

            # Update the GUI with the processed image
            self.show_image_callback(img)

            # Log each recognized shape
            for shape in recognized_shapes:
                try:
                    pattern = shape.get('pattern', 'Unknown')
                    color = shape.get('color', 'Unknown')
                    confidence = shape.get('confidence', 'N/A')
                    print(f"Logging - Pattern: {pattern}, Color: {color}, Confidence: {confidence}")
                    self.logger.log_data(
                        pattern=pattern,
                        color=color,
                        frame=frame_count,  # For camera mode
                        confidence=confidence
                    )
                except PermissionError as e:
                    self.update_status_callback(f"Logging Error: {e}")
                    print(f"Logging Error: {e}")
                except Exception as e:
                    self.update_status_callback(f"Unexpected Logging Error: {e}")
                    print(f"Unexpected Logging Error: {e}")

        cap.release()
        if self.running:
            self.update_status_callback("Status: Camera detection completed.")
            print("Status: Camera detection completed.")
        else:
            self.update_status_callback("Status: Camera detection stopped.")
            print("Status: Camera detection stopped.")

    def detect_from_image(self, image_path: str) -> None:
        """Performs object detection on a static image.

        Args:
            image_path: Path to the image file.
        """
        if not os.path.isfile(image_path):
            self.update_status_callback(
                f"Error: File {image_path} does not exist."
            )
            print(f"Error: File {image_path} does not exist.")
            return

        img = cv2.imread(image_path)
        if img is None:
            self.update_status_callback(
                f"Error: Cannot load image from {image_path}"
            )
            print(f"Error: Cannot load image from {image_path}")
            return

        # Perform shape detection and recognition
        searching_for_shapes = Detection.shape_detection(img)
        recognized_shapes = Detection.shape_recognition(searching_for_shapes, img)
        print(f"Recognized shapes in image: {recognized_shapes}")

        # Resize image
        img = PictureModifications.resize_the_picture(img)

        # Update the GUI with the processed image
        self.show_image_callback(img)

        # Log each recognized shape
        for shape in recognized_shapes:
            try:
                pattern = shape.get('pattern', 'Unknown')
                color = shape.get('color', 'Unknown')
                confidence = shape.get('confidence', 'N/A')
                print(f"Logging - Pattern: {pattern}, Color: {color}, Confidence: {confidence}")
                self.logger.log_data(
                    pattern=pattern,
                    color=color,
                    image_path=image_path,  # For image mode
                    confidence=confidence
                )
            except PermissionError as e:
                self.update_status_callback(f"Logging Error: {e}")
                print(f"Logging Error: {e}")
            except Exception as e:
                self.update_status_callback(f"Unexpected Logging Error: {e}")
                print(f"Unexpected Logging Error: {e}")

        self.update_status_callback("Status: Image detection completed.")
        print("Status: Image detection completed.")
