"""
Real-Time Speech-to-Text Captioner Module

This module provides real-time speech recognition and text overlay functionality
for the webcam filter application.
"""

from .captioner_manager import CaptionerManager
from .audio_capture import AudioCapture
from .speech_recognition import SpeechRecognition
from .text_renderer import TextRenderer

__all__ = [
    'CaptionerManager',
    'AudioCapture', 
    'SpeechRecognition',
    'TextRenderer'
]

__version__ = "1.0.0" 