from configparser import ConfigParser

class ConfigReader:
    def __init__(self, config_path:str='config.ini')->None:
        self._config_path = config_path
        
    def get_input_path(self)->tuple[str, bool]:
        """get output path from config file.

        Returns:
            tuple[str, bool]: 
                    - str   : path of output folder
                    - bool  : True, if relative path. False, otherwise
        """
        config = ConfigParser()
        config.read(self._config_path)
        path_in = str(config.get('PATHS', 'dir_input'))
        is_relative_in = bool(config.get('PATHS', 'is_relative_path_in'))
        return (path_in, is_relative_in)
    
    def get_output_path(self)->tuple[str, bool]:
        """get output path from config file.

        Returns:
            tuple[str, bool]: 
                    - str   : path of output folder
                    - bool  : True, if relative path. False, otherwise
        """
        config = ConfigParser()
        config.read(self._config_path)
        path_out = str(config.get('PATHS', 'dir_output'))
        is_relative_out = bool(config.get('PATHS', 'is_relative_path_out'))
        return (path_out, is_relative_out)

if __name__ == "__main__": 
    import os
    cr = ConfigReader()
    in_path, is_relative = cr.get_input_path()
    if is_relative:
        in_path = os.path.join(os.getcwd(), in_path)
    print(in_path)
        
    