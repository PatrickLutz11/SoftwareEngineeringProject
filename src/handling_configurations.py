import json
from typing import Any, Union, Dict
from pathlib import Path

class ConfigWriter:
    """Config writer with path handling"""
    def __init__(self, filepath: Union[str, Path]):
        """initialize config writer

        Args:
            filepath (Union[str, Path]): Path of config file
        """
        self.filepath = Path(filepath)
    
    def save_value(self, key: str, value: Any) -> None:
        """Save a single object

        Args:
            key (str): key of object
            value (Any): value of object (can be found with key)
        """
        # Load existing data if available
        data = {}
        if self.filepath.exists():
            with open(self.filepath, 'r', encoding='utf-8') as f:
                data = json.load(f)
        
        # Convert Path to string if necessary
        if isinstance(value, Path):
            value = str(value)
        
        # Save value and write file
        data[key] = value
        with open(self.filepath, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2)

    def save_dict(self, config_dict: Dict[str, Any]) -> None:
        """Save multiple objects at once

        Args:
            config_dict (Dict[str, Any]): dictionary of multiple objects
        """
        # Convert all Path objects to strings
        converted_dict = {}
        for key, value in config_dict.items():
            if isinstance(value, Path):
                converted_dict[key] = str(value)
            else:
                converted_dict[key] = value
                
        with open(self.filepath, 'w', encoding='utf-8') as f:
            json.dump(converted_dict, f, indent=2)


class ConfigReader:
    """Config reader"""
    def __init__(self, filepath: Union[str, Path]):
        """Initiaize config reader

        Args:
            filepath (Union[str, Path]): path of config file
        """
        self.filepath = Path(filepath)
    
    
    def get_value(self, key: str, default: Any = None) -> Any:
        """get a value from object with key. Return default, if not found

        Args:
            key (str): key of object
            default (Any, optional): Default value. Defaults to None.

        Returns:
            Any: value of object. Default, otherwise.
        """
        if not self.filepath.exists():
            return default
        
        with open(self.filepath, 'r', encoding='utf-8') as f:
            data = json.load(f)
            return data.get(key, default)
    
    
    def get_path(self, key: str, default: Union[str, Path] = "") -> Path:
        """get a path from object with key.

        Args:
            key (str): key of object
            default (Union[str, Path], optional): default value. Defaults to "".

        Returns:
            Path: value as path
        """
        value = self.get_value(key, default)
        return Path(value)
    
    def get_int(self, key: str, default: int = 0) -> int:
        """get int-value from object with key.

        Args:
            key (str): key of object
            default (int, optional): default value. Defaults to 0.

        Returns:
            int: value as int
        """
        value = self.get_value(key, default)
        return int(value)
    
    def get_all(self) -> Dict[str, Any]:
        """Read all configuration values

        Returns:
            Dict[str, Any]: Dictionary of config
        """
        if not self.filepath.exists():
            return {}
            
        with open(self.filepath, 'r', encoding='utf-8') as f:
            return json.load(f)


if __name__ == "__main__":
    """testing functions of configurators"""
    # Create and write config
    writer = ConfigWriter("config.json")
    writer.save_value('app_name', 'Object_Pattern_Recognition')
    
    # Read config
    reader = ConfigReader("config.json")
    app_name = reader.get_value('app_name')
    print(f"App Name: {app_name}")