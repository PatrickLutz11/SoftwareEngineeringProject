from configparser import ConfigParser
import os

config = ConfigParser()

config['PROJECT'] = {
    'app_name': 'Object_Pattern_Recognition',
    'version': '1.0'
    }
    
config['PATHS'] = {    
    'dir_input': 'in',
    'dir_output': 'out',
    'is_relative_path_in': True,
    'is_relative_path_out': True,
}
config['BGR_COLORS'] = {
    "BLUE" : [255, 0, 0],
    "GREEN" : [0, 255, 0],
    "RED" : [0, 0, 255],
    "MANGENTA": [255, 0, 255],
    "CYAN" : [255, 255, 0],
    "YELLOW": [0, 255, 255],
    "BLACK": [0, 0, 0],
    "WHITE": [255, 255, 255],
}

# Write the configuration to a file
with open('config.ini', 'w') as configfile:
    config.write(configfile)
print("Config file created successfully!")
