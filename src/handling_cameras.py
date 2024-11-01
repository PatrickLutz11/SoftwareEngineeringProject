import cv2
from typing import Union

class CameraOperator:
    def __init__(self):
        self.cap = None
        self.device_index = 0

    def select_camera_device(self, device_index: int = 0) -> bool:
        """Select and initialize the camera device."""
        self.device_index = device_index
        self.cap = cv2.VideoCapture(device_index)
        if self.cap.isOpened():
            print(f"INFO: Camera device {device_index} successfully selected.")
        else:
            print(f"ERROR: Failed to open camera device {device_index}.")
        return self.cap.isOpened()

    def open_camera_stream(self) -> bool:
        """Check if the camera stream is open."""
        if self.cap is None:
            print("ERROR: No camera device selected.")
            return False
        if not self.cap.isOpened():
            print("ERROR: Camera stream is not open.")
            return False
        print(f"INFO: Camera stream {self.device_index} is open.")
        return True

    def get_image_camera(self) -> Union[None, cv2.Mat]:
        """Capture an image from the camera."""
        if self.cap is None or not self.cap.isOpened():
            print("ERROR: Camera is not open.")
            return None
        ret, frame = self.cap.read()
        if not ret:
            print("ERROR: Failed to capture image from camera.")
            return None
        return frame

    def show_camera_feed(self, window_name: str = "Camera Feed", delay: int = 1) -> None:
        """Display the live camera feed."""
        if not self.open_camera_stream():
            return

        print("INFO: Press 'q' to quit the camera feed.")
        while True:
            frame = self.get_image_camera()
            if frame is None:
                break
            cv2.imshow(window_name, frame)
            if cv2.waitKey(delay) & 0xFF == ord('q'):
                break

        self.close_camera_stream()
        cv2.destroyAllWindows()

    def close_camera_stream(self) -> bool:
        """Closes the camera stream."""
        if self.cap:
            self.cap.release()
            self.cap = None
            print(f"INFO: Camera device {self.device_index} released.")
            return True
        print("INFO: No camera stream to close.")
        return False
