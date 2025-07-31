#!/usr/bin/env python3
"""
Test script to check if parameter sliders are working.
"""

import sys
import logging
from PyQt5.QtWidgets import QApplication
from src.gui.v2_main_window import ProfessionalV2MainWindow

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

def test_parameter_sliders():
    """Test if parameter sliders are working."""
    app = QApplication(sys.argv)
    
    # Create main window
    main_window = ProfessionalV2MainWindow()
    main_window.show()
    
    # Wait a moment for initialization
    app.processEvents()
    
    # Test parameter manager
    if hasattr(main_window, 'parameter_manager'):
        print("✅ Parameter manager found")
        
        # Test updating parameter controls
        try:
            main_window.parameter_manager.update_parameter_controls("Edge Detection")
            print("✅ Parameter controls updated successfully")
            
            # Check if embedded widgets were created
            if hasattr(main_window, 'embedded_param_widgets'):
                widget_count = len(main_window.embedded_param_widgets)
                print(f"✅ Created {widget_count} embedded parameter widgets")
                
                # List the widgets
                for name, widget in main_window.embedded_param_widgets.items():
                    print(f"   - {name}: {type(widget).__name__}")
            else:
                print("❌ No embedded parameter widgets found")
                
        except Exception as e:
            print(f"❌ Error updating parameter controls: {e}")
    else:
        print("❌ Parameter manager not found")
    
    # Test effect application
    if hasattr(main_window, 'effect_manager'):
        print("✅ Effect manager found")
        
        # Test applying an effect
        try:
            main_window.effect_manager.apply_effect("🔍 Edge Detection")
            print("✅ Effect applied successfully")
        except Exception as e:
            print(f"❌ Error applying effect: {e}")
    else:
        print("❌ Effect manager not found")
    
    print("\n🎯 Test completed! Check the application window to see if sliders are working.")
    print("Try moving the sliders to see if they affect the video preview.")
    
    # Keep the application running
    sys.exit(app.exec_())

if __name__ == "__main__":
    test_parameter_sliders() 