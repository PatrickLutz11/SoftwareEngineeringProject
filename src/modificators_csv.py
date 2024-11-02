import os
import csv

class CSVWriter:
    def __init__(self, file_path: str):
        """Initialize CSV writer with file path.

        Args:
            file_path (str): path of logger file
        """
        self.file_path = file_path
        self.fieldnames = None

    def write_entry(self, data: dict) -> None:
        """Write log entry to CSV file.

        Args:
            data (dict): data as dict

        Raises:
            PermissionError: permission to write file
        """
        if self.fieldnames is None:
            self.fieldnames = list(data.keys())
            self._ensure_file_exists()

        if WritePermissionChecker.can_write(self.file_path):
            with open(self.file_path, mode='a', newline='', encoding='utf-8') as csvfile:
                writer = csv.DictWriter(csvfile, fieldnames=self.fieldnames)
                writer.writerow(data)
        else:
            raise PermissionError(f"No write permission for file: {self.file_path}")

    def _ensure_file_exists(self) -> None:
        """Create CSV file with header if it does not exist.
        """
        if not os.path.isfile(self.file_path):
            with open(self.file_path, mode='w', newline='', encoding='utf-8') as csvfile:
                writer = csv.DictWriter(csvfile, fieldnames=self.fieldnames)
                writer.writeheader()
                

class WritePermissionChecker:
    @staticmethod
    def can_write(file_path: str) -> bool:
        """Check if the file exists and is writable.

        Args:
            file_path (str): path of file

        Returns:
            bool: True, path is file. False, otherwise. 
        """
        if os.path.isfile(file_path):
            return os.access(file_path, os.W_OK)
        else:
            directory = os.path.dirname(file_path) or '.'
            return os.access(directory, os.W_OK)