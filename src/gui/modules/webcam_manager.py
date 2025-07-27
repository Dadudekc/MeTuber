"""
Webcam Manager Module for MeTuber V2 Professional

Handles all webcam-related functionality including service initialization,
frame processing, error handling, and service lifecycle management.
"""

import logging
import time
from PyQt5.QtCore import QThread, pyqtSignal, Qt


class WebcamManager:
    """Manages all webcam-related functionality."""
    
    def __init__(self, main_window):
        """Initialize webcam manager with reference to main window."""
        self.main_window = main_window
        self.logger = logging.getLogger(__name__)
        
        # Webcam service
        self.webcam_service = None
        self.is_initialized = False
        
        # Service state
        self.is_running = False
        self.current_device = 0
        
    def init_webcam_service(self):
        """Initialize the webcam service."""
        try:
            self.logger.info("Initializing webcam service")
            
            # Import webcam service
            from src.services.webcam_service import WebcamService
            
            # Create webcam service instance
            self.webcam_service = WebcamService()
            
            # Connect signals with queued connections for thread safety (if they exist)
            if hasattr(self.webcam_service, 'frame_ready'):
                self.webcam_service.frame_ready.connect(
                    self.on_frame_ready, Qt.QueuedConnection
                )
            if hasattr(self.webcam_service, 'error_occurred'):
                self.webcam_service.error_occurred.connect(
                    self.on_webcam_error, Qt.QueuedConnection
                )
            if hasattr(self.webcam_service, 'info_message'):
                self.webcam_service.info_message.connect(
                    self.on_webcam_info, Qt.QueuedConnection
                )
            
            # Store reference in main window for easy access
            self.main_window.webcam_service = self.webcam_service
            
            self.is_initialized = True
            self.logger.info("Webcam service initialized with queued connections")
            
        except Exception as e:
            self.logger.error(f"Error initializing webcam service: {e}")
            import traceback
            self.logger.error(f"Traceback: {traceback.format_exc()}")
            
    def pre_load_camera(self):
        """Pre-load camera for instant startup."""
        try:
            self.logger.info("PRE-LOADING CAMERA...")
            
            # Initialize webcam service
            self.init_webcam_service()
            
            # Test camera access (just initialize, don't start processing)
            if self.webcam_service:
                # Just verify the service is ready, don't start processing during pre-load
                self.logger.info("Webcam service ready for processing")
                
            self.logger.info("Camera pre-loaded and ready!")
            
        except Exception as e:
            self.logger.error(f"Error pre-loading camera: {e}")
            
    def on_frame_ready(self, frame):
        """Handle frame ready signal from webcam service."""
        try:
            # Store current frame for preview manager
            if hasattr(self.main_window, 'webcam_service'):
                self.main_window.webcam_service.current_frame = frame
                
            # Update preview if processing
            if hasattr(self.main_window, 'preview_manager'):
                if self.main_window.preview_manager.is_processing:
                    # Frame will be processed in preview update
                    pass
                    
        except Exception as e:
            self.logger.error(f"Error handling frame ready: {e}")
            
    def on_webcam_error(self, error_msg):
        """Handle webcam error signal."""
        try:
            self.logger.error(f"Webcam error: {error_msg}")
            
            # Update status
            if hasattr(self.main_window, 'status_label'):
                self.main_window.status_label.setText(f"Webcam Error: {error_msg}")
                
            # Stop processing
            self.stop_processing()
            
        except Exception as e:
            self.logger.error(f"Error handling webcam error: {e}")
            
    def on_webcam_info(self, info_msg):
        """Handle webcam info signal."""
        try:
            self.logger.info(f"Webcam info: {info_msg}")
            
            # Update status
            if hasattr(self.main_window, 'status_label'):
                self.main_window.status_label.setText(info_msg)
                
        except Exception as e:
            self.logger.error(f"Error handling webcam info: {e}")
            
    def start_processing_minimal(self):
        """Start webcam processing with minimal loading for fastest startup."""
        try:
            if not self.is_initialized:
                self.init_webcam_service()
                
            if self.webcam_service:
                # Start processing without any style (raw video)
                device = str(self.current_device)
                
                # Start processing with minimal parameters
                try:
                    success = self.webcam_service.start_processing(device, None, {})
                    if success:
                        self.is_running = True
                        self.logger.info("Webcam processing started successfully (minimal mode)")
                    else:
                        self.logger.error("Failed to start webcam processing")
                        return
                except Exception as e:
                    self.logger.error(f"Error starting webcam processing: {e}")
                    return
                
                # Update UI
                if hasattr(self.main_window, 'start_stop_btn'):
                    self.main_window.start_stop_btn.setText("Stop Processing")
                    self.main_window.start_stop_btn.setStyleSheet("""
                        QPushButton {
                            background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                                stop:0 #aa0000, stop:1 #880000);
                            border: 1px solid #aa0000;
                            border-radius: 6px;
                            font-size: 12px;
                            font-weight: bold;
                        }
                        QPushButton:hover {
                            background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                                stop:0 #cc0000, stop:1 #aa0000);
                        }
                        QPushButton:pressed {
                            background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                                stop:0 #880000, stop:1 #660000);
                        }
                    """)
                
        except Exception as e:
            self.logger.error(f"Error in minimal processing start: {e}")
    
    def start_processing(self):
        """Start webcam processing."""
        try:
            if not self.is_initialized:
                self.init_webcam_service()
                
            if self.webcam_service:
                # Get default device and style for starting
                device = str(self.current_device)
                style_instance = None
                style_params = {}
                
                # Try to get a default style from style manager
                if hasattr(self.main_window, 'style_manager'):
                    try:
                        # Get a simple default style like "Original"
                        style_instance = self.main_window.style_manager.get_style("Original")
                        if not style_instance:
                            # Fallback to any available style
                            available_styles = self.main_window.style_manager.get_categories()
                            if available_styles:
                                first_category = list(available_styles.keys())[0]
                                first_style = available_styles[first_category][0] if available_styles[first_category] else None
                                if first_style:
                                    style_instance = self.main_window.style_manager.get_style(first_style)
                    except Exception as e:
                        self.logger.warning(f"Could not get default style: {e}")
                
                # Start processing with the parameters
                try:
                    success = self.webcam_service.start_processing(device, style_instance, style_params)
                    if success:
                        self.is_running = True
                        self.logger.info("Webcam processing started successfully")
                    else:
                        self.logger.error("Failed to start webcam processing")
                        return
                except Exception as e:
                    self.logger.error(f"Error starting webcam processing: {e}")
                    return
                
                # Update UI
                if hasattr(self.main_window, 'start_stop_btn'):
                    self.main_window.start_stop_btn.setText("Stop Processing")
                    self.main_window.start_stop_btn.setStyleSheet("""
                        QPushButton {
                            background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                                stop:0 #aa0000, stop:1 #880000);
                            border: 1px solid #aa0000;
                            border-radius: 6px;
                            font-size: 12px;
                            font-weight: bold;
                        }
                        QPushButton:hover {
                            background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                                stop:0 #cc0000, stop:1 #aa0000);
                        }
                        QPushButton:pressed {
                            background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                                stop:0 #880000, stop:1 #660000);
                        }
                    """)
                    
        except Exception as e:
            self.logger.error(f"Error starting webcam processing: {e}")
            
    def stop_processing(self):
        """Stop webcam processing."""
        try:
            if self.webcam_service:
                # Check if stop_processing method exists
                if hasattr(self.webcam_service, 'stop_processing'):
                    self.webcam_service.stop_processing()
                else:
                    # Alternative cleanup if method doesn't exist
                    if hasattr(self.webcam_service, 'release'):
                        self.webcam_service.release()
                    
                self.is_running = False
                self.logger.info("Webcam processing stopped")
                
                # Update UI
                if hasattr(self.main_window, 'start_stop_btn'):
                    self.main_window.start_stop_btn.setText("Start Processing")
                    self.main_window.start_stop_btn.setStyleSheet("""
                        QPushButton {
                            background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                                stop:0 #00aa00, stop:1 #008800);
                            border: 1px solid #00aa00;
                            border-radius: 6px;
                            font-size: 12px;
                            font-weight: bold;
                        }
                        QPushButton:hover {
                            background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                                stop:0 #00cc00, stop:1 #00aa00);
                        }
                        QPushButton:pressed {
                            background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                                stop:0 #008800, stop:1 #006600);
                        }
                    """)
                    
        except Exception as e:
            self.logger.error(f"Error stopping webcam processing: {e}")
            
    def toggle_processing(self):
        """Toggle webcam processing on/off."""
        try:
            if self.is_running:
                self.stop_processing()
            else:
                self.start_processing()
                
        except Exception as e:
            self.logger.error(f"Error toggling processing: {e}")
            
    def update_style(self, style_instance, parameters=None):
        """Update the current style in webcam service."""
        try:
            if self.webcam_service:
                self.webcam_service.update_style(style_instance, parameters or {})
                self.logger.info(f"Updated style to {style_instance.__class__.__name__}")
                
        except Exception as e:
            self.logger.error(f"Error updating style: {e}")
            
    def on_device_changed(self, device_name):
        """Handle device change."""
        try:
            self.logger.info(f"Device changed to: {device_name}")
            
            # Parse device index from name
            if "Device" in device_name:
                try:
                    device_index = int(device_name.split()[-1]) - 1
                    self.current_device = device_index
                    
                    # Restart service with new device
                    if self.is_running:
                        self.stop_processing()
                        time.sleep(0.1)
                        self.start_processing()
                        
                except ValueError:
                    self.logger.warning(f"Could not parse device index from: {device_name}")
                    
        except Exception as e:
            self.logger.error(f"Error handling device change: {e}")
            
    def get_available_devices(self):
        """Get list of available webcam devices."""
        try:
            import cv2
            
            devices = []
            for i in range(10):  # Check first 10 devices
                cap = cv2.VideoCapture(i)
                if cap.isOpened():
                    devices.append(f"Device {i + 1}")
                    cap.release()
                    
            return devices
            
        except Exception as e:
            self.logger.error(f"Error getting available devices: {e}")
            return ["Device 1"]  # Fallback
            
    def get_current_frame(self):
        """Get current frame from webcam service."""
        try:
            if self.webcam_service and hasattr(self.webcam_service, 'current_frame'):
                return self.webcam_service.current_frame
            return None
            
        except Exception as e:
            self.logger.error(f"Error getting current frame: {e}")
            return None
            
    def is_processing_active(self):
        """Check if webcam processing is active."""
        return self.is_running and self.is_initialized
        
    def cleanup(self):
        """Clean up webcam resources."""
        try:
            if self.webcam_service:
                # Check if stop_processing method exists
                if hasattr(self.webcam_service, 'stop_processing'):
                    self.webcam_service.stop_processing()
                elif hasattr(self.webcam_service, 'release'):
                    self.webcam_service.release()
                    
                self.webcam_service = None
                
            self.is_initialized = False
            self.is_running = False
            
            self.logger.info("Webcam manager cleaned up")
            
        except Exception as e:
            self.logger.error(f"Error cleaning up webcam manager: {e}")
            
    def get_service_status(self):
        """Get current webcam service status."""
        return {
            'initialized': self.is_initialized,
            'running': self.is_running,
            'device': self.current_device,
            'service': self.webcam_service is not None
        } 