
from datetime import datetime
from modificators_csv import CSVWriter

class Logger:
    def __init__(self, file_path='log.csv'):
        """Initialize CSV writer with file path.

        Args:
            file_path (str, optional): path to CSV-log. Defaults to 'log.csv'.
        """
        self.csv_writer = CSVWriter(file_path)

    def log_data(self, pattern: str, color: str, **kwargs) -> None:
        """Loggt einen Eintrag.

        Args:
            pattern (str): Name des Musters (z.B. 'Quadrat', 'Kreis').
            color (str): Farbe der Form.
            **kwargs: Zusätzliche optionale Informationen.
        """

        entry_creator = LogEntryCreator(pattern, color, **kwargs)
        entry_data = entry_creator.to_dict()
        self.csv_writer.write_entry(entry_data)

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



if __name__ == "__main__":
    """Testing of functions of this file"""
    try:
        logger = Logger('log.csv')
        logger.log_data("Circle", "Red", additional_info="Erkannt in Frame 5")
        logger.log_data("Quadrat", "Blau", additional_info="Erkannt in Frame 8", confidence="Hoch")
        print("Einträge erfolgreich geloggt.")
    except PermissionError as e:
        print(e)