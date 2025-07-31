"""
Watercolor Effect Plugin

Converts the existing watercolor effect from the styles directory to the new plugin format.
"""

import cv2
import numpy as np
from typing import Dict, Any, Optional
from src.plugins.plugin_base import EffectPlugin

class WatercolorEffectPlugin(EffectPlugin):
    """Watercolor effect converted to plugin format."""
    
    def __init__(self):
        super().__init__(
            name="Watercolor",
            category="Artistic",
            description="Beautiful watercolor painting effect with customizable stylization"
        )
        
        # Define parameters based on the original style
        self.parameters = {
            'sigma_s': {
                'type': 'int',
                'default': 60,
                'min': 10,
                'max': 100,
                'step': 10,
                'label': 'Sigma S',
                'description': 'Spatial sigma for stylization',
                'category': 'Stylization'
            },
            'sigma_r': {
                'type': 'float',
                'default': 0.5,
                'min': 0.1,
                'max': 1.0,
                'step': 0.1,
                'decimals': 1,
                'label': 'Sigma R',
                'description': 'Range sigma for stylization',
                'category': 'Stylization'
            },
            'color_intensity': {
                'type': 'float',
                'default': 1.2,
                'min': 0.5,
                'max': 2.0,
                'step': 0.1,
                'decimals': 1,
                'label': 'Color Intensity',
                'description': 'Intensity of watercolor colors',
                'category': 'Color'
            },
            'edge_preservation': {
                'type': 'float',
                'default': 0.8,
                'min': 0.0,
                'max': 1.0,
                'step': 0.05,
                'decimals': 2,
                'label': 'Edge Preservation',
                'description': 'Preserve edges in watercolor effect',
                'category': 'Stylization'
            },
            'texture_overlay': {
                'type': 'bool',
                'default': True,
                'label': 'Texture Overlay',
                'description': 'Add watercolor paper texture',
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
                'description': 'Strength of paper texture overlay',
                'category': 'Style'
            }
        }
    
    def apply(self, frame, parameters: Optional[Dict[str, Any]] = None):
        """Apply the watercolor effect to a frame."""
        if parameters is None:
            parameters = self.parameters
        
        # Extract parameters
        sigma_s = parameters.get('sigma_s', 60)
        sigma_r = parameters.get('sigma_r', 0.5)
        color_intensity = parameters.get('color_intensity', 1.2)
        edge_preservation = parameters.get('edge_preservation', 0.8)
        texture_overlay = parameters.get('texture_overlay', True)
        texture_strength = parameters.get('texture_strength', 0.3)
        
        # Apply stylization using OpenCV's stylization function
        watercolor = cv2.stylization(frame, sigma_s=sigma_s, sigma_r=sigma_r)
        
        # Apply color intensity
        if color_intensity != 1.0:
            watercolor = np.clip(watercolor * color_intensity, 0, 255).astype(np.uint8)
        
        # Preserve edges if enabled
        if edge_preservation < 1.0:
            watercolor = self._preserve_edges(frame, watercolor, edge_preservation)
        
        # Add texture overlay if enabled
        if texture_overlay and texture_strength > 0:
            watercolor = self._add_watercolor_texture(watercolor, texture_strength)
        
        return watercolor
    
    def _preserve_edges(self, original, processed, preservation):
        """Preserve edges from original image."""
        # Extract edges from original
        gray_original = cv2.cvtColor(original, cv2.COLOR_BGR2GRAY)
        edges = cv2.Canny(gray_original, 50, 150)
        
        # Dilate edges for better visibility
        kernel = np.ones((2, 2), np.uint8)
        edges = cv2.dilate(edges, kernel, iterations=1)
        
        # Blend edges with processed image
        edges_3d = cv2.cvtColor(edges, cv2.COLOR_GRAY2BGR)
        result = cv2.addWeighted(processed, 1 - preservation, edges_3d, preservation, 0)
        
        return result
    
    def _add_watercolor_texture(self, frame, strength):
        """Add watercolor paper texture."""
        height, width = frame.shape[:2]
        
        # Generate watercolor paper texture
        texture = np.random.rand(height, width, 3) * strength * 50
        
        # Blend texture with frame
        result = np.clip(frame + texture, 0, 255).astype(np.uint8)
        
        return result 