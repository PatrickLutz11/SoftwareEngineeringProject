"""Module for logging detection results in logs folder."""

from datetime import datetime
import os
from modificators_csv import CSVWriter

class Logger:
    """Logger class for recording detection results.
    
    This class handles the creation and management of log files, including
    organizing them in a dedicated folder and creating unique filenames
    for each session.
    """
    
    def __init__(self, base_file_path='log.csv'):
        """Initialize CSV writer with unique file path.

        Args:
            base_file_path (str, optional): Base path for CSV-log. Defaults to 'log.csv'.
        """
        # Create logs folder in current directory
        self.log_dir = os.path.join(os.getcwd(), 'logs')
        os.makedirs(self.log_dir, exist_ok=True)
        
        # Combine folder with filename
        base_name = os.path.basename(base_file_path)
        self.file_path = self._create_unique_filename(os.path.join(self.log_dir, base_name))
        self.csv_writer = CSVWriter(self.file_path)
        self.current_image = None

    def _create_unique_filename(self, base_file_path: str) -> str:
        """Create unique filename with timestamp.

        Args:
            base_file_path: Base path for the log file

        Returns:
            str: Path with timestamp included
        """
        directory, filename = os.path.split(base_file_path)
        name, ext = os.path.splitext(filename)
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        new_filename = f"{name}_{timestamp}{ext}"
        
        return os.path.join(directory, new_filename)

    def set_current_image(self, image_identifier: str) -> None:
        """Set the current image being processed.

        Args:
            image_identifier (str): Name or number of current image
        """
        self.current_image = image_identifier

    def log_data(self, pattern: str, color: str, **kwargs) -> None:
        """Log an entry with detection results.

        Args:
            pattern (str): Name of the detected pattern (e.g., 'Square', 'Circle')
            color (str): Color of the detected shape
            **kwargs: Additional optional information to log
        """
        if self.current_image:
            kwargs['image'] = self.current_image
            
        entry_creator = LogEntryCreator(pattern, color, **kwargs)
        entry_data = entry_creator.to_dict()
        self.csv_writer.write_entry(entry_data)


class TimestampGenerator:
    """Utility class for generating timestamps."""
    
    @staticmethod
    def get_timestamp() -> str:
        """Get current timestamp with millisecond precision.

        Returns:
            str: Formatted string of current time
        """
        return datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f')[:-3]


class LogEntryCreator:
    """Creates structured log entries for detection results."""
    
    def __init__(self, pattern: str, color: str, **kwargs):
        """Initialize a log entry.

        Args:
            pattern (str): Name of pattern
            color (str): Name of color
            **kwargs: Additional optional information
        """
        self.timestamp = TimestampGenerator.get_timestamp()
        self.pattern = pattern
        self.color = color
        self.additional_data = kwargs

    def to_dict(self) -> dict:
        """Convert log entry to a dictionary.

        Returns:
            dict: Dictionary containing all log data
        """
        data = {
            'Timestamp': self.timestamp,
            'Pattern': self.pattern,
            'Color': self.color
        }
        data.update(self.additional_data)
        return data


if __name__ == "__main__":
    """Testing of logger functionality."""
    try:
        logger = Logger('log.csv')
        
        # Test with first image
        logger.set_current_image("image_1")
        logger.log_data("Circle", "Red", confidence="High")
        logger.log_data("Square", "Blue", confidence="Medium")
        
        # Test with second image
        logger.set_current_image("image_2")
        logger.log_data("Triangle", "Green", confidence="High")
        
        print(f"Entries successfully logged to: {logger.file_path}")
    except Exception as e:
        print(f"Error during testing: {e}")