import cv2
import numpy as np
from typing import List, Tuple

class Detection:
    
    def shape_detection(img) -> List:
        gray_img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY) 

        blurred = cv2.GaussianBlur(gray_img, (5, 5), 0)
        
        thresholded = cv2.adaptiveThreshold(blurred, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 11, 2)
        
        found_shapes, _ = cv2.findContours(thresholded, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)      
        
        return found_shapes

            
    def shape_recognition(found_shapes,img) -> None:
        i = 0
        for shape in found_shapes:
            if i == 0:
                i = 1
                continue
            
            define_shape = cv2.approxPolyDP(shape, 0.01 * cv2.arcLength(shape, True), True)
            shape_color = Detection.get_color(img, shape)
            
            shape_points = cv2.moments(shape) 
            if shape_points['m00'] != 0.0: 
                x = int(shape_points['m10']/shape_points['m00']) - 100
                y = int(shape_points['m01']/shape_points['m00']) 
             
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
                cv2.drawContours(img, [shape], 0, (0, 0, 255), 5)
                cv2.putText(img, f'Circle, {shape_color}', (x, y), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 255), 2)
                
                
    def get_color(img, shape) -> str:
        mask = np.zeros(img.shape[:2], dtype="uint8")
        cv2.drawContours(mask, [shape], -1, 255, -1)
        
        rgb_values = cv2.mean(img, mask=mask)[:3]

        if 80 < rgb_values[0] < 150 and 140 < rgb_values[1] < 190 and 60 < rgb_values[2] < 140:
            return "Green"
        
        elif 60 < rgb_values[0] < 200 and 90 < rgb_values[1] < 140 and 70 < rgb_values[2] < 180:
            return "Blue"
        
        elif rgb_values[0] < 100 and rgb_values[1] < 100 and rgb_values[2] > 150:
            return "Red"
        
        elif rgb_values[0] < 100 and rgb_values[1] > 100 and 150 < rgb_values[2]:
            return "Orange"
        
        elif rgb_values[1] < 100 and rgb_values[0] > 100 and rgb_values[2] > 100:
            return "Violet"
        
        else:
            return "Unknown Color"