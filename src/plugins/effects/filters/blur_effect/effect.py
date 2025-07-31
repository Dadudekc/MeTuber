"""
Blur Effect Plugin

A blur effect that applies different types of blur to video frames.
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

class BlurEffectPlugin(EffectPlugin):
    """Blur effect plugin that applies different types of blur."""
    
    def __init__(self, name="Blur Effect", category="filters", description="Applies different types of blur to video frames"):
        super().__init__(name, category, description)
        
        # Add version attribute
        self.version = "1.0.0"
        
        # Define parameters with new format
        self.parameters = {
            "blur_type": {
                "type": "str",
                "default": "Gaussian",
                "options": ["Gaussian", "Median", "Bilateral"],
                "label": "Blur Type",
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
        Apply blur effect to the frame.
        
        Args:
            frame: Input video frame (BGR format)
            parameters: Dictionary of parameter values
            
        Returns:
            Processed frame (BGR format)
        """
        try:
            # Get parameters
            blur_type = parameters.get('blur_type', 'Gaussian')
            blur_strength = parameters.get('blur_strength', 5)
            
            # Ensure blur strength is odd for Gaussian blur
            if blur_strength % 2 == 0:
                blur_strength += 1
            
            # Apply different blur types
            if blur_type == 'Gaussian':
                result = cv2.GaussianBlur(frame, (blur_strength, blur_strength), 0)
            elif blur_type == 'Box':
                result = cv2.blur(frame, (blur_strength, blur_strength))
            elif blur_type == 'Median':
                result = cv2.medianBlur(frame, blur_strength)
            else:
                # Default to Gaussian blur
                result = cv2.GaussianBlur(frame, (blur_strength, blur_strength), 0)
            
            return result
            
        except Exception as e:
            self.logger.error(f"Error applying blur effect: {e}")
            return frame 