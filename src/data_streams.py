import cv2
from typing import Optional, Tuple, final
from abc import ABC, abstractmethod

import handling_cameras
import handling_paths_files
from handling_paths_files import IntegrityChecker


class DataStream(ABC):
    """Abstract base class for different data streams."""

    def __init__(self) -> None:
        """Initialized DataStream"""
        self.current_image = None
        self.image_tuple:Tuple[cv2.typing.matLike, str]=("","")

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
    
    @final
    def get_names_images_list(self):
        """
        Get name of opened images.

        Returns:
            List[str]: List of image names.
        """
        return self.image_tuple[1]



class CameraStream(DataStream):
    """Stream of Camera"""
    def __init__(self) -> None:
        """Initialized CameraStream"""
        super().__init__()
        self.cam_op = handling_cameras.CameraOperator()


    def open_data_stream(self) -> bool:
        """setups and opens camera stream.

        Returns:
            bool: True, if successful. False, otherwise.
        """
        if not self.cam_op.select_camera_device():
            return False
        if not self.cam_op.open_camera_stream():
            return False
        return self.update_data_stream()


    def update_data_stream(self) -> bool:
        """updates camera stream i.e. the current image.

        Returns:
            bool: True, if successful. False, otherwise.
        """
        self.current_image = self.cam_op.get_image_camera()
        return self.current_image is not None


    def close_data_stream(self) -> bool:
        """closes camera stream.

        Returns:
            bool: True, if successful. False, otherwise.
        """
        return self.cam_op.close_camera_stream()


class FolderStream(DataStream):
    """Stream of Folder/Image"""
    
    def __init__(self, _folder_path:str="") -> None:
        """Initialized FolderStream

        Args:
            _folder_path (str, optional): Path to folder. Defaults to "".
        """
        super().__init__()
        self._id_image:int = 0
        
        self.ph = handling_paths_files.PathHandling(_folder_path)
        self.fh = handling_paths_files.FileHandling()


    def open_data_stream(self) -> bool:
        """setups and opens folder stream.

        Returns:
            bool: True, if successful. False, otherwise.
        """
        input_path = self.ph.get_path_abs_input()
        
        if not(IntegrityChecker.check_path_validity(input_path)):
            return False
        self.fh = handling_paths_files.FileHandling(input_path)
        self.image_tuple = self.fh.open_all_files()
        if len(self.image_tuple[0]) == 0:
            print("ERROR: no Image found")
            return False
        self._id_image = 0
        return self.update_data_stream()


    def update_data_stream(self) -> bool:
        """updates folder stream i.e. the current image.

        Returns:
            bool: True, if successful. False, otherwise.
        """
        image_list = self.image_tuple[0]
        amount_images = len(image_list)
        
        if amount_images > self._id_image:
            self.current_image = image_list[self._id_image]
            self._id_image += 1
            return True
        return False

    def close_data_stream(self) -> bool:
        """closes folder stream.

        Returns:
            bool: True, if successful. False, otherwise.
        """
        self.current_image = None
        self.image_tuple = ()
        self._id_image = 0
        return True
