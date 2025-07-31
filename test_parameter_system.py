#!/usr/bin/env python3
"""
Test script to verify parameter system functionality.
"""

import sys
import logging
from PyQt5.QtWidgets import QApplication
from PyQt5.QtCore import QTimer

# Add the src directory to the path
sys.path.insert(0, 'src')

from gui.v2_main_window import ProfessionalV2MainWindow

# Set up logging
logging.basicConfig(level=logging.DEBUG)

def test_parameter_system():
    """Test the parameter system."""
    app = QApplication(sys.argv)
    
    # Create main window
    main_window = ProfessionalV2MainWindow()
    main_window.show()
    
    # Test parameter updates
    def test_parameter_update():
        print("Testing parameter system...")
        
        # Test applying an effect
        if hasattr(main_window, 'effect_manager'):
            print("Applying Cartoon effect...")
            main_window.effect_manager.apply_effect("🎭 Cartoon Effects")
            
            # Test parameter changes
            if hasattr(main_window, 'parameter_manager'):
                print("Testing parameter changes...")
                main_window.parameter_manager.on_embedded_parameter_changed("bilateral_filter_diameter", 15)
                main_window.parameter_manager.on_embedded_parameter_changed("canny_threshold1", 150)
                main_window.parameter_manager.on_embedded_parameter_changed("color_levels", 12)
        
        print("Parameter system test completed.")
    
    # Run test after a short delay
    QTimer.singleShot(2000, test_parameter_update)
    
    # Run the application
    sys.exit(app.exec_())

if __name__ == "__main__":
    test_parameter_system() 