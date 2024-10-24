import cv2
from abc import ABC, abstractmethod

import handling_cameras 
import handling_paths_files 

class DataStream(ABC):
    
    
    def __init__(self)->None:
        self.current_image = None
        
    @abstractmethod
    def open_data_stream(self)->bool:
        pass
    
    @abstractmethod
    def update_data_stream(self)->bool:
        pass
    
    @abstractmethod
    def close_data_stream(self)->bool:
        pass
    
    def get_current_image(self)->cv2.typing.MatLike:
        return self.current_image
    
    




class CameraStream(DataStream):
    def __init__(self)->None:
        super().__init__()
        self.cam_op = handling_cameras.CameraOperator()

    def open_data_stream(self)->bool:
        if not (self.cam_op.select_camera_device()):
            return False
        if not (self.cam_op.open_camera_stream()):
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
    def _init__(self)->None:
        super.__init__()
        self.fol_op = handling_paths_files.FileHandling()
    
    def open_data_stream(self)->bool:
        if self.channel_selected in self._camera_keywords:
            self.cam_op.select_camera_device()
            self.cam_op.open_camera_stream()
            return True
        
        if self.channel_selected in self._folder_keywords:
            # TODO implement folder
            print("Folder tbd implemented")
            return True
        return False
    
    def update_data_stream(self)->bool:
        self.current_image = "gfg"
        return True

    def close_data_stream(self)->bool:
        if self.channel_selected in self._camera_keywords:
            self.cam_op.close_camera_stream()
            return True
        
        if self.channel_selected in self._folder_keywords:
            # TODO implement folder
            print("Folder tbd implemented")
            return True
        return False
    

    
    

    