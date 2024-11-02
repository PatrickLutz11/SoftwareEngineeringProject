"""Module for detecting and recognizing shapes in images.

This module provides functionality to detect shapes in images and identify their
patterns and colors using computer vision techniques.
"""

from typing import Dict, List, Tuple

import cv2
import numpy as np
from numpy.typing import NDArray


class Detection:
    """Class for shape detection and recognition in images."""

    # Color recognition thresholds
    COLOR_RANGES = {
        "Green": ((80, 140, 60), (150, 190, 140)),
        "Blue": ((60, 90, 70), (200, 140, 180)),
        "Red": ((0, 0, 150), (100, 100, 255)),
        "Orange": ((0, 100, 150), (100, 255, 255)),
        "Violet": ((100, 0, 100), (255, 100, 255))
    }

    @staticmethod
    def shape_detection(
        img: NDArray, 
        ratio_image_to_shape: int = 100
    ) -> List[NDArray]:
        """Detect shapes in the given image.

        Args:
            img: The input image as a numpy array.
            ratio_image_to_shape: Ratio determining minimum shape size.
                Defaults to 100.

        Returns:
            List of detected shape contours.

        Raises:
            ValueError: If the input image is None or empty.
        """
        if img is None or img.size == 0:
            raise ValueError("Input image is empty or None")

        # Convert to grayscale and calculate minimum area
        gray_img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        area_of_img = gray_img.shape[0] * gray_img.shape[1]
        minimum_area = int(area_of_img / ratio_image_to_shape)

        # Apply image processing
        blurred = cv2.GaussianBlur(gray_img, (5, 5), 0)
        thresholded = cv2.adaptiveThreshold(
            blurred, 
            255, 
            cv2.ADAPTIVE_THRESH_GAUSSIAN_C, 
            cv2.THRESH_BINARY, 
            11, 
            2
        )

        # Find and filter contours
        contours, _ = cv2.findContours(
            thresholded,
            cv2.RETR_TREE,
            cv2.CHAIN_APPROX_SIMPLE
        )
        
        # Sort contours by area and filter
        found_shapes = sorted(contours, key=cv2.contourArea, reverse=True)[1:]
        return [shape for shape in found_shapes 
                if cv2.contourArea(shape) >= minimum_area]

    @staticmethod
    def shape_recognition(
        found_shapes: List[NDArray],
        img: NDArray
    ) -> List[Dict[str, str]]:
        """Identify patterns and colors of detected shapes.

        Args:
            found_shapes: List of shape contours to analyze.
            img: Original image containing the shapes.

        Returns:
            List of dictionaries containing pattern and color information.

        Raises:
            ValueError: If found_shapes is None or empty.
        """
        if not found_shapes:
            return []

        recognized_shapes = []
        for shape in found_shapes[1:]:  # Skip first shape (usually background)
            try:
                pattern, confidence = Detection._identify_pattern(shape)
                color = Detection.get_color(img, shape)
                
                if pattern and color:
                    # Get position for text overlay
                    x, y = Detection._calculate_text_position(shape)
                    
                    # Draw shape and text
                    Detection._draw_shape_overlay(
                        img, shape, pattern, color, x, y
                    )
                    
                    recognized_shapes.append({
                        'pattern': pattern,
                        'color': color,
                        'confidence': confidence
                    })
            
            except Exception as e:
                print(f"Error processing shape: {e}")
                continue

        return recognized_shapes

    @staticmethod
    def get_color(img: NDArray, shape: NDArray) -> str:
        """Identify the color of a shape.

        Args:
            img: Original image containing the shape.
            shape: Contour of the shape to analyze.

        Returns:
            Color name as string, empty if unknown.
        """
        # Create mask for the shape
        mask = np.zeros(img.shape[:2], dtype="uint8")
        cv2.drawContours(mask, [shape], -1, 255, -1)
        
        # Get mean color values
        rgb_values = cv2.mean(img, mask=mask)[:3]
        
        # Check each color range
        for color_name, (lower, upper) in Detection.COLOR_RANGES.items():
            if all(l < v < u for v, l, u in zip(rgb_values, lower, upper)):
                return color_name
        
        return ""

    @staticmethod
    def _identify_pattern(shape: NDArray) -> Tuple[str, str]:
        """Identify the pattern of a shape based on its vertices.

        Args:
            shape: Contour of the shape to analyze.

        Returns:
            Tuple of (pattern name, confidence level).
        """
        vertices = cv2.approxPolyDP(
            shape,
            0.01 * cv2.arcLength(shape, True),
            True
        )
        vertex_count = len(vertices)

        if vertex_count == 3:
            return 'Triangle', 'High'
        
        if vertex_count == 4:
            x, y, w, h = cv2.boundingRect(vertices)
            aspect_ratio = float(w) / h
            return ('Square', 'High') if 0.95 <= aspect_ratio <= 1.05 else ('Rectangle', 'High')
        
        if vertex_count == 5:
            return 'Pentacle', 'High'
        
        if vertex_count == 6:
            return 'Hexagram', 'High'
        
        return 'Circle', 'Medium'

    @staticmethod
    def _calculate_text_position(shape: NDArray) -> Tuple[int, int]:
        """Calculate position for text overlay on shape.

        Args:
            shape: Contour of the shape.

        Returns:
            Tuple of (x, y) coordinates.
        """
        moments = cv2.moments(shape)
        if moments['m00'] != 0.0:
            x = int(moments['m10'] / moments['m00']) - 100
            y = int(moments['m01'] / moments['m00'])
            return x, y
        return 0, 0

    @staticmethod
    def _draw_shape_overlay(
        img: NDArray,
        shape: NDArray,
        pattern: str,
        color: str,
        x: int,
        y: int
    ) -> None:
        """Draw shape contour and label on image.

        Args:
            img: Image to draw on.
            shape: Shape contour to draw.
            pattern: Pattern name to display.
            color: Color name to display.
            x: X-coordinate for text.
            y: Y-coordinate for text.
        """
        cv2.drawContours(img, [shape], 0, (0, 255, 0), 5)
        cv2.putText(
            img,
            f'{pattern}, {color}',
            (x, y),
            cv2.FONT_HERSHEY_SIMPLEX,
            1,
            (255, 0, 255),
            2
        )


if __name__ == "__main__":
    # Test code for debugging
    try:
        test_img = cv2.imread("in/test_image_03.jpg")
        if test_img is None:
            raise ValueError("Could not load test image")

        cv2.imshow("Original", test_img)
        detected_shapes = Detection.shape_detection(test_img)
        recognized = Detection.shape_recognition(detected_shapes, test_img)
        
        print(f"Detected {len(detected_shapes)} shapes")
        print("Recognized shapes:", recognized)
        
        cv2.imshow("Processed", test_img)
        cv2.waitKey(0)
        cv2.destroyAllWindows()

    except Exception as e:
        print(f"Error in test code: {e}")