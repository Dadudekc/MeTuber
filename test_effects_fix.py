#!/usr/bin/env python3
"""
Test script to check if effects are working properly
"""

import sys
import logging
from PyQt5.QtWidgets import QApplication
from src.gui.v2_main_window import ProfessionalV2MainWindow

def test_effects():
    """Test if effects are working properly."""
    app = QApplication(sys.argv)
    
    # Set up logging
    logging.basicConfig(level=logging.DEBUG)
    logger = logging.getLogger(__name__)
    
    try:
        # Create main window
        logger.info("Creating main window...")
        main_window = ProfessionalV2MainWindow()
        
        # Test effect buttons
        logger.info("Testing effect buttons...")
        
        # Check if effects layout exists
        if hasattr(main_window, 'effects_layout'):
            logger.info("Effects layout found")
            
            # Count effect buttons
            button_count = main_window.effects_layout.count() - 1  # Subtract 1 for stretch
            logger.info(f"Found {button_count} effect buttons")
            
            # Test first few buttons
            for i in range(min(3, button_count)):
                item = main_window.effects_layout.itemAt(i)
                if item and item.widget():
                    button = item.widget()
                    logger.info(f"Button {i+1}: {button.text()}")
                    
                    # Test button click
                    try:
                        button.click()
                        logger.info(f"Button {i+1} clicked successfully")
                    except Exception as e:
                        logger.error(f"Error clicking button {i+1}: {e}")
        else:
            logger.error("Effects layout not found!")
            
        # Test style manager
        logger.info("Testing style manager...")
        if hasattr(main_window, 'style_manager'):
            edge_detection = main_window.style_manager.get_style("Edge Detection")
            if edge_detection:
                logger.info("Edge Detection style found")
            else:
                logger.error("Edge Detection style not found")
        else:
            logger.error("Style manager not found!")
            
        # Test parameter manager
        logger.info("Testing parameter manager...")
        if hasattr(main_window, 'parameter_manager'):
            try:
                main_window.parameter_manager.update_parameter_controls("Edge Detection")
                logger.info("Parameter controls updated successfully")
            except Exception as e:
                logger.error(f"Error updating parameter controls: {e}")
        else:
            logger.error("Parameter manager not found!")
            
        logger.info("Effects test completed!")
        
    except Exception as e:
        logger.error(f"Error in effects test: {e}")
        import traceback
        logger.error(f"Traceback: {traceback.format_exc()}")
        
    finally:
        app.quit()

if __name__ == "__main__":
    test_effects() 