import threading
from typing import Callable, Optional, Any


from detection import Detection
from picture_modifications import PictureModifications
from logger import Log
from data_selector import DataSelector
from data_stream import DataStream


class DetectionController:
    """Controller for managing image and camera detection."""

    def __init__(
        self,
        mode,
        image_path,
        show_image_callback: Callable[[Any], None],
        update_status_callback: Callable[[str], None],
        log_file_path: str = 'log.csv',  # Default path for the log file
        source_type: str = "c"  # Parameter to select data source
    ) -> None:
        """
        Initializes the controller.

        Args:
            mode: Current mode with a `get()` method that returns "CAMERA" or "IMAGE".
            image_path: Object with a `get()` method that returns the path to the folder (only in IMAGE mode).
            show_image_callback: Callback function to display the image.
            update_status_callback: Callback function to update the status.
            log_file_path: Path to the CSV log file. Defaults to 'log.csv'.
            source_type: Type of data source ("c" for camera, "i" for image folder). Defaults to "c".
        """
        self.mode = mode
        self.image_path = image_path
        self.show_image_callback = show_image_callback
        self.update_status_callback = update_status_callback
        self.running = False
        self.detection_thread: Optional[threading.Thread] = None
        self.logger = Log(file_path=log_file_path)  # Initialize the logger

        # Initialize DataSelector based on the initial mode
        current_mode = self.mode.get().upper()
        folder_path = self.image_path.get() if current_mode == "IMAGE" else ""
        self.data_selector = DataSelector(source_type=source_type, folder_path=folder_path)
        print(f"Logger initialized with path: {log_file_path}")
        print(f"DataSelector initialized with source type: {source_type}")

    def start_detection(self) -> None:
        """Starts object detection in a separate thread."""
        if not self.running:
            current_mode = self.mode.get().upper()

            if current_mode in ["CAMERA", "IMAGE"]:
                folder_path = self.image_path.get() if current_mode == "IMAGE" else ""
                success = self.data_selector.select_stream(
                    source_type="i" if current_mode == "IMAGE" else "c",
                    folder_path=folder_path
                )
                if not success:
                    self.update_status_callback("Status: Failed to initialize data source.")
                    return

                stream = self.data_selector.get_stream()
                if not stream:
                    self.update_status_callback("Status: Data source could not be initialized.")
                    return

                if not stream.open_data_stream():
                    self.update_status_callback("Status: Data source could not be opened.")
                    return

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
            stream = self.data_selector.get_stream()
            if stream:
                stream.close_data_stream()

    def run_detection(self) -> None:
        """Performs object detection based on the current mode."""
        try:
            current_mode = self.mode.get().upper()
            print(f"Current mode: {current_mode}")

            if current_mode in ["CAMERA", "IMAGE"]:
                stream = self.data_selector.get_stream()
                if not stream:
                    self.update_status_callback("Status: No valid data source selected.")
                    self.running = False
                    return
                self.detect_from_stream(stream, mode=current_mode)
            else:
                self.update_status_callback(f"Status: Unknown mode '{current_mode}'.")
        except Exception as e:
            self.update_status_callback(f"Error: {e}")
            print(f"Error in run_detection: {e}")
        finally:
            self.running = False
            self.update_status_callback("Status: Detection stopped.")

    def detect_from_stream(self, stream: DataStream, mode: str) -> None:
        """Performs object detection using the selected data stream.

        Args:
            stream (DataStream): The data stream to use.
            mode (str): The current mode ("CAMERA" or "IMAGE").
        """
        self.update_status_callback(f"Status: {mode} detection started.")
        frame_count = 0  # To keep track of frame numbers
        while self.running:
            img = stream.get_current_image()
            if img is None:
                self.update_status_callback("Status: No more images to process.")
                print("Status: No more images to process.")
                break

            frame_count += 1

            # Perform shape detection and recognition
            searching_for_shapes = Detection.shape_detection(img)
            recognized_shapes = Detection.shape_recognition(searching_for_shapes, img)
            print(f"Frame {frame_count}: Recognized shapes: {recognized_shapes}")

            # Resize image for display
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
                    if mode == "CAMERA":
                        self.logger.log_data(
                            pattern=pattern,
                            color=color,
                            frame=frame_count,  # For camera mode
                            confidence=confidence
                        )
                    elif mode == "IMAGE":
                        image_path = stream.get_current_image_path() if hasattr(stream, 'get_current_image_path') else "N/A"
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

            # Update the data stream to the next image
            success = stream.update_data_stream()
            if not success:
                print("Error updating data stream.")
                break

        # Close the data stream after processing all images
        if mode == "IMAGE":
            stream.close_data_stream()

        if self.running:
            self.update_status_callback(f"Status: {mode} detection completed.")
            print(f"Status: {mode} detection completed.")
        else:
            self.update_status_callback(f"Status: {mode} detection stopped.")
            print(f"Status: {mode} detection stopped.")
