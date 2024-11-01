

import cv2
import numpy as np
from typing import List, Dict, Any

class Detection:
    @staticmethod
    def shape_detection(img: np.ndarray) -> List[np.ndarray]:
        """
        Detects contours (shapes) in the given image.

        Args:
            img (numpy.ndarray): The input image in BGR format.

        Returns:
            List[np.ndarray]: A list of detected contours.
        """
        gray_img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        blurred = cv2.GaussianBlur(gray_img, (5, 5), 0)
        thresholded = cv2.adaptiveThreshold(
            blurred,
            255,
            cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
            cv2.THRESH_BINARY,
            11,
            2
        )
        found_shapes, _ = cv2.findContours(
            thresholded,
            cv2.RETR_TREE,
            cv2.CHAIN_APPROX_SIMPLE
        )
        return found_shapes

    @staticmethod
    def shape_recognition(found_shapes: List[np.ndarray], img: np.ndarray) -> List[Dict[str, Any]]:
        """
        Identifies and annotates found shapes in the image.

        Args:
            found_shapes (List[np.ndarray]): Found shapes within the image.
            img (numpy.ndarray): The image with shapes.

        Returns:
            List[Dict[str, Any]]: A list of dictionaries containing details about each detected shape.
        """
        recognized_shapes = []
        i = 0  # Index to skip the first contour (usually the outer boundary)

        for shape in found_shapes:
            if i == 0:
                i = 1
                continue  # Skip the first contour
            i += 1

            # Approximate the shape to reduce the number of points
            peri = cv2.arcLength(shape, True)
            approx = cv2.approxPolyDP(shape, 0.01 * peri, True)
            vertices = len(approx)

            # Get the color of the shape
            shape_color = Detection.get_color(img, shape)

            # Calculate the centroid of the shape for labeling
            M = cv2.moments(shape)
            if M['m00'] != 0.0:
                cX = int(M['m10'] / M['m00'])
                cY = int(M['m01'] / M['m00'])
            else:
                cX, cY = 0, 0

            # Determine the shape type based on the number of vertices
            if vertices == 3:
                shape_type = "Triangle"
                color_bgr = (0, 255, 255)  # Yellow
            elif vertices == 4:
                # Compute the aspect ratio to distinguish between square and rectangle
                x, y, w, h = cv2.boundingRect(approx)
                aspect_ratio = float(w) / h
                if 0.95 <= aspect_ratio <= 1.05:
                    shape_type = "Square"
                    color_bgr = (0, 255, 0)  # Green
                else:
                    shape_type = "Rectangle"
                    color_bgr = (0, 0, 0)    # Black
            elif vertices == 5:
                shape_type = "Pentagon"
                color_bgr = (0, 0, 255)      # Red
            elif vertices == 6:
                shape_type = "Hexagon"
                color_bgr = (0, 255, 255)    # Yellow
            else:
                shape_type = "Circle"
                color_bgr = (0, 0, 255)      # Red

            # Draw the contour and label it on the image
            cv2.drawContours(img, [shape], -1, color_bgr, 5)
            cv2.putText(
                img,
                f"{shape_type}, {shape_color}",
                (cX - 50, cY),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.7,
                (255, 0, 255),
                2
            )

            # Append the detected shape details to the list
            shape_info = {
                'pattern': shape_type,
                'color': shape_color,
                'confidence': "High"  # Placeholder, can be adjusted based on additional metrics
            }
            recognized_shapes.append(shape_info)

        return recognized_shapes

    @staticmethod
    def get_color(img: np.ndarray, shape: np.ndarray) -> str:
        """
        Identifies the color of the given shape.

        Args:
            img (numpy.ndarray): The image with shapes in BGR format.
            shape (numpy.ndarray): The contour of the shape.

        Returns:
            str: The color of the shape.
        """
        # Create a mask for the shape
        mask = np.zeros(img.shape[:2], dtype="uint8")
        cv2.drawContours(mask, [shape], -1, 255, -1)

        # Compute the mean color within the mask
        mean = cv2.mean(img, mask=mask)[:3]  # BGR values

        # Define color ranges (these can be adjusted based on requirements)
        if 80 < mean[0] < 150 and 140 < mean[1] < 190 and 60 < mean[2] < 140:
            return "Green"
        elif 60 < mean[0] < 200 and 90 < mean[1] < 140 and 70 < mean[2] < 180:
            return "Blue"
        elif mean[0] < 100 and mean[1] < 100 and mean[2] > 150:
            return "Red"
        elif mean[0] < 100 and mean[1] > 100 and mean[2] > 150:
            return "Orange"
        elif mean[1] < 100 and mean[0] > 100 and mean[2] > 100:
            return "Violet"
        else:
            return "Unknown Color"
