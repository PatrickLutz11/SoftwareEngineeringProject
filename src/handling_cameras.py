import numpy as np
import cv2
from typing import List, Tuple

class CameraSearch:
    @staticmethod
    def list_camera_devices()->List[int]:
        """checks system for avaiable and working device ports.

        Returns:
            List: list of avaiable ports (integer). Empty, otherwise.
        """
        # Source code: https://stackoverflow.com/questions/57577445/list-available-cameras-opencv-python
        is_working = True
        device_port = 0
        working_ports = []
        available_ports = []
        
        while is_working:
            #TODO catch error, so it's not put on console
            camera = cv2.VideoCapture(device_port)
            if not camera.isOpened():
                is_working = False
                print("Port %s is not working." %device_port)
                camera.release()
                
            else:
                is_reading, img = camera.read()
                width_camera = camera.get(3)
                height_camera = camera.get(4)
                
                if is_reading:
                    print("Port %s is working and reads images (%s x %s)" %(device_port,height_camera,width_camera))
                    working_ports.append(device_port)
                else:
                    print("Port %s for camera ( %s x %s) is present but does not reads." %(device_port,height_camera,width_camera))
                    available_ports.append(device_port)
            device_port +=1
        return working_ports



class CameraOperator:
    def __init__(self, _camera_device_port:int=0)->None:
        self.camera_device_port = 0
        if _camera_device_port >= 0:
            self.camera_device_port = _camera_device_port
        
        self._capture = cv2.VideoCapture(self.camera_device_port)
        self._stream_opened = False
        self._camera_available = True
    
    
    def select_camera_device(self)->bool:
        """users can select from found camera devices. 

        Returns:
            bool: True, if successful. False, otherwise.
        """
        msg_not_found_port = f"Port could not be found. Port %s remains." %(self.camera_device_port)
        working_device_ports = CameraSearch().list_camera_devices()
        if 0 not in working_device_ports:
            self._camera_available = False
            return False
        
        print("\r\nEnter one of the following numbers to select camera port:", 
              working_device_ports)
        try: 
            user_number_input = int(input())
        except:
            print("ERROR: No valid number!", msg_not_found_port)
            return False
            
        if user_number_input in working_device_ports:
            print(f"Port {user_number_input} is selected")
            self.camera_device_port = user_number_input
            return True
        else: 
            print(msg_not_found_port)
        return False

    
    def open_camera_stream(self) -> bool:
        """opens camera stream.

        Returns:
            bool: _True, if successful. False, otherwise.
        """
        temp_cap = self._capture
        self._capture = cv2.VideoCapture(self.camera_device_port)
        
        if not self._capture.isOpened():
            print("ERROR: Cannot open camera")
            self._capture = temp_cap
            exit()
            return False
        self._stream_opened = True
        return True
    
    
    def close_camera_stream(self)->bool:
        """closes camera stream.

        Returns:
            bool: _True, if successful. False, otherwise.
        """
        self._capture.release()
        return True
        
    
    def get_image_camera(self)->cv2.typing.MatLike:
        """get image/frame of camera and returns it.

        Returns:
            cv2.typing.MatLike: Image of camera. None, oterwise. 
        """
        if not self._stream_opened:
            self.open_camera_stream()
        
        retrived, frame = self._capture.read()
        if not retrived:
            print("ERROR: Can't receive frame (stream end?). Exiting ...")
            self._stream_opened = False
            return None
        
        return frame
        

    



        

    

def main():
    cam_op = CameraOperator()
    #cam_op.select_camera_device()
    cam_op.open_camera_stream()
    images = []
    for i in range(0,10):
        image = cam_op.get_image_camera()
        images.append(image)
        cv2.imshow(f"{i}) q:close windows", image)
        cv2.waitKey(100)
    if cv2.waitKey(0) == ord('q'):
        cam_op.close_camera_stream
    print(images)
    
    
    
if __name__ == "__main__":
    main()