"""
Pencil Sketch Effect Plugin

Converts the existing pencil sketch effect from the styles directory to the new plugin format.
"""

import cv2
import numpy as np
from typing import Dict, Any, Optional
from src.plugins.plugin_base import EffectPlugin

class PencilSketchEffectPlugin(EffectPlugin):
    """Pencil sketch effect converted to plugin format."""
    
    def __init__(self):
        super().__init__(
            name="Pencil Sketch",
            category="Artistic",
            description="Classic pencil sketch effect with customizable blur and contrast"
        )
        
        # Define parameters based on the original style
        self.parameters = {
            'blur_intensity': {
                'type': 'int',
                'default': 15,
                'min': 1,
                'max': 51,
                'step': 2,
                'label': 'Blur Intensity',
                'description': 'Intensity of the blur effect for sketch lines',
                'category': 'Sketch'
            },
            'contrast': {
                'type': 'float',
                'default': 1.5,
                'min': 0.5,
                'max': 5.0,
                'step': 0.1,
                'decimals': 1,
                'label': 'Contrast',
                'description': 'Contrast adjustment for the sketch',
                'category': 'Sketch'
            },
            'line_thickness': {
                'type': 'int',
                'default': 1,
                'min': 1,
                'max': 5,
                'step': 1,
                'label': 'Line Thickness',
                'description': 'Thickness of sketch lines',
                'category': 'Sketch'
            },
            'paper_texture': {
                'type': 'bool',
                'default': True,
                'label': 'Paper Texture',
                'description': 'Add paper texture to the sketch',
                'category': 'Style'
            },
            'texture_strength': {
                'type': 'float',
                'default': 0.3,
                'min': 0.0,
                'max': 1.0,
                'step': 0.05,
                'decimals': 2,
                'label': 'Texture Strength',
                'description': 'Strength of paper texture',
                'category': 'Style'
            }
        }
    
    def apply(self, frame, parameters: Optional[Dict[str, Any]] = None):
        """Apply the pencil sketch effect to a frame."""
        if parameters is None:
            parameters = self.parameters
        
        # Extract parameters
        blur_intensity = parameters.get('blur_intensity', 15)
        contrast = parameters.get('contrast', 1.5)
        line_thickness = parameters.get('line_thickness', 1)
        paper_texture = parameters.get('paper_texture', True)
        texture_strength = parameters.get('texture_strength', 0.3)
        
        # Ensure blur intensity is odd
        if blur_intensity % 2 == 0:
            blur_intensity += 1
        
        # Convert to grayscale
        gray_image = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        
        # Apply contrast adjustment
        gray_image = np.clip(gray_image * contrast, 0, 255).astype(np.uint8)
        
        # Create inverted blurred image
        inverted_image = 255 - gray_image
        blurred = cv2.GaussianBlur(inverted_image, (blur_intensity, blur_intensity), 0)
        inverted_blurred = 255 - blurred
        
        # Create pencil sketch effect
        pencil_sketch = cv2.divide(gray_image, inverted_blurred, scale=256.0)
        
        # Apply line thickness
        if line_thickness > 1:
            kernel = np.ones((line_thickness, line_thickness), np.uint8)
            pencil_sketch = cv2.erode(pencil_sketch, kernel, iterations=1)
        
        # Add paper texture if enabled
        if paper_texture and texture_strength > 0:
            pencil_sketch = self._add_paper_texture(pencil_sketch, texture_strength)
        
        # Convert back to BGR
        return cv2.cvtColor(pencil_sketch, cv2.COLOR_GRAY2BGR)
    
    def _add_paper_texture(self, sketch, strength):
        """Add paper texture to the sketch."""
        height, width = sketch.shape
        
        # Generate paper texture
        texture = np.random.rand(height, width) * strength * 255
        
        # Blend texture with sketch
        result = np.clip(sketch + texture, 0, 255).astype(np.uint8)
        
        return result 