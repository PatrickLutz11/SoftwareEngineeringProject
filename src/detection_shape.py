import cv2
from typing import List, Dict, Tuple
from abc import abstractmethod

from handling_configurations import ConfigReader
from detection_color import ColorDetector

BGR_COLORS = ConfigReader("config.json").get_value('BGR_COLORS')


class Detection:
    """Functions to detect shape and recognize it"""
    @abstractmethod
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
        minimum_area_for_shape = int(area_of_img/ratio_image_to_shape)

        blurred = cv2.GaussianBlur(gray_img, (5, 5), 0)
        thresholded = cv2.adaptiveThreshold(blurred, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 11, 2)
        
        contours, _ = cv2.findContours(thresholded, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        found_shapes = sorted(contours, key=cv2.contourArea, reverse=True)[1:] # excluding background
        
        filtered_shapes = FilterShapes.minimum_shape_size(found_shapes, 
                                                          minimum_area_for_shape)
        filtered_shapes = FilterShapes.minimum_center_distance(filtered_shapes,
                                                               miniumum_distance=2)
        
        if False: # Debugging 
            cv2.imshow("gray", gray_img)
            cv2.imshow("blurred", blurred)
            cv2.imshow("thresholded", thresholded)
            img_contours = cv2.drawContours(img, filtered_found_shapes, -1, (120, 255, 0), 1)
            cv2.imshow("Contours", img_contours)
            print(len(contours))
            print(len(found_shapes))
            print(len(filtered_found_shapes))
        
        return filtered_shapes 

    @abstractmethod
    def shape_recognition(found_shapes:List, img:cv2.typing.MatLike) -> List[Dict[str, str]]:
        """Identification of found shapes

        Args:
            found_shapes (List): List of found shapes within the image
            img (cv2.typing.MatLike): The image with shapes
            
        Returns:
            List[Dict[str, str]]: List of recognized shapes with pattern and color
        """
        recognized_shapes = []  # List to store recognized shapes
        for shape in found_shapes:            
            define_shape = cv2.approxPolyDP(shape, 0.01 * cv2.arcLength(shape, True), True)
            shape_color = ColorDetector().get_color(img, shape)
            shape_name = "Circle"
            
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
                shape_name = "Pentagon"
            
            if len(define_shape) == 6:
                shape_name = "Hexagon"
            
            
            cv2.drawContours(img, [shape], 0, BGR_COLORS["CYAN"], 5)
            
            text = f'{shape_name}, {shape_color}'
            coords_text = OperationShapes.get_shape_center(shape)
            img = TextPlacer.place_text(img, text, coords_text)
            
            recognized_shapes.append({'pattern': shape_name, 'color': shape_color})
        return recognized_shapes
    

class FilterShapes:
    @staticmethod
    def minimum_shape_size(found_shapes:List[cv2.typing.MatLike], 
                                  minimum_area_for_shape:int
                                  )->List[cv2.typing.MatLike]:
        """
        Apply minimum area shape filter onto shapes.
        Shapes with smaller area will be removed. 
        
        Args:
            found_shapes (List[cv2.typing.MatLike]): List of shapes
            miniumum_area_for_shape (int): required minimum area of shape

        Returns:
            List[cv2.typing.MatLike]: List of filtered shapes. Empty, otherwise.
        """
        filtered_found_shapes = []
        for shape in found_shapes:
            area = cv2.contourArea(shape)
            if minimum_area_for_shape > area:
                break
            filtered_found_shapes.append(shape)
        return filtered_found_shapes
    
    @staticmethod
    def minimum_center_distance(found_shapes:List[cv2.typing.MatLike], 
                                      miniumum_distance:int=2
                                      )->List[cv2.typing.MatLike]:
        """
        Apply minimum center distance filter onto shapes.
        Shapes with smaller center distance will be removed. 

        Args:
            found_shapes (List[cv2.typing.MatLike]): List of shapes
            miniumum_distance (int, optional): Minimum distance which needs to be exceeded. Defaults to 2.

        Returns:
            List[cv2.typing.MatLike]: List of filtered shapes. Empty, otherwise.
        """
        filtered_found_shapes = []
        center_points = [(0,0)]
        
        for shape in found_shapes:
            center_point_new = OperationShapes.get_shape_center(shape)
            
            center_exists:bool = False
            for center in center_points:
                x_delta = abs(center[0]-center_point_new[0])
                y_delta = abs(center[1]-center_point_new[1])
                if (x_delta <= miniumum_distance) or (y_delta <= miniumum_distance):
                    center_exists = True
            
            if center_exists == True:
                continue
            center_points.append(center_point_new)
            filtered_found_shapes.append(shape)
        return filtered_found_shapes


class OperationShapes:
    @staticmethod
    def get_shape_center(shape:cv2.typing.MatLike)->Tuple[int, int]:
        """Get center of shape.

        Args:
            shape (cv2.typing.MatLike): Selected shape to determine center.

        Returns:
            Tuple[int, int]: Coordinates of shape center.
        """
        shape_points = cv2.moments(shape) 
        x_coord = 0
        y_coord = 0
        if shape_points['m00'] != 0.0: 
            x_coord = int(shape_points['m10']/shape_points['m00'])
            y_coord = int(shape_points['m01']/shape_points['m00']) 
        return x_coord, y_coord


class TextPlacer:
    @staticmethod
    def place_text(img:cv2.typing.MatLike, text:str, 
                   coords_text:Tuple[int, int])->cv2.typing.MatLike:
        """
        Places text onto image at given coordinates.

        Args:
            img (cv2.typing.MatLike): Image, onto which text is placed.
            text (str): Text, which should be placed
            coords_text (Tuple[int, int]): coordinates of text center.

        Returns:
            cv2.typing.MatLike: Image with placed text. 
        """
        font = {
                'face' : cv2.FONT_HERSHEY_SIMPLEX,
                'scale' : 0.8,
                'color' : BGR_COLORS["BLACK"],
                'thickness' : 2
            }
        text_size, baseline = cv2.getTextSize(text, font["face"], font["scale"], font["thickness"])
        x, y = coords_text
        text_coord = (int(x-text_size[0]/2), y)
        
        new_img = cv2.putText(img, text, text_coord, 
                        font["face"], font["scale"], font["color"], font["thickness"])
        return new_img

        
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

