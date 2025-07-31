"""
Neural Style Transfer Effect Plugin

Advanced effect that simulates neural style transfer with artistic filters.
"""

import cv2
import numpy as np
from typing import Dict, Any, Optional
from src.plugins.plugin_base import EffectPlugin

class NeuralStyleEffectPlugin(EffectPlugin):
    """Neural style transfer effect with artistic filters."""
    
    def __init__(self):
        super().__init__(
            name="Neural Style Transfer",
            category="Artistic",
            description="Advanced neural style transfer effect with artistic filters and AI-like processing"
        )
        
        # Define comprehensive parameters
        self.parameters = {
            # Style Parameters
            'style_strength': {
                'type': 'float',
                'default': 0.7,
                'min': 0.1,
                'max': 1.0,
                'step': 0.05,
                'decimals': 2,
                'label': 'Style Strength',
                'description': 'Strength of the artistic style transfer',
                'category': 'Style'
            },
            'content_weight': {
                'type': 'float',
                'default': 0.5,
                'min': 0.1,
                'max': 1.0,
                'step': 0.05,
                'decimals': 2,
                'label': 'Content Weight',
                'description': 'Weight given to content preservation',
                'category': 'Style'
            },
            
            # Artistic Style
            'artistic_style': {
                'type': 'str',
                'default': 'Van Gogh',
                'options': ['Van Gogh', 'Monet', 'Picasso', 'Watercolor', 'Oil Painting', 'Sketch'],
                'label': 'Artistic Style',
                'description': 'Artistic style to apply',
                'category': 'Style'
            },
            'brush_stroke_size': {
                'type': 'int',
                'default': 15,
                'min': 5,
                'max': 50,
                'step': 5,
                'label': 'Brush Stroke Size',
                'description': 'Size of brush strokes',
                'category': 'Style'
            },
            
            # Color Processing
            'color_palette': {
                'type': 'str',
                'default': 'Vibrant',
                'options': ['Vibrant', 'Muted', 'Warm', 'Cool', 'Monochrome', 'Sepia'],
                'label': 'Color Palette',
                'description': 'Color palette to apply',
                'category': 'Color'
            },
            'saturation_boost': {
                'type': 'float',
                'default': 1.2,
                'min': 0.5,
                'max': 2.0,
                'step': 0.1,
                'decimals': 1,
                'label': 'Saturation Boost',
                'description': 'Boost color saturation',
                'category': 'Color'
            },
            
            # Texture and Detail
            'texture_strength': {
                'type': 'float',
                'default': 0.6,
                'min': 0.0,
                'max': 1.0,
                'step': 0.05,
                'decimals': 2,
                'label': 'Texture Strength',
                'description': 'Strength of texture overlay',
                'category': 'Texture'
            },
            'detail_preservation': {
                'type': 'float',
                'default': 0.8,
                'min': 0.0,
                'max': 1.0,
                'step': 0.05,
                'decimals': 2,
                'label': 'Detail Preservation',
                'description': 'Preserve fine details',
                'category': 'Texture'
            },
            
            # AI Features
            'enable_ai_enhancement': {
                'type': 'bool',
                'default': True,
                'label': 'AI Enhancement',
                'description': 'Enable AI-powered enhancement',
                'category': 'AI'
            },
            'ai_quality': {
                'type': 'str',
                'default': 'Balanced',
                'options': ['Fast', 'Balanced', 'Quality'],
                'label': 'AI Quality',
                'description': 'Quality of AI processing',
                'category': 'AI'
            }
        }
    
    def apply(self, frame, parameters: Optional[Dict[str, Any]] = None):
        """Apply the neural style transfer effect to a frame."""
        if parameters is None:
            parameters = self.parameters
        
        # Extract parameters
        style_strength = parameters.get('style_strength', 0.7)
        content_weight = parameters.get('content_weight', 0.5)
        artistic_style = parameters.get('artistic_style', 'Van Gogh')
        brush_stroke_size = parameters.get('brush_stroke_size', 15)
        color_palette = parameters.get('color_palette', 'Vibrant')
        saturation_boost = parameters.get('saturation_boost', 1.2)
        texture_strength = parameters.get('texture_strength', 0.6)
        detail_preservation = parameters.get('detail_preservation', 0.8)
        enable_ai = parameters.get('enable_ai_enhancement', True)
        ai_quality = parameters.get('ai_quality', 'Balanced')
        
        # Apply neural style transfer effect
        result = self._apply_neural_style(
            frame, style_strength, content_weight, artistic_style, 
            brush_stroke_size, color_palette, saturation_boost,
            texture_strength, detail_preservation, enable_ai, ai_quality
        )
        
        return result
    
    def _apply_neural_style(self, frame, style_strength, content_weight, 
                           artistic_style, brush_stroke_size, color_palette,
                           saturation_boost, texture_strength, detail_preservation,
                           enable_ai, ai_quality):
        """Apply neural style transfer effect."""
        # Convert to float for processing
        frame_float = frame.astype(np.float32) / 255.0
        
        # Apply artistic style based on selection
        if artistic_style == 'Van Gogh':
            result = self._apply_van_gogh_style(frame_float, brush_stroke_size)
        elif artistic_style == 'Monet':
            result = self._apply_monet_style(frame_float)
        elif artistic_style == 'Picasso':
            result = self._apply_picasso_style(frame_float)
        elif artistic_style == 'Watercolor':
            result = self._apply_watercolor_style(frame_float)
        elif artistic_style == 'Oil Painting':
            result = self._apply_oil_painting_style(frame_float, brush_stroke_size)
        elif artistic_style == 'Sketch':
            result = self._apply_sketch_style(frame_float)
        else:
            result = frame_float
        
        # Apply color palette
        result = self._apply_color_palette(result, color_palette, saturation_boost)
        
        # Apply texture overlay
        if texture_strength > 0:
            result = self._apply_texture_overlay(result, texture_strength)
        
        # Preserve details
        if detail_preservation < 1.0:
            result = self._preserve_details(frame_float, result, detail_preservation)
        
        # Apply AI enhancement if enabled
        if enable_ai:
            result = self._apply_ai_enhancement(result, ai_quality)
        
        # Blend with original based on style strength
        result = result * style_strength + frame_float * (1 - style_strength)
        
        # Convert back to uint8
        return np.clip(result * 255, 0, 255).astype(np.uint8)
    
    def _apply_van_gogh_style(self, frame, brush_stroke_size):
        """Apply Van Gogh style with swirling brush strokes."""
        # Create swirling brush stroke effect
        height, width = frame.shape[:2]
        
        # Generate swirling pattern
        y, x = np.ogrid[:height, :width]
        center_y, center_x = height // 2, width // 2
        
        # Create swirling effect
        angle = np.arctan2(y - center_y, x - center_x)
        radius = np.sqrt((x - center_x)**2 + (y - center_y)**2)
        
        # Apply swirling distortion
        swirl_strength = brush_stroke_size / 100.0
        distorted_x = x + swirl_strength * radius * np.cos(angle)
        distorted_y = y + swirl_strength * radius * np.sin(angle)
        
        # Apply distortion
        result = cv2.remap(frame, distorted_x.astype(np.float32), 
                          distorted_y.astype(np.float32), cv2.INTER_LINEAR)
        
        # Add texture
        texture = np.random.rand(height, width, 3) * 0.1
        result = np.clip(result + texture, 0, 1)
        
        return result
    
    def _apply_monet_style(self, frame):
        """Apply Monet impressionist style."""
        # Soft blur for impressionist effect
        blurred = cv2.GaussianBlur(frame, (15, 15), 0)
        
        # Enhance colors
        hsv = cv2.cvtColor(blurred, cv2.COLOR_BGR2HSV)
        hsv[:, :, 1] = np.clip(hsv[:, :, 1] * 1.3, 0, 1)  # Increase saturation
        result = cv2.cvtColor(hsv, cv2.COLOR_HSV2BGR)
        
        return result
    
    def _apply_picasso_style(self, frame):
        """Apply Picasso cubist style."""
        # Create geometric distortions
        height, width = frame.shape[:2]
        
        # Divide image into geometric regions
        regions = []
        for i in range(0, height, height//4):
            for j in range(0, width, width//4):
                region = frame[i:i+height//4, j:j+width//4]
                if region.size > 0:
                    # Apply different transformations to each region
                    if np.random.random() > 0.5:
                        region = cv2.rotate(region, cv2.ROTATE_90_CLOCKWISE)
                    regions.append(region)
        
        # Reconstruct with geometric arrangement
        result = np.zeros_like(frame)
        idx = 0
        for i in range(0, height, height//4):
            for j in range(0, width, width//4):
                if idx < len(regions):
                    region = regions[idx]
                    h, w = region.shape[:2]
                    result[i:i+h, j:j+w] = region
                    idx += 1
        
        return result
    
    def _apply_watercolor_style(self, frame):
        """Apply watercolor style."""
        # Bilateral filter for edge preservation
        filtered = cv2.bilateralFilter(frame, 9, 75, 75)
        
        # Add watercolor texture
        height, width = frame.shape[:2]
        texture = np.random.rand(height, width, 3) * 0.2
        result = np.clip(filtered + texture, 0, 1)
        
        return result
    
    def _apply_oil_painting_style(self, frame, brush_stroke_size):
        """Apply oil painting style."""
        # Use bilateral filter for oil painting effect
        result = cv2.bilateralFilter(frame, brush_stroke_size, 75, 75)
        
        # Add canvas texture
        height, width = frame.shape[:2]
        canvas_texture = np.random.rand(height, width, 3) * 0.15
        result = np.clip(result + canvas_texture, 0, 1)
        
        return result
    
    def _apply_sketch_style(self, frame):
        """Apply sketch style."""
        # Convert to grayscale
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        
        # Apply edge detection
        edges = cv2.Canny(gray, 50, 150)
        
        # Invert for sketch effect
        sketch = 255 - edges
        
        # Convert back to BGR
        result = cv2.cvtColor(sketch, cv2.COLOR_GRAY2BGR) / 255.0
        
        return result
    
    def _apply_color_palette(self, frame, palette, saturation_boost):
        """Apply color palette."""
        hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
        
        if palette == 'Vibrant':
            hsv[:, :, 1] = np.clip(hsv[:, :, 1] * saturation_boost, 0, 1)
        elif palette == 'Muted':
            hsv[:, :, 1] = np.clip(hsv[:, :, 1] * 0.7, 0, 1)
        elif palette == 'Warm':
            # Shift hue towards warm colors
            hsv[:, :, 0] = np.clip(hsv[:, :, 0] * 0.8, 0, 179)
        elif palette == 'Cool':
            # Shift hue towards cool colors
            hsv[:, :, 0] = np.clip(hsv[:, :, 0] * 1.2, 0, 179)
        elif palette == 'Monochrome':
            # Convert to grayscale
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            return cv2.cvtColor(gray, cv2.COLOR_GRAY2BGR)
        elif palette == 'Sepia':
            # Apply sepia filter
            sepia_filter = np.array([[0.272, 0.534, 0.131],
                                   [0.349, 0.686, 0.168],
                                   [0.393, 0.769, 0.189]], dtype=np.float32)
            return cv2.transform(frame, sepia_filter)
        
        return cv2.cvtColor(hsv, cv2.COLOR_HSV2BGR)
    
    def _apply_texture_overlay(self, frame, strength):
        """Apply texture overlay."""
        height, width = frame.shape[:2]
        
        # Generate artistic texture
        texture = np.random.rand(height, width, 3) * strength
        
        return np.clip(frame + texture, 0, 1)
    
    def _preserve_details(self, original, processed, preservation):
        """Preserve details from original image."""
        # Extract high-frequency details from original
        blurred_original = cv2.GaussianBlur(original, (5, 5), 0)
        details = original - blurred_original
        
        # Blend details back
        result = processed * (1 - preservation) + details * preservation
        
        return np.clip(result, 0, 1)
    
    def _apply_ai_enhancement(self, frame, quality):
        """Apply AI-like enhancement."""
        if quality == 'Quality':
            # High-quality enhancement
            enhanced = cv2.bilateralFilter(frame, 15, 100, 100)
            kernel = np.array([[-1, -1, -1], [-1, 9, -1], [-1, -1, -1]])
            enhanced = cv2.filter2D(enhanced, -1, kernel)
        elif quality == 'Balanced':
            # Balanced enhancement
            enhanced = cv2.bilateralFilter(frame, 9, 75, 75)
        else:  # Fast
            # Fast enhancement
            enhanced = cv2.GaussianBlur(frame, (3, 3), 0)
        
        return enhanced 