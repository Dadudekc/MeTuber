#!/usr/bin/env python3
"""
Quick test to verify slider functionality
"""

import sys
import logging
from PyQt5.QtWidgets import QApplication
from src.gui.v2_main_window import ProfessionalV2MainWindow

# Set up logging to see parameter changes
logging.basicConfig(level=logging.INFO)

def test_sliders():
    """Test that sliders are working properly."""
    app = QApplication(sys.argv)
    
    # Create main window
    main_window = ProfessionalV2MainWindow()
    main_window.show()
    
    print("🎯 SLIDER FUNCTIONALITY TEST")
    print("=" * 50)
    print("📱 Application should be visible")
    print("🎬 Click 'Start Preview' button")
    print("🎨 Select '🎭 Cartoon Effects' from effects dock")
    print("🎛️ Look for sliders in properties dock:")
    print("   - Bilateral Filter Diameter")
    print("   - Bilateral Filter Sigma Color")
    print("   - Canny Threshold 1")
    print("   - Canny Threshold 2")
    print("   - Color Levels")
    print("👁️ Move sliders and watch preview update")
    print("📊 Check console for parameter change logs")
    print("=" * 50)
    
    # Run the application
    sys.exit(app.exec_())

if __name__ == "__main__":
    test_sliders() 