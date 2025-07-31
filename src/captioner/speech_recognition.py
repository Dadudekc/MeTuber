"""
Speech Recognition Module

Provides speech-to-text conversion functionality with support for
both local and cloud-based recognition engines.
"""

import numpy as np
import logging
import threading
import time
from typing import Callable, Optional, List
from queue import Queue
import io
import wave

try:
    import speech_recognition as sr
    SPEECH_RECOGNITION_AVAILABLE = True
except ImportError:
    SPEECH_RECOGNITION_AVAILABLE = False
    logging.warning("speech_recognition not available - cloud recognition disabled")

try:
    import whisper
    WHISPER_AVAILABLE = True
except ImportError:
    WHISPER_AVAILABLE = False
    logging.warning("whisper not available - local recognition disabled")

class SpeechRecognition:
    """Speech recognition engine with multiple backends."""
    
    def __init__(self, engine: str = "whisper", language: str = "en"):
        """
        Initialize speech recognition.
        
        Args:
            engine: Recognition engine ("whisper", "google", "azure")
            language: Language code (e.g., "en", "es", "fr")
        """
        self.logger = logging.getLogger(__name__)
        self.engine = engine
        self.language = language
        
        # Recognition state
        self.is_listening = False
        self.audio_buffer = []
        self.buffer_duration = 2.0  # seconds
        self.sample_rate = 16000
        
        # Callbacks
        self.on_transcription: Optional[Callable] = None
        self.on_error: Optional[Callable] = None
        
        # Threading
        self.recognition_thread = None
        self.audio_queue = Queue(maxsize=50)
        
        # Initialize recognition engine
        self._init_engine()
        
        self.logger.info(f"SpeechRecognition initialized with {engine} engine")
    
    def _init_engine(self):
        """Initialize the selected recognition engine."""
        try:
            if self.engine == "whisper":
                if WHISPER_AVAILABLE:
                    self.model = whisper.load_model("base")
                else:
                    self.logger.error("Whisper not available")
                    self.engine = "google"
            
            elif self.engine == "google":
                if SPEECH_RECOGNITION_AVAILABLE:
                    self.recognizer = sr.Recognizer()
                else:
                    self.logger.error("Google Speech Recognition not available")
                    self.engine = "dummy"
            
            elif self.engine == "dummy":
                pass  # No logging for dummy engine
            
            else:
                self.logger.warning(f"Unknown engine {self.engine}, using dummy")
                self.engine = "dummy"
                
        except Exception as e:
            self.logger.error(f"Error initializing {self.engine} engine: {e}")
            self.engine = "dummy"
    
    def start_listening(self):
        """Start listening for speech."""
        try:
            if self.is_listening:
                self.logger.warning("Already listening for speech")
                return True
            
            self.is_listening = True
            self.audio_buffer = []
            
            # Start recognition thread
            self.recognition_thread = threading.Thread(target=self._recognition_loop, daemon=True)
            self.recognition_thread.start()
            
            return True
            
        except Exception as e:
            self.logger.error(f"Failed to start speech recognition: {e}")
            return False
    
    def stop_listening(self):
        """Stop listening for speech."""
        try:
            self.is_listening = False
            
            if self.recognition_thread and self.recognition_thread.is_alive():
                self.recognition_thread.join(timeout=2.0)
            
            self.audio_buffer.clear()
            
        except Exception as e:
            self.logger.error(f"Error stopping speech recognition: {e}")
    
    def process_audio(self, audio_data: np.ndarray):
        """Process audio data for speech recognition."""
        try:
            if not self.is_listening:
                return
            
            # Add to buffer
            self.audio_buffer.extend(audio_data)
            
            # Check if buffer is full enough for recognition
            buffer_duration = len(self.audio_buffer) / self.sample_rate
            
            if buffer_duration >= self.buffer_duration:
                # Process buffer
                if not self.audio_queue.full():
                    self.audio_queue.put(np.array(self.audio_buffer))
                
                # Clear buffer
                self.audio_buffer = []
                
        except Exception as e:
            self.logger.error(f"Error processing audio: {e}")
    
    def _recognition_loop(self):
        """Main recognition loop."""
        while self.is_listening:
            try:
                # Get audio from queue
                if not self.audio_queue.empty():
                    audio_data = self.audio_queue.get(timeout=0.1)
                    
                    # Perform recognition
                    text = self._recognize_speech(audio_data)
                    
                    if text and text.strip():
                        # Call transcription callback
                        if self.on_transcription:
                            self.on_transcription(text.strip())
                
                time.sleep(0.1)  # Small delay to prevent busy waiting
                
            except Exception as e:
                self.logger.error(f"Error in recognition loop: {e}")
                time.sleep(0.5)
    
    def _recognize_speech(self, audio_data: np.ndarray) -> Optional[str]:
        """Recognize speech from audio data."""
        try:
            if self.engine == "whisper":
                return self._recognize_whisper(audio_data)
            elif self.engine == "google":
                return self._recognize_google(audio_data)
            elif self.engine == "dummy":
                return self._recognize_dummy(audio_data)
            else:
                return None
                
        except Exception as e:
            self.logger.error(f"Error in speech recognition: {e}")
            if self.on_error:
                self.on_error(str(e))
            return None
    
    def _recognize_whisper(self, audio_data: np.ndarray) -> Optional[str]:
        """Recognize speech using Whisper."""
        try:
            if not WHISPER_AVAILABLE:
                return None
            
            # Normalize audio
            audio_data = audio_data.astype(np.float32)
            if np.max(np.abs(audio_data)) > 0:
                audio_data = audio_data / np.max(np.abs(audio_data))
            
            # Perform recognition
            result = self.model.transcribe(audio_data, language=self.language)
            return result["text"]
            
        except Exception as e:
            self.logger.error(f"Whisper recognition error: {e}")
            return None
    
    def _recognize_google(self, audio_data: np.ndarray) -> Optional[str]:
        """Recognize speech using Google Speech Recognition."""
        try:
            if not SPEECH_RECOGNITION_AVAILABLE:
                return None
            
            # Convert to audio data format
            audio_bytes = self._numpy_to_audio_bytes(audio_data)
            
            # Create AudioData object
            audio = sr.AudioData(audio_bytes, self.sample_rate, 2)
            
            # Perform recognition
            text = self.recognizer.recognize_google(audio, language=self.language)
            return text
            
        except sr.UnknownValueError:
            # Speech was unintelligible
            return None
        except sr.RequestError as e:
            self.logger.error(f"Google Speech Recognition error: {e}")
            return None
        except Exception as e:
            self.logger.error(f"Google recognition error: {e}")
            return None
    
    def _recognize_dummy(self, audio_data: np.ndarray) -> Optional[str]:
        """Dummy recognition for testing."""
        try:
            # Simple energy-based speech detection
            rms = np.sqrt(np.mean(audio_data**2))
            
            if rms > 0.01:  # Threshold for speech detection
                # Return a dummy transcription
                return "Hello, this is a test transcription"
            
            return None
            
        except Exception as e:
            self.logger.error(f"Dummy recognition error: {e}")
            return None
    
    def _numpy_to_audio_bytes(self, audio_data: np.ndarray) -> bytes:
        """Convert numpy array to audio bytes."""
        try:
            # Normalize to 16-bit integers
            audio_int16 = (audio_data * 32767).astype(np.int16)
            
            # Create WAV file in memory
            with io.BytesIO() as wav_buffer:
                with wave.open(wav_buffer, 'wb') as wav_file:
                    wav_file.setnchannels(1)  # Mono
                    wav_file.setsampwidth(2)  # 16-bit
                    wav_file.setframerate(self.sample_rate)
                    wav_file.writeframes(audio_int16.tobytes())
                
                return wav_buffer.getvalue()
                
        except Exception as e:
            self.logger.error(f"Error converting audio to bytes: {e}")
            return b""
    
    def set_transcription_callback(self, callback: Callable):
        """Set callback for transcription results."""
        self.on_transcription = callback
    
    def set_error_callback(self, callback: Callable):
        """Set callback for recognition errors."""
        self.on_error = callback
    
    def set_language(self, language: str):
        """Set recognition language."""
        self.language = language
        self.logger.info(f"Language set to: {language}")
    
    def set_engine(self, engine: str):
        """Set recognition engine."""
        self.engine = engine
        self._init_engine()
        self.logger.info(f"Engine changed to: {engine}")
    
    def get_available_engines(self) -> List[str]:
        """Get list of available recognition engines."""
        engines = []
        
        if WHISPER_AVAILABLE:
            engines.append("whisper")
        
        if SPEECH_RECOGNITION_AVAILABLE:
            engines.append("google")
        
        engines.append("dummy")  # Always available for testing
        
        return engines
    
    def cleanup(self):
        """Clean up resources."""
        try:
            self.stop_listening()
            
            # Clear queues
            while not self.audio_queue.empty():
                try:
                    self.audio_queue.get_nowait()
                except:
                    pass
            
            self.logger.info("SpeechRecognition cleanup complete")
            
        except Exception as e:
            self.logger.error(f"Error during cleanup: {e}")
    
    def __del__(self):
        """Destructor to ensure cleanup."""
        self.cleanup() 