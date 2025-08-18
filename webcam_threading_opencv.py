# webcam_threading_opencv.py

import pyvirtualcam
import logging
from PyQt5.QtCore import QThread, pyqtSignal
import cv2
import numpy as np
import os
import traceback
import time
import queue
from collections import deque

DEBUG_MODE = os.environ.get("METUBER_DEBUG", "0") == "1"


class WebcamThreadOpenCV(QThread):
    """
    A QThread that captures video frames using OpenCV, applies the chosen style,
    and publishes them to a virtual camera with pyvirtualcam.
    """
    error_signal = pyqtSignal(str, object)  # message, exception
    info_signal = pyqtSignal(str)

    last_frame = None  # For snapshot feature

    def __init__(self, input_device, style_instance, style_params):
        super().__init__()
        self.input_device = input_device
        self.style_instance = style_instance
        self.style_params = style_params
        self.running = False
        self.last_frame = None
        self.logger = logging.getLogger(__name__)
        self.logger.setLevel(logging.INFO)
        
        # Prevent duplicate logs
        if not self.logger.handlers:
            handler = logging.StreamHandler()
            formatter = logging.Formatter(
                '%(asctime)s - %(levelname)s - %(name)s - %(message)s'
            )
            handler.setFormatter(formatter)
            self.logger.addHandler(handler)

        # Attempt to import CameraError with fallback
        try:
            from pyvirtualcam import CameraError
            self.CameraError = CameraError
        except ImportError:
            try:
                from pyvirtualcam.errors import CameraError
                self.CameraError = CameraError
            except ImportError:
                self.CameraError = Exception  # Fallback to generic Exception

        # Buffer management settings
        self.max_fps = 30  # Limit frame rate
        self.frame_skip = 0  # Skip every Nth frame (0 = no skip)
        self.frame_count = 0
        self.last_frame_time = 0
        
        # Frame queue to prevent buffer buildup
        self.frame_queue = deque(maxlen=5)  # Only keep 5 frames max

    def _parse_input_device(self, input_device):
        """
        Parse input device string to determine if it's a camera index or device name.
        Returns camera index (int) or None if parsing fails.
        """
        try:
            # If it's just a number, treat as camera index
            if input_device.isdigit():
                return int(input_device)
            
            # If it starts with "video=", try to extract camera index
            if input_device.startswith("video="):
                # Try to find a working camera index
                for i in range(10):
                    cap = cv2.VideoCapture(i)
                    if cap.isOpened():
                        ret, frame = cap.read()
                        if ret:
                            cap.release()
                            self.logger.info(f"Using camera index {i} for device: {input_device}")
                            return i
                        cap.release()
                
                # If no working camera found, default to 0
                self.logger.warning(f"No working camera found, defaulting to index 0")
                return 0
            
            # If it's a device name, try to find a working camera
            self.logger.info(f"Searching for working camera for device: {input_device}")
            for i in range(10):
                cap = cv2.VideoCapture(i)
                if cap.isOpened():
                    ret, frame = cap.read()
                    if ret:
                        cap.release()
                        self.logger.info(f"Using camera index {i} for device: {input_device}")
                        return i
                    cap.release()
            
            # Default to 0 if nothing works
            self.logger.warning(f"Could not find working camera, defaulting to index 0")
            return 0
            
        except Exception as e:
            self.logger.error(f"Error parsing input device '{input_device}': {e}")
            return 0

    def run(self):
        """
        Continuously capture frames from the webcam using OpenCV,
        apply the chosen style, and send them to a virtual camera.
        """
        self.logger.info("WebcamThread started.")
        self.info_signal.emit("Webcam thread started.")
        
        camera_index = self._parse_input_device(self.input_device)
        
        try:
            # Open webcam with OpenCV
            cap = cv2.VideoCapture(camera_index)
            if not cap.isOpened():
                raise Exception(f"Could not open camera at index {camera_index}")
            
            # Get camera properties
            width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
            height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
            fps = cap.get(cv2.CAP_PROP_FPS)
            
            if width == 0 or height == 0:
                # Set default resolution if camera doesn't report it
                cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
                cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
                width, height = 640, 480
            
            # Limit FPS to reasonable value
            target_fps = min(self.max_fps, 15)  # Cap at 15 FPS to reduce load
            frame_interval = 1.0 / target_fps
            
            self.logger.info(f"Camera opened: {width}x{height} @ {fps}fps, target: {target_fps}fps")
            self.info_signal.emit(f"Camera ready: {width}x{height}")
            
            # Set up virtual camera
            with pyvirtualcam.Camera(width=width, height=height, fps=target_fps) as cam:
                self.logger.info(f"Virtual camera initialized: {width}x{height} @ {target_fps}fps")
                self.info_signal.emit(f"Virtual camera ready: {width}x{height}")
                
                frames_processed = 0
                frames_dropped = 0
                last_stats_time = time.time()
                
                while self.running:
                    # Frame rate limiting
                    current_time = time.time()
                    if current_time - self.last_frame_time < frame_interval:
                        time.sleep(0.001)  # Small sleep to prevent busy waiting
                        continue
                    
                    # Capture frame
                    ret, frame = cap.read()
                    if not ret:
                        self.logger.warning("Failed to capture frame")
                        frames_dropped += 1
                        continue
                    
                    # Frame skipping
                    self.frame_count += 1
                    if self.frame_skip > 0 and self.frame_count % (self.frame_skip + 1) != 0:
                        frames_dropped += 1
                        continue
                    
                    # Queue management - drop old frames if queue is full
                    if len(self.frame_queue) >= 3:  # Keep queue small
                        try:
                            self.frame_queue.popleft()  # Drop oldest frame
                            frames_dropped += 1
                        except IndexError:
                            pass
                    
                    try:
                        # Add to queue
                        self.frame_queue.append(frame)
                        
                        # Apply style
                        if self.style_instance:
                            processed_frame = self.style_instance.apply(frame, self.style_params)
                        else:
                            processed_frame = frame
                        
                        # Send to virtual camera
                        cam.send(processed_frame)
                        cam.sleep_until_next_frame()
                        
                        # Store last frame for snapshot
                        self.last_frame = processed_frame.copy()
                        self.last_frame_time = current_time
                        frames_processed += 1
                        
                        # Log stats every 5 seconds
                        if current_time - last_stats_time > 5.0:
                            self.logger.info(f"Buffer stats: {frames_processed} processed, {frames_dropped} dropped")
                            frames_processed = 0
                            frames_dropped = 0
                            last_stats_time = current_time
                        
                    except Exception as frame_error:
                        self.logger.warning(f"Frame processing error: {frame_error}")
                        frames_dropped += 1
                        # Continue processing other frames
                        continue
                        
        except Exception as e:
            error_msg = f"Unexpected error in WebcamThread: {e}"
            self.logger.error(error_msg, exc_info=True)
            if DEBUG_MODE:
                tb = traceback.format_exc()
                self.error_signal.emit(f"{error_msg}\n\nTraceback:\n{tb}", e)
            else:
                self.error_signal.emit(error_msg, e)
        finally:
            if 'cap' in locals():
                cap.release()
            self.logger.info("WebcamThread stopped.")
            self.info_signal.emit("Webcam thread stopped.")

    def stop(self):
        """Stop the webcam thread."""
        self.running = False
        self.logger.info("WebcamThread stop requested.")

    def get_last_frame(self):
        """Get the last captured frame for snapshot functionality."""
        return self.last_frame.copy() if self.last_frame is not None else None


