import cv2
import numpy as np
from typing import List

BGR_COLORS = {
    "BLUE" : [255, 0, 0],
    "GREEN" : [0, 255, 0],
    "RED" : [0, 0, 255],
    "MANGENTA": [255, 0, 255],
    "CYAN" : [255, 255, 0],
    "YELLOW": [0, 255, 255],
    "BLACK": [0, 0, 0],
    "WHITE": [255, 255, 255],
}

def get_limits_hsv(color_bgr:List):
    color = np.array([[color_bgr]], dtype=np.uint8)
    hsv_color = cv2.cvtColor(color, cv2.COLOR_BGR2HSV)
    
    lower_limit = hsv_color[0][0][0] - 10, 100, 100
    upper_limit = hsv_color[0][0][0] + 10, 255, 255
    
    lower_limit = np.array(lower_limit, dtype=np.uint8)
    upper_limit = np.array(upper_limit, dtype=np.uint8)
    
    return lower_limit, upper_limit


if __name__ == "__main__":
    width_img = 500
    height_img = 500
    image = np.zeros((height_img, width_img, 3), np.uint8) # Color = BLACK
    image[:] = (255, 0, 0) # Color = BLUE
    image_hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
    hue, saturation, value = cv2.split(image_hsv)
    lim_low, lim_high = get_limits_hsv(BGR_COLORS["BLUE"])
    mask = cv2.inRange(image_hsv, get_limits_hsv(BGR_COLORS["BLUE"]))
    
    print(mask.shape[:2])
    while True:
        image_hsv = cv2.merge([hue, saturation, value])
        cv2.imshow("image_hsv", image_hsv)
        if cv2.waitKey(1) == ord('q'):
            break



