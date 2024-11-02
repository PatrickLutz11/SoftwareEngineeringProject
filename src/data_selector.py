"""
programm to select data channel and get data stream of selected channel.
"""

from data_streams import DataStream, CameraStream, FolderStream
from typing import Optional

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

    def select_stream(self, source_type:str = 'c', folder_path:str = "") -> bool:
        """Selects and sets the data stream based on the source type.

        Args:
            source_type (str): The data source type.
                ["c", "camera", "cam"]: Camera stream
                ["i", "image"]: Image folder stream

        Returns:
            bool: True if successful, False otherwise.
        """
        self.folder_path=folder_path
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
        """Get selected data stream

        Returns:
            DataStream: Data stream instance or None.
        """
        return self.stream

if __name__ == "__main__":
    import cv2
    selector = DataSelector("i", R"C:\Users\janni\Downloads\test_images") # must be absolute path
    
    selector.select_stream('i') # 'c' or 'i'
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