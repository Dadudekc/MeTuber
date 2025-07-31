#!/usr/bin/env python3
"""
Test slider functionality
"""

import sys
import logging
import time
from PyQt5.QtWidgets import QApplication
from src.gui.v2_main_window import ProfessionalV2MainWindow

# Set up logging
logging.basicConfig(level=logging.INFO)

def test_slider_functionality():
    """Test that sliders update the preview in real-time."""
    app = QApplication(sys.argv)
    
    # Create main window
    main_window = ProfessionalV2MainWindow()
    main_window.show()
    
    print("🔍 Testing slider functionality...")
    print("📱 Main window should be visible")
    print("🎬 Click 'Start Preview' to begin")
    print("🎨 Select '🎭 Cartoon Effects' from the effects dock")
    print("🎛️ Adjust the sliders in the properties dock")
    print("👁️ Watch the preview update in real-time")
    
    # Run the application
    sys.exit(app.exec_())

if __name__ == "__main__":
    test_slider_functionality() 