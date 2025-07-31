#!/usr/bin/env python3
"""
Quick test to verify parameter sliders are working.
"""

import sys
import logging
from PyQt5.QtWidgets import QApplication
from src.gui.v2_main_window import ProfessionalV2MainWindow

# Set up logging to see parameter changes
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

def test_slider_fix():
    """Test if the slider fix is working."""
    app = QApplication(sys.argv)
    
    print("🕊️ Dreamscape Parameter Slider Test")
    print("=" * 50)
    
    # Create main window
    main_window = ProfessionalV2MainWindow()
    main_window.show()
    
    print("✅ Main window created and shown")
    print("✅ Application is running - try the following:")
    print("   1. Click on an effect button (Edge Detection, Cartoon Effects, etc.)")
    print("   2. Look for parameter sliders in the Properties panel")
    print("   3. Move the sliders to see if they affect the video")
    print("   4. Check the console for parameter change logs")
    
    # Keep the application running
    sys.exit(app.exec_())

if __name__ == "__main__":
    test_slider_fix() 