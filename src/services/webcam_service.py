import logging
import threading
import time
import av
import cv2
import numpy as np
from PyQt5.QtCore import QObject, pyqtSignal, QTimer
from typing import Optional, Dict, Any
from pyvirtualcam import Camera, PixelFormat, Backend

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
        self._initialization_timer = None
        
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
                
            # Store style information first
            self._style_instance = style_instance
            self._style_params = style_params or {}
            self._input_device = device
            
            # Set running flag immediately
            self._is_running = True
            self.logger.info("Webcam service starting...")
            
            # Initialize camera directly (simpler approach)
            success = self._initialize_camera_async(device)
            if not success:
                self._is_running = False
                return False
            
            return True
                
        except Exception as e:
            error_msg = f"Error starting webcam service: {e}"
            self.logger.error(error_msg)
            self.error_signal.emit(error_msg)
            self._is_running = False  # Reset flag on error
            return False
    
    def _initialize_camera_async(self, device: str):
        """Initialize camera synchronously (simplified approach)."""
        try:
            self.logger.info(f"Initializing camera for device: {device}")
            
            # Try to open camera directly
            device_index = int(device) if device.isdigit() else 0
            
            # Try camera indices in order
            camera_indices = [device_index, 0, 1, 2]
            
            for idx in camera_indices:
                try:
                    self.logger.info(f"Trying camera index: {idx}")
                    
                    # Open camera with timeout
                    import threading
                    import time
                    
                    camera_result = {'success': False, 'cap': None}
                    
                    def open_camera():
                        try:
                            # Try different backends in order of preference
                            backends = [
                                cv2.CAP_ANY,  # Auto-detect
                                cv2.CAP_DSHOW,  # DirectShow
                                cv2.CAP_MSMF,   # Media Foundation
                                cv2.CAP_V4L2    # Video4Linux2
                            ]
                            
                            for backend in backends:
                                try:
                                    cap = cv2.VideoCapture(idx, backend)
                                    if cap.isOpened():
                                        # Set camera properties
                                        cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
                                        cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
                                        cap.set(cv2.CAP_PROP_FPS, 30)
                                        
                                        # Test reading a frame
                                        ret, test_frame = cap.read()
                                        if ret and test_frame is not None:
                                            camera_result['success'] = True
                                            camera_result['cap'] = cap
                                            self.logger.info(f"Camera {idx} can read frames: {test_frame.shape} (backend: {backend})")
                                            break
                                        else:
                                            cap.release()
                                    else:
                                        self.logger.warning(f"Failed to open camera {idx} with backend {backend}")
                                except Exception as e:
                                    self.logger.warning(f"Error trying camera {idx} with backend {backend}: {e}")
                                    continue
                            
                            if not camera_result['success']:
                                self.logger.warning(f"All backends failed for camera {idx}")
                                
                        except Exception as e:
                            self.logger.warning(f"Error trying camera {idx}: {e}")
                    
                    # Run camera opening in a separate thread with timeout
                    camera_thread = threading.Thread(target=open_camera)
                    camera_thread.daemon = True
                    camera_thread.start()
                    
                    # Wait for camera thread with timeout
                    timeout = 1.5  # Reduced timeout to 1.5 seconds
                    start_time = time.time()
                    while camera_thread.is_alive() and (time.time() - start_time) < timeout:
                        time.sleep(0.05)  # Faster polling
                    
                    if camera_result['success']:
                        self._container = camera_result['cap']
                        self.logger.info(f"Camera initialized successfully at index: {idx}")
                        self.info_signal.emit(f"Camera initialized: {idx}")
                        break
                    else:
                        if camera_thread.is_alive():
                            self.logger.warning(f"Camera {idx} initialization timed out")
                        else:
                            self.logger.warning(f"Camera {idx} failed to initialize")
                        
                except Exception as e:
                    self.logger.warning(f"Error trying camera {idx}: {e}")
                    continue
            else:
                # If we get here, no camera was found
                self.logger.warning("No camera available, continuing without camera")
                self.logger.warning("Camera initialization failed - will use test frames")
                self.info_signal.emit("No camera available")
                
            # Open virtual camera (uses OBS Virtual Camera by default)
            try:
                # Create virtual camera - it will automatically use OBS Virtual Camera
                self._camera = Camera(
                    width=640, 
                    height=480, 
                    fps=30, 
                    fmt=PixelFormat.BGR
                )
                
                # Log the actual device name that was created
                device_name = getattr(self._camera, 'device', 'Unknown')
                backend_name = getattr(self._camera, 'backend', 'Unknown')
                self.logger.info(f"Virtual camera enabled - Device: {device_name}, Backend: {backend_name}")
                self.info_signal.emit(f"Virtual camera enabled - {device_name}")
                
            except Exception as e:
                error_msg = f"Error opening virtual camera: {e}"
                self.logger.error(error_msg)
                self.error_signal.emit(error_msg)
                if self._container:
                    self._container.release()
                    self._container = None
                return False
            # Always start processing thread (even without camera for proper state management)
            self._thread = threading.Thread(target=self._process_frames)
            self._thread.daemon = True  # Make thread daemon so it doesn't block app exit
            self._thread.start()
            
            if self._container and self._container.isOpened():
                self.logger.info("Camera processing thread started with camera")
            else:
                self.logger.info("Camera processing thread started without camera (test mode)")
            
            self.logger.info("Camera initialization completed")
            return True
            
        except Exception as e:
            error_msg = f"Error in camera initialization: {e}"
            self.logger.error(error_msg)
            self.error_signal.emit(error_msg)
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
            # Check if we have a valid camera
            has_camera = self._container and self._container.isOpened()
            self.logger.info(f"Has camera: {has_camera}")
            
            if not has_camera:
                self.logger.info("No camera available, running in test mode with generated frames")
                self.logger.info("Camera container: " + str(self._container))
                self.logger.info("Camera container is opened: " + str(self._container.isOpened() if self._container else "No container"))
                
            while self._is_running:
                # Only log every 100 frames to reduce noise
                if frame_count % 100 == 0:
                    self.logger.info(f"Processing frame {frame_count + 1}")
                frame_array = None
                
                if has_camera:
                    # Read frame from OpenCV VideoCapture
                    ret, frame_array = self._container.read()
                    
                    if not ret:
                        self.logger.warning("Failed to read frame from camera")
                        time.sleep(0.01)  # Brief pause before retry
                        continue
                else:
                    # Generate test frame when no camera is available
                    frame_array = self._generate_test_frame()
                    time.sleep(1/30)  # ~30 FPS for test frames
                    
                if not self._is_running:
                    self.logger.info("Service stopped, breaking processing loop")
                    break
                
                frame_count += 1
                
                # Apply style if available
                if self._style_instance:
                    try:
                        # Ensure params is a dictionary, even if empty
                        params = self._style_params or {}
                        
                        # Log parameter application more frequently for debugging
                        if params and frame_count % 10 == 0:
                            self.logger.info(f"🎨 Applying {self._style_instance.__class__.__name__} with params: {params}")
                        
                        frame_array = self._style_instance.apply(frame_array, params)
                        
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
                    self.frame_ready.emit(frame_array)
                except Exception as e:
                    self.logger.error(f"Error emitting frame: {e}")
                
                # Write to virtual camera
                if self._camera:
                    try:
                        self._camera.send(frame_array)
                    except Exception as e:
                        self.logger.error(f"Error writing to virtual camera: {e}")
                            
                # Small delay to control frame rate (only for camera frames)
                if has_camera:
                    time.sleep(1/30)  # ~30 FPS
                            
        except Exception as e:
            error_msg = f"Error processing frames: {e}"
            self.logger.error(error_msg)
            try:
                self.error_signal.emit(error_msg)
            except Exception:
                pass  # Ignore signal errors if object is being deleted
        finally:
            self.logger.info("Frame processing thread ending")
            self._is_running = False
    
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
        
    def update_parameters(self, params: Dict[str, Any]) -> None:
        """Update style parameters.
        
        Args:
            params (dict): New style parameters
        """
        self._style_params = params or {}
        self.logger.info(f"🔧 PARAMETERS UPDATED: {self._style_params}")
        
    def update_style(self, style_instance: Any, params: Dict[str, Any]) -> None:
        """Update the current style and parameters.
        
        Args:
            style_instance: Style instance to apply
            params (dict): Style parameters
        """
        self._style_instance = style_instance
        self._style_params = params or {}
        self.logger.info(f"Updated style to {style_instance.__class__.__name__ if style_instance else 'None'}")
        self.logger.info(f"Updated parameters: {self._style_params}")
        
    def get_last_frame(self) -> Optional[np.ndarray]:
        """Get the last processed frame."""
        if self._last_frame is not None:
            self.logger.debug(f"Returning last frame: {self._last_frame.shape}")
        else:
            self.logger.debug("No last frame available")
        return self._last_frame
        
    def is_running(self) -> bool:
        """Check if the service is running."""
        return self._is_running
    
    def get_available_styles(self) -> list:
        """Get list of available style names."""
        if self._style_instance:
            return [self._style_instance.__class__.__name__]
        return []
    
    def check_virtual_camera_availability(self) -> dict:
        """Check virtual camera availability and provide diagnostics."""
        diagnostics = {
            'available': False,
            'device_name': 'OBS Virtual Camera',
            'backends': [],
            'errors': [],
            'recommendations': []
        }
        
        try:
            # Test creating a virtual camera
            test_camera = Camera(width=640, height=480, fps=30, fmt=PixelFormat.BGR)
            device_name = getattr(test_camera, 'device', 'Unknown')
            backend_name = getattr(test_camera, 'backend', 'Unknown')
            test_camera.close()
            
            diagnostics['available'] = True
            diagnostics['backends'] = [backend_name]
            diagnostics['device_name'] = device_name
            
            diagnostics['recommendations'].append("Virtual camera should be available in OBS/Zoom")
            diagnostics['recommendations'].append(f"Look for '{device_name}' in device list")
                
        except Exception as e:
            diagnostics['errors'].append(f"Error creating virtual camera: {e}")
            diagnostics['recommendations'].append("Install OBS Studio to enable virtual camera support")
            diagnostics['recommendations'].append("Check Windows Camera privacy settings")
            diagnostics['recommendations'].append("Ensure pyvirtualcam is properly installed")
        
        return diagnostics
    
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
    
    @property
    def info_message(self):
        """Alias for info_signal for compatibility."""
        return self.info_signal 