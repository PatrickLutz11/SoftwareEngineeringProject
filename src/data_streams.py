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
        """setups and opens data stream.

        Returns:
            bool: True, if successful. False, otherwise.
        """
        pass

    @abstractmethod
    def update_data_stream(self) -> bool:
        """updates data stream i.e. the current image.

        Returns:
            bool: True, if successful. False, otherwise.
        """
        pass

    @abstractmethod
    def close_data_stream(self) -> bool:
        """closes data stream.

        Returns:
            bool: True, if successful. False, otherwise.
        """
        pass

    @final
    def get_current_image(self) -> Optional[cv2.Mat]:
        """get current image of data stream.

        Returns:
            cv2.typing.MatLike: current image, if successful. None, otherwise.
        """
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
    def __init__(self, _folder_path:str="") -> None:
        super().__init__()
        self.image_list = []
        self._id_image:int = 0
        
        self.ph = handling_paths_files.PathHandling(_folder_path)
        self.fh = handling_paths_files.FileHandling()

    def open_data_stream(self) -> bool:
        input_path = self.ph.get_path_abs_input()
        if not (self.ph.check_path_validity(input_path)):
            return False
        self.fh = handling_paths_files.FileHandling(input_path)
        self.image_list = self.fh.open_all_files()[0]
        if len(self.image_list[0]) == 0:
            print("ERROR: no Image found")
            return False
        self._id_image = 0
        return self.update_data_stream()

    def update_data_stream(self) -> bool:
        amount_images = len(self.image_list)
        if amount_images > self._id_image:
            self.current_image = self.image_list[self._id_image]
            self._id_image += 1
            return True
        return False

    def close_data_stream(self) -> bool:
        self.current_image = None
        self.image_list = []
        self._id_image = 0
        return True
