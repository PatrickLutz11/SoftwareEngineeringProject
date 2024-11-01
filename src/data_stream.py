import os
import cv2
from typing import Optional, List, final
from abc import ABC, abstractmethod

import handling_cameras
import handling_paths_files


class DataStream(ABC):
    """Abstract base class for different data streams."""

    def __init__(self) -> None:
        self.current_image = None

    @abstractmethod
    def open_data_stream(self) -> bool:
        """Sets up and opens the data stream."""
        pass

    @abstractmethod
    def update_data_stream(self) -> bool:
        """Updates the data stream."""
        pass

    @abstractmethod
    def close_data_stream(self) -> bool:
        """Closes the data stream."""
        pass

    @final
    def get_current_image(self) -> Optional[cv2.Mat]:
        """Returns the current image of the data stream."""
        return self.current_image


class CameraStream(DataStream):
    def __init__(self) -> None:
        super().__init__()
        self.cam_op = handling_cameras.CameraOperator()

    def open_data_stream(self) -> bool:
        if not self.cam_op.select_camera_device():
            return False
        if not self.cam_op.open_camera_stream():
            return False
        return self.update_data_stream()

    def update_data_stream(self) -> bool:
        self.current_image = self.cam_op.get_image_camera()
        return self.current_image is not None

    def close_data_stream(self) -> bool:
        return self.cam_op.close_camera_stream()


class FolderStream(DataStream):
    def __init__(self, folder_path: str) -> None:
        super().__init__()
        self.folder_path = folder_path
        self.image_list: Optional[List[str]] = []
        self._id_image: int = 0
        self.ph = handling_paths_files.PathHandling()
        self.fh = handling_paths_files.FileHandling()

    def open_data_stream(self) -> bool:
        if not self.ph.check_path_validity(self.folder_path):
            print(f"Error: Invalid path {self.folder_path}")
            return False
        self.fh = handling_paths_files.FileHandling(self.folder_path)
        self.image_list = self.fh.open_all_files()[0]  # Assuming this returns a list of image paths
        if not self.image_list:
            print("ERROR: No images found in the specified folder.")
            return False
        self._id_image = 0
        return self.update_data_stream()

    def update_data_stream(self) -> bool:
        if self._id_image < len(self.image_list):
            image_path = self.image_list[self._id_image]
            self.current_image = cv2.imread(image_path)
            if self.current_image is None:
                print(f"Warning: Unable to load image {image_path}. Skipping.")
                self._id_image += 1
                return self.update_data_stream()
            self._id_image += 1
            return True
        else:
            self._id_image = 0  # Restart from the beginning if needed
            return False

    def close_data_stream(self) -> bool:
        self.current_image = None
        self.image_list = []
        self._id_image = 0
        return True

    def get_current_image_path(self) -> Optional[str]:
        if 0 <= self._id_image - 1 < len(self.image_list):
            return self.image_list[self._id_image - 1]
        return None
