import os
import numpy as np
import cv2
from PIL import Image as PilImg
from PIL.Image import Image
from typing import List, Tuple

VALID_TYPES = [".jpg", ".png"]

class PathHandling():
    def __init__(self, _path_abs_in: str="", ) -> None:
        self.path_rel_in = "in"
        self.path_rel_out = "out"
        
        self.path_abs_parent = ""
        self.path_abs_in = ""
        self.path_abs_out = ""

        if (len(_path_abs_in)>0) and IntegrityChecker.check_path_validity(_path_abs_in):
            self.path_abs_in = _path_abs_in

        
    def get_path_abs_parent(self) -> str:
        """get parent folder as absolute path

        Returns:
            str: path of parent folder
        """
        self._create_abs_paths()
        return self.path_abs_parent
    
    
    def get_path_abs_input(self) -> str:
        """get input folder as absolute path

        Returns:
            str: path of input folder
        """
        self._create_abs_paths()
        return self.path_abs_in
    
    
    def get_path_abs_output(self) -> str:
        """get output folder as absolute path

        Returns:
            str: path of output folder
        """
        self._create_abs_paths()
        return self.path_abs_out
    
    
    def _create_abs_paths(self) -> bool:
        """creates absolute paths for parent, input and output

        Returns:
            bool: True, if successful. False, otherwise.
        """
        if not self.path_abs_parent:
            self.path_abs_parent = os.getcwd()
            
        if not self.path_abs_in:
            self.path_abs_in = os.path.join(self.path_abs_parent,
                                            self.path_rel_in)
        if not self.path_abs_out:
            self.path_abs_out = os.path.join(self.path_abs_parent, 
                                               self.path_rel_out)
        return True
        
    
    
class FileHandling():
    def __init__(self, _path_input:str=""):
        self.path_input = _path_input
        self._file_current = ""
        
    
    
    def open_all_files(self) -> Tuple[List]:
        """opens all files in folder

        Returns:
            Tuple[List]: Tuple with lists aof images and paths
                    - Tuple[0] cv2.typing.MatLike:  images
                    - Tuple[1] str:                 paths of images
        """
        result = self.open_searched_files() # opens all files
        return result
    
    
    def open_searched_files(self, search_term:str="") -> Tuple[List]:
        """opens all files which contain search term (file name or type). 
        If no search term is given, it opens all files. 

        Args:
            search_term (str, optional): search term for specific files or 
                                         file types. 
                                         Defaults to "", opens all files.

        Returns:
            Tuple[List]: Tuple with lists aof images and paths
                    - Tuple[0] cv2.typing.MatLike:  images
                    - Tuple[1] str:                 paths of images
        """
        subfolderCheck: bool=False
        
        path = self.path_input
        items = []
        filenames = [] 
        for root, dirs, files in os.walk(path):
                for file in files: 
                    file = str(file)
                    if not(search_term) or search_term in file: 
                        if IntegrityChecker.check_file_type(file):
                            filepath = os.path.join(path, file)
                            item = self.open_one_file(filepath)
                            items.append(item)
                            filenames.append(file)
                if (subfolderCheck is False): 
                    break
        if not items: 
            print("ERROR: No files found")
        return (items, filenames)
    
    
    def open_one_file(self, path_file:str):
        try:
            ImageCv = ImageConverter().open_image_opencv(path_file)
        except Exception as e:
             print(f"ERROR: Cannot open image: \n{e}")
             return None
        return ImageCv
    
    
    def remove_one_file(self, path_file: str): 
        os.remove(path_file)
        return
      
    

class ImageConverter:
    """use pillow to open an image (more types are supported) and converts it to openCV image. 
    """
    def open_image_opencv(self, path_image: str)->cv2.typing.MatShape:
        """opens an image in openCV format with pillow

        Args:
            path_image (str): path to image

        Returns:
            cv2.typing.MatShape: image in openCV format
        """
        return self.convert_image_pillow_to_opencv(self.open_image_pillow(path_image))
    
    def open_image_pillow(self, path_image: str) -> Image:
        """opens an image with pillow

        Args:
            path_image (str): path to image

        Returns:
            Image: image in pillow format
        """ 
        return PilImg.open(path_image)
    
    def convert_image_pillow_to_opencv(self, pil_image: Image) -> cv2.typing.MatLike:
        """converts image from pillow into openCV format

        Args:
            pil_image (Image): image in pillow format

        Returns:
            cv2.typing.MatLike: image in openCV format
        """
        return cv2.cvtColor(np.array(pil_image), cv2.COLOR_RGB2BGR)
    
    def convert_image_opencv_to_pillow(self, cv_image:cv2.typing.MatLike) -> Image:
        """converts image from openCV into pillow format

        Args:
            cv_image (cv2.typing.MatLike): image in openCV format

        Returns:
            Image: image in pillow format
        """
        return PilImg.fromarray(cv2.cvtColor(cv_image, cv2.COLOR_BGR2RGB))
    
class IntegrityChecker:
    @staticmethod
    def check_path_validity(path:str, error_print:bool = True) -> bool:
        """checks if path exists

        Args:
            path (str): system path of directory, folder or file

        Returns:
            bool: True, if exists, otherwise False
        """
        if (os.path.exists(path)) is False: 
            if error_print:
                print(f"ERROR: This path does not exist! \n{path = }\n")
            return False
        return True
    
    @staticmethod
    def check_file_type(path:str) -> bool:
        """checks, if file type is supported

        Args:
            path (str): path of file

        Returns:
            bool: True, if supported. False, otherwise.
        """
        for endings in VALID_TYPES:
            if path.endswith(endings):
                return True
        return False