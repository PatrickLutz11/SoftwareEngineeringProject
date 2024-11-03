import cv2
import numpy as np
from typing import List, Dict, Tuple

from config_reader_test import ConfigReader
from detection_color import ColorDetector

BGR_COLORS = ConfigReader().get_bgr_color_dict()

class Detection:
    def shape_detection(img:cv2.typing.MatLike, ratio_image_to_shape:int=100) -> List:
        """Shape detection from the image

        Args:
            img (cv2.typing.MatLike): The image with shapes
            ratio_image_to_shape (float): Ratio of image to shape, i.e. 
                                          how many times the image is bigger 
                                          than the shape. Defaults to 100.

        Returns:
            List: The shapes within the image
        """
        gray_img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY) 
        area_of_img = gray_img.shape[0]*gray_img.shape[1]
        miniumum_area_for_shape = int(area_of_img/ratio_image_to_shape)

        blurred = cv2.GaussianBlur(gray_img, (5, 5), 0)
        
        thresholded = cv2.adaptiveThreshold(blurred, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 11, 2)
        
        contours, _ = cv2.findContours(thresholded, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        found_shapes = sorted(contours, key=cv2.contourArea, reverse=True) # excluding background
        
        filtered_found_shapes = []
        center_points = [(0,0)]
        for shape in found_shapes:
            area = cv2.contourArea(shape)
            if miniumum_area_for_shape > area:
                break
            
            center_point_new = Detection.get_shape_center(shape)
            
            center_exists:bool = False
            for center in center_points:
                x_delta = abs(center[0]-center_point_new[0])
                y_delta = abs(center[1]-center_point_new[1])
                if x_delta <= 2 or y_delta <= 2:
                    center_exists = True
            if center_exists == True:
                continue
            
            center_points.append(center_point_new)
            filtered_found_shapes.append(shape)
        """
         print(center_point_new, center_points)
                print(len(filtered_found_shapes))
                print(f"\r\n")
        """
                #continue
            #print(center_point_new)
            #center_points.append(center_point_new)
            #filtered_found_shapes.append(shape)
        
        
        # Debugging 
        if False: 
            cv2.imshow("gray", gray_img)
            cv2.imshow("blurred", blurred)
            cv2.imshow("thresholded", thresholded)
            img_contours = cv2.drawContours(img, filtered_found_shapes, -1, (120, 255, 0), 1)
            cv2.imshow("Contours", img_contours)
            print(len(contours))
            print(len(found_shapes))
            print(len(filtered_found_shapes))
        
        return filtered_found_shapes 

            
    def shape_recognition(found_shapes:List, img:cv2.typing.MatLike) -> List[Dict[str, str]]:
        """Identification of found shapes

        Args:
            found_shapes (List): List of found shapes within the image
            img (cv2.typing.MatLike): The image with shapes
            
        Returns:
            List[Dict[str, str]]: List of recognized shapes with pattern and color
        """
        recognized_shapes = []  # List to store recognized shapes
        print("Shape detection:", len(found_shapes))
        i = 0
        for shape in found_shapes:
            if i == 0:
                i = 1
                continue
            
            define_shape = cv2.approxPolyDP(shape, 0.01 * cv2.arcLength(shape, True), True)
            print(len(define_shape))
            i += 1
            shape_color = ColorDetector().get_color(img, shape)
            shape_name = "Circle"
            """
            shape_points = cv2.moments(shape) 
            if shape_points['m00'] != 0.0: 
                x = int(shape_points['m10']/shape_points['m00']) - 100
                y = int(shape_points['m01']/shape_points['m00']) 
            """
            
            if len(define_shape) == 3:
                shape_name = "Triangle"
            
            if len(define_shape) == 4:
                (x1, y1, w, h) = cv2.boundingRect(define_shape)
                aspect_ratio = float(w) / h
                if 0.95 <= aspect_ratio <= 1.05:
                    shape_name = "Square"
                else:
                    shape_name = "Rectangle"
            
            if len(define_shape) == 5:
                shape_name = "Pentacle"
            
            if len(define_shape) == 6:
                shape_name = "Hexagram"
            """
            if len(define_shape) == 3:
                cv2.drawContours(img, [shape], 0, (0, 255, 255), 5)
                cv2.putText(img, f'Triangle, {shape_color}', (x, y), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 255), 2) 
                
            elif len(define_shape) == 4:
                (x1, y1, w, h) = cv2.boundingRect(define_shape)
                aspect_ratio = float(w) / h
                
                if 0.95 <= aspect_ratio <= 1.05:
                    cv2.drawContours(img, [shape], 0, (0, 255, 0), 5)
                    cv2.putText(img, f'Square, {shape_color}', (x, y), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 255), 2)
                else:
                    cv2.drawContours(img, [shape], 0, (0, 0, 0), 5)
                    cv2.putText(img, f'Rectangle, {shape_color}', (x, y), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 255), 2)
                
            elif len(define_shape) == 5:
                cv2.drawContours(img, [shape], 0, (0, 0, 255), 5)
                cv2.putText(img, f'Pentacle, {shape_color}', (x, y), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 255), 2)
                
            elif len(define_shape) == 6:
                cv2.drawContours(img, [shape], 0, (0, 255, 255), 5)
                cv2.putText(img, f'Hexagram, {shape_color}', (x, y), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 255), 2)
            else:
                cv2.drawContours(img, [shape], 0, BGR_COLORS["BLACK"], 5)
                cv2.putText(img, f'Circle, {shape_color}', (x, y), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 255), 2)
            """
            x_coord_text, y_coord_text = Detection.get_shape_center(shape)
            cv2.drawContours(img, [shape], 0, BGR_COLORS["CYAN"], 5)
            print(shape_name, shape_color, (x_coord_text, y_coord_text))
            text = f'{shape_name}, {shape_color}'
            font_face = cv2.FONT_HERSHEY_SIMPLEX
            font_scale = 0.8
            font_color = BGR_COLORS["BLACK"]
            font_thickness = 2

            text_size, baseline = cv2.getTextSize(text, font_face, font_scale, font_thickness)
            text_coord = (int(x_coord_text-text_size[0]/2), y_coord_text)
            
            cv2.putText(img, text, text_coord, 
                        font_face, font_scale, font_color, font_thickness)
            recognized_shapes.append({'pattern': shape_name, 'color': shape_color})
        print(f"\r\n\n")
        return recognized_shapes
    
    def get_shape_center(mask_shape:cv2.typing.MatLike)->Tuple[int, int]:
        shape_points = cv2.moments(mask_shape) 
        x_coord = 0
        y_coord = 0
        if shape_points['m00'] != 0.0: 
            x_coord = int(shape_points['m10']/shape_points['m00'])
            y_coord = int(shape_points['m01']/shape_points['m00']) 
        return x_coord, y_coord



if __name__ == "__main__": 
    """Debugging of functions
    """
    img = cv2.imread(R"in/test_image_03.jpg")#(R"in/test_image_03.jpg")
    cv2.imshow("test", img)
    shapes = Detection.shape_detection(img)
    print(len(shapes))

    Detection.shape_recognition(shapes, img)
    cv2.imshow("newimage", img)

    if cv2.waitKey() == ord('q'):
        cv2.destroyAllWindows()

