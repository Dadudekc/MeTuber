#!/usr/bin/env python3
"""
Test Audio and Captioner Integration

This script tests the integration of audio capture and captioner functionality
into the main GUI application.
"""

import sys
import logging
from PyQt5.QtWidgets import QApplication
from PyQt5.QtCore import QTimer

# Add the src directory to the path
sys.path.insert(0, 'src')

from gui.v2_main_window import ProfessionalV2MainWindow


def test_audio_captioner_integration():
    """Test the audio and captioner integration."""
    print("🎤 Testing Audio and Captioner Integration")
    print("=" * 50)
    
    # Setup logging
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    
    # Create application
    app = QApplication(sys.argv)
    
    try:
        # Create main window
        print("Creating main window...")
        window = ProfessionalV2MainWindow()
        
        # Check if audio captioner controls were created
        if (hasattr(window, 'ui_components') and 
            hasattr(window.ui_components, 'audio_captioner_controls')):
            
            audio_controls = window.ui_components.audio_captioner_controls
            print("✅ Audio captioner controls created successfully")
            
            # Test captioner initialization
            print("Testing captioner initialization...")
            if audio_controls.initialize_captioner():
                print("✅ Captioner initialized successfully")
            else:
                print("⚠️ Captioner initialization failed (this is normal if dependencies are missing)")
            
            # Test audio device detection
            print("Testing audio device detection...")
            try:
                audio_controls.refresh_audio_devices()
                device_count = len(audio_controls.available_audio_devices)
                print(f"✅ Found {device_count} audio devices")
            except Exception as e:
                print(f"⚠️ Audio device detection failed: {e}")
            
            # Show the window
            window.show()
            print("✅ Main window displayed successfully")
            
            # Set up a timer to close the application after 10 seconds
            def close_app():
                print("Closing test application...")
                app.quit()
            
            timer = QTimer()
            timer.timeout.connect(close_app)
            timer.start(10000)  # 10 seconds
            
            print("\n🎬 Test Application Running!")
            print("📝 Look for the '🎤 Audio & Captions' dock panel")
            print("🎤 Try enabling the captioner and speaking into your microphone")
            print("⏰ Application will close automatically in 10 seconds")
            
            # Start the application
            sys.exit(app.exec_())
            
        else:
            print("❌ Audio captioner controls not found!")
            return False
            
    except Exception as e:
        print(f"❌ Error during test: {e}")
        import traceback
        traceback.print_exc()
        return False


if __name__ == "__main__":
    test_audio_captioner_integration() 