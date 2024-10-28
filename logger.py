import csv
import os
from datetime import datetime

class TimestampGenerator:
    @staticmethod
    def get_timestamp()-> str:
        """Get current timestamp with millisecond precision.

        Returns:
            str: formated string of current time
        """
        return datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f')[:-3]

class LogEntryCreator:
    def __init__(self, pattern: str, color: str, **kwargs):
        """Initialize a log entry.

        Args:
            pattern (str): name of pattern
            color (str): name of color
            **kwargs: Additional optional information.
        """
        self.timestamp = TimestampGenerator.get_timestamp()
        self.pattern = pattern
        self.color = color
        self.additional_data = kwargs

    def to_dict(self) -> dict:
        """Convert log entry to a dictionary.

        Returns:
            dict: dictionary of data
        """
        data = {
            'Timestamp': self.timestamp,
            'Pattern': self.pattern,
            'Color': self.color
        }
        data.update(self.additional_data)
        return data

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

def log_data(pattern: str, color: str, file_path='log.csv', **kwargs) -> None:
    """Logging of entery data.

    Args:
        pattern (str): Name of the pattern (e.g., 'Square', 'Circle').
        color (str): Color of the shape.
        file_path (str, optional): Path to CSV File. Defaults to 'log.csv'.
        **kwargs: Additional optional information.
    """
    # Create the log entry
    entry_creator = LogEntryCreator(pattern, color, **kwargs)
    entry_data = entry_creator.to_dict()

    # Write the entry to the CSV file
    csv_writer = CSVWriter(file_path)
    csv_writer.write_entry(entry_data)
    

if __name__ == "__main__":
    """Test function to demonstrate logging functionality."""
    try:
        log_data("Circle", "Red", additional_info="Detected in frame 5")
        log_data("Square", "Blue", additional_info="Detected in frame 8", confidence="High")
        print("Entries logged successfully.")
    except PermissionError as e:
        print(e)
