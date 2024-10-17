from abc import ABC

class DataStream:
    def __init__(self) -> None: 
        pass
    
    def select_stream(self):
        pass
    
    def set_stream_camera(self):
        pass
    
    def set_stream_input(self):
        pass
    
    def set_stream_output(self):
        pass
    

class Camera(DataStream):
    def __init__(self):
        pass
    def __str__(self) -> str:
        return ""
    
class StreamFolder(DataStream):
    def __init__(self):
        pass

class StreamInput(StreamFolder):
    def __init__(self):
        pass

class StreamOutput(DataStream):
    def __init__(self):
        pass

def main():
    pass
    
if __name__ == "__main__":
    main()
    