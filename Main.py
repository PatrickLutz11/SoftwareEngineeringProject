##Software Engineering Project
##Group B
##
##
import cv2
from abc import ABC, abstractmethod

class Shape(ABC):

    @abstractmethod
    def __str__(self) -> str:
        pass

class Circle(Shape):
    def __init__(self, radius: float) -> None:
        self.radius = radius

    def __str__(self) -> str:
        return f"Circle with a radius of {self.radius}"

class Triangle(Shape):

    def __init__(self, width: float, height: float) -> None:
        self.width = width
        self.height = height

    def __str__(self) -> str:
        return f"Triangle with a base {self.width} and height {self.height}"
     
class Rectangle(Shape):

    def __init__(self, width: float, height: float) -> None:
        self.width = width
        self.height = height

    # def calculate_area(self) -> float:
    #     return self.width * self.height

    def __str__(self) -> str:
        return f"Rectangle with height {self.height} and width {self.width}"
    
class Pentacle(Shape):

    def __init__(self, width: float, height: float) -> None:
        self.width = width
        self.height = height

    def __str__(self) -> str:
        return f"Pentacle with height {self.height} and width {self.width}"
      
class Hexagram(Shape):

    def __init__(self, width: float, height: float) -> None:
        self.width = width
        self.height = height

    def __str__(self) -> str:
        return f"Hexagram with height {self.height} and width {self.width}"

class detection:
    def shape_detection(img):
        gray_img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY) 

        blurred = cv2.GaussianBlur(gray_img, (5, 5), 0)
        
        thresholded = cv2.adaptiveThreshold(blurred, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 11, 2)
        edged = cv2.Canny(thresholded, 30, 200)
        
        found_shapes, _ = cv2.findContours(thresholded, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)      
        
        return found_shapes

            
    def shape_recognition(found_shapes):
        i = 0
        for shape in found_shapes:
            if i == 0:
                i = 1
                continue
            define_shape = cv2.approxPolyDP(shape, 0.01 * cv2.arcLength(shape, True), True)
            
            M = cv2.moments(shape) 
            if M['m00'] != 0.0: 
                x = int(M['m10']/M['m00'])
                y = int(M['m01']/M['m00']) 
            
            if len(define_shape) == 3:
                cv2.drawContours(img, [shape], 0, (0, 255, 255), 5)
                cv2.putText(img, 'Triangle', (x, y), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2) 
                # triangle = Triangle(width = y, height = x)
                # print(triangle)
                
            # elif len(define_shape) == 4:
            #     cv2.drawContours(img, [shape], 0, (0, 0, 0), 5)
            #     cv2.putText(img, 'Rectangle', (x, y), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2) 
            #     # rectangle = Rectangle(width = x, height = y)
            #     # print(rectangle)
                
            elif len(define_shape) == 4:
                # Prüfen, ob es ein Quadrat ist
                (x1, y1, w, h) = cv2.boundingRect(define_shape)
                aspect_ratio = float(w) / h
                
                if 0.95 <= aspect_ratio <= 1.05:  # Nahezu gleiche Seitenlängen
                    cv2.drawContours(img, [shape], 0, (0, 255, 0), 5)
                    cv2.putText(img, 'Square', (x, y), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)
                    # square = Rectangle(width = w, height = h)  # Du könntest hierfür auch eine separate Square-Klasse erstellen
                    # print(square)
                else:
                    cv2.drawContours(img, [shape], 0, (0, 0, 0), 5)
                    cv2.putText(img, 'Rectangle', (x, y), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)
                    # rectangle = Rectangle(width = w, height = h)
                    # print(rectangle)
                
            elif len(define_shape) == 5:
                cv2.drawContours(img, [shape], 0, (0, 0, 255), 5)
                cv2.putText(img, 'Pentacle', (x, y), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2) 
                # pentacle = Pentacle(width = x, height = y)
                # print(pentacle)
                
            elif len(define_shape) == 6:
                cv2.drawContours(img, [shape], 0, (0, 255, 255), 5)
                cv2.putText(img, 'Hexagram', (x, y), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2) 
                # hexagram = Hexagram(width=x, height=y)
                # print(hexagram)   
                
            else:
                cv2.drawContours(img, [shape], 0, (0, 0, 255), 5)
                cv2.putText(img, 'Circle', (x, y), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2) 
                # circle = Circle(radius=1)
                # print(circle)

class picture_modifications:
    def resize_the_picture(img):
        scale = 70
        width = int(img.shape[1] * scale / 100)
        height = int(img.shape[0] * scale / 100)

        resized_img = cv2.resize(img, (width, height), interpolation=cv2.INTER_AREA)
        return resized_img


if __name__ == "__main__":
    img = cv2.imread('formen.png')
    
    searching_for_shapes = detection.shape_detection(img)
    
    detection.shape_recognition(searching_for_shapes)
    
    img = picture_modifications.resize_the_picture(img)
    
    cv2.imshow('shapes', img)
    cv2.waitKey(0) 
    cv2.destroyAllWindows() 
    