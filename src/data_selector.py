"""
programm to select data channel and get data stream of selected channel.
"""

from data_stream import DataStream, CameraStream, FolderStream
from typing import Optional

class DataSelector:
    _camera_keywords = ["c", "camera", "cam"]
    _image_keywords = ["i", "image"]

    def __init__(self, source_type: str = "c", folder_path: str = "") -> None:
        """Initialize DataSelector

        Args:
            source_type (str, optional): Type of source. Defaults to "c".
            folder_path (str, optional): Path to the image folder (only for image mode). Defaults to "".
        """
        self.folder_path = folder_path
        self.stream: Optional[DataStream] = None
        self.select_stream(source_type, folder_path)

    def select_stream(self, source_type: str = 'c', folder_path: str = "") -> bool:
        """Selects and sets the data stream based on the source type.

        Args:
            source_type (str): The data source type.
                ["c", "camera", "cam"]: Camera stream
                ["i", "image"]: Image folder stream

        Returns:
            bool: True if successful, False otherwise.
        """
        source_type = source_type.lower()
        if source_type in self._camera_keywords:
            print("\nCamera input selected.")
            self.stream = CameraStream()
            return True

        if source_type in self._image_keywords:
            if not folder_path:
                print("Error: Folder path must be provided for ImageStream.")
                self.stream = None
                return False
            print("\nImage folder input selected.")
            self.stream = FolderStream(folder_path=folder_path)
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
