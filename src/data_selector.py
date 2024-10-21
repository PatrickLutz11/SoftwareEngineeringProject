"""
programm to select data channel and get data stream of selected channel.
"""
import handling_cameras
import handling_paths_files
import cv2

class DataStream:
    _camera_keywords = ["c", "camera", "cam"]
    _folder_keywords = ["f", "folder"]
    
    def __init__(self)->None:
        self.current_image = None
        self.selected_channel = 'c'
        
        self.cam_op = handling_cameras.CameraOperator()
        #self.fol_op = handling_paths_files.FileHandling()
        
        
    
    
    def select_channel(self, channel:str='f')->bool:
        """selects and sets the data channel for the input.

        Args:
            channel (str): The channels where to take an image from
                ["c", "camera", "cam"]: to select camera as data channel
                ["f", "folder"]:        to select folder as data channel
                
        Returns:
            bool: True, if successful, False otherwise.
        """
        if channel in self._camera_keywords:
            print("camera input selected")
            self.channel_selected = 'c'
            return True
        
        if channel in self._folder_keywords:
            print("folder input selected")
            self.channel_selected = 'f'
            return True
        
        return False
    
    
    def open_data_stream(self)->bool:
        if self.channel_selected in self._camera_keywords:
            self.cam_op.select_camera_device()
            self.cam_op.open_camera_stream()
            return True
        
        if self.channel_selected in self._folder_keywords:
            # TODO implement folder
            print("Folder tbd implemented")
            return True
        return False
    
    def close_data_stream(self)->bool:
        if self.channel_selected in self._camera_keywords:
            self.cam_op.close_camera_stream()
            return True
        
        if self.channel_selected in self._folder_keywords:
            # TODO implement folder
            print("Folder tbd implemented")
            return True
        return False
        
    def get_current_image(self)->cv2.typing.MatLike:
        if not self._update_current_image():
            print("ERROR: Cannot update iamge!")
            return None
        return self.current_image
    
    
    def _update_current_image(self)->bool:
        if self.channel_selected in self._folder_keywords:
            # TODO implement folder
            print("Folder tbd implemented")
            return True
            
        if self.channel_selected in self._camera_keywords:
            self.current_image = self.cam_op.get_image_camera()
            return True
        return False

def main():
    ds = DataStream()
    ds.select_channel('c')
    is_opened = ds.open_data_stream()
    while(is_opened):
        img = ds.get_current_image()
        cv2.imwrite("test.png", img)
        cv2.imshow("q: end stream", img)
        if cv2.waitKey(1) == ord('q'):
            break
    ds.close_data_stream()
    
if __name__ == "__main__":
    main()