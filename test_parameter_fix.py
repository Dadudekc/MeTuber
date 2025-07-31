#!/usr/bin/env python3
"""
Test script to verify parameter system fix.
"""

import sys
import logging
from PyQt5.QtWidgets import QApplication
from src.gui.v2_main_window import ProfessionalV2MainWindow

# Set up logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(sys.stdout)
    ]
)

def test_parameter_fix():
    """Test the parameter system fix."""
    app = QApplication(sys.argv)

    print("🕊️ Dreamscape Parameter System Fix Test")
    print("=" * 50)
    print("✅ Testing parameter system with updated style mapping")
    print("✅ Application is running - test the following:")
    print("   1. Click on '🔍 Edge Detection' effect button")
    print("   2. Look for parameter sliders in the Properties panel")
    print("   3. Move the sliders and watch for parameter change logs")
    print("   4. Check that 'Style not found' warnings are gone")
    print("   5. Verify parameters are being applied to the video")
    print("=" * 50)

    # Create main window
    main_window = ProfessionalV2MainWindow()
    main_window.show()

    # Keep the application running
    sys.exit(app.exec_())

if __name__ == "__main__":
    test_parameter_fix() 