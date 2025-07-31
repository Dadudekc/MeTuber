"""
Audio Capture Module for Real-Time Speech Recognition

Handles microphone input and audio stream processing for the captioner.
"""

import pyaudio
import numpy as np
import threading
import time
import logging
from typing import Callable, Optional
from queue import Queue

class AudioCapture:
    """Real-time audio capture from microphone."""
    
    def __init__(self, sample_rate: int = 16000, chunk_size: int = 1024, channels: int = 1):
        """
        Initialize audio capture.
        
        Args:
            sample_rate: Audio sample rate (Hz)
            chunk_size: Number of frames per buffer
            channels: Number of audio channels (1 for mono)
        """
        self.logger = logging.getLogger(__name__)
        self.sample_rate = sample_rate
        self.chunk_size = chunk_size
        self.channels = channels
        
        # Audio processing
        self.audio = pyaudio.PyAudio()
        self.stream = None
        self.is_recording = False
        self.audio_queue = Queue(maxsize=10)  # Buffer for audio chunks
        
        # Callbacks
        self.on_audio_data: Optional[Callable] = None
        
        # Threading
        self.audio_thread = None
        
        self.logger.info(f"AudioCapture initialized")
    
    def get_available_devices(self) -> list:
        """Get list of available audio input devices."""
        devices = []
        try:
            for i in range(self.audio.get_device_count()):
                device_info = self.audio.get_device_info_by_index(i)
                if device_info['maxInputChannels'] > 0:  # Input device
                    devices.append({
                        'index': i,
                        'name': device_info['name'],
                        'channels': device_info['maxInputChannels'],
                        'sample_rate': int(device_info['defaultSampleRate'])
                    })
        except Exception as e:
            self.logger.error(f"Error getting audio devices: {e}")
        
        return devices
    
    def start_recording(self, device_index: Optional[int] = None) -> bool:
        """
        Start recording audio from microphone.
        
        Args:
            device_index: Audio device index (None for default)
            
        Returns:
            True if recording started successfully
        """
        try:
            if self.is_recording:
                self.logger.warning("Already recording audio")
                return True
            
            # Open audio stream
            self.stream = self.audio.open(
                format=pyaudio.paFloat32,
                channels=self.channels,
                rate=self.sample_rate,
                input=True,
                input_device_index=device_index,
                frames_per_buffer=self.chunk_size,
                stream_callback=self._audio_callback
            )
            
            self.is_recording = True
            self.stream.start_stream()
            
            # Start processing thread
            self.audio_thread = threading.Thread(target=self._process_audio, daemon=True)
            self.audio_thread.start()
            
            self.logger.info("Audio recording started")
            return True
            
        except Exception as e:
            self.logger.error(f"Failed to start audio recording: {e}")
            return False
    
    def stop_recording(self):
        """Stop recording audio."""
        try:
            self.is_recording = False
            
            if self.stream:
                self.stream.stop_stream()
                self.stream.close()
                self.stream = None
            
            if self.audio_thread and self.audio_thread.is_alive():
                self.audio_thread.join(timeout=1.0)
            
            self.logger.info("Audio recording stopped")
            
        except Exception as e:
            self.logger.error(f"Error stopping audio recording: {e}")
    
    def _audio_callback(self, in_data, frame_count, time_info, status):
        """Callback for audio stream data."""
        try:
            if self.is_recording:
                # Convert bytes to numpy array
                audio_data = np.frombuffer(in_data, dtype=np.float32)
                
                # Add to queue for processing
                if not self.audio_queue.full():
                    self.audio_queue.put(audio_data)
                else:
                    # Queue is full, remove oldest data
                    try:
                        self.audio_queue.get_nowait()
                        self.audio_queue.put(audio_data)
                    except:
                        pass
                
        except Exception as e:
            self.logger.error(f"Error in audio callback: {e}")
        
        return (None, pyaudio.paContinue)
    
    def _process_audio(self):
        """Process audio data in background thread."""
        while self.is_recording:
            try:
                # Get audio data from queue
                if not self.audio_queue.empty():
                    audio_data = self.audio_queue.get(timeout=0.1)
                    
                    # Apply basic noise reduction
                    audio_data = self._reduce_noise(audio_data)
                    
                    # Check if audio contains speech (simple energy-based detection)
                    if self._has_speech(audio_data):
                        # Call callback with audio data
                        if self.on_audio_data:
                            self.on_audio_data(audio_data)
                
                time.sleep(0.01)  # Small delay to prevent busy waiting
                
            except Exception as e:
                self.logger.error(f"Error processing audio: {e}")
                time.sleep(0.1)
    
    def _reduce_noise(self, audio_data: np.ndarray) -> np.ndarray:
        """Apply basic noise reduction to audio data."""
        try:
            # Simple high-pass filter to remove low-frequency noise
            # This is a basic implementation - more sophisticated filters can be added
            if len(audio_data) > 1:
                # Remove DC component
                audio_data = audio_data - np.mean(audio_data)
                
                # Simple high-pass filter (remove frequencies below 80Hz)
                # This is a very basic implementation
                pass
            
            return audio_data
            
        except Exception as e:
            self.logger.error(f"Error in noise reduction: {e}")
            return audio_data
    
    def _has_speech(self, audio_data: np.ndarray) -> bool:
        """
        Detect if audio contains speech using energy-based detection.
        
        Args:
            audio_data: Audio data as numpy array
            
        Returns:
            True if speech is detected
        """
        try:
            # Calculate RMS energy
            rms = np.sqrt(np.mean(audio_data**2))
            
            # Simple threshold-based detection
            # This threshold might need adjustment based on microphone sensitivity
            threshold = 0.01
            
            return rms > threshold
            
        except Exception as e:
            self.logger.error(f"Error in speech detection: {e}")
            return False
    
    def set_audio_callback(self, callback: Callable):
        """Set callback function for audio data."""
        self.on_audio_data = callback
    
    def cleanup(self):
        """Clean up audio resources."""
        try:
            self.stop_recording()
            
            if self.audio:
                self.audio.terminate()
            
            self.logger.info("AudioCapture cleanup complete")
            
        except Exception as e:
            self.logger.error(f"Error during cleanup: {e}")
    
    def __del__(self):
        """Destructor to ensure cleanup."""
        self.cleanup() 