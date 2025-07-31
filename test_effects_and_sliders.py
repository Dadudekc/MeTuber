#!/usr/bin/env python3
"""
Focused test for effects and parameter sliders.
"""

import sys
import logging
from PyQt5.QtWidgets import QApplication
from src.gui.v2_main_window import ProfessionalV2MainWindow

# Set up focused logging - only show effects and parameter changes
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(sys.stdout)
    ]
)

# Filter out verbose logging
class FocusedFilter(logging.Filter):
    def filter(self, record):
        # Only show effects, parameters, and important messages
        important_keywords = [
            '🎭 APPLYING EFFECT',
            '🎨 STYLE APPLIED', 
            '🎨 EFFECT APPLIED',
            '🎛️ PARAMETER CHANGE',
            '🎨 Applying',
            'ERROR',
            'WARNING'
        ]
        return any(keyword in record.getMessage() for keyword in important_keywords)

# Apply the filter
for handler in logging.getLogger().handlers:
    handler.addFilter(FocusedFilter())

def test_effects_and_sliders():
    """Test effects and parameter sliders with focused logging."""
    app = QApplication(sys.argv)

    print("🕊️ Dreamscape Effects & Sliders Test")
    print("=" * 50)
    print("✅ Focused logging enabled - only showing effects and parameters")
    print("✅ Application is running - test the following:")
    print("   1. Click on '🔍 Edge Detection' effect button")
    print("   2. Look for parameter sliders in the Properties panel")
    print("   3. Move the sliders and watch for parameter change logs")
    print("   4. Try different effects to see their parameters")
    print("   5. Check console for focused effect and parameter logs")
    print("=" * 50)

    # Create main window
    main_window = ProfessionalV2MainWindow()
    main_window.show()

    # Keep the application running
    sys.exit(app.exec_())

if __name__ == "__main__":
    test_effects_and_sliders() 