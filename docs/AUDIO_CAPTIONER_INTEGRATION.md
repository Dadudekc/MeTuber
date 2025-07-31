# Audio and Captioner Integration

## Overview

The Dreamscape Stream Software now includes comprehensive audio capture and speech-to-text captioner functionality. This feature allows users to capture audio from their microphone and display live captions/subtitles over their video feed in real-time.

## Features

### 🎤 Audio Capture
- **Multi-device support**: Automatically detects and lists all available audio input devices
- **Real-time audio level monitoring**: Visual indicator shows microphone input levels
- **Device selection**: Choose from available microphones and audio interfaces
- **Audio processing**: Noise reduction and speech detection capabilities

### 📝 Live Captioner
- **Multiple speech recognition engines**: Support for Whisper, Google Speech Recognition, and dummy engine
- **Multi-language support**: 10+ languages including English, Spanish, French, German, Italian, Portuguese, Russian, Japanese, Korean, and Chinese
- **Customizable text styling**: Font size, color, background opacity, and outline options
- **Animation effects**: Typing speed, fade in/out, and display duration controls
- **Real-time processing**: Low-latency speech-to-text conversion

## GUI Integration

### Audio & Captions Dock Panel

The audio and captioner functionality is integrated into the main GUI through a dedicated dock panel:

```
🎤 Audio & Captions
├── 🎤 Audio Input
│   ├── Device: [Dropdown with available microphones]
│   └── Level: [Progress bar showing audio input level]
├── 📝 Captioner Settings
│   ├── ☑️ Enable Live Captions
│   ├── Engine: [Whisper/Google/Dummy]
│   └── Language: [en/es/fr/de/it/pt/ru/ja/ko/zh]
├── 🎨 Text Styling
│   ├── Font Size: [12-72px slider]
│   ├── Font Color: [White/Yellow/Green/Cyan/Magenta]
│   └── Background Opacity: [0-100% slider]
├── ⚡ Animation
│   ├── Typing Speed: [1-20 slider]
│   └── Show Duration: [1-10 seconds slider]
├── 📊 Status
│   └── Captioner: [Ready/Active/Error status]
└── 🔄 Refresh Devices | 🎤 Test Captioner
```

### Integration Points

1. **Preview Pipeline**: Captions are rendered directly on the video feed in the preview area
2. **Real-time Updates**: Audio level monitoring and caption updates happen in real-time
3. **Configuration Persistence**: Settings are maintained across application sessions
4. **Error Handling**: Comprehensive error reporting and status updates

## Technical Architecture

### Components

#### AudioCaptionerControls (`src/gui/components/audio_captioner_controls.py`)
- Main UI component for audio and captioner controls
- Manages captioner initialization and lifecycle
- Handles audio device detection and selection
- Provides real-time status updates

#### CaptionerManager (`src/captioner/captioner_manager.py`)
- Core captioner functionality coordinator
- Integrates audio capture, speech recognition, and text rendering
- Manages configuration and state

#### AudioCapture (`src/captioner/audio_capture.py`)
- Real-time microphone input handling
- Audio device enumeration and selection
- Audio processing and noise reduction

#### SpeechRecognition (`src/captioner/speech_recognition.py`)
- Multi-engine speech recognition support
- Real-time audio processing and text conversion
- Language detection and processing

#### TextRenderer (`src/captioner/text_renderer.py`)
- Caption text rendering and styling
- Animation effects and timing
- Overlay composition on video frames

### Integration Flow

```
Microphone Input → AudioCapture → SpeechRecognition → CaptionerManager → TextRenderer → Preview Display
```

1. **Audio Input**: Microphone captures audio in real-time
2. **Processing**: Audio is processed for noise reduction and speech detection
3. **Recognition**: Speech is converted to text using selected engine
4. **Rendering**: Text is styled and animated according to settings
5. **Display**: Captions are overlaid on the video preview

## Usage Instructions

### Basic Setup

1. **Launch the Application**: Start Dreamscape Stream Software
2. **Locate Audio Panel**: Find the "🎤 Audio & Captions" dock panel
3. **Select Audio Device**: Choose your microphone from the device dropdown
4. **Enable Captioner**: Check the "Enable Live Captions" checkbox
5. **Configure Settings**: Adjust text styling and animation as desired
6. **Start Speaking**: Begin speaking to see live captions appear

### Advanced Configuration

#### Speech Recognition Engines

- **Whisper**: High-accuracy offline recognition (requires model download)
- **Google**: Cloud-based recognition (requires internet connection)
- **Dummy**: Test mode for development and debugging

#### Text Styling Options

- **Font Size**: 12-72 pixels for optimal readability
- **Font Color**: White, Yellow, Green, Cyan, or Magenta
- **Background Opacity**: 0-100% for text background visibility
- **Outline**: Black outline for better contrast

#### Animation Settings

- **Typing Speed**: Controls how quickly text appears (1-20)
- **Show Duration**: How long captions remain visible (1-10 seconds)
- **Fade Effects**: Smooth transitions for better user experience

### Troubleshooting

#### Common Issues

1. **No Audio Devices Found**
   - Check microphone permissions
   - Verify microphone is not muted
   - Try refreshing devices

2. **Captioner Not Working**
   - Ensure microphone is selected
   - Check if speech recognition engine is properly initialized
   - Verify language settings match your speech

3. **Poor Recognition Accuracy**
   - Speak clearly and at normal volume
   - Reduce background noise
   - Try different speech recognition engines
   - Adjust microphone sensitivity

#### Performance Optimization

- **Lower FPS**: Reduce preview frame rate if performance is poor
- **Simpler Animations**: Use faster typing speed and shorter display duration
- **Smaller Font Size**: Reduce font size for better performance
- **Disable Background**: Set background opacity to 0 for faster rendering

## Dependencies

### Required Packages

```bash
pip install pyaudio numpy opencv-python PyQt5
```

### Optional Dependencies

For enhanced speech recognition:
```bash
pip install speechrecognition openai-whisper
```

### System Requirements

- **Audio**: Working microphone or audio input device
- **Memory**: 2GB+ RAM for real-time processing
- **CPU**: Multi-core processor recommended for smooth performance
- **Storage**: 1GB+ free space for speech recognition models

## Development

### Adding New Features

1. **New Speech Recognition Engine**: Extend `SpeechRecognition` class
2. **Additional Text Styles**: Modify `TextRenderer` styling options
3. **Custom Audio Processing**: Enhance `AudioCapture` processing pipeline
4. **UI Enhancements**: Add new controls to `AudioCaptionerControls`

### Testing

Run the integration test:
```bash
python test_audio_captioner_integration.py
```

### Debugging

Enable debug logging:
```python
import logging
logging.basicConfig(level=logging.DEBUG)
```

## Future Enhancements

### Planned Features

- **Multi-language Support**: Automatic language detection
- **Custom Fonts**: Support for custom font files
- **Advanced Animations**: More sophisticated text effects
- **Audio Effects**: Real-time audio processing and effects
- **Streaming Integration**: Direct integration with streaming platforms
- **Accessibility**: Enhanced accessibility features for hearing-impaired users

### Performance Improvements

- **GPU Acceleration**: Hardware-accelerated text rendering
- **Optimized Audio Processing**: More efficient audio pipeline
- **Caching**: Intelligent caching for speech recognition models
- **Parallel Processing**: Multi-threaded audio and video processing

## Support

For issues and feature requests:
- Check the troubleshooting section above
- Review the application logs for error details
- Test with different audio devices and settings
- Report bugs with detailed system information

---

*This integration provides a professional-grade audio capture and captioning solution that enhances the streaming and content creation experience.* 