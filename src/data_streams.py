import os
import cv2
from typing import Optional, List, final
from abc import ABC, abstractmethod

import handling_cameras
import handling_paths_files


class DataStream(ABC):
    """_summary_

    Args:
        ABC (_type_): _description_
    """
    def __init__(self)->None:
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

    def open_data_stream(self)->bool:
        if not (self.cam_op.select_camera_device()):
            return False
        if not self.cam_op.open_camera_stream():
            return False
        self.update_data_stream()
        return True
    
    def update_data_stream(self)->bool:
        self.current_image = self.cam_op.get_image_camera()
        return True
    
    def close_data_stream(self)->bool:
        if not (self.cam_op.close_camera_stream()):
            return False
        return True




class FolderStream(DataStream):
    
    def __init__(self)->None:
        super().__init__()
        self.folder_path = folder_path
        self.image_list: Optional[List[str]] = []
        self._id_image: int = 0
        self.ph = handling_paths_files.PathHandling()
        self.fh = handling_paths_files.FileHandling()
        self.image_list = None
    
    def open_data_stream(self)->bool:
        input_path = self.ph.get_path_abs_input()
        if not (self.ph.check_path_validity(input_path)):
            return False
        self.fh = handling_paths_files.FileHandling(self.folder_path)
        self.image_list = self.fh.open_all_files()[0]  # Assuming this returns a list of image paths
        if not self.image_list:
            print("ERROR: No images found in the specified folder.")
            return False
        self._id_image = 0
        self.update_data_stream()
        return True
    
    def update_data_stream(self)->bool:
        amount_images = len(self.image_list)
        self.current_image = self.image_list[self._id_image % amount_images]
        self._id_image += 1
        return True

    def close_data_stream(self)->bool:
        self._id_image = 0
        return True
        
    

    
    

    