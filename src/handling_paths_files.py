import os
from typing import Tuple, List


class PathHandling:
    def __init__(self, input_dir: str = "in") -> None:
        self.input_dir = input_dir
        self.abs_input_path = ""

    def get_path_abs_input(self) -> str:
        """Returns the absolute input path."""
        if not self.abs_input_path:
            self.abs_input_path = os.path.abspath(self.input_dir)
        return self.abs_input_path

    def check_path_validity(self, path: str) -> bool:
        """Checks if the given path is a valid directory."""
        if not os.path.isdir(path):
            print(f"WARNING: The path '{path}' is not a valid directory.")
            return False
        return True

    def ensure_directory_exists(self, path: str) -> None:
        """Creates the directory if it does not exist."""
        if not os.path.exists(path):
            os.makedirs(path)
            print(f"INFO: Directory '{path}' created.")


class FileHandling:
    def __init__(self, input_path: str = "") -> None:
        self.input_path = input_path
        self.files = []

    def open_all_files(self) -> Tuple[List[str]]:
        """Opens all image files in the specified folder.

        Returns:
            Tuple[List[str]]: A tuple containing a list of image file paths.
        """
        image_files = []
        supported_formats = self.get_supported_formats()

        if not os.path.isdir(self.input_path):
            print(f"ERROR: The input path '{self.input_path}' is not valid.")
            return ([],)

        for file_name in os.listdir(self.input_path):
            if file_name.lower().endswith(supported_formats):
                full_path = os.path.join(self.input_path, file_name)
                image_files.append(full_path)

        if not image_files:
            print("WARNING: No image files found in the specified folder.")
        return (image_files,)

    @staticmethod
    def get_supported_formats() -> Tuple[str, ...]:
        """Returns the supported image formats."""
        return ('.png', '.jpg', '.jpeg', '.bmp', '.tiff')

    def log_files_found(self) -> None:
        """Logs the files found in the input directory."""
        if not self.files:
            print("INFO: No files have been loaded yet.")
        else:
            print(f"INFO: {len(self.files)} files found.")
