"""
Preview Manager Module for Dreamscape V2 Professional

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
        self.preview_timer = QTimer()
        self.preview_timer.timeout.connect(self.update_preview)
        self.preview_timer.setInterval(1)  # 1000 FPS for instant response
        
    def pre_initialize_timer(self):
        """Pre-initialize timer for instant startup."""
        self.init_preview_timer()
        
    def update_preview(self):
        """Update the preview display with current frame."""
        try:
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
                    
                    processed_frame = self.main_window.current_style.apply(frame, params)
                    if processed_frame is not None:
                        frame = processed_frame
                except Exception as style_error:
                    self.logger.warning(f"Style application failed: {style_error}")
            
            # Apply plugin effect if available
            if hasattr(self.main_window, 'effect_manager') and self.main_window.effect_manager.current_effect:
                try:
                    current_effect = self.main_window.effect_manager.current_effect
                    
                    # Check if it's a plugin effect
                    if hasattr(current_effect, 'apply') and callable(current_effect.apply):
                        # Get current parameters from the effect manager
                        effect_params = {}
                        if hasattr(self.main_window.effect_manager, 'current_effect_params'):
                            effect_params = self.main_window.effect_manager.current_effect_params.copy()
                        
                        # If no stored parameters, get defaults from effect
                        if not effect_params and hasattr(current_effect, 'parameters'):
                            for param_name, param_def in current_effect.parameters.items():
                                effect_params[param_name] = param_def.get('default', 0)
                        
                        # Apply the plugin effect
                        processed_frame = current_effect.apply(frame, effect_params)
                        if processed_frame is not None:
                            frame = processed_frame
                            
                except Exception as plugin_error:
                    self.logger.warning(f"Plugin effect application failed: {plugin_error}")
                    
            # Apply camera adjustments
            frame = self.apply_camera_adjustments(frame)
            
            # Apply captioner overlay if active
            frame = self.apply_captioner_overlay(frame)
            
            # Store current frame
            self.current_frame = frame.copy()
            
            # Update display
            self.update_preview_display(frame)
            
            # Update performance indicators
            self.update_performance_indicators()
            
        except Exception as e:
            self.logger.error(f"Error updating preview: {e}")
            
    def get_current_frame(self):
        """Get current frame from webcam or direct capture."""
        try:
            # Try webcam service first (check both direct and through webcam_manager)
            webcam_service = None
            
            # Check if webcam_service is directly accessible
            if hasattr(self.main_window, 'webcam_service') and self.main_window.webcam_service:
                webcam_service = self.main_window.webcam_service
            # Check if webcam_service is accessible through webcam_manager
            elif (hasattr(self.main_window, 'webcam_manager') and 
                  self.main_window.webcam_manager and 
                  hasattr(self.main_window.webcam_manager, 'webcam_service') and 
                  self.main_window.webcam_manager.webcam_service):
                webcam_service = self.main_window.webcam_manager.webcam_service
            
            if webcam_service:
                # Try to get the last frame from webcam service
                if hasattr(webcam_service, 'get_last_frame'):
                    frame = webcam_service.get_last_frame()
                    if frame is not None:
                        self.logger.debug(f"Got frame from webcam service: {frame.shape}")
                        return frame
                    else:
                        self.logger.debug("Webcam service returned None frame")
                        
            # Try webcam manager
            if hasattr(self.main_window, 'webcam_manager') and self.main_window.webcam_manager:
                if hasattr(self.main_window.webcam_manager, 'get_current_frame'):
                    frame = self.main_window.webcam_manager.get_current_frame()
                    if frame is not None:
                        self.logger.debug(f"Got frame from webcam manager: {frame.shape}")
                        return frame
                        
            self.logger.info("No frames available from webcam services, trying direct capture...")
            # Fallback to direct capture (with timeout to prevent blocking)
            if not hasattr(self, '_cap'):
                try:
                    # Use a timeout approach to prevent blocking
                    import threading
                    import time
                    
                    self._cap = None
                    self._cap_ready = False
                    
                    def open_camera():
                        try:
                            cap = cv2.VideoCapture(0)
                            if cap.isOpened():
                                self._cap = cap
                                self._cap_ready = True
                            else:
                                self.logger.warning("Failed to open direct camera capture")
                        except Exception as e:
                            self.logger.error(f"Error opening direct camera: {e}")
                    
                    # Start camera opening in a separate thread with timeout
                    camera_thread = threading.Thread(target=open_camera)
                    camera_thread.daemon = True
                    camera_thread.start()
                    
                    # Wait for camera to be ready (with timeout)
                    timeout = 2.0  # 2 second timeout
                    start_time = time.time()
                    while not self._cap_ready and (time.time() - start_time) < timeout:
                        time.sleep(0.1)
                    
                    if not self._cap_ready:
                        self.logger.warning("Camera initialization timed out")
                        return self._generate_test_frame()
                        
                except Exception as e:
                    self.logger.error(f"Error in camera initialization: {e}")
                    return self._generate_test_frame()
                    
            # Read frame from direct capture
            if self._cap and self._cap.isOpened():
                ret, frame = self._cap.read()
                if ret:
                    return frame
                    
            # If no camera available, generate test frame
            return self._generate_test_frame()
            
        except Exception as e:
            self.logger.error(f"Error getting current frame: {e}")
            return self._generate_test_frame()
    
    def _generate_test_frame(self):
        """Generate a test frame when no camera is available."""
        try:
            # Create a simple test frame
            height, width = 480, 640
            frame = np.zeros((height, width, 3), dtype=np.uint8)
            
            # Add some visual elements to show it's working
            # Draw a gradient background
            for y in range(height):
                for x in range(width):
                    frame[y, x] = [
                        int(255 * x / width),  # Blue gradient
                        int(255 * y / height), # Green gradient
                        128  # Red constant
                    ]
            
            # Add text overlay
            cv2.putText(frame, "No Camera Available", (50, height//2), 
                       cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)
            cv2.putText(frame, "Check camera connection", (50, height//2 + 50), 
                       cv2.FONT_HERSHEY_SIMPLEX, 0.7, (200, 200, 200), 2)
            
            return frame
            
        except Exception as e:
            self.logger.error(f"Error generating test frame: {e}")
            # Return a simple black frame as last resort
            return np.zeros((480, 640, 3), dtype=np.uint8)
            
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
    
    def apply_captioner_overlay(self, frame):
        """Apply captioner overlay to the frame if active."""
        try:
            if frame is None:
                return frame
                
            # Check if captioner is available and active
            if (hasattr(self.main_window, 'ui_components') and 
                hasattr(self.main_window.ui_components, 'audio_captioner_controls')):
                
                audio_controls = self.main_window.ui_components.audio_captioner_controls
                
                if audio_controls and audio_controls.is_active():
                    captioner_manager = audio_controls.get_captioner_manager()
                    
                    if captioner_manager:
                        # Render captioner overlay
                        frame_with_captions = captioner_manager.render_frame(frame)
                        if frame_with_captions is not None:
                            return frame_with_captions
            
            return frame
            
        except Exception as e:
            self.logger.error(f"Error applying captioner overlay: {e}")
            return frame
            
    def update_preview_display(self, frame):
        """Update the preview display with the given frame."""
        try:
            if frame is None:
                return
                
            # Convert BGR to RGB
            rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            
            # Get frame dimensions
            height, width, channel = rgb_frame.shape
            bytes_per_line = 3 * width
            
            # Create QImage
            q_image = QImage(rgb_frame.data, width, height, bytes_per_line, QImage.Format_RGB888)
            
            # Scale to fill the entire preview label
            label_size = self.main_window.preview_label.size()
            scaled_pixmap = QPixmap.fromImage(q_image).scaled(
                label_size.width(), label_size.height(), 
                Qt.KeepAspectRatio, Qt.SmoothTransformation
            )
            
            # Update preview label
            self.main_window.preview_label.setPixmap(scaled_pixmap)
            
            # Force a repaint to ensure the pixmap is displayed
            self.main_window.preview_label.repaint()
            
        except Exception as e:
            self.logger.error(f"Error updating preview display: {e}")
            
    def get_preview_size(self):
        """Get current preview size based on size combo selection."""
        try:
            if hasattr(self.main_window, 'size_combo'):
                size_text = self.main_window.size_combo.currentText()
                
                if size_text == "480x360":
                    return (640, 480)  # Match label minimum size
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
                    return (640, 480)  # Default to match label size
            else:
                return (640, 480)  # Default to match label size
                
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
            # Zoom will be applied on next frame update
            pass
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
                
        except Exception as e:
            self.logger.error(f"Error handling performance change: {e}")
            
    def start_preview(self):
        """Start the preview display."""
        try:
            # Check if we have any frame source available
            test_frame = self.get_current_frame()
            if test_frame is None:
                self.logger.warning("No frame source available, preview will show test frame")
            
            self.is_processing = True
            
            # Update preview immediately without timer
            self.update_preview()
            
            # Start the preview timer for continuous updates (optional)
            if self.preview_timer and not self.preview_timer.isActive():
                self.preview_timer.start()
            
        except Exception as e:
            self.logger.error(f"Error starting preview: {e}")
            # Even if there's an error, try to show at least a test frame
            self.is_processing = True
            if self.preview_timer and not self.preview_timer.isActive():
                self.preview_timer.start()
            
    def stop_preview(self):
        """Stop the preview display."""
        try:
            self.is_processing = False
            if self.preview_timer:
                self.preview_timer.stop()
        except Exception as e:
            self.logger.error(f"Error stopping preview: {e}")
            
    def toggle_performance_graph(self):
        """Toggle performance graph display."""
        try:
            # Implementation for performance graph toggle
            pass
        except Exception as e:
            self.logger.error(f"Error toggling performance graph: {e}")
            
    def cleanup(self):
        """Clean up preview resources."""
        try:
            if hasattr(self, '_cap') and self._cap:
                self._cap.release()
            if self.preview_timer:
                self.preview_timer.stop()
        except Exception as e:
            self.logger.error(f"Error cleaning up preview manager: {e}") 