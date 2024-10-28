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

# Write the configuration to a file
with open('config.ini', 'w') as configfile:
    config.write(configfile)
print("Config file created successfully!")



    