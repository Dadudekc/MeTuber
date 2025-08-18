#!/usr/bin/env python3
"""
Main entry point for Webcam Filter App V2.
This module provides the V2 application with improved GUI and functionality.
"""

import sys
import os
import logging

# CRITICAL FIX: Add the project root AND src directory to Python path BEFORE imports
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
src_path = os.path.join(project_root, "src")
sys.path.insert(0, project_root)
sys.path.insert(0, src_path)

from PyQt5.QtWidgets import QApplication
from PyQt5.QtCore import Qt

# Import V2 components (Modular Version)
try:
    from gui.v2_main_window import ProfessionalV2MainWindow
    from core.device_manager import DeviceManagerFactory
    from core.style_manager import StyleManager
    from services.webcam_service import WebcamService
    from config.settings_manager import SettingsManager
    from plugins.plugin_manager import PluginManager
except ImportError as e:
    logging.error(f"Failed to import V2 components: {e}")
    raise

def setup_logging():
    """Setup logging for the V2 application."""
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler('webcam_app_v2.log', encoding='utf-8'),
            logging.StreamHandler()
        ]
    )

def initialize_plugin_system():
    """Initialize the plugin system."""
    logger = logging.getLogger(__name__)
    logger.info("Initializing plugin system...")
    
    try:
        # Create plugin manager
        plugin_manager = PluginManager()
        
        # Initialize with plugin directories
        plugin_directories = [
            os.path.join(project_root, "src/plugins/effects"),
            os.path.join(project_root, "styles")  # Legacy styles for conversion
        ]
        
        plugin_manager.initialize(plugin_directories)
        
        # Log plugin statistics
        effects = plugin_manager.get_all_effects()
        categories = plugin_manager.get_categories()
        
        logger.info(f"Plugin system initialized successfully")
        logger.info(f"Loaded {len(effects)} effects across {len(categories)} categories")
        
        for category in categories:
            category_effects = plugin_manager.get_effects_by_category(category)
            logger.info(f"  {category}: {len(category_effects)} effects")
        
        return plugin_manager
        
    except Exception as e:
        logger.error(f"Failed to initialize plugin system: {e}")
        import traceback
        traceback.print_exc()
        return None

def main():
    """Main entry point for the V2 application."""
    # Setup logging
    setup_logging()
    logger = logging.getLogger(__name__)
    
    try:
        # Create QApplication first
        app = QApplication(sys.argv)
        app.setApplicationName("Dreamscape Stream Software (Open Source)")
        app.setApplicationVersion("2.0.0")
        
        # Show splash screen immediately
        from gui.components.splash_screen import SplashScreen
        splash = SplashScreen()
        splash.show()
        app.processEvents()  # Make sure splash appears
        
        logger.info("Starting Dreamscape Stream Software (Open Source)...")
        
        # Define loading tasks for splash animation
        loading_tasks = [
            "Camera System",
            "Plugin System",
            "Style Engine", 
            "GUI Components",
            "Final Setup"
        ]
        splash.start_loading(loading_tasks)
        
        # Initialize plugin system
        splash.update_message("Initializing plugin system...")
        app.processEvents()
        plugin_manager = initialize_plugin_system()
        
        # Initialize managers and services
        splash.update_message("Initializing core systems...")
        app.processEvents()
        logger.info("Initializing managers and services...")
        
        # Create main window with plugin manager
        splash.update_message("Pre-loading camera and styles...")
        app.processEvents()
        logger.info("Creating main window...")
        main_window = ProfessionalV2MainWindow(plugin_manager=plugin_manager)
        
        # Setup splash completion
        def show_main_window():
            main_window.show()
            main_window.setVisible(True)
            main_window.raise_()
            main_window.activateWindow()
            logger.info("Main window displayed successfully")
        
        splash.finished.connect(show_main_window)
        
        # Finish splash screen immediately since loading is complete
        splash.close()
        splash.finished.emit()
        
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