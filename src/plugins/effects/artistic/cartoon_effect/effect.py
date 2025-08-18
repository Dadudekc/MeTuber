"""
Cartoon Effect Plugin

A cartoon effect that creates a cartoon-like appearance by reducing colors
and enhancing edges.
"""

import sys
import os

# Add the project root to Python path for imports
project_root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))))
if project_root not in sys.path:
    sys.path.insert(0, project_root)

import cv2
import numpy as np
from typing import Dict, Any, Optional
from src.plugins.plugin_base import EffectPlugin

class CartoonEffectPlugin(EffectPlugin):
    """Cartoon effect plugin that creates a cartoon-like appearance."""
    
    def __init__(self, name="Cartoon Effect", category="artistic", description="Creates a cartoon-like appearance by reducing colors and enhancing edges"):
        super().__init__(name, category, description)
        
        # Add version attribute
        self.version = "1.0.0"
        
        # Define parameters with new format
        self.parameters = {
            "edge_strength": {
                "type": "float",
                "default": 1.0,
                "min": 0.1,
                "max": 3.0,
                "step": 0.1,
                "label": "Edge Strength",
                "category": "Basic"
            },
            "color_reduction": {
                "type": "int",
                "default": 8,
                "min": 2,
                "max": 16,
                "step": 2,
                "label": "Color Reduction",
                "category": "Basic"
            },
            "blur_strength": {
                "type": "int",
                "default": 5,
                "min": 1,
                "max": 15,
                "step": 1,
                "label": "Blur Strength",
                "category": "Basic"
            }
        }
    
    def apply(self, frame, parameters: Optional[Dict[str, Any]] = None):
        """
        Apply cartoon effect to the frame with performance optimization.
        
        Args:
            frame: Input video frame (BGR format)
            parameters: Dictionary of parameter values
            
        Returns:
            Processed frame (BGR format)
        """
        try:
            # Get parameters
            edge_strength = parameters.get('edge_strength', 1.0)
            color_reduction = parameters.get('color_reduction', 8)
            blur_strength = parameters.get('blur_strength', 5)
            
            # PERFORMANCE: Ensure odd kernel sizes for OpenCV compatibility
            if blur_strength % 2 == 0:
                blur_strength += 1
            if color_reduction % 2 == 0:
                color_reduction += 1
            
            # PERFORMANCE: Use smaller blur for better performance
            blur_strength = min(blur_strength, 9)  # Cap at 9 for performance
            color_reduction = min(color_reduction, 9)  # Cap at 9 for performance
            
            # Convert to grayscale for edge detection
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            
            # PERFORMANCE: Use smaller bilateral filter for speed
            bilateral = cv2.bilateralFilter(gray, blur_strength, 75, 75)
            
            # Detect edges with optimized parameters
            edges = cv2.adaptiveThreshold(
                bilateral, 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY, 9, 2
            )
            
            # Apply edge strength
            edges = cv2.bitwise_not(edges)
            edges = cv2.cvtColor(edges, cv2.COLOR_GRAY2BGR)
            edges = cv2.addWeighted(edges, edge_strength, edges, 0, 0)
            
            # PERFORMANCE: Use optimized color reduction
            if color_reduction > 1:
                color_reduced = cv2.medianBlur(frame, color_reduction)
            else:
                color_reduced = frame.copy()
            
            # Combine color reduction with edges
            cartoon = cv2.bitwise_and(color_reduced, edges)
            
            return cartoon
            
        except Exception as e:
            print(f"Error applying cartoon effect: {e}")
            # Return original frame on error
            return frame 