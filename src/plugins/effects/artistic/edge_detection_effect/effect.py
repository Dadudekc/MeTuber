"""
Edge Detection Effect Plugin

Converts the existing edge detection effect from the styles directory to the new plugin format.
"""

import cv2
import numpy as np
from typing import Dict, Any, Optional
from src.plugins.plugin_base import EffectPlugin

class EdgeDetectionEffectPlugin(EffectPlugin):
    """Edge detection effect converted to plugin format."""
    
    def __init__(self):
        super().__init__(
            name="Edge Detection",
            category="Artistic",
            description="Advanced edge detection with multiple algorithms and customization options"
        )
        
        # Define parameters based on the original style
        self.parameters = {
            'algorithm': {
                'type': 'str',
                'default': 'Canny',
                'options': ['Canny', 'Sobel', 'Laplacian', 'Scharr'],
                'label': 'Algorithm',
                'description': 'Edge detection algorithm to use',
                'category': 'Detection'
            },
            'threshold1': {
                'type': 'int',
                'default': 100,
                'min': 0,
                'max': 500,
                'step': 10,
                'label': 'Threshold 1',
                'description': 'First threshold for edge detection',
                'category': 'Detection'
            },
            'threshold2': {
                'type': 'int',
                'default': 200,
                'min': 0,
                'max': 500,
                'step': 10,
                'label': 'Threshold 2',
                'description': 'Second threshold for edge detection',
                'category': 'Detection'
            },
            'edge_color': {
                'type': 'str',
                'default': 'White',
                'options': ['White', 'Black', 'Red', 'Green', 'Blue', 'Yellow'],
                'label': 'Edge Color',
                'description': 'Color of detected edges',
                'category': 'Style'
            },
            'background_color': {
                'type': 'str',
                'default': 'Black',
                'options': ['Black', 'White', 'Gray'],
                'label': 'Background Color',
                'description': 'Background color for edge detection',
                'category': 'Style'
            },
            'line_thickness': {
                'type': 'int',
                'default': 1,
                'min': 1,
                'max': 5,
                'step': 1,
                'label': 'Line Thickness',
                'description': 'Thickness of detected edges',
                'category': 'Style'
            },
            'blur_preprocessing': {
                'type': 'bool',
                'default': True,
                'label': 'Blur Preprocessing',
                'description': 'Apply blur before edge detection',
                'category': 'Advanced'
            },
            'blur_strength': {
                'type': 'int',
                'default': 3,
                'min': 1,
                'max': 15,
                'step': 2,
                'label': 'Blur Strength',
                'description': 'Strength of blur preprocessing',
                'category': 'Advanced'
            },
            'invert_edges': {
                'type': 'bool',
                'default': False,
                'label': 'Invert Edges',
                'description': 'Invert the edge detection result',
                'category': 'Style'
            }
        }
    
    def apply(self, frame, parameters: Optional[Dict[str, Any]] = None):
        """Apply the edge detection effect to a frame."""
        if parameters is None:
            parameters = self.parameters
        
        # Extract parameters
        algorithm = parameters.get('algorithm', 'Canny')
        threshold1 = parameters.get('threshold1', 100)
        threshold2 = parameters.get('threshold2', 200)
        edge_color = parameters.get('edge_color', 'White')
        background_color = parameters.get('background_color', 'Black')
        line_thickness = parameters.get('line_thickness', 1)
        blur_preprocessing = parameters.get('blur_preprocessing', True)
        blur_strength = parameters.get('blur_strength', 3)
        invert_edges = parameters.get('invert_edges', False)
        
        # Convert to grayscale
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        
        # Apply blur preprocessing if enabled
        if blur_preprocessing:
            if blur_strength % 2 == 0:
                blur_strength += 1  # Ensure odd kernel size
            gray = cv2.GaussianBlur(gray, (blur_strength, blur_strength), 0)
        
        # Apply edge detection based on algorithm
        if algorithm == 'Canny':
            edges = cv2.Canny(gray, threshold1, threshold2)
        elif algorithm == 'Sobel':
            edges = self._apply_sobel(gray)
        elif algorithm == 'Laplacian':
            edges = self._apply_laplacian(gray)
        elif algorithm == 'Scharr':
            edges = self._apply_scharr(gray)
        else:
            edges = cv2.Canny(gray, threshold1, threshold2)
        
        # Apply line thickness
        if line_thickness > 1:
            kernel = np.ones((line_thickness, line_thickness), np.uint8)
            edges = cv2.dilate(edges, kernel, iterations=1)
        
        # Invert edges if requested
        if invert_edges:
            edges = 255 - edges
        
        # Create colored result
        result = self._create_colored_edges(edges, edge_color, background_color)
        
        return result
    
    def _apply_sobel(self, gray):
        """Apply Sobel edge detection."""
        sobelx = cv2.Sobel(gray, cv2.CV_64F, 1, 0, ksize=3)
        sobely = cv2.Sobel(gray, cv2.CV_64F, 0, 1, ksize=3)
        
        # Combine gradients
        magnitude = np.sqrt(sobelx**2 + sobely**2)
        magnitude = np.uint8(magnitude / magnitude.max() * 255)
        
        # Apply threshold
        _, edges = cv2.threshold(magnitude, 50, 255, cv2.THRESH_BINARY)
        
        return edges
    
    def _apply_laplacian(self, gray):
        """Apply Laplacian edge detection."""
        laplacian = cv2.Laplacian(gray, cv2.CV_64F)
        laplacian = np.uint8(np.absolute(laplacian))
        
        # Apply threshold
        _, edges = cv2.threshold(laplacian, 50, 255, cv2.THRESH_BINARY)
        
        return edges
    
    def _apply_scharr(self, gray):
        """Apply Scharr edge detection."""
        scharrx = cv2.Scharr(gray, cv2.CV_64F, 1, 0)
        scharry = cv2.Scharr(gray, cv2.CV_64F, 0, 1)
        
        # Combine gradients
        magnitude = np.sqrt(scharrx**2 + scharry**2)
        magnitude = np.uint8(magnitude / magnitude.max() * 255)
        
        # Apply threshold
        _, edges = cv2.threshold(magnitude, 50, 255, cv2.THRESH_BINARY)
        
        return edges
    
    def _create_colored_edges(self, edges, edge_color, background_color):
        """Create colored edge detection result."""
        height, width = edges.shape
        
        # Create background
        if background_color == 'Black':
            background = np.zeros((height, width, 3), dtype=np.uint8)
        elif background_color == 'White':
            background = np.full((height, width, 3), 255, dtype=np.uint8)
        else:  # Gray
            background = np.full((height, width, 3), 128, dtype=np.uint8)
        
        # Define edge colors
        color_map = {
            'White': [255, 255, 255],
            'Black': [0, 0, 0],
            'Red': [0, 0, 255],
            'Green': [0, 255, 0],
            'Blue': [255, 0, 0],
            'Yellow': [0, 255, 255]
        }
        
        edge_color_bgr = color_map.get(edge_color, [255, 255, 255])
        
        # Apply edge color
        edge_mask = edges > 0
        background[edge_mask] = edge_color_bgr
        
        return background 