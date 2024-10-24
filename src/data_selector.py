"""
programm to select data channel and get data stream of selected channel.
"""

from data_stream import DataStream, CameraStream, FolderStream
import cv2
from abc import ABC, abstractmethod


class DataSelector:
    _camera_keywords = ["c", "camera", "cam"]
    _folder_keywords = ["f", "folder"]
    
    def __init__(self, source_type:str="c")->None:
        if source_type in self._camera_keywords:
            self.stream = CameraStream()
        elif source_type in self._folder_keywords:
            self.stream = FolderStream()
        else:
            raise ValueError("Invalid source type")
    
    
    def select_channel(self, source_type:str='f')->bool:
        """selects and sets the data stream for the input.

        Args:
            source_type (str): The stream where to take an image from
                ["c", "camera", "cam"]: to select camera as data stream
                ["f", "folder"]:        to select folder as data stream
                
        Returns:
            bool: True, if successful, False otherwise.
        """
        print()
        if source_type in self._camera_keywords:
            print("camera input selected")
            self.stream = CameraStream()
            return True
        
        if source_type in self._folder_keywords:
            print("folder input selected")
            self.stream = FolderStream()
            return True
        
        return False
    
    
    def get_stream(self) -> DataStream:
        return self.stream
    



def main():
    selector = DataSelector()
    
    selector.select_channel('c') # or 'f'
    stream = selector.get_stream()
    
    display_time_img = 1
    is_opened = stream.open_data_stream()
    while(is_opened):
        stream.update_data_stream()
        img = stream.get_current_image()
        cv2.imwrite("test.png", img)
        cv2.imshow("q: end stream", img)
        if cv2.waitKey(display_time_img) == ord('q'):
            break
    stream.close_data_stream()
    
if __name__ == "__main__":
    main()