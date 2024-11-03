import cv2
import numpy as np
from typing import List, Tuple

from config_reader_test import ConfigReader

BGR_COLORS = ConfigReader().get_bgr_color_dict()

class ColorDetector:
    def __init__(self):
        self. _range_spectrum = 15
    
    
    def get_color(self, img:cv2.typing.MatLike, shape:List) -> str:
        """Identifying the color of the found shapes

        Args:
            img (cv2.typing.MatLike): The image with shapes
            shape (List): Shapes found within the image

        Returns:
            str: str: The color of the shape. Empty string, if color is unkown.
        """        
        # mask section and get mean value
        mask = np.zeros(img.shape[:2], dtype="uint8")
        mask = cv2.drawContours(mask, [shape], -1, 255, -1)
        rgb_values_float = cv2.mean(img, mask=mask)[:3]
        rgb_values_int = np.array([[rgb_values_float]], dtype=np.uint8)
        
        # convert from RGB to HSV
        hsv_value = cv2.cvtColor(rgb_values_int, cv2.COLOR_BGR2HSV)
        detected_color = ""
        for name_color, values_color in BGR_COLORS.items():
            limits_lower, limits_upper = self.get_limits_hsv(values_color)
            
            mask_color_lower = cv2.inRange(hsv_value, 
                                           limits_lower[0], limits_lower[1])
            mask_color_upper = cv2.inRange(hsv_value, 
                                           limits_upper[0], limits_upper[1])
            
            if (mask_color_lower>0) or (mask_color_upper>0):
                detected_color = name_color
                break
        return detected_color # unkown color is ""
        
    
class ColorLimiter:
    def get_limits_hsv(self, color_bgr:List[int])->Tuple:
        color = np.array([[color_bgr]], dtype=np.uint8)
        hsv_color = cv2.cvtColor(color, cv2.COLOR_BGR2HSV)
        hue = hsv_color[0][0][0]
        hue_limits_lower = self._get_hue_limits_lower(int(hue))
        hue_limits_upper = self._get_hue_limits_upper(int(hue))
        limit_array_1 = self._get_limits_array(hue_limits_lower)
        limit_array_2 = self._get_limits_array(hue_limits_upper)
        
        return limit_array_1, limit_array_2
    
    def _get_hue_limits_lower(self, hue:int)->Tuple[np.uint8, np.uint8]:
        """get lower hue limits of color.

        Args:
            hue (int): hue of color

        Returns:
            Tuple[np.uint8, np.uint8]: both lower hue limits
        """
        lower_limit_1 = (hue-self._range_spectrum)%180
        lower_limit_2 = hue
        if (hue-self._range_spectrum < 0):
            lower_limit_2 = 180
        return lower_limit_1, lower_limit_2
    
    
    def _get_hue_limits_upper(self, hue:int)->Tuple[np.uint8, np.uint8]:
        """get upper hue limits of color.

        Args:
            hue (int): hue of color

        Returns:
            Tuple[np.uint8, np.uint8]: both upper hue limits
        """
        upper_limit_1 = hue
        upper_limit_2 = (hue+self._range_spectrum)%180
        if (hue+self._range_spectrum > 180):
            upper_limit_1 = 0
        return upper_limit_1, upper_limit_2
    
    
    def _get_hsv_limits(self, hue:Tuple[int, int])->Tuple[np.array, np.array]:
        """get limiter array of hues, saturations and values (HSV).

        Args:
            hue (Tuple[int, int]): lower and upper limits of hue

        Returns:
            Tuple[np.array, np.array]: Array first and second array limiter of HSV
        """
        lim1 = np.array([hue[0], 100, 100], dtype=np.uint8)
        lim2 = np.array([hue[1], 255, 255], dtype=np.uint8)
        return lim1, lim2




if __name__ == "__main__": 
    """Debugging of functions
    """
    from detection import Detection
    img = cv2.imread(R"in/test_image_03.jpg")#(R"in/test_image_03.jpg")
    cv2.imshow("test", img)
    shapes = Detection.shape_detection(img)
    print(len(shapes))
    
    print(BGR_COLORS['WHITE'])
    
    Detection.shape_recognition(shapes, img)
    cv2.imshow("newimage", img)

    if cv2.waitKey() == ord('q'):
        cv2.destroyAllWindows()