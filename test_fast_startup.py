#!/usr/bin/env python3
"""
Test for fast application startup
"""

import sys
import time
import logging
from PyQt5.QtWidgets import QApplication
from src.gui.v2_main_window import ProfessionalV2MainWindow

# Set up logging
logging.basicConfig(level=logging.INFO)

def test_fast_startup():
    """Test that the application starts up quickly."""
    start_time = time.time()
    
    app = QApplication(sys.argv)
    
    # Create main window
    main_window = ProfessionalV2MainWindow()
    main_window.show()
    
    end_time = time.time()
    startup_time = end_time - start_time
    
    print(f"🚀 Application startup time: {startup_time:.2f} seconds")
    print("📱 Main window should be visible")
    print("🎬 Click 'Start Preview' to test camera")
    print("🎨 Select effects from the effects dock")
    
    # Run the application
    sys.exit(app.exec_())

if __name__ == "__main__":
    test_fast_startup() 