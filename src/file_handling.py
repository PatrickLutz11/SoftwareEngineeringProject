"""
@data:      file_handling.py
@author:    Jannis Mathiuet
@versions:  ver 0.0.0 - 31.03.2024 - Jannis Mathiuet
            ver 0.1.0 - 05.04.2024 - Jannis Mathiuet
            ver 1.0.0 - 20.05.2024 - Jannis Mathiuet
@desc: 
    programm to handle paths and files
    If there are any questions or problems, please contact me.
"""
import os
from PIL import Image as imageMain
from PIL.Image import Image
import cv2
import pdf2image
import tempfile
import shutil
import numpy as np
from typing import List, Tuple

# =============================================================================
# PUBLIC FUNCTIONS
# =============================================================================
class FileHandling(): 
    # =========================================================================
    # Path Functions (PUBLIC)
    # =========================================================================
    def __init__(self, inRelPath: str="in", outRelPath: str="out", 
                 configRelPath: str="config", debug: bool=False): 
        
        DIR_PARENT = self._setDirParent()
        DIR_INPUT = self._setDirInput(inRelPath)
        DIR_OUTPUT = self._setDirOutput(outRelPath)
        DIR_CONFIG = self._setDirConfig(configRelPath)
        CLASS_DEBUG = debug
        
        if CLASS_DEBUG is True:
            print(DIR_PARENT)
            print(DIR_INPUT)
            print(DIR_OUTPUT)
            print(CLASS_DEBUG)
        
        return None
    
    def getDirParent(self):
        global DIR_PARENT
        return DIR_PARENT
    
    def getDirInput(self):
        global DIR_INPUT
        return DIR_INPUT
    
    def getDirOutput(self):
        global DIR_OUTPUT
        return DIR_OUTPUT
    
    def getDirConfig(self):
        global DIR_CONFIG
        return DIR_CONFIG
    
    def getDirLogos(self):
        global DIR_CONFIG
        return self.editDir(DIR_CONFIG, "logos")
    
    def getAbsDir(self):
        path = os.getcwd()
        # path = self._removePathEndings(path, remove)
        return path
    
    def editDir(self, path, *folders, remove: np.uint=0, create: bool=False) :
        newpath = self._removePathEndings(path, remove)
        
        folderpath = ""
        for folder in folders :
            banned = ["", " "]
            if folder not in banned: 
                folderpath = os.path.join(folderpath, folder)
        newpath = os.path.join(path, folderpath)
        if not (self.checkValidPath(newpath)):
            if (create): 
                self.createFolders(newpath)
        return newpath
    
    def createFolders(self, pathToFolder):
        if not (self.checkValidPath(pathToFolder)):
            os.makedirs(pathToFolder)
        return None
    
    def checkValidPath(self, path):
        if (os.path.exists(path)) is False: 
            print(f"\nThis path does not currently exist! \n{path = }\n")
            return False
        return True
    
    # Remove all files/directories inside a folder
    def clearFolder(self, pathToFolder):
        for root, dirs, files in os.walk(pathToFolder):
            for f in files:
                os.unlink(os.path.join(root, f))
            for d in dirs:
                shutil.rmtree(os.path.join(root, d))
        return None
    
    # -------------------------------------------------------------------------
    # Path Functions (PRIVATE)
    # -------------------------------------------------------------------------
    DIR_PARENT = ""
    DIR_INPUT = ""
    DIR_OUTPUT = ""
    CLASS_DEBUG = False
    
    def _setDirParent(self):
        global DIR_PARENT
        DIR_PARENT = self.getAbsDir()
        return self.getAbsDir()

    def _setDirInput(self, relpath: str):
        path = self.getDirParent()
        newpath = self.editDir(path, relpath)
        global DIR_INPUT 
        DIR_INPUT = newpath
        return newpath

    def _setDirOutput(self, relpath: str):
        path = self.getDirParent()
        newpath = self.editDir(path, relpath)
        global DIR_OUTPUT 
        DIR_OUTPUT = newpath
        return newpath
    
    def _setDirConfig(self, relPath: str):
        path = self.getDirParent()
        newpath = self.editDir(path, relPath)
        global DIR_CONFIG
        DIR_CONFIG = newpath
        return newpath
    # =========================================================================
    # Files Functions (PUBLIC)
    # =========================================================================
    # all Functions are inspired from Leo Ertuna
    # source: https://github.com/JPLeoRX/opencv-text-deskew/blob/master/python-service/services/graphics_service.py
    def openAllFiles(self, subfolderCheck: bool=False) -> Tuple[List]:
        path = self.getDirInput()
        result = self.openSearchedFiles() # opens all files
        return result
    
    def openSearchedFiles(self, searchTerm: str=None):
        subfolderCheck: bool=False
        
        path = self.getDirInput()
        items = []
        filepaths = [] 
        for root, dirs, files in os.walk(path):
                for f in files: 
                    if searchTerm is None or searchTerm in str(f): 
                        filepath = self.editDir(path, str(f))
                        item = self.openOneFile(filepath)
                        items.append(item)
                        filepaths.append(filepath)
                if (subfolderCheck is False): 
                    break
        if not items: 
            print("No files found")
        return (items, filepaths)
    
    def openOneFile(self, path: str):
        if ".pdf" in path:
            print("PDF detected")
            return
        try:
            ImageCv = self._openImageCv(path)
        except Exception as e:
             print(f"Error during opening of image: \n{e}")
        return ImageCv
    
    def removeOneFile(self, path: str): 
        os.remove(path)
        return
    
    def convertPilImageToCvImage(self, pilImage: Image):
        return cv2.cvtColor(np.array(pilImage), cv2.COLOR_RGB2BGR)

    def convertCvImagetToPilImage(self, cvImage) -> Image:
        return imageMain.fromarray(cv2.cvtColor(cvImage, cv2.COLOR_BGR2RGB))

    # -------------------------------------------------------------------------
    # Files Functions (PRIVATE)
    # -------------------------------------------------------------------------
    # all Functions are from Leo Ertuna
    # source: https://github.com/JPLeoRX/opencv-text-deskew/blob/master/python-service/services/graphics_service.py
    def _openImagePil(self, imagePath: str) -> Image:
        return imageMain.open(imagePath)

    def _openImageCv(self, imagePath: str):
        return self.convertPilImageToCvImage(self._openImagePil(imagePath))
    
    # Render one page of a PDF document to image
    def _renderPdfDocumentPageToImageFromPath(self, pdfDocPath: str, pageNumber: int, dpi: int) -> str:
        tempFolder = tempfile.gettempdir()
        pageImagePaths = pdf2image.convert_from_path(pdfDocPath, dpi=dpi, output_folder=tempFolder, fmt='png', paths_only=True, thread_count=1, first_page=pageNumber, last_page=pageNumber)
        return pageImagePaths[0]
    
    def _removePathEndings(self, path, cntremove: np.uint=1):
        if cntremove is None:
            return path
        try: 
            cntremove = int(cntremove)
        except RuntimeError as error: 
            print(error)
            print("cntremove must be an integer")
    
        if cntremove < 0 :
            raise Exception(f"The number should be higher than 0. ({cntremove=})")
    
        for i in range(cntremove): 
            path, element = os.path.split(path)
            # path = os.path.join(path, os.pardir)
        newpath = path
    
        return newpath

# =============================================================================
#     def chooseFile(self, path: str, **kwargs) :
#         # kwargs list
#         ftype = kwargs.get('ftype', None) # file type
#         fname = kwargs.get('fname', None) # file name
#         # depth = kwargs.get('depth', 0)
#         dircs = kwargs.get('dircs', [""]) 
#     
#         # select path
#         newpath = path
#         for dirc in dircs :    
#             newpath = os.path.join(newpath, dirc)
#             if (os.path.exists(newpath)) is False: 
#                 print(f"\nThis path does not exist! Try another one. \n{newpath = }\n")
#     
#     
#         d_limiter = 0
#         for (root, dirs, files) in os.walk(path):
#             if ftype is None : 
#                 print(f"Directory ({len(dirs)}): {dirs} ")
#                 print(f"Files     ({len(files)}): {files} ")
#                 
#             if ftype and fname is type(str): 
#                 for file in files:
#                     if (ftype.endswith(file)):
#                         if (fname in file):
#                             print(file)            
#             if d_limiter == 0: 
#                 break
#             d_limiter += 1
#             # for f in file:
#             #     f.conta
#             #     for ftype in f:
#             #         for fname in f:
#             #         if fname is None: 
#             #             print(f)
#             #         if k_ele is element: 
#             #             filepath = os.path.join(newpath, f)
#             #             return filepath
#             #         k_ele += 1
#         return path
# =============================================================================
