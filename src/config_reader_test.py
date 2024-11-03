from configparser import ConfigParser
import ast

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
    
    def get_bgr_color_dict(self)->dict:
        """get dictionary of BGR colors from config file.

        Returns:
            dict: dictionary of BGR colors.
        """
        config = ConfigParser()
        config.read(self._config_path)
        config_dict = dict(config.items('BGR_COLORS'))
        
        bgr_colors = {}
        for bgr_name, bgr_value in config_dict.items():
            bgr_colors[bgr_name.upper()] = list(map(int, ast.literal_eval(bgr_value)))

        return bgr_colors

if __name__ == "__main__": 
    import os
    cr = ConfigReader()
    in_path, is_relative = cr.get_input_path()
    if is_relative:
        in_path = os.path.join(os.getcwd(), in_path)
    print(in_path)
    
    BGR_COLORS = cr.get_bgr_color_dict()
    print(BGR_COLORS)
        