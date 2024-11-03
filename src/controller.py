"""Module for managing object detection in camera and image streams."""

import threading
from typing import Any, Callable, Optional, List

from data_selector import DataSelector
from logger import Logger
from modificators_image import PictureModifications
from detection_shape import Detection


class DetectionController:
    """Controls and manages object detection processes for camera and image inputs.

    This class handles the initialization and management of detection processes,
    including thread management and logging of detected objects, interacting with
    streams only through DataSelector.

    Attributes:
        mode: Current detection mode selector (CAMERA/IMAGE).
        image_path: Path to image directory for IMAGE mode.
        show_image_callback: Callback function to display processed images.
        update_status_callback: Callback function to update status messages.
        running: Boolean indicating if detection is currently active.
        detection_thread: Thread object for running detection process.
        stop_event: Threading event to signal detection stopping.
        logger: Logger instance for recording detection results.
        data_selector: Selector for managing different input streams.
    """

    def __init__(
        self,
        mode: Any,
        image_path: Any,
        show_image_callback: Callable[[Any, str], None],
        update_status_callback: Callable[[str], None],
        log_file_path: str = 'log.csv',
        source_type: str = "c"
    ) -> None:
        """Initialize the DetectionController.

        Args:
            mode: Mode selector with get() method returning "CAMERA" or "IMAGE".
            image_path: Object with get() method returning folder path for IMAGE mode.
            show_image_callback: Function to display processed images.
            update_status_callback: Function to update status messages.
            log_file_path: Path to CSV log file. Defaults to 'log.csv'.
            source_type: Type of data source ("c" for camera, "i" for images).
                Defaults to "c".
        """
        self.mode = mode
        self.image_path = image_path
        self.show_image_callback = show_image_callback
        self.update_status_callback = update_status_callback
        self.running = False
        self.detection_thread: Optional[threading.Thread] = None
        self.stop_event = threading.Event()
        self.logger = Logger(base_file_path=log_file_path)
        self.data_selector = None
        
        # Initialize data selector
        self._initialize_data_selector(
            source_type,
            self.image_path.get() if self.mode.get().upper() == "IMAGE" else ""
        )

    def get_image_names(self) -> List[str]:
        """Get names of all available images in the current stream.

        Returns:
            List[str]: List of image names, empty list if not in IMAGE mode
                    or if no stream is available.
        """
        if (self.mode.get().upper() == "IMAGE" and 
            self.data_selector and 
            self.data_selector.get_stream()):
            return self.data_selector.get_stream().get_names_images_list()
        return []

    def _initialize_data_selector(self, source_type: str, folder_path: str = "") -> None:
        """Initialize the DataSelector with given parameters.

        Args:
            source_type: Type of data source ("c" for camera, "i" for images).
            folder_path: Path to image folder for IMAGE mode. Defaults to empty.
        """
        try:
            self.data_selector = DataSelector(
                source_type=source_type,
                folder_path=folder_path
            )
            print(f"DataSelector initialized with source type: {source_type}")
        except Exception as e:
            print(f"Error initializing DataSelector: {e}")
            self.update_status_callback(f"Error initializing data source: {e}")

    def start_detection(self) -> None:
        """Start object detection in a separate thread."""
        if self.running:
            return

        current_mode = self.mode.get().upper()
        if current_mode in ["CAMERA", "IMAGE"]:
            if not self._setup_stream(current_mode):
                return

        self.running = True
        self.stop_event.clear()
        self.update_status_callback("Status: Detection running...")
        self.detection_thread = threading.Thread(
            target=self.run_detection,
            daemon=True
        )
        self.detection_thread.start()

    def _setup_stream(self, mode: str) -> bool:
        """Set up the data stream through DataSelector.

        Args:
            mode: Current detection mode ("CAMERA" or "IMAGE").

        Returns:
            bool: True if stream setup was successful, False otherwise.
        """
        try:
            folder_path = self.image_path.get() if mode == "IMAGE" else ""
            source_type = "i" if mode == "IMAGE" else "c"
            
            if not self.data_selector.select_stream(
                source_type=source_type,
                folder_path=folder_path
            ):
                self.update_status_callback("Status: Failed to initialize source.")
                return False

            stream = self.data_selector.get_stream()
            if not stream or not stream.open_data_stream():
                self.update_status_callback("Status: Could not open data source.")
                return False
            
            return True

        except Exception as e:
            self.update_status_callback(f"Error starting detection: {e}")
            return False

    def stop_detection(self) -> None:
        """Stop the ongoing object detection process."""
        if not self.running:
            return

        try:
            self.running = False
            self.stop_event.set()
            self.update_status_callback("Status: Stopping detection...")
            
            if self.detection_thread and self.detection_thread.is_alive():
                self.detection_thread.join(timeout=2.0)
            
            stream = self.data_selector.get_stream()
            if stream:
                try:
                    stream.close_data_stream()
                except Exception as e:
                    print(f"Error closing stream: {e}")
            
            self.update_status_callback("Status: Detection stopped.")

        except Exception as e:
            print(f"Error in stop_detection: {e}")
            self.update_status_callback(f"Error stopping detection: {e}")
            self.running = False

    def run_detection(self) -> None:
        """Execute the main detection loop based on current mode."""
        try:
            current_mode = self.mode.get().upper()
            print(f"Current mode: {current_mode}")

            if current_mode not in ["CAMERA", "IMAGE"]:
                self.update_status_callback(f"Status: Unknown mode '{current_mode}'.")
                return

            stream = self.data_selector.get_stream()
            if not stream:
                self.update_status_callback("Status: No valid data source selected.")
                return

            self.detect_from_stream(mode=current_mode)

        except Exception as e:
            self.update_status_callback(f"Error: {e}")
            print(f"Error in run_detection: {e}")
        finally:
            self.running = False
            self.update_status_callback("Status: Detection completed.")

    def detect_from_stream(self, mode: str) -> None:
        """Process images from the data stream and perform object detection.

        Args:
            mode: Current detection mode ("CAMERA" or "IMAGE").
        """
        self.update_status_callback(f"Status: {mode} detection started.")
        frame_count = 0
        stream = self.data_selector.get_stream()
        
        while self.running and not self.stop_event.is_set() and stream:
            try:
                img = stream.get_current_image()
                if img is None:
                    print("No image received from stream")
                    break

                frame_count += 1
                self._process_frame(img, frame_count, mode)

                if not stream.update_data_stream():
                    print("Failed to update data stream")
                    break

            except Exception as e:
                print(f"Error processing frame: {e}")
                break

        self._cleanup_detection(mode)

    def _process_frame(self, img: Any, frame_count: int, mode: str) -> None:
        """Process a single frame for object detection.
        
        Args:
            img: Image data to process.
            frame_count: Current frame number.
            mode: Current detection mode.
        """
        try:
            # set Image Name
            current_image_name = None
            if mode == "IMAGE":
                image_names = self.get_image_names()
                if image_names and 0 <= frame_count - 1 < len(image_names):
                    current_image_name = image_names[frame_count - 1]
            else:
                current_image_name = f"frame_{frame_count}"
            
            # Name for Logger
            image_identifier = current_image_name if current_image_name else f"image_{frame_count}"
            self.logger.set_current_image(image_identifier)
            
            # Image processing
            processed_img = PictureModifications.resize_the_picture(img)
            

            
            # Detect shapes
            shapes = Detection.shape_detection(img)
            recognized = Detection.shape_recognition(shapes, img)
           
            # show the image
            self.show_image_callback(img)

            # Logging
            for shape in recognized:
                self.logger.log_data(
                    pattern=shape.get('pattern', 'Unknown'),
                    color=shape.get('color', 'Unknown'),
                    frame=frame_count if mode == "CAMERA" else None,
                    confidence=shape.get('confidence', 'N/A')
                )
    
        except Exception as e:
            print(f"General error in _process_frame: {e}")

    def _cleanup_detection(self, mode: str) -> None:
        """Clean up after detection is complete.

        Args:
            mode: Current detection mode.
        """
        try:
            stream = self.data_selector.get_stream()
            if stream and (mode == "IMAGE" or self.stop_event.is_set()):
                stream.close_data_stream()
        except Exception as e:
            print(f"Error during cleanup: {e}")