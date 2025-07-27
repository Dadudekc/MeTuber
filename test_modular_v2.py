#!/usr/bin/env python3
"""
Test script for the modular V2 application
"""

import sys
import os
import logging

# Add the src directory to the path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

def test_modular_v2():
    """Test the modular V2 application."""
    try:
        # Setup logging
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        )
        
        print("🧪 Testing Modular V2 Application...")
        
        # Test module imports
        print("📦 Testing module imports...")
        from src.gui.modules import (
            UIComponents,
            ParameterManager,
            EffectManager,
            PreviewManager,
            WebcamManager,
            StyleManager,
            WidgetManager
        )
        print("✅ All modules imported successfully!")
        
        # Test main window import
        print("🪟 Testing main window import...")
        from src.gui.v2_main_window_modular import ProfessionalV2MainWindow
        print("✅ Main window imported successfully!")
        
        # Test PyQt5 import
        print("🎨 Testing PyQt5 import...")
        from PyQt5.QtWidgets import QApplication
        print("✅ PyQt5 imported successfully!")
        
        print("🎉 All tests passed! Modular V2 application is ready to run.")
        print("\n🚀 To run the application, use:")
        print("   python src/v2_main.py")
        print("\n📦 Or run the modular version directly:")
        print("   python src/gui/v2_main_window_modular.py")
        
        return True
        
    except ImportError as e:
        print(f"❌ Import error: {e}")
        return False
    except Exception as e:
        print(f"❌ Test failed: {e}")
        return False

if __name__ == "__main__":
    success = test_modular_v2()
    sys.exit(0 if success else 1) 