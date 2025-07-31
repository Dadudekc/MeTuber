#!/usr/bin/env python3
"""
Debug test for parameter system.
"""

import sys
import logging
from PyQt5.QtWidgets import QApplication
from src.gui.v2_main_window import ProfessionalV2MainWindow

# Set up detailed logging
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(sys.stdout)
    ]
)

def test_parameter_debug():
    """Debug test for parameter system."""
    app = QApplication(sys.argv)

    print("🕊️ Dreamscape Parameter Debug Test")
    print("=" * 50)
    print("✅ Testing parameter system with detailed logging")
    print("✅ Application is running - test the following:")
    print("   1. Click on '🔍 Edge Detection' effect button")
    print("   2. Look for parameter sliders in the Properties panel")
    print("   3. Move the sliders and watch for detailed parameter logs")
    print("   4. Check that parameters are being passed to webcam service")
    print("   5. Verify style.apply() is being called with correct parameters")
    print("=" * 50)

    # Create main window
    main_window = ProfessionalV2MainWindow()
    main_window.show()

    # Keep the application running
    sys.exit(app.exec_())

if __name__ == "__main__":
    test_parameter_debug() 