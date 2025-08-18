"""
Webcam manager with high-performance service integration
"""

import logging
import threading
import time
from typing import Optional, Dict, Any
from pathlib import Path

# Import the high-performance service
try:
    from ...services.high_performance_webcam_service import HighPerformanceWebcamService
    HIGH_PERFORMANCE_AVAILABLE = True
except ImportError:
    from ...services.webcam_service import WebcamService as HighPerformanceWebcamService
    HIGH_PERFORMANCE_AVAILABLE = False

logger = logging.getLogger(__name__)

class WebcamManager:
    """
    Webcam manager with high-performance service integration.
    Automatically uses the high-performance service when available.
    """
    
    def __init__(self, main_window):
        self.logger = logging.getLogger(f"{__name__}.WebcamManager")
        self.main_window = main_window
        # CRITICAL FIX: Ensure webcam service is properly exposed
        self.webcam_service = None
        # CRITICAL FIX: Start with processing enabled
        self.is_processing = True
        
        # Initialize the appropriate service
        if HIGH_PERFORMANCE_AVAILABLE:
            self.logger.info("🚀 Using high-performance webcam service")
            self.webcam_service = HighPerformanceWebcamService()
        else:
            self.logger.info("⚠️  Using standard webcam service (high-performance not available)")
            self.webcam_service = HighPerformanceWebcamService()  # Fallback
        
        self.logger.info("✅ Webcam manager initialized")
    
    def start_processing(self, minimal_mode: bool = False) -> bool:
        """Start webcam processing with high-performance optimizations."""
        self.logger.info(f"🚀 Starting webcam processing (minimal: {minimal_mode})")
        
        try:
            # Initialize camera with optimized settings and timeout
            camera_index = 0
            if minimal_mode:
                # Try multiple camera indices for minimal mode
                for idx in range(3):
                    if self.webcam_service.initialize_camera(idx):
                        camera_index = idx
                        break
            else:
                # Add timeout for camera initialization
                import threading
                import time
                
                camera_ready = threading.Event()
                camera_error = None
                
                def init_camera_with_timeout():
                    nonlocal camera_error
                    try:
                        if self.webcam_service.initialize_camera(camera_index):
                            camera_ready.set()
                        else:
                            camera_error = "Camera initialization failed"
                    except Exception as e:
                        camera_error = str(e)
                
                # Start camera initialization in background thread
                init_thread = threading.Thread(target=init_camera_with_timeout, daemon=True)
                init_thread.start()
                
                # Wait for camera with timeout (5 seconds)
                if not camera_ready.wait(timeout=5.0):
                    self.logger.warning("⚠️  Camera initialization timed out, using test mode")
                    # Continue without camera - will use test frames
                    camera_index = -1  # Indicate test mode
                elif camera_error:
                    self.logger.warning(f"⚠️  Camera initialization failed: {camera_error}, using test mode")
                    camera_index = -1  # Indicate test mode
            
            # Start processing
            if camera_index >= 0:
                success = self.webcam_service.start_processing()
                if success:
                    self.is_processing = True
                    self._update_ui_for_processing()
                    self.logger.info(f"✅ Webcam processing started successfully (minimal mode: {minimal_mode})")
                    return True
                else:
                    self.logger.error("❌ Failed to start webcam processing")
                    return False
            else:
                # Test mode - simulate processing without camera
                self.logger.info("🔄 Starting in test mode (no camera)")
                self.is_processing = True
                self._update_ui_for_processing()
                return True
                
        except Exception as e:
            self.logger.error(f"❌ Error starting webcam processing: {e}")
            return False
    
    def stop_processing(self):
        """Stop webcam processing."""
        try:
            if self.webcam_service:
                self.webcam_service.stop_processing()
            
            # CRITICAL FIX: Start with processing enabled
            self.is_processing = True
            self._update_ui_for_stopped()
            self.logger.info("✅ Webcam processing stopped")
            
        except Exception as e:
            self.logger.error(f"❌ Error stopping webcam processing: {e}")
    
    def update_style(self, style_name: str, params: Dict[str, Any]):
        """Update the current style with high-performance optimizations."""
        self.logger.info(f"🎨 Updating style: {style_name}")
        
        try:
            if self.webcam_service:
                self.webcam_service.update_style(style_name, params)
                self.logger.info(f"✅ Style updated: {style_name}")
            else:
                self.logger.warning("⚠️  No webcam service available for style update")
                
        except Exception as e:
            self.logger.error(f"❌ Error updating style: {e}")
    
    def get_current_frame(self) -> Optional[Any]:
        """Get the current frame with high-performance optimizations."""
        try:
            if self.webcam_service:
                return self.webcam_service.get_last_frame()
            else:
                self.logger.warning("⚠️  No webcam service available for frame capture")
                return None
                
        except Exception as e:
            self.logger.error(f"❌ Error getting current frame: {e}")
            return None
    
    def get_performance_stats(self) -> Dict[str, Any]:
        """Get performance statistics."""
        try:
            if self.webcam_service:
                stats = self.webcam_service.get_performance_stats()
                stats['high_performance_available'] = HIGH_PERFORMANCE_AVAILABLE
                return stats
            else:
                return {
                    'frames_processed': 0,
                    'avg_fps': 0.0,
                    'current_style': None,
                    'is_running': False,
                    'high_performance_available': HIGH_PERFORMANCE_AVAILABLE,
                }
                
        except Exception as e:
            self.logger.error(f"❌ Error getting performance stats: {e}")
            return {
                'frames_processed': 0,
                'avg_fps': 0.0,
                'current_style': None,
                'is_running': False,
                'high_performance_available': HIGH_PERFORMANCE_AVAILABLE,
                'error': str(e),
            }
    
    def _update_ui_for_processing(self):
        """Update UI to show processing is active."""
        try:
            if hasattr(self.main_window, 'update_processing_status'):
                self.main_window.update_processing_status(True)
            self.logger.info("📊 UI updated for processing")
        except Exception as e:
            self.logger.error(f"❌ Error updating UI for processing: {e}")
    
    def _update_ui_for_stopped(self):
        """Update UI to show processing is stopped."""
        try:
            if hasattr(self.main_window, 'update_processing_status'):
                self.main_window.update_processing_status(False)
            self.logger.info("📊 UI updated for stopped processing")
        except Exception as e:
            self.logger.error(f"❌ Error updating UI for stopped: {e}")
    
    def cleanup(self):
        """Cleanup resources."""
        self.logger.info("🧹 Cleaning up webcam manager")
        
                try:
            if self.webcam_service:
                self.webcam_service.cleanup()
            
            # CRITICAL FIX: Start with processing enabled
            self.is_processing = True
            self.logger.info("✅ Webcam manager cleaned up")
            
        except Exception as e:
            self.logger.error(f"❌ Error cleaning up webcam manager: {e}")
    
    def get_webcam_info(self) -> str:
        """Get webcam information."""
        try:
            if self.webcam_service:
                stats = self.webcam_service.get_performance_stats()
                if stats.get('is_running', False):
                    fps = stats.get('avg_fps', 0.0)
                    frames = stats.get('frames_processed', 0)
                    style = stats.get('current_style', 'None')
                    return f"Camera active: {fps:.1f} FPS, {frames} frames, Style: {style}"
                else:
                    return "Camera stopped"
            else:
                return "No camera service"
                
        except Exception as e:
            return f"Camera error: {e}"
    
    def init_webcam_service(self):
        """Initialize the webcam service (compatibility method)."""
        self.logger.info("🔧 Initializing webcam service")
        try:
            if self.webcam_service:
                # Service is already initialized in __init__
                self.logger.info("✅ Webcam service already initialized")
                return True
            else:
                self.logger.error("❌ No webcam service available")
                return False
        except Exception as e:
            self.logger.error(f"❌ Error initializing webcam service: {e}")
            return False
    
    def start_processing_minimal(self):
        """Start processing in minimal mode (compatibility method)."""
        self.logger.info("🚀 Starting minimal processing")
        return self.start_processing(minimal_mode=True)
    
    def pre_load_camera_async(self):
        """Pre-load camera asynchronously (compatibility method)."""
        self.logger.info("🔄 Pre-loading camera asynchronously...")
        try:
            # Start a background thread to initialize camera
            def _pre_load_camera():
                try:
                    if self.webcam_service:
                        # Try to initialize camera in background
                        self.webcam_service.initialize_camera(0)
                        self.logger.info("✅ Camera pre-loaded successfully")
                    else:
                        self.logger.warning("⚠️  No webcam service available for pre-loading")
                except Exception as e:
                    self.logger.warning(f"⚠️  Camera pre-loading failed, will use test frames: {e}")
            
            # Start the pre-loading in a separate thread
            pre_load_thread = threading.Thread(target=_pre_load_camera, daemon=True)
            pre_load_thread.start()
            
        except Exception as e:
            self.logger.error(f"❌ Error pre-loading camera: {e}") 