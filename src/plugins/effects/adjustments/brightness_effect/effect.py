"""
Brightness Effect Plugin

A simple brightness adjustment effect that increases or decreases the brightness
of video frames.
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

class BrightnessEffectPlugin(EffectPlugin):
    """Brightness adjustment effect plugin."""
    
    def __init__(self, name="Brightness Effect", category="adjustments", description="Adjusts the brightness of video frames"):
        super().__init__(name, category, description)
        
        # Add version attribute
        self.version = "1.0.0"
        
        # Define parameters with new format
        self.parameters = {
            "brightness": {
                "type": "int",
                "default": 0,
                "min": -100,
                "max": 100,
                "step": 5,
                "label": "Brightness",
                "category": "Basic"
            }
        }
    
    def apply(self, frame, parameters: Optional[Dict[str, Any]] = None):
        """
        Apply brightness adjustment to the frame.
        
        Args:
            frame: Input video frame (BGR format)
            parameters: Dictionary of parameter values
            
        Returns:
            Processed frame (BGR format)
        """
        try:
            # Get brightness parameter
            brightness = parameters.get('brightness', 0)
            
            # Apply brightness adjustment
            # Convert to HSV for better brightness control
            hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
            
            # Adjust V channel (brightness)
            hsv[:, :, 2] = cv2.add(hsv[:, :, 2], brightness)
            
            # Clip values to valid range
            hsv[:, :, 2] = np.clip(hsv[:, :, 2], 0, 255)
            
            # Convert back to BGR
            result = cv2.cvtColor(hsv, cv2.COLOR_HSV2BGR)
            
            return result
            
        except Exception as e:
            self.logger.error(f"Error applying brightness effect: {e}")
            return frame 