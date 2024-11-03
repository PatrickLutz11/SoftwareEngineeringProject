import json
from typing import Any, Union, Dict
from pathlib import Path

class ConfigWriter:
    """Config writer with path handling"""
    def __init__(self, filepath: Union[str, Path]):
        self.filepath = Path(filepath)
    
    def save_value(self, key: str, value: Any) -> None:
        """Save a single value"""
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
        """Save multiple values at once"""
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
        self.filepath = Path(filepath)
    
    def get_value(self, key: str, default: Any = None) -> Any:
        """Read a value, return default if not found"""
        if not self.filepath.exists():
            return default
        
        with open(self.filepath, 'r', encoding='utf-8') as f:
            data = json.load(f)
            return data.get(key, default)
    
    def get_path(self, key: str, default: Union[str, Path] = "") -> Path:
        """Read a path and return it as Path object"""
        value = self.get_value(key, default)
        return Path(value)
    
    def get_int(self, key: str, default: int = 0) -> int:
        """Read an integer value"""
        value = self.get_value(key, default)
        return int(value)
    
    def get_all(self) -> Dict[str, Any]:
        """Read all configuration values"""
        if not self.filepath.exists():
            return {}
            
        with open(self.filepath, 'r', encoding='utf-8') as f:
            return json.load(f)


if __name__ == "__main__":
    # Create and write config
    writer = ConfigWriter("config.json")
    writer.save_value('app_name', 'Object_Pattern_Recognition')
    
    # Read config
    reader = ConfigReader("config.json")
    app_name = reader.get_value('app_name')
    print(f"App Name: {app_name}")