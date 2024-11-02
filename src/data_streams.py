import cv2
from abc import ABC, abstractmethod
from typing import final

import handling_cameras 
import handling_paths_files 

class DataStream(ABC):
    def __init__(self)->None:
        self.current_image = None
        
    @abstractmethod
    def open_data_stream(self)->bool:
        """setups and opens data stream.

        Returns:
            bool: True, if successful. False, otherwise.
        """
        pass
    
    @abstractmethod
    def update_data_stream(self)->bool:
        """updates data stream i.e. the current image.

        Returns:
            bool: True, if successful. False, otherwise.
        """
        pass
    
    @abstractmethod
    def close_data_stream(self)->bool:
        """closes data stream.

        Returns:
            bool: True, if successful. False, otherwise.
        """
        pass
    
    @final
    def get_current_image(self)->cv2.typing.MatLike:
        """get current image of data stream.

        Returns:
            cv2.typing.MatLike: current image, if successful. None, otherwise.
        """
        return self.current_image


class CameraStream(DataStream):
    def __init__(self)->None:
        super().__init__()
        self.cam_op = handling_cameras.CameraOperator()

    def open_data_stream(self)->bool:
        """setups and opens camera stream.

        Returns:
            bool: True, if successful. False, otherwise.
        """
        if not (self.cam_op.select_camera_device()):
            return False
        if not (self.cam_op.open_camera_stream()):
            return False
        self.update_data_stream()
        return True
    
    def update_data_stream(self)->bool:
        """updates camera stream i.e. the current image.

        Returns:
            bool: True, if successful. False, otherwise.
        """
        self.current_image = self.cam_op.get_image_camera()
        return True
    
    def close_data_stream(self)->bool:
        """closes camera stream.

        Returns:
            bool: True, if successful. False, otherwise.
        """
        if not (self.cam_op.close_camera_stream()):
            return False
        return True




class ImageStream(DataStream):
    
    def __init__(self)->None:
        super().__init__()
        self.ph = handling_paths_files.PathHandling()
        self.fh = handling_paths_files.FileHandling()
        self.image_list = None
    
    def open_data_stream(self)->bool:
        """setups and opens image stream.

        Returns:
            bool: True, if successful. False, otherwise.
        """
        input_path = self.ph.get_path_abs_input()
        if not (self.ph.check_path_validity(input_path)):
            return False
        self.fh = handling_paths_files.FileHandling(input_path)
        self.image_list = self.fh.open_all_files()[0]
        if len(self.image_list[0]) == 0:
            print("ERROR: no Image found")
            return False
        self._id_image = 0
        self.update_data_stream()
        return True
    
    def update_data_stream(self)->bool:
        """updates image stream i.e. the current image.

        Returns:
            bool: True, if successful. False, otherwise.
        """
        amount_images = len(self.image_list)
        self.current_image = self.image_list[self._id_image % amount_images]
        self._id_image += 1
        return True

    def close_data_stream(self)->bool:
        """closes image stream.

        Returns:
            bool: True, if successful. False, otherwise.
        """
        self._id_image = 0
        self.update_data_stream()
        return True
