"""
Text Renderer Module for Video Overlay

Handles rendering transcribed text as an overlay on video frames with
customizable styling and animation effects.
"""

import cv2
import numpy as np
from PIL import Image, ImageDraw, ImageFont
import logging
from typing import Tuple, Optional, Dict, Any
from dataclasses import dataclass
import time

@dataclass
class TextStyle:
    """Text styling configuration."""
    font_family: str = "Arial"
    font_size: int = 32
    font_color: Tuple[int, int, int] = (255, 255, 255)  # White
    background_color: Optional[Tuple[int, int, int]] = (0, 0, 0)  # Black
    background_opacity: float = 0.7
    outline_color: Optional[Tuple[int, int, int]] = (0, 0, 0)  # Black outline
    outline_width: int = 2
    padding: int = 10
    corner_radius: int = 5
    shadow_offset: Tuple[int, int] = (2, 2)
    shadow_color: Tuple[int, int, int] = (0, 0, 0)
    shadow_blur: int = 3

@dataclass
class AnimationConfig:
    """Animation configuration."""
    fade_in_duration: float = 0.3
    fade_out_duration: float = 0.5
    typing_speed: float = 0.05  # seconds per character
    scroll_speed: float = 1.0   # pixels per second
    bounce_amplitude: float = 5.0
    bounce_frequency: float = 2.0

class TextRenderer:
    """Renders text overlays on video frames."""
    
    def __init__(self):
        """Initialize text renderer."""
        self.logger = logging.getLogger(__name__)
        self.style = TextStyle()
        self.animation = AnimationConfig()
        
        # Text state
        self.current_text = ""
        self.text_history = []
        self.max_history = 5
        
        # Animation state
        self.text_start_time = 0
        self.typing_index = 0
        self.fade_alpha = 0.0
        self.is_visible = False
        
        # Font cache
        self.font_cache = {}
        
        self.logger.info("TextRenderer initialized")
    
    def set_style(self, style: TextStyle):
        """Set text styling."""
        self.style = style
    
    def set_animation(self, animation: AnimationConfig):
        """Set animation configuration."""
        self.animation = animation
    
    def update_text(self, text: str):
        """Update the current text to display."""
        if text != self.current_text:
            self.current_text = text
            self.text_start_time = time.time()
            self.typing_index = 0
            self.fade_alpha = 0.0
            self.is_visible = True
            
            # Add to history
            if text.strip():
                self.text_history.append({
                    'text': text,
                    'timestamp': time.time()
                })
                
                # Keep only recent history
                if len(self.text_history) > self.max_history:
                    self.text_history.pop(0)
    
    def render_overlay(self, frame: np.ndarray, position: Tuple[int, int] = None) -> np.ndarray:
        """
        Render text overlay on video frame.
        
        Args:
            frame: Input video frame (BGR format)
            position: Text position (x, y) - None for auto-positioning
            
        Returns:
            Frame with text overlay
        """
        try:
            if not self.current_text or not self.is_visible:
                return frame
            
            # Update animation state
            self._update_animation_state()
            
            # Get display text (with typing effect)
            display_text = self._get_display_text()
            
            if not display_text:
                return frame
            
            # Determine position
            if position is None:
                position = self._calculate_position(frame)
            
            # Create text image
            text_image = self._create_text_image(display_text)
            
            if text_image is None:
                return frame
            
            # Apply fade effect
            if self.fade_alpha < 1.0:
                text_image = self._apply_fade_effect(text_image)
            
            # Overlay on frame
            result_frame = self._overlay_text(frame, text_image, position)
            
            return result_frame
            
        except Exception as e:
            self.logger.error(f"Error rendering text overlay: {e}")
            return frame
    
    def _update_animation_state(self):
        """Update animation state based on time."""
        current_time = time.time()
        elapsed = current_time - self.text_start_time
        
        # Update typing effect
        if self.animation.typing_speed > 0:
            target_chars = int(elapsed / self.animation.typing_speed)
            self.typing_index = min(target_chars, len(self.current_text))
        
        # Update fade effect
        if elapsed < self.animation.fade_in_duration:
            # Fade in
            self.fade_alpha = elapsed / self.animation.fade_in_duration
        elif len(self.current_text) > 0 and elapsed > 3.0:  # Show for 3 seconds
            # Fade out
            fade_out_start = 3.0
            fade_out_elapsed = elapsed - fade_out_start
            if fade_out_elapsed < self.animation.fade_out_duration:
                self.fade_alpha = 1.0 - (fade_out_elapsed / self.animation.fade_out_duration)
            else:
                self.is_visible = False
                self.fade_alpha = 0.0
        else:
            # Fully visible
            self.fade_alpha = 1.0
    
    def _get_display_text(self) -> str:
        """Get text to display (with typing effect)."""
        if self.animation.typing_speed > 0:
            return self.current_text[:self.typing_index]
        else:
            return self.current_text
    
    def _calculate_position(self, frame: np.ndarray) -> Tuple[int, int]:
        """Calculate optimal text position on frame."""
        height, width = frame.shape[:2]
        
        # Default position: bottom center
        x = width // 2
        y = height - 100
        
        # TODO: Add face detection to avoid covering faces
        # TODO: Add smart positioning based on content
        
        return (x, y)
    
    def _create_text_image(self, text: str) -> Optional[np.ndarray]:
        """Create image with rendered text."""
        try:
            if not text.strip():
                return None
            
            # Get font
            font = self._get_font()
            if font is None:
                return None
            
            # Get text size
            bbox = font.getbbox(text)
            text_width = bbox[2] - bbox[0]
            text_height = bbox[3] - bbox[1]
            
            # Add padding
            total_width = text_width + (self.style.padding * 2)
            total_height = text_height + (self.style.padding * 2)
            
            # Create image with alpha channel
            image = Image.new('RGBA', (total_width, total_height), (0, 0, 0, 0))
            draw = ImageDraw.Draw(image)
            
            # Draw background if specified
            if self.style.background_color:
                background_alpha = int(255 * self.style.background_opacity)
                background_color = (*self.style.background_color, background_alpha)
                
                # Draw rounded rectangle background
                draw.rounded_rectangle(
                    [0, 0, total_width, total_height],
                    radius=self.style.corner_radius,
                    fill=background_color
                )
            
            # Draw shadow if specified
            if self.style.shadow_offset != (0, 0):
                shadow_x = self.style.padding + self.style.shadow_offset[0]
                shadow_y = self.style.padding + self.style.shadow_offset[1]
                draw.text(
                    (shadow_x, shadow_y),
                    text,
                    font=font,
                    fill=(*self.style.shadow_color, 128)
                )
            
            # Draw outline if specified
            if self.style.outline_color and self.style.outline_width > 0:
                for dx in range(-self.style.outline_width, self.style.outline_width + 1):
                    for dy in range(-self.style.outline_width, self.style.outline_width + 1):
                        if dx*dx + dy*dy <= self.style.outline_width*self.style.outline_width:
                            draw.text(
                                (self.style.padding + dx, self.style.padding + dy),
                                text,
                                font=font,
                                fill=(*self.style.outline_color, 255)
                            )
            
            # Draw main text
            draw.text(
                (self.style.padding, self.style.padding),
                text,
                font=font,
                fill=(*self.style.font_color, 255)
            )
            
            # Convert to numpy array (BGR format for OpenCV)
            text_image = np.array(image)
            text_image = cv2.cvtColor(text_image, cv2.COLOR_RGBA2BGRA)
            
            return text_image
            
        except Exception as e:
            self.logger.error(f"Error creating text image: {e}")
            return None
    
    def _get_font(self) -> Optional[ImageFont.FreeTypeFont]:
        """Get font for text rendering."""
        try:
            font_key = f"{self.style.font_family}_{self.style.font_size}"
            
            if font_key not in self.font_cache:
                # Try to load font
                try:
                    font = ImageFont.truetype(self.style.font_family, self.style.font_size)
                except:
                    # Fallback to default font
                    font = ImageFont.load_default()
                
                self.font_cache[font_key] = font
            
            return self.font_cache[font_key]
            
        except Exception as e:
            self.logger.error(f"Error loading font: {e}")
            return None
    
    def _apply_fade_effect(self, text_image: np.ndarray) -> np.ndarray:
        """Apply fade effect to text image."""
        try:
            if self.fade_alpha >= 1.0:
                return text_image
            
            # Apply alpha blending
            alpha_channel = text_image[:, :, 3].astype(np.float32)
            alpha_channel *= self.fade_alpha
            text_image[:, :, 3] = alpha_channel.astype(np.uint8)
            
            return text_image
            
        except Exception as e:
            self.logger.error(f"Error applying fade effect: {e}")
            return text_image
    
    def _overlay_text(self, frame: np.ndarray, text_image: np.ndarray, position: Tuple[int, int]) -> np.ndarray:
        """Overlay text image on video frame."""
        try:
            # Convert frame to RGBA if needed
            if frame.shape[2] == 3:
                frame_rgba = cv2.cvtColor(frame, cv2.COLOR_BGR2BGRA)
            else:
                frame_rgba = frame.copy()
            
            # Calculate position (center text horizontally)
            x, y = position
            text_height, text_width = text_image.shape[:2]
            x = x - text_width // 2
            y = y - text_height // 2
            
            # Ensure position is within frame bounds
            x = max(0, min(x, frame_rgba.shape[1] - text_width))
            y = max(0, min(y, frame_rgba.shape[0] - text_height))
            
            # Extract region of interest
            roi = frame_rgba[y:y+text_height, x:x+text_width]
            
            # Blend text image with ROI
            alpha = text_image[:, :, 3:4].astype(np.float32) / 255.0
            alpha = np.repeat(alpha, 3, axis=2)
            
            blended = (text_image[:, :, :3].astype(np.float32) * alpha + 
                      roi[:, :, :3].astype(np.float32) * (1 - alpha))
            
            # Update ROI
            roi[:, :, :3] = blended.astype(np.uint8)
            
            # Convert back to BGR if original was BGR
            if frame.shape[2] == 3:
                result = cv2.cvtColor(frame_rgba, cv2.COLOR_BGRA2BGR)
            else:
                result = frame_rgba
            
            return result
            
        except Exception as e:
            self.logger.error(f"Error overlaying text: {e}")
            return frame
    
    def clear_text(self):
        """Clear current text."""
        self.current_text = ""
        self.is_visible = False
        self.fade_alpha = 0.0
        self.logger.debug("Text cleared")
    
    def get_text_history(self) -> list:
        """Get text history."""
        return self.text_history.copy()
    
    def cleanup(self):
        """Clean up resources."""
        try:
            self.font_cache.clear()
            self.text_history.clear()
            self.logger.info("TextRenderer cleanup complete")
        except Exception as e:
            self.logger.error(f"Error during cleanup: {e}")
    
    def __del__(self):
        """Destructor to ensure cleanup."""
        self.cleanup() 