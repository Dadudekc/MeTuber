"""
Brightness & Contrast Effect Plugin

Converts the existing brightness/contrast effect from the styles directory to the new plugin format.
"""

import cv2
import numpy as np
from typing import Dict, Any, Optional
from src.plugins.plugin_base import EffectPlugin

class BrightnessContrastEffectPlugin(EffectPlugin):
    """Brightness and contrast effect converted to plugin format."""
    
    def __init__(self):
        super().__init__(
            name="Brightness & Contrast",
            category="Adjustments",
            description="Adjust brightness and contrast with real-time preview"
        )
        
        # Define parameters based on the original style
        self.parameters = {
            'brightness': {
                'type': 'int',
                'default': 0,
                'min': -100,
                'max': 100,
                'step': 5,
                'label': 'Brightness',
                'description': 'Adjust image brightness',
                'category': 'Basic'
            },
            'contrast': {
                'type': 'float',
                'default': 1.0,
                'min': 0.5,
                'max': 3.0,
                'step': 0.1,
                'decimals': 1,
                'label': 'Contrast',
                'description': 'Adjust image contrast',
                'category': 'Basic'
            },
            'gamma': {
                'type': 'float',
                'default': 1.0,
                'min': 0.1,
                'max': 3.0,
                'step': 0.1,
                'decimals': 1,
                'label': 'Gamma',
                'description': 'Adjust gamma correction',
                'category': 'Advanced'
            },
            'auto_adjust': {
                'type': 'bool',
                'default': False,
                'label': 'Auto Adjust',
                'description': 'Automatically adjust brightness and contrast',
                'category': 'Advanced'
            },
            'preserve_highlights': {
                'type': 'bool',
                'default': True,
                'label': 'Preserve Highlights',
                'description': 'Preserve highlight details',
                'category': 'Advanced'
            },
            'preserve_shadows': {
                'type': 'bool',
                'default': True,
                'label': 'Preserve Shadows',
                'description': 'Preserve shadow details',
                'category': 'Advanced'
            }
        }
    
    def apply(self, frame, parameters: Optional[Dict[str, Any]] = None):
        """Apply the brightness and contrast effect to a frame."""
        if parameters is None:
            parameters = self.parameters
        
        # Extract parameters
        brightness = parameters.get('brightness', 0)
        contrast = parameters.get('contrast', 1.0)
        gamma = parameters.get('gamma', 1.0)
        auto_adjust = parameters.get('auto_adjust', False)
        preserve_highlights = parameters.get('preserve_highlights', True)
        preserve_shadows = parameters.get('preserve_shadows', True)
        
        # Apply auto adjustment if enabled
        if auto_adjust:
            frame = self._auto_adjust_brightness_contrast(frame)
        
        # Apply basic brightness and contrast
        adjusted = cv2.convertScaleAbs(frame, alpha=contrast, beta=brightness)
        
        # Apply gamma correction
        if gamma != 1.0:
            adjusted = self._apply_gamma_correction(adjusted, gamma)
        
        # Preserve highlights and shadows if enabled
        if preserve_highlights or preserve_shadows:
            adjusted = self._preserve_details(frame, adjusted, preserve_highlights, preserve_shadows)
        
        return adjusted
    
    def _auto_adjust_brightness_contrast(self, frame):
        """Automatically adjust brightness and contrast."""
        # Convert to LAB color space
        lab = cv2.cvtColor(frame, cv2.COLOR_BGR2LAB)
        
        # Calculate mean and standard deviation for L channel
        l_channel = lab[:, :, 0]
        mean_l = np.mean(l_channel)
        std_l = np.std(l_channel)
        
        # Calculate target values
        target_mean = 127
        target_std = 50
        
        # Calculate scaling factors
        alpha = target_std / std_l if std_l > 0 else 1.0
        beta = target_mean - alpha * mean_l
        
        # Apply adjustment
        adjusted_l = np.clip(alpha * l_channel + beta, 0, 255).astype(np.uint8)
        lab[:, :, 0] = adjusted_l
        
        # Convert back to BGR
        return cv2.cvtColor(lab, cv2.COLOR_LAB2BGR)
    
    def _apply_gamma_correction(self, frame, gamma):
        """Apply gamma correction to the frame."""
        # Create gamma lookup table
        inv_gamma = 1.0 / gamma
        table = np.array([((i / 255.0) ** inv_gamma) * 255 for i in np.arange(0, 256)]).astype("uint8")
        
        # Apply gamma correction
        return cv2.LUT(frame, table)
    
    def _preserve_details(self, original, processed, preserve_highlights, preserve_shadows):
        """Preserve highlight and shadow details."""
        # Convert to grayscale for analysis
        gray_original = cv2.cvtColor(original, cv2.COLOR_BGR2GRAY)
        gray_processed = cv2.cvtColor(processed, cv2.COLOR_BGR2GRAY)
        
        # Create masks for highlights and shadows
        if preserve_highlights:
            highlight_mask = gray_original > 200
            processed[highlight_mask] = original[highlight_mask]
        
        if preserve_shadows:
            shadow_mask = gray_original < 50
            processed[shadow_mask] = original[shadow_mask]
        
        return processed 