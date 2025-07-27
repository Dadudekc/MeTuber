import logging
import threading
import time
import av
import cv2
import numpy as np
from PyQt5.QtCore import QObject, pyqtSignal
from typing import Optional, Dict, Any
from pyvirtualcam import Camera, PixelFormat

# Handle different PyAV versions
try:
    AVError = av.AVError
except AttributeError:
    # Fallback for newer PyAV versions where AVError might not exist
    AVError = Exception

class WebcamService(QObject):
    """Service for managing webcam input and virtual camera output."""
    
    frame_ready = pyqtSignal(np.ndarray)
    error_signal = pyqtSignal(str)
    info_signal = pyqtSignal(str)
    
    def __init__(self):
        super().__init__()
        self.logger = logging.getLogger(__name__)
        
        # Initialize state
        self._is_running = False
        self._container = None
        self._camera = None
        self._style_instance = None
        self._style_params = {}
        self._thread = None
        self._last_frame = None
        self._input_device = ""
        
    def start(self, device: str, style_instance: Any, style_params: Dict[str, Any]) -> bool:
        """Start the webcam service.
        
        Args:
            device (str): Device identifier
            style_instance: Style instance to apply
            style_params (dict): Style parameters
            
        Returns:
            bool: True if started successfully, False otherwise
        """
        try:
            if self._is_running:
                self.logger.warning("Webcam service is already running")
                return False
                
            # Open input device using OpenCV (more reliable than PyAV)
            try:
                device_index = int(device) if device.isdigit() else 0
                self._container = cv2.VideoCapture(device_index)
                
                if not self._container.isOpened():
                    raise Exception(f"Failed to open camera {device_index}")
                    
                # Set camera properties for better quality
                self._container.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
                self._container.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
                self._container.set(cv2.CAP_PROP_FPS, 30)
                
                self._input_device = device
                self.logger.info(f"Opened input device: {device} using OpenCV")
                self.info_signal.emit(f"Opened input device: {device}")
            except Exception as e:
                error_msg = f"Error opening webcam: {e}"
                self.logger.error(error_msg)
                self.error_signal.emit(error_msg)
                return False
                
            # Open virtual camera (temporarily disabled to debug crashes)
            try:
                # self._camera = Camera(width=640, height=480, fps=30, fmt=PixelFormat.BGR)
                self._camera = None  # Temporarily disabled
                self.logger.info("Virtual camera disabled for debugging")
                self.info_signal.emit("Virtual camera disabled for debugging")
            except Exception as e:
                error_msg = f"Error opening virtual camera: {e}"
                self.logger.error(error_msg)
                self.error_signal.emit(error_msg)
                if self._container:
                    self._container.release()
                    self._container = None
                return False
                
            # Store style information
            self._style_instance = style_instance
            self._style_params = style_params or {}
            
            # Start processing thread
            self._is_running = True
            self._thread = threading.Thread(target=self._process_frames)
            self._thread.start()
            
            self.logger.info("Webcam service started")
            self.info_signal.emit("Webcam service started")
            return True
            
        except Exception as e:
            error_msg = f"Error starting webcam service: {e}"
            self.logger.error(error_msg)
            self.error_signal.emit(error_msg)
            self.stop()
            return False
            
    def stop(self) -> None:
        """Stop the webcam service."""
        self._is_running = False
        
        # Wait for thread to finish
        if self._thread and self._thread.is_alive():
            try:
                self._thread.join(timeout=2)
                if self._thread.is_alive():
                    self.logger.warning("Thread did not stop gracefully, continuing anyway")
            except Exception as e:
                self.logger.error(f"Error stopping thread: {e}")
            
        # Close resources
        try:
            if self._container:
                self._container.release()
                self._container = None
        except Exception as e:
            self.logger.error(f"Error closing container: {e}")
            
        try:
            if self._camera:
                self._camera.close()
                self._camera = None
        except Exception as e:
            self.logger.error(f"Error closing camera: {e}")
            
        # Clear style information
        self._style_instance = None
        self._style_params = {}
        self._input_device = ""
        
        self.logger.info("Webcam service stopped")
        try:
            self.info_signal.emit("Webcam service stopped")
        except Exception as e:
            self.logger.error(f"Error emitting info signal: {e}")
        
    def _process_frames(self) -> None:
        """Process frames from the input device."""
        self.logger.info("Frame processing thread started")
        frame_count = 0
        
        try:
            while self._is_running:
                # Read frame from OpenCV VideoCapture
                ret, frame_array = self._container.read()
                
                if not ret:
                    self.logger.warning("Failed to read frame from camera")
                    time.sleep(0.01)  # Brief pause before retry
                    continue
                    
                if not self._is_running:
                    break
                
                frame_count += 1
                if frame_count <= 5:  # Log first 5 frames
                    self.logger.info(f"Processing frame {frame_count}: {frame_array.shape}")
                    
                # Apply style if available
                if self._style_instance and self._style_params:
                    try:
                        frame_array = self._style_instance.apply(frame_array, self._style_params)
                        # Ensure BGR format
                        if len(frame_array.shape) == 2:
                            frame_array = cv2.cvtColor(frame_array, cv2.COLOR_GRAY2BGR)
                    except Exception as e:
                        self.logger.error(f"Error applying style: {e}")
                        try:
                            self.error_signal.emit(f"Error applying style: {e}")
                        except Exception:
                            pass  # Ignore signal errors if object is being deleted
                        
                # Save last frame
                self._last_frame = frame_array.copy()
                
                # Emit frame
                try:
                    if frame_count <= 3:  # Log first 3 emissions
                        self.logger.info(f"Emitting frame {frame_count}")
                    self.frame_ready.emit(frame_array)
                except Exception as e:
                    self.logger.error(f"Error emitting frame: {e}")
                
                # Write to virtual camera (disabled for now)
                # if self._camera:
                #     try:
                #         self._camera.send(frame_array)
                #     except Exception as e:
                #         self.logger.error(f"Error writing to virtual camera: {e}")
                            
                # Small delay to control frame rate
                time.sleep(1/30)  # ~30 FPS
                            
        except Exception as e:
            error_msg = f"Error processing frames: {e}"
            self.logger.error(error_msg)
            try:
                self.error_signal.emit(error_msg)
            except Exception:
                pass  # Ignore signal errors if object is being deleted
        finally:
            self._is_running = False
            
    def update_parameters(self, params: Dict[str, Any]) -> None:
        """Update style parameters.
        
        Args:
            params (dict): New style parameters
        """
        self._style_params = params or {}
        
    def update_style(self, style_instance: Any, params: Dict[str, Any]) -> None:
        """Update the current style and parameters.
        
        Args:
            style_instance: Style instance to apply
            params (dict): Style parameters
        """
        self._style_instance = style_instance
        self._style_params = params or {}
        self.logger.info(f"Updated style to {style_instance.__class__.__name__ if style_instance else 'None'}")
        
    def get_last_frame(self) -> Optional[np.ndarray]:
        """Get the last processed frame."""
        return self._last_frame
        
    def is_running(self) -> bool:
        """Check if the service is running."""
        return self._is_running
    
    # Alias methods for compatibility with GUI modules
    def start_processing(self, device: str, style_instance: Any, style_params: Dict[str, Any]) -> bool:
        """Alias for start() method for compatibility."""
        return self.start(device, style_instance, style_params)
    
    def stop_processing(self) -> None:
        """Alias for stop() method for compatibility."""
        self.stop()
    
    @property
    def error_occurred(self):
        """Alias for error_signal for compatibility."""
        return self.error_signal 