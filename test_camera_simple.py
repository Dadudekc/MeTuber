#!/usr/bin/env python3
"""
Simple camera test
"""

import sys
import time
import logging
from PyQt5.QtWidgets import QApplication
from src.gui.v2_main_window import ProfessionalV2MainWindow

# Set up logging
logging.basicConfig(level=logging.INFO)

def test_camera():
    """Test camera functionality."""
    app = QApplication(sys.argv)
    
    # Create main window
    main_window = ProfessionalV2MainWindow()
    main_window.show()
    
    print("🎥 CAMERA TEST")
    print("=" * 50)
    print("📱 Application should be visible")
    print("🎬 Click 'Start Preview' button")
    print("📷 Camera should initialize and show preview")
    print("🎨 Select '🎭 Cartoon Effects' to test effects")
    print("🎛️ Adjust sliders to see real-time changes")
    print("⏱️ Wait a few seconds for camera to initialize...")
    
    # Run the application
    sys.exit(app.exec_())

if __name__ == "__main__":
    test_camera() 