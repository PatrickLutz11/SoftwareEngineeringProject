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
            self.stream = None
            raise ValueError("Invalid source type")
    
    
    def select_stream(self, source_type:str='f')->bool:
        """selects and sets the data stream for the input.

        Args:
            source_type (str): The stream where to take an image from
                ["c", "camera", "cam"]: to select camera as data stream
                ["f", "folder"]:        to select folder as data stream
                
        Returns:
            bool: True, if successful, False otherwise.
        """
        if source_type in self._camera_keywords:
            print(f"\r\ncamera input selected")
            self.stream = CameraStream()
            return True
        
        if source_type in self._folder_keywords:
            print(f"\r\nfolder input selected")
            self.stream = FolderStream()
            return True
        
        return False
    
    
    def get_stream(self) -> DataStream:
        """get selected data stream

        Returns:
            DataStream: data of slected stream. Otherwise None
        """
        return self.stream
    



def main():
    selector = DataSelector()
    
    selector.select_stream('f') # 'c' or 'f'
    stream = selector.get_stream()
    
    display_time_img = 1000 # in ms
    is_opened = stream.open_data_stream()
    while(is_opened):
        img = stream.get_current_image()
        cv2.imshow("q: end stream", img)
        if cv2.waitKey(display_time_img) == ord('q'):
            break
        stream.update_data_stream()
    stream.close_data_stream()
    
if __name__ == "__main__":
    main()