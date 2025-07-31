# Real-Time Speech-to-Text Captioner Feature Plan

## Overview
Implement a real-time speech-to-text captioner that captures audio from the microphone, transcribes it to text, and displays it as an overlay on the video feed with customizable styling and effects.

## Core Components

### 1. Audio Capture Module
- **Microphone Input**: Capture audio from system microphone
- **Audio Processing**: Real-time audio stream processing
- **Noise Reduction**: Optional noise filtering for better accuracy
- **Audio Format**: Support for common audio formats (16kHz, mono recommended)

### 2. Speech Recognition Engine
- **Local Recognition**: Use local models for privacy and speed
- **Cloud Recognition**: Optional cloud-based services for better accuracy
- **Language Support**: Multi-language support
- **Real-time Processing**: Low-latency transcription

### 3. Text Display System
- **Overlay Rendering**: Display text on video feed
- **Styling Options**: Font, color, size, background, effects
- **Animation**: Text fade-in/out, scrolling, typing effects
- **Positioning**: Customizable text placement

### 4. Configuration & Controls
- **UI Controls**: Enable/disable, style settings, language selection
- **Hotkeys**: Keyboard shortcuts for quick control
- **Settings Persistence**: Save user preferences

## Technical Implementation

### Audio Libraries
```python
# Primary options:
- pyaudio (cross-platform audio I/O)
- sounddevice (simpler alternative)
- speech_recognition (Google Speech Recognition API)
- whisper (OpenAI's local speech recognition)
```

### Speech Recognition Options
```python
# Local (Recommended for privacy):
- whisper (OpenAI) - High accuracy, local processing
- vosk - Lightweight, offline
- pocketsphinx - Very lightweight

# Cloud-based:
- Google Speech Recognition
- Azure Speech Services
- AWS Transcribe
```

### Text Rendering
```python
# Video overlay:
- OpenCV text rendering
- PIL/Pillow for text effects
- Custom font rendering
- Real-time compositing
```

## Feature Specifications

### Core Features
1. **Real-time Transcription**: < 500ms latency
2. **Text Overlay**: Customizable positioning and styling
3. **Language Support**: English (initial), expandable
4. **Noise Handling**: Basic noise reduction
5. **Privacy**: Local processing option

### Advanced Features
1. **Text Effects**: 
   - Fade in/out animations
   - Typing effect
   - Color transitions
   - Background blur/glow
2. **Smart Positioning**: Auto-avoid face detection
3. **Word Highlighting**: Emphasize important words
4. **Emotion Detection**: Color coding based on sentiment
5. **Translation**: Real-time translation overlay

### UI Controls
1. **Main Controls**:
   - Enable/Disable captioner
   - Microphone selection
   - Language selection
   - Text style presets
2. **Style Customization**:
   - Font family and size
   - Text color and opacity
   - Background style
   - Animation speed
3. **Advanced Settings**:
   - Noise reduction level
   - Recognition sensitivity
   - Text history length
   - Export options

## Implementation Phases

### Phase 1: Basic Audio Capture & Display
- [ ] Audio capture from microphone
- [ ] Basic text overlay on video
- [ ] Simple enable/disable controls
- [ ] Basic styling options

### Phase 2: Speech Recognition Integration
- [ ] Whisper integration for local recognition
- [ ] Real-time transcription
- [ ] Text formatting and display
- [ ] Error handling and fallbacks

### Phase 3: Advanced Features
- [ ] Text animations and effects
- [ ] Smart positioning
- [ ] Multiple language support
- [ ] Performance optimization

### Phase 4: Polish & Integration
- [ ] UI integration with existing app
- [ ] Settings persistence
- [ ] Hotkey support
- [ ] Documentation and testing

## File Structure
```
src/
├── captioner/
│   ├── __init__.py
│   ├── audio_capture.py      # Microphone input
│   ├── speech_recognition.py # Speech-to-text engine
│   ├── text_renderer.py      # Text overlay rendering
│   ├── captioner_manager.py  # Main coordination
│   └── ui_controls.py        # Captioner UI components
├── gui/
│   └── components/
│       └── captioner_panel.py # Captioner settings panel
└── styles/
    └── captioner/
        ├── text_effects.py   # Text animation effects
        └── overlay_styles.py # Overlay styling presets
```

## Dependencies
```python
# New dependencies needed:
- whisper (OpenAI speech recognition)
- pyaudio (audio capture)
- numpy (audio processing)
- pillow (text rendering)
- opencv-python (video overlay)
```

## Performance Considerations
- **Latency**: Target < 500ms end-to-end
- **CPU Usage**: Optimize for real-time processing
- **Memory**: Efficient audio buffer management
- **GPU**: Optional GPU acceleration for text rendering

## Privacy & Security
- **Local Processing**: Default to local speech recognition
- **No Data Storage**: Don't store audio or transcriptions
- **User Control**: Clear enable/disable controls
- **Transparency**: Clear indication when recording

## Future Enhancements
1. **Multi-language Support**: Automatic language detection
2. **Voice Commands**: Control app with voice
3. **Text-to-Speech**: Read back transcriptions
4. **Export Features**: Save transcriptions to file
5. **Integration**: Connect with streaming platforms
6. **AI Features**: Sentiment analysis, keyword highlighting 