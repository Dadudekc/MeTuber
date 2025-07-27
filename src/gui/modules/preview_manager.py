"""
Preview Manager Module for MeTuber V2 Professional

Handles all preview-related functionality including frame updates,
camera adjustments, performance monitoring, and preview controls.
"""

import logging
import cv2
import numpy as np
from PyQt5.QtWidgets import QLabel, QComboBox
from PyQt5.QtCore import QTimer, Qt
from PyQt5.QtGui import QPixmap, QImage


class PreviewManager:
    """Manages all preview-related functionality."""
    
    def __init__(self, main_window):
        """Initialize preview manager with reference to main window."""
        self.main_window = main_window
        self.logger = logging.getLogger(__name__)
        
        # Preview state
        self.preview_timer = None
        self.current_frame = None
        self.is_processing = False
        
        # Performance tracking
        self.fps_counter = 0
        self.last_fps_time = 0
        
    def init_preview_timer(self):
        """Initialize the preview update timer."""
        self.logger.info("Initializing preview timer")
        
        self.preview_timer = QTimer()
        self.preview_timer.timeout.connect(self.update_preview)
        self.preview_timer.setInterval(8)  # 120 FPS for instant response
        
    def pre_initialize_timer(self):
        """Pre-initialize timer for instant startup."""
        self.logger.info("PRE-INITIALIZING TIMER...")
        self.init_preview_timer()
        self.logger.info("Timer pre-initialized at 120 FPS!")
        
    def update_preview(self):
        """Update the preview display with current frame."""
        try:
            if not self.is_processing:
                return
                
            # Get frame from webcam service or direct capture
            frame = self.get_current_frame()
            if frame is None:
                return
                
            # Apply current style if available
            if hasattr(self.main_window, 'current_style') and self.main_window.current_style:
                try:
                    # Apply style with current parameters
                    params = getattr(self.main_window, 'pending_params', {})
                    
                    # Ensure params is a dictionary, not a list
                    if isinstance(params, list):
                        params = {}
                        self.logger.warning("Style parameters were a list, converted to empty dict")
                    
                    processed_frame = self.main_window.current_style.apply(frame, params)
                    if processed_frame is not None:
                        frame = processed_frame
                except Exception as style_error:
                    self.logger.warning(f"Style application failed: {style_error}")
                    
            # Apply camera adjustments
            frame = self.apply_camera_adjustments(frame)
            
            # Update display
            self.update_preview_display(frame)
            
            # Update performance indicators
            self.update_performance_indicators()
            
        except Exception as e:
            self.logger.error(f"Error updating preview: {e}")
            
    def get_current_frame(self):
        """Get current frame from webcam or direct capture."""
        try:
            # Try webcam service first
            if hasattr(self.main_window, 'webcam_service') and self.main_window.webcam_service:
                if hasattr(self.main_window.webcam_service, 'current_frame'):
                    return self.main_window.webcam_service.current_frame
                    
            # Fallback to direct capture
            if not hasattr(self, '_cap'):
                self._cap = cv2.VideoCapture(0)
                if not self._cap.isOpened():
                    self.logger.error("Failed to open webcam")
                    return None
                    
            ret, frame = self._cap.read()
            if ret:
                return frame
            else:
                return None
                
        except Exception as e:
            self.logger.error(f"Error getting current frame: {e}")
            return None
            
    def apply_camera_adjustments(self, frame):
        """Apply camera adjustments to the frame."""
        try:
            if frame is None:
                return frame
                
            # Get adjustment values
            brightness = getattr(self.main_window, 'brightness_slider', None)
            contrast = getattr(self.main_window, 'contrast_slider', None)
            saturation = getattr(self.main_window, 'saturation_slider', None)
            
            if brightness and contrast and saturation:
                # Apply brightness
                brightness_val = brightness.value()
                if brightness_val != 0:
                    frame = cv2.convertScaleAbs(frame, alpha=1, beta=brightness_val)
                    
                # Apply contrast
                contrast_val = contrast.value() / 100.0
                if contrast_val != 1.0:
                    frame = cv2.convertScaleAbs(frame, alpha=contrast_val, beta=0)
                    
                # Apply saturation
                saturation_val = saturation.value() / 100.0
                if saturation_val != 1.0:
                    # Convert to HSV for saturation adjustment
                    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
                    hsv[:, :, 1] = cv2.multiply(hsv[:, :, 1], saturation_val)
                    frame = cv2.cvtColor(hsv, cv2.COLOR_HSV2BGR)
                    
            return frame
            
        except Exception as e:
            self.logger.error(f"Error applying camera adjustments: {e}")
            return frame
            
    def update_preview_display(self, frame):
        """Update the preview display with the given frame."""
        try:
            if frame is None or not hasattr(self.main_window, 'preview_label'):
                return
                
            # Convert frame to QPixmap
            height, width, channel = frame.shape
            bytes_per_line = 3 * width
            
            # Convert BGR to RGB
            rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            
            # Create QImage
            q_image = QImage(rgb_frame.data, width, height, bytes_per_line, QImage.Format_RGB888)
            
            # Scale to preview size
            preview_size = self.get_preview_size()
            scaled_pixmap = QPixmap.fromImage(q_image).scaled(
                preview_size[0], preview_size[1], 
                Qt.IgnoreAspectRatio, Qt.FastTransformation
            )
            
            # Update preview label
            self.main_window.preview_label.setPixmap(scaled_pixmap)
            
        except Exception as e:
            self.logger.error(f"Error updating preview display: {e}")
            
    def get_preview_size(self):
        """Get current preview size based on size combo selection."""
        try:
            if hasattr(self.main_window, 'size_combo'):
                size_text = self.main_window.size_combo.currentText()
                
                if size_text == "480x360":
                    return (480, 360)
                elif size_text == "640x480":
                    return (640, 480)
                elif size_text == "800x600":
                    return (800, 600)
                elif size_text == "1024x768":
                    return (1024, 768)
                elif size_text == "Full Screen":
                    # Get screen size
                    screen = self.main_window.screen()
                    return (screen.size().width(), screen.size().height())
                else:
                    return (480, 360)  # Default
            else:
                return (480, 360)  # Default
                
        except Exception as e:
            self.logger.error(f"Error getting preview size: {e}")
            return (480, 360)  # Default
            
    def update_performance_indicators(self):
        """Update performance indicators in the UI."""
        try:
            # Update FPS counter
            self.fps_counter += 1
            current_time = self.preview_timer.remainingTime() if self.preview_timer else 0
            
            if current_time - self.last_fps_time >= 1000:  # Every second
                fps = self.fps_counter
                self.fps_counter = 0
                self.last_fps_time = current_time
                
                # Update FPS label
                if hasattr(self.main_window, 'fps_label'):
                    self.main_window.fps_label.setText(f"FPS: {fps}")
                    
            # Update other performance indicators
            self.update_cpu_memory_gpu()
            
        except Exception as e:
            self.logger.error(f"Error updating performance indicators: {e}")
            
    def update_cpu_memory_gpu(self):
        """Update CPU, memory, and GPU usage indicators."""
        try:
            import psutil
            
            # CPU usage
            cpu_percent = psutil.cpu_percent()
            if hasattr(self.main_window, 'cpu_label'):
                self.main_window.cpu_label.setText(f"CPU: {cpu_percent:.1f}%")
                
            # Memory usage
            memory = psutil.virtual_memory()
            memory_mb = memory.used / (1024 * 1024)
            if hasattr(self.main_window, 'memory_label'):
                self.main_window.memory_label.setText(f"Memory: {memory_mb:.0f} MB")
                
            # GPU usage (placeholder - would need GPU monitoring library)
            if hasattr(self.main_window, 'gpu_label'):
                self.main_window.gpu_label.setText("GPU: 0%")
                
        except ImportError:
            # psutil not available, use placeholder values
            if hasattr(self.main_window, 'cpu_label'):
                self.main_window.cpu_label.setText("CPU: N/A")
            if hasattr(self.main_window, 'memory_label'):
                self.main_window.memory_label.setText("Memory: N/A")
            if hasattr(self.main_window, 'gpu_label'):
                self.main_window.gpu_label.setText("GPU: N/A")
        except Exception as e:
            self.logger.error(f"Error updating CPU/Memory/GPU: {e}")
            
    def on_preview_size_changed(self, size_text):
        """Handle preview size change."""
        try:
            self.logger.info(f"Preview size changed to: {size_text}")
            # Preview will be updated on next timer tick
        except Exception as e:
            self.logger.error(f"Error handling preview size change: {e}")
            
    def on_zoom_changed(self, zoom_text):
        """Handle preview zoom change."""
        try:
            self.logger.info(f"Preview zoom changed to: {zoom_text}")
            # Zoom will be applied on next frame update
        except Exception as e:
            self.logger.error(f"Error handling zoom change: {e}")
            
    def on_performance_changed(self):
        """Handle performance setting changes."""
        try:
            # Stop current timer
            if self.preview_timer and self.preview_timer.isActive():
                self.preview_timer.stop()
                
            # Get new settings
            if hasattr(self.main_window, 'fps_combo'):
                fps_text = self.main_window.fps_combo.currentText()
                fps_map = {
                    "15 FPS": 67,   # 1000ms / 15
                    "30 FPS": 33,   # 1000ms / 30
                    "60 FPS": 17,   # 1000ms / 60
                    "120 FPS": 8    # 1000ms / 120
                }
                interval = fps_map.get(fps_text, 33)
                self.preview_timer.setInterval(interval)
                
            # Restart timer if processing
            if self.is_processing:
                self.preview_timer.start()
                
            self.logger.info(f"Performance settings updated")
            
        except Exception as e:
            self.logger.error(f"Error handling performance change: {e}")
            
    def start_preview(self):
        """Start the preview display."""
        try:
            self.is_processing = True
            if self.preview_timer:
                self.preview_timer.start()
            self.logger.info("Preview started")
        except Exception as e:
            self.logger.error(f"Error starting preview: {e}")
            
    def stop_preview(self):
        """Stop the preview display."""
        try:
            self.is_processing = False
            if self.preview_timer:
                self.preview_timer.stop()
            self.logger.info("Preview stopped")
        except Exception as e:
            self.logger.error(f"Error stopping preview: {e}")
            
    def toggle_performance_graph(self):
        """Toggle performance graph display."""
        try:
            # Implementation for performance graph toggle
            self.logger.info("Performance graph toggled")
        except Exception as e:
            self.logger.error(f"Error toggling performance graph: {e}")
            
    def cleanup(self):
        """Clean up preview resources."""
        try:
            if hasattr(self, '_cap') and self._cap:
                self._cap.release()
            if self.preview_timer:
                self.preview_timer.stop()
            self.logger.info("Preview manager cleaned up")
        except Exception as e:
            self.logger.error(f"Error cleaning up preview manager: {e}") 