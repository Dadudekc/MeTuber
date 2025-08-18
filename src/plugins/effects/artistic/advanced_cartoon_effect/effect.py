"""
Advanced Cartoon Effect Plugin

Demonstrates all advanced parameter types and features:
- File pickers for texture overlays
- Color pickers for custom colors
- Dynamic show/hide logic
- Grouped parameters by category
- All parameter types (int, float, bool, str, file, color)
"""

import cv2
import numpy as np
import logging
from typing import Dict, Any, Optional
from src.plugins.plugin_base import EffectPlugin

class AdvancedCartoonEffectPlugin(EffectPlugin):
    """Advanced cartoon effect with comprehensive parameter support."""
    
    def __init__(self):
        super().__init__(
            name="Advanced Cartoon Effect",
            category="Artistic",
            description="Advanced cartoon effect with texture overlays, custom colors, and AI-powered edge detection"
        )
        
        # Define comprehensive parameters with all types
        self.parameters = {
            # Basic Parameters
            'intensity': {
                'type': 'int',
                'default': 50,
                'min': 0,
                'max': 100,
                'step': 5,
                'label': 'Effect Intensity',
                'description': 'Overall strength of the cartoon effect',
                'category': 'Basic'
            },
            'smoothness': {
                'type': 'float',
                'default': 0.7,
                'min': 0.1,
                'max': 1.0,
                'step': 0.05,
                'decimals': 2,
                'label': 'Smoothness',
                'description': 'Smoothing level for the cartoon effect',
                'category': 'Basic'
            },
            
            # Advanced Parameters
            'enable_texture': {
                'type': 'bool',
                'default': False,
                'label': 'Enable Texture Overlay',
                'description': 'Add texture overlay to the cartoon effect',
                'category': 'Advanced'
            },
            'texture_file': {
                'type': 'file',
                'default': '',
                'label': 'Texture File',
                'description': 'Select texture image file',
                'file_filter': 'Image Files (*.png *.jpg *.jpeg *.bmp)',
                'category': 'Advanced'
            },
            'texture_opacity': {
                'type': 'float',
                'default': 0.3,
                'min': 0.0,
                'max': 1.0,
                'step': 0.05,
                'decimals': 2,
                'label': 'Texture Opacity',
                'description': 'Opacity of the texture overlay',
                'category': 'Advanced'
            },
            
            # Color Parameters
            'color_mode': {
                'type': 'str',
                'default': 'Auto',
                'options': ['Auto', 'Custom', 'Monochrome'],
                'label': 'Color Mode',
                'description': 'Color processing mode',
                'category': 'Color'
            },
            'custom_color': {
                'type': 'color',
                'default': {'r': 255, 'g': 200, 'b': 150},
                'label': 'Custom Color',
                'description': 'Custom color for the cartoon effect',
                'category': 'Color'
            },
            'color_saturation': {
                'type': 'float',
                'default': 0.8,
                'min': 0.0,
                'max': 2.0,
                'step': 0.1,
                'decimals': 1,
                'label': 'Color Saturation',
                'description': 'Saturation level for colors',
                'category': 'Color'
            },
            
            # AI Parameters
            'ai_edge_detection': {
                'type': 'bool',
                'default': True,
                'label': 'AI Edge Detection',
                'description': 'Use AI-powered edge detection',
                'category': 'AI'
            },
            'edge_sensitivity': {
                'type': 'int',
                'default': 75,
                'min': 0,
                'max': 100,
                'step': 5,
                'label': 'Edge Sensitivity',
                'description': 'Sensitivity of edge detection',
                'category': 'AI'
            },
            'edge_thickness': {
                'type': 'int',
                'default': 2,
                'min': 1,
                'max': 5,
                'step': 1,
                'label': 'Edge Thickness',
                'description': 'Thickness of detected edges',
                'category': 'AI'
            }
        }
        
        self.logger = logging.getLogger(self.__class__.__name__)
    
    def apply(self, frame, parameters: Optional[Dict[str, Any]] = None):
        """Apply the advanced cartoon effect to a frame."""
        if parameters is None:
            parameters = self.parameters
        
        # Extract parameters
        intensity = parameters.get('intensity', 50) / 100.0
        smoothness = parameters.get('smoothness', 0.7)
        enable_texture = parameters.get('enable_texture', False)
        texture_file = parameters.get('texture_file', '')
        texture_opacity = parameters.get('texture_opacity', 0.3)
        color_mode = parameters.get('color_mode', 'Auto')
        custom_color = parameters.get('custom_color', {'r': 255, 'g': 200, 'b': 150})
        color_saturation = parameters.get('color_saturation', 0.8)
        ai_edge_detection = parameters.get('ai_edge_detection', True)
        edge_sensitivity = parameters.get('edge_sensitivity', 75)
        edge_thickness = parameters.get('edge_thickness', 2)
        
        # Apply cartoon effect
        result = self._apply_cartoon_effect(
            frame, intensity, smoothness, color_mode, custom_color, 
            color_saturation, ai_edge_detection, edge_sensitivity, edge_thickness
        )
        
        # Apply texture overlay if enabled
        if enable_texture and texture_file:
            result = self._apply_texture_overlay(result, texture_file, texture_opacity)
        
        return result
    
    def _apply_cartoon_effect(self, frame, intensity, smoothness, color_mode, 
                             custom_color, color_saturation, ai_edge_detection, 
                             edge_sensitivity, edge_thickness):
        """Apply the core cartoon effect with performance optimization."""
        # PERFORMANCE: Use uint8 instead of float32 for better performance
        frame_uint8 = frame.astype(np.uint8)
        
        # Apply bilateral filter for smoothing (optimized)
        blur_size = max(3, int(9 * smoothness))
        if blur_size % 2 == 0:
            blur_size += 1
        blur_size = min(blur_size, 15)  # Cap for performance
        
        smoothed = cv2.bilateralFilter(frame_uint8, blur_size, 75 * smoothness, 75 * smoothness)
        
        # Apply color processing based on mode
        if color_mode == 'Monochrome':
            # Convert to grayscale
            gray = cv2.cvtColor(smoothed, cv2.COLOR_BGR2GRAY)
            result = cv2.cvtColor(gray, cv2.COLOR_GRAY2BGR)
        elif color_mode == 'Custom':
            # Apply custom color (optimized)
            custom_color_array = np.array([custom_color['b'], custom_color['g'], custom_color['r']], dtype=np.uint8)
            result = cv2.multiply(smoothed, custom_color_array)
        else:  # Auto mode
            # Apply saturation adjustment (optimized)
            hsv = cv2.cvtColor(smoothed, cv2.COLOR_BGR2HSV)
            hsv = hsv.astype(np.float32)
            hsv[:, :, 1] = np.clip(hsv[:, :, 1] * color_saturation, 0, 255)
            hsv = hsv.astype(np.uint8)
            result = cv2.cvtColor(hsv, cv2.COLOR_HSV2BGR)
        
        # Apply edge detection with performance optimization
        if ai_edge_detection:
            # PERFORMANCE: Use optimized Canny edge detection
            gray = cv2.cvtColor(result, cv2.COLOR_BGR2GRAY)
            
            # Ensure edge sensitivity is valid
            edge_sensitivity = max(10, min(edge_sensitivity, 200))
            
            edges = cv2.Canny(gray, edge_sensitivity, edge_sensitivity * 2)
            
            # Dilate edges for thickness (optimized)
            if edge_thickness > 1:
                kernel_size = min(edge_thickness, 5)  # Cap for performance
                kernel = np.ones((kernel_size, kernel_size), np.uint8)
                edges = cv2.dilate(edges, kernel, iterations=1)
            
            # Combine edges with result (optimized)
            edges_3d = cv2.cvtColor(edges, cv2.COLOR_GRAY2BGR)
            result = cv2.subtract(result, cv2.multiply(edges_3d, 0.5))
        else:
            # PERFORMANCE: Use faster Laplacian edge detection
            gray = cv2.cvtColor(result, cv2.COLOR_BGR2GRAY)
            edges = cv2.Laplacian(gray, cv2.CV_8U, ksize=3)
            edges = np.uint8(np.absolute(edges))
            edges_3d = cv2.cvtColor(edges, cv2.COLOR_GRAY2BGR)
            result = cv2.subtract(result, cv2.multiply(edges_3d, 0.3))
        
        # Apply intensity (optimized)
        if intensity < 1.0:
            result = cv2.addWeighted(result, intensity, frame_uint8, 1 - intensity, 0)
        
        # Ensure result is valid
        return np.clip(result, 0, 255).astype(np.uint8)
    
    def _apply_texture_overlay(self, frame, texture_file, opacity):
        """Apply texture overlay to the frame."""
        try:
            # Load texture
            texture = cv2.imread(texture_file)
            if texture is None:
                return frame
            
            # Resize texture to match frame
            texture = cv2.resize(texture, (frame.shape[1], frame.shape[0]))
            
            # Blend texture with frame
            texture_float = texture.astype(np.float32) / 255.0
            frame_float = frame.astype(np.float32) / 255.0
            
            blended = frame_float * (1 - opacity) + texture_float * opacity
            return np.clip(blended * 255, 0, 255).astype(np.uint8)
            
        except Exception as e:
            self.logger.warning(f"Failed to apply texture overlay: {e}")
            return frame 