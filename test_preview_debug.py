#!/usr/bin/env python3
"""
Simple test to debug preview functionality
"""

import sys
import logging
from PyQt5.QtWidgets import QApplication
from src.gui.v2_main_window import ProfessionalV2MainWindow

# Set up logging
logging.basicConfig(level=logging.DEBUG)

def test_preview():
    """Test the preview functionality."""
    app = QApplication(sys.argv)
    
    # Create main window
    main_window = ProfessionalV2MainWindow()
    main_window.show()
    
    print("🔍 Testing preview functionality...")
    print("📱 Main window should be visible")
    print("🎬 Look for the 'Start Preview' button in the controls dock")
    print("🖱️  Click the 'Start Preview' button to test camera")
    
    # Run the application
    sys.exit(app.exec_())

if __name__ == "__main__":
    test_preview() 