"""
@data:      data_selector.py
@author:    Jannis Mathiuet
@versions:  ver 0.0.0 - 30.09.2024 - Jannis Mathiuet

@desc: 
    programm to select which data channel should be used.
    If there are any questions or problems, please contact me.
"""
import file_handling
import webcam

class DataSelector:
    def __init__(self)->int:
        return 0
    
    def select_channel(self, channel:str='f')->int:
        """selects and sets the data channel for the input.

        Args:
            channel (str): The channels where to take an image from
                ["f", "folder"]:        to select folder as data channel
                ["w", "webcam", "cam"]: to select camera as data channel
        Returns:
            int: 0 if successful, failed otherwise.
        """
        if channel in ["f", "folder"]:
            print("folder input selected")
        
        if channel in ["w", "webcam", "cam"]:
            print("camera input selected")
        return 0