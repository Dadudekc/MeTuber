"""
Legacy Cartoon Effect Plugin

Converts the existing cartoon effect from the styles directory to the new plugin format.
"""

import cv2
import numpy as np
from typing import Dict, Any, Optional
from src.plugins.plugin_base import EffectPlugin

class LegacyCartoonEffectPlugin(EffectPlugin):
    """Legacy cartoon effect converted to plugin format."""
    
    def __init__(self):
        super().__init__(
            name="Legacy Cartoon",
            category="Artistic",
            description="Classic cartoon effect with bilateral filtering and edge detection"
        )
        
        # Define parameters based on the original style
        self.parameters = {
            'bilateral_filter_diameter': {
                'type': 'int',
                'default': 9,
                'min': 1,
                'max': 20,
                'step': 1,
                'label': 'Filter Diameter',
                'description': 'Diameter of the bilateral filter',
                'category': 'Filter'
            },
            'bilateral_filter_sigmaColor': {
                'type': 'int',
                'default': 75,
                'min': 1,
                'max': 150,
                'step': 5,
                'label': 'Color Sigma',
                'description': 'Color sigma for bilateral filter',
                'category': 'Filter'
            },
            'bilateral_filter_sigmaSpace': {
                'type': 'int',
                'default': 75,
                'min': 1,
                'max': 150,
                'step': 5,
                'label': 'Space Sigma',
                'description': 'Space sigma for bilateral filter',
                'category': 'Filter'
            },
            'canny_threshold1': {
                'type': 'int',
                'default': 100,
                'min': 0,
                'max': 500,
                'step': 10,
                'label': 'Edge Threshold 1',
                'description': 'First threshold for edge detection',
                'category': 'Edge Detection'
            },
            'canny_threshold2': {
                'type': 'int',
                'default': 200,
                'min': 0,
                'max': 500,
                'step': 10,
                'label': 'Edge Threshold 2',
                'description': 'Second threshold for edge detection',
                'category': 'Edge Detection'
            },
            'color_levels': {
                'type': 'int',
                'default': 8,
                'min': 2,
                'max': 16,
                'step': 1,
                'label': 'Color Levels',
                'description': 'Number of color levels for quantization',
                'category': 'Color'
            }
        }
    
    def apply(self, frame, parameters: Optional[Dict[str, Any]] = None):
        """Apply the legacy cartoon effect to a frame."""
        if parameters is None:
            parameters = self.parameters
        
        # Extract parameters
        d = parameters.get('bilateral_filter_diameter', 9)
        sigma_color = parameters.get('bilateral_filter_sigmaColor', 75)
        sigma_space = parameters.get('bilateral_filter_sigmaSpace', 75)
        t1 = parameters.get('canny_threshold1', 100)
        t2 = parameters.get('canny_threshold2', 200)
        levels = parameters.get('color_levels', 8)
        
        # Apply bilateral filter for smoothing while preserving edges
        color = cv2.bilateralFilter(frame, d, sigma_color, sigma_space)
        
        # Convert to grayscale for edge detection
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        
        # Apply edge detection
        edges = cv2.Canny(gray, t1, t2)
        edges = cv2.dilate(edges, None)
        
        # Reduce color palette
        div = 256 // levels
        color = color // div * div + div // 2
        
        # Combine edges with color image
        cartoon = cv2.bitwise_and(color, color, mask=255 - edges)
        
        return cartoon 