"""
Captioner Manager Module

Main coordinator for the speech-to-text captioner system.
Integrates audio capture, speech recognition, and text rendering.
"""

import logging
import threading
import time
from typing import Optional, Callable, Dict, Any
from dataclasses import dataclass

from .audio_capture import AudioCapture
from .speech_recognition import SpeechRecognition
from .text_renderer import TextRenderer, TextStyle, AnimationConfig

@dataclass
class CaptionerConfig:
    """Configuration for the captioner system."""
    enabled: bool = False
    engine: str = "whisper"
    language: str = "en"
    device_index: Optional[int] = None
    sample_rate: int = 16000
    buffer_duration: float = 2.0
    
    # Text styling
    font_family: str = "Arial"
    font_size: int = 32
    font_color: tuple = (255, 255, 255)  # White
    background_color: Optional[tuple] = (0, 0, 0)  # Black
    background_opacity: float = 0.7
    outline_color: Optional[tuple] = (0, 0, 0)  # Black outline
    outline_width: int = 2
    
    # Animation
    fade_in_duration: float = 0.3
    fade_out_duration: float = 0.5
    typing_speed: float = 0.05
    show_duration: float = 3.0

class CaptionerManager:
    """Main manager for the speech-to-text captioner system."""
    
    def __init__(self, config: Optional[CaptionerConfig] = None):
        """
        Initialize captioner manager.
        
        Args:
            config: Configuration for the captioner system
        """
        self.logger = logging.getLogger(__name__)
        self.config = config or CaptionerConfig()
        
        # Components
        self.audio_capture: Optional[AudioCapture] = None
        self.speech_recognition: Optional[SpeechRecognition] = None
        self.text_renderer: Optional[TextRenderer] = None
        
        # State
        self.is_running = False
        self.is_initialized = False
        
        # Callbacks
        self.on_text_update: Optional[Callable] = None
        self.on_error: Optional[Callable] = None
        self.on_status_change: Optional[Callable] = None
        
        # Threading
        self.manager_thread = None
        
        self.logger.info("CaptionerManager initialized")
    
    def initialize(self) -> bool:
        """Initialize all captioner components."""
        try:
            # Initialize audio capture
            self.audio_capture = AudioCapture(
                sample_rate=self.config.sample_rate,
                chunk_size=1024,
                channels=1
            )
            
            # Initialize speech recognition
            self.speech_recognition = SpeechRecognition(
                engine=self.config.engine,
                language=self.config.language
            )
            
            # Initialize text renderer
            self.text_renderer = TextRenderer()
            
            # Configure text styling
            style = TextStyle(
                font_family=self.config.font_family,
                font_size=self.config.font_size,
                font_color=self.config.font_color,
                background_color=self.config.background_color,
                background_opacity=self.config.background_opacity,
                outline_color=self.config.outline_color,
                outline_width=self.config.outline_width
            )
            self.text_renderer.set_style(style)
            
            # Configure animation
            animation = AnimationConfig(
                fade_in_duration=self.config.fade_in_duration,
                fade_out_duration=self.config.fade_out_duration,
                typing_speed=self.config.typing_speed
            )
            self.text_renderer.set_animation(animation)
            
            # Set up callbacks
            self._setup_callbacks()
            
            self.is_initialized = True
            
            if self.on_status_change:
                self.on_status_change("Initialized")
            
            return True
            
        except Exception as e:
            self.logger.error(f"Failed to initialize captioner: {e}")
            if self.on_error:
                self.on_error(f"Initialization failed: {e}")
            return False
    
    def _setup_callbacks(self):
        """Set up callback connections between components."""
        try:
            # Audio capture -> Speech recognition
            if self.audio_capture and self.speech_recognition:
                self.audio_capture.set_audio_callback(self.speech_recognition.process_audio)
            
            # Speech recognition -> Text renderer
            if self.speech_recognition and self.text_renderer:
                self.speech_recognition.set_transcription_callback(self.text_renderer.update_text)
                self.speech_recognition.set_error_callback(self._handle_recognition_error)
            
        except Exception as e:
            self.logger.error(f"Error setting up callbacks: {e}")
    
    def start(self) -> bool:
        """Start the captioner system."""
        try:
            if not self.is_initialized:
                if not self.initialize():
                    return False
            
            if self.is_running:
                self.logger.warning("Captioner is already running")
                return True
            
            # Start audio capture
            if self.audio_capture:
                if not self.audio_capture.start_recording(self.config.device_index):
                    raise Exception("Failed to start audio capture")
            
            # Start speech recognition
            if self.speech_recognition:
                if not self.speech_recognition.start_listening():
                    raise Exception("Failed to start speech recognition")
            
            self.is_running = True
            
            # Start manager thread for monitoring
            self.manager_thread = threading.Thread(target=self._manager_loop, daemon=True)
            self.manager_thread.start()
            
            if self.on_status_change:
                self.on_status_change("Running")
            
            return True
            
        except Exception as e:
            self.logger.error(f"Failed to start captioner: {e}")
            if self.on_error:
                self.on_error(f"Start failed: {e}")
            return False
    
    def stop(self):
        """Stop the captioner system."""
        try:
            if not self.is_running:
                self.logger.warning("Captioner is not running")
                return
            
            self.is_running = False
            
            # Stop audio capture
            if self.audio_capture:
                self.audio_capture.stop_recording()
            
            # Stop speech recognition
            if self.speech_recognition:
                self.speech_recognition.stop_listening()
            
            # Wait for manager thread
            if self.manager_thread and self.manager_thread.is_alive():
                self.manager_thread.join(timeout=2.0)
            
            if self.on_status_change:
                self.on_status_change("Stopped")
            
        except Exception as e:
            self.logger.error(f"Error stopping captioner: {e}")
    
    def _manager_loop(self):
        """Main management loop for monitoring system health."""
        while self.is_running:
            try:
                # Check component health
                if self.audio_capture and not self.audio_capture.is_recording:
                    self.logger.warning("Audio capture stopped unexpectedly")
                    if self.on_error:
                        self.on_error("Audio capture stopped")
                
                if self.speech_recognition and not self.speech_recognition.is_listening:
                    self.logger.warning("Speech recognition stopped unexpectedly")
                    if self.on_error:
                        self.on_error("Speech recognition stopped")
                
                time.sleep(1.0)  # Check every second
                
            except Exception as e:
                self.logger.error(f"Error in manager loop: {e}")
                time.sleep(5.0)
    
    def _handle_recognition_error(self, error: str):
        """Handle speech recognition errors."""
        self.logger.error(f"Speech recognition error: {error}")
        if self.on_error:
            self.on_error(f"Recognition error: {error}")
    
    def render_frame(self, frame) -> Any:
        """
        Render text overlay on video frame.
        
        Args:
            frame: Input video frame
            
        Returns:
            Frame with text overlay
        """
        try:
            if not self.is_running or not self.text_renderer:
                return frame
            
            return self.text_renderer.render_overlay(frame)
            
        except Exception as e:
            self.logger.error(f"Error rendering frame: {e}")
            return frame
    
    def update_config(self, config: CaptionerConfig):
        """Update captioner configuration."""
        try:
            self.logger.info("Updating captioner configuration...")
            
            # Stop if running
            was_running = self.is_running
            if was_running:
                self.stop()
            
            # Update config
            self.config = config
            
            # Reinitialize if needed
            if self.is_initialized:
                self.cleanup()
                self.initialize()
            
            # Restart if was running
            if was_running and config.enabled:
                self.start()
            
            self.logger.info("Configuration updated successfully")
            
        except Exception as e:
            self.logger.error(f"Error updating configuration: {e}")
            if self.on_error:
                self.on_error(f"Config update failed: {e}")
    
    def get_available_devices(self) -> list:
        """Get list of available audio input devices."""
        try:
            if self.audio_capture:
                return self.audio_capture.get_available_devices()
            return []
        except Exception as e:
            self.logger.error(f"Error getting devices: {e}")
            return []
    
    def get_available_engines(self) -> list:
        """Get list of available speech recognition engines."""
        try:
            if self.speech_recognition:
                return self.speech_recognition.get_available_engines()
            return []
        except Exception as e:
            self.logger.error(f"Error getting engines: {e}")
            return []
    
    def get_text_history(self) -> list:
        """Get text transcription history."""
        try:
            if self.text_renderer:
                return self.text_renderer.get_text_history()
            return []
        except Exception as e:
            self.logger.error(f"Error getting text history: {e}")
            return []
    
    def clear_text(self):
        """Clear current text display."""
        try:
            if self.text_renderer:
                self.text_renderer.clear_text()
        except Exception as e:
            self.logger.error(f"Error clearing text: {e}")
    
    def set_text_callback(self, callback: Callable):
        """Set callback for text updates."""
        self.on_text_update = callback
    
    def set_error_callback(self, callback: Callable):
        """Set callback for errors."""
        self.on_error = callback
    
    def set_status_callback(self, callback: Callable):
        """Set callback for status changes."""
        self.on_status_change = callback
    
    def get_status(self) -> Dict[str, Any]:
        """Get current system status."""
        try:
            status = {
                'running': self.is_running,
                'initialized': self.is_initialized,
                'enabled': self.config.enabled,
                'engine': self.config.engine,
                'language': self.config.language,
                'audio_capture_running': False,
                'speech_recognition_running': False
            }
            
            if self.audio_capture:
                status['audio_capture_running'] = self.audio_capture.is_recording
            
            if self.speech_recognition:
                status['speech_recognition_running'] = self.speech_recognition.is_listening
            
            return status
            
        except Exception as e:
            self.logger.error(f"Error getting status: {e}")
            return {'error': str(e)}
    
    def cleanup(self):
        """Clean up all resources."""
        try:
            self.logger.info("Cleaning up captioner resources...")
            
            # Stop if running
            if self.is_running:
                self.stop()
            
            # Clean up components
            if self.audio_capture:
                self.audio_capture.cleanup()
                self.audio_capture = None
            
            if self.speech_recognition:
                self.speech_recognition.cleanup()
                self.speech_recognition = None
            
            if self.text_renderer:
                self.text_renderer.cleanup()
                self.text_renderer = None
            
            self.is_initialized = False
            self.logger.info("Captioner cleanup complete")
            
        except Exception as e:
            self.logger.error(f"Error during cleanup: {e}")
    
    def __del__(self):
        """Destructor to ensure cleanup."""
        self.cleanup() 