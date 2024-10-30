import cv2
from Detection import *
from PictureModifications import *

if __name__ == "__main__":

    img = cv2.imread('formen.png')
    
    searching_for_shapes = Detection.shape_detection(img)
    
    Detection.shape_recognition(searching_for_shapes, img)
    
    img = PictureModifications.resize_the_picture(img)
    
    cv2.imshow('shapes', img)
    cv2.waitKey(0) 
    cv2.destroyAllWindows()