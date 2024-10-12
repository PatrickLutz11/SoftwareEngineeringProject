import csv
import os
from datetime import datetime

class TimestampGenerator:
    @staticmethod
    def get_timestamp():
        """Return current timestamp with millisecond precision."""
        return datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f')[:-3]

class LogEntryCreator:
    def __init__(self, pattern, color, **kwargs):
        """Initialize a log entry."""
        self.timestamp = TimestampGenerator.get_timestamp()
        self.pattern = pattern
        self.color = color
        self.additional_data = kwargs

    def to_dict(self):
        """Convert log entry to a dictionary."""
        data = {
            'Timestamp': self.timestamp,
            'Pattern': self.pattern,
            'Color': self.color
        }
        data.update(self.additional_data)
        return data

class WritePermissionChecker:
    @staticmethod
    def can_write(file_path):
        """Check if the file exists and is writable."""
        if os.path.isfile(file_path):
            return os.access(file_path, os.W_OK)
        else:
            directory = os.path.dirname(file_path) or '.'
            return os.access(directory, os.W_OK)

class CSVWriter:
    def __init__(self, file_path):
        """Initialize CSV writer with file path."""
        self.file_path = file_path
        self.fieldnames = None

    def write_entry(self, data):
        """Write log entry to CSV file."""
        if self.fieldnames is None:
            self.fieldnames = list(data.keys())
            self._ensure_file_exists()

        if WritePermissionChecker.can_write(self.file_path):
            with open(self.file_path, mode='a', newline='', encoding='utf-8') as csvfile:
                writer = csv.DictWriter(csvfile, fieldnames=self.fieldnames)
                writer.writerow(data)
        else:
            raise PermissionError(f"No write permission for file: {self.file_path}")

    def _ensure_file_exists(self):
        """Create CSV file with header if it does not exist."""
        if not os.path.isfile(self.file_path):
            with open(self.file_path, mode='w', newline='', encoding='utf-8') as csvfile:
                writer = csv.DictWriter(csvfile, fieldnames=self.fieldnames)
                writer.writeheader()

def log(pattern, color, file_path='log.csv', **kwargs):
    """Main function to log an entry.

    Args:
        pattern: Name of the pattern (e.g., 'Square', 'Circle').
        color: Color of the pattern.
        file_path: Path to the CSV file (default is 'log.csv').
        **kwargs: Additional optional information.
    """
    # Create the log entry
    entry_creator = LogEntryCreator(pattern, color, **kwargs)
    entry_data = entry_creator.to_dict()

    # Write the entry to the CSV file
    csv_writer = CSVWriter(file_path)
    csv_writer.write_entry(entry_data)
