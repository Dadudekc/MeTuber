#!/usr/bin/env python3
"""
Main entry point for Webcam Filter App V2.
This module provides the V2 application with improved GUI and functionality.
"""

import sys
import os
import logging
from PyQt5.QtWidgets import QApplication
from PyQt5.QtCore import Qt

# Add the project root to Python path
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, project_root)

# Import V2 components (Modular Version)
try:
    from src.gui.v2_main_window import ProfessionalV2MainWindow
    from src.core.device_manager import DeviceManagerFactory
    from src.core.style_manager import StyleManager
    from src.services.webcam_service import WebcamService
    from src.config.settings_manager import SettingsManager
except ImportError as e:
    logging.error(f"Failed to import V2 components: {e}")
    raise

def setup_logging():
    """Setup logging for the V2 application."""
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler('webcam_app_v2.log'),
            logging.StreamHandler()
        ]
    )

def main():
    """Main entry point for the V2 application."""
    # Setup logging
    setup_logging()
    logger = logging.getLogger(__name__)
    
    try:
        # Create QApplication first
        app = QApplication(sys.argv)
        app.setApplicationName("Dream.OS Stream Software (Open Source)")
        app.setApplicationVersion("2.0.0")
        
        # Show splash screen immediately
        from src.gui.components.splash_screen import SplashScreen
        splash = SplashScreen()
        splash.show()
        app.processEvents()  # Make sure splash appears
        
        logger.info("Starting Dream.OS Stream Software (Open Source)...")
        
        # Define loading tasks for splash animation
        loading_tasks = [
            "Camera System",
            "Style Engine", 
            "GUI Components",
            "Final Setup"
        ]
        splash.start_loading(loading_tasks)
        
        # Initialize managers and services
        splash.update_message("Initializing core systems...")
        app.processEvents()
        logger.info("Initializing managers and services...")
        
        # Note: MainWindow will initialize its own managers and services
        
        # Create main window (this does the pre-loading)
        splash.update_message("Pre-loading camera and styles...")
        app.processEvents()
        logger.info("Creating main window...")
        main_window = ProfessionalV2MainWindow()
        
        # Setup splash completion
        def show_main_window():
            main_window.show()
            logger.info("Main window displayed successfully")
        
        splash.finished.connect(show_main_window)
        
        # Start the application event loop
        logger.info("Starting application event loop...")
        return app.exec_()
        
    except Exception as e:
        logger.error(f"Failed to start V2 application: {e}")
        import traceback
        traceback.print_exc()
        return 1

if __name__ == "__main__":
    sys.exit(main()) 