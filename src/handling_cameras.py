import numpy as np
import cv2

class CameraOperator:
    def __init__(self):
        self.camera = CameraDevice()
        print(self.camera)
        self._capture = cv2.VideoCapture
    
    
    def set_camera_device(self, _camera_device):
        self.camera = _camera_device
    
    
    def open_camera_stream(self) -> int:
        temp_cap = self._capture
        self._capture = cv2.VideoCapture(self.camera.device_id)
        
        if not self._capture.isOpened():
            print("ERROR: Cannot open camera")
            self._capture = temp_cap
            exit()
            return -1
        
        return 0
    
    
    def run_camera_stream(self) -> None:
        frame_delay_millis = int(1000/self.camera.frames_per_second)
        self.open_camera_stream()
        
        while(True):
            retrived, frame = self._capture.read()
            
            if not retrived:
                print("ERROR: Can't receive frame (stream end?). Exiting ...")
                break
            
            cv2.imshow('webcame - q: end stream', frame)
            if cv2.waitKey(frame_delay_millis) == ord('q'):
                break
        self._capture.release()
        cv2.destroyAllWindows()
    


class CameraDevice:
    def __init__(self, _device_id:int=0, _fps:float=1000):
        self.device_id = _device_id
        self.frames_per_second = _fps
        
        
    def set_frames_per_second(self, new_fps:float) -> None:
        fps = self._correct_frames_per_second(new_fps)
        self.frames_per_second = fps
        
        
    def set_device_id(self, new_device_id:int) -> None:
        device_id = self._correct_device_id(new_device_id)
        self.device_id = device_id
    
    
    def _correct_device_id(self, _new_device_id) -> None:
        cap = cv2.VideoCapture(_new_device_id)
        
        if not cap.isOpened():
            print("ERROR: Cannot open camera")
            exit()
            return -1
        cap.release()
    
    
    def _correct_frames_per_second(self, new_fps:float) -> float:
        if new_fps == 0.:
            return -1.
        if new_fps > 1000.:
            return 1000.
        
        
    def __str__(self):
        return f'Camera(ID:{self.device_id}, {self.frames_per_second}fps)'
        

    

def main():
    cam_op = CameraOperator()
    cam_op.run_camera_stream()
    
if __name__ == "__main__":
    main()