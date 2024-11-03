"""
programm to select data channel and get data stream of selected channel.
"""

from data_streams import DataStream, CameraStream, FolderStream
from handling_paths_files import IntegrityChecker
from typing import List, Optional

class DataSelector:
    _camera_keywords = ["c", "camera", "cam"]
    _image_keywords = ["i", "image"]

    def __init__(self, source_type: str = "c", folder_path: str = "") -> None:
        """Initialize DataSelector

        Args:
            source_type (str, optional): Type of source. Defaults to "c".
                ["c", "camera", "cam"]: Camera stream
                ["i", "image"]: Image folder stream
            folder_path (str, optional): Absolute(!) path to the image folder (only for image mode). Defaults to "".
        """
        self.folder_path = folder_path
        self.stream: Optional[DataStream] = None
        self.select_stream(source_type)

    def select_stream(self, source_type:str = 'c', folder_path:str="") -> bool:
        """Select data stream.

        Args:
            source_type (str, optional): The data source type. Defaults to 'c'.
                        ["c", "camera", "cam"]: Camera stream
                        ["i", "image"]: Image folder stream
            folder_path (str, optional): path of image folder. Defaults to "".

        Returns:
            bool: True if successful, False otherwise.
        """
        if (folder_path) and (IntegrityChecker.check_path_validity(folder_path,
                                                                      False)):
            self.folder_path = folder_path
        source_type = source_type.lower()
        
        if source_type in self._camera_keywords:
            print("\nCamera input selected.")
            self.stream = CameraStream()
            return True

        if source_type in self._image_keywords:
            print("\nImage folder input selected.")
            self.stream = FolderStream(self.folder_path)
            return True

        print("Invalid source type selected.")
        self.stream = None
        return False

    def get_stream(self) -> Optional[DataStream]:
        """Get selected data stream.

        Returns:
            DataStream: Data stream instance or None.
        """
        return self.stream
    
    def get_names_image(self) -> List[str]:
        """Get name of images, if they exist.

        Returns:
            List[str]: List of image names. Empty, otherwise.
        """
        return stream.image_tuple[1]
    
    

if __name__ == "__main__":
    """Testing of data selector functions
    """
    import cv2
    selector = DataSelector("i", "in") # must be absolute path
    
    selector.select_stream('i') # 'c' or 'i'
    stream = selector.get_stream()
    display_time_img = 1000 # in ms
    is_opened = stream.open_data_stream()
    test_name = selector.get_names_image()
    print(test_name)
    while(is_opened):
        img = stream.get_current_image()
        cv2.imshow("q: end stream", img)
        if cv2.waitKey(display_time_img) == ord('q'):
            break
        stream.update_data_stream()
    stream.close_data_stream()