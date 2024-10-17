import os
import numpy as np
import cv2
from PIL import Image as PilImg
from PIL.Image import Image
from typing import List, Tuple


class PathHandling():
    def __init__(self, _path_rel_in: str="in", _path_rel_out: str="out",) -> None:
        self.path_rel_in = _path_rel_in
        self.path_rel_out = _path_rel_out
        self.path_abs_parent = ""
        self.path_abs_in = ""
        self.path_abs_out = ""
        
        
    def get_path_abs_parent(self) -> str:
        self._check_abs_paths()
        return self.path_abs_parent
    
    
    def get_path_abs_input(self) -> str:
        self._check_abs_paths()
        return self.path_abs_in
    
    
    def get_path_abs_output(self) -> str:
        self._check_abs_paths()
        return self.path_abs_out
    
    
    def check_path_validity(self, path:str) -> bool:
        if (os.path.exists(path)) is False: 
            print(f"ERROR: This path does not exist! \n{path = }\n")
            return False
        return True
    
    
    def _check_abs_paths(self) -> bool:
        if self.path_abs_parent.empty():
            self.path_abs_parent = os.getcwd()
            
        if self.path_abs_in.empty():
            self.path_abs_in = os.path.join(self.path_abs_parent,
                                            self.path_rel_in)
        if self.path_abs_out.empty():
            self.path_abs_out = os.path.join(self.path_abs_parent, 
                                               self.path_rel_out)
        return True
        
    
    
class FileHandling():
    def __init__(self, _path_input:str):
        self.path_input = _path_input
        self._file_current = ""
        
    
    
    def open_all_files(self, subfolderCheck: bool=False) -> Tuple[List]:
        result = self.open_searched_files() # opens all files
        return result
    
    
    def open_searched_files(self, search_term:str="") -> Tuple[List]:
        subfolderCheck: bool=False
        
        path = self.path_input
        items = []
        filepaths = [] 
        for root, dirs, files in os.walk(path):
                for f in files: 
                    if search_term is None or search_term in str(f): 
                        filepath = self.editDir(path, str(f))
                        item = self.open_one_file(filepath)
                        items.append(item)
                        filepaths.append(filepath)
                if (subfolderCheck is False): 
                    break
        if not items: 
            print("ERROR: No files found")
        return (items, filepaths)
    
    
    def open_one_file(self, path_file:str):
        try:
            ImageCv = self._open_image_opencv(path_file)
        except Exception as e:
             print(f"ERROR: Cannot open image: \n{e}")
        return ImageCv
    
    
    def remove_one_file(self, path_file: str): 
        os.remove(path_file)
        return
    
    
    def _open_image_pillow(self, path_image: str) -> Image:
        return PilImg.open(path_image)
    
    def _open_image_opencv(self, path_image: str):
        return self._convert_image_pillow_to_opencv(self._open_image_pillow(path_image))
    
    def _convert_image_pillow_to_opencv(self, pil_image: Image):
        return cv2.cvtColor(np.array(pil_image), cv2.COLOR_RGB2BGR)
    
    def _convert_image_opencv_to_pillow(self, cv_image) -> Image:
        return PilImg.fromarray(cv2.cvtColor(cv_image, cv2.COLOR_BGR2RGB))