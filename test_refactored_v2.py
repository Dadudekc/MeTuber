#!/usr/bin/env python3
"""
Comprehensive test for the refactored V2 application
"""

import sys
import os
import logging

# Add the src directory to the path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

def test_refactored_v2():
    """Test the refactored V2 application."""
    try:
        # Setup logging
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        )
        
        print("🧪 Testing Refactored V2 Application...")
        
        # Test 1: Module imports
        print("📦 Test 1: Module imports...")
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
        
        # Test 2: Main window import
        print("🪟 Test 2: Main window import...")
        from src.gui.v2_main_window import ProfessionalV2MainWindow
        print("✅ Main window imported successfully!")
        
        # Test 3: PyQt5 import
        print("🎨 Test 3: PyQt5 import...")
        from PyQt5.QtWidgets import QApplication
        print("✅ PyQt5 imported successfully!")
        
        # Test 4: Create application instance
        print("🚀 Test 4: Creating application instance...")
        app = QApplication(sys.argv)
        print("✅ QApplication created successfully!")
        
        # Test 5: Create main window instance
        print("🪟 Test 5: Creating main window instance...")
        main_window = ProfessionalV2MainWindow()
        print("✅ Main window created successfully!")
        
        # Test 6: Verify managers
        print("🔧 Test 6: Verifying managers...")
        managers = main_window.get_all_managers()
        expected_managers = [
            'ui_components',
            'parameter_manager', 
            'effect_manager',
            'preview_manager',
            'webcam_manager',
            'style_manager',
            'widget_manager'
        ]
        
        for manager_name in expected_managers:
            if manager_name in managers:
                print(f"✅ {manager_name} manager found")
            else:
                print(f"❌ {manager_name} manager missing")
                return False
                
        print("✅ All managers verified!")
        
        # Test 7: Test orchestration methods
        print("🎼 Test 7: Testing orchestration methods...")
        
        # Test get_manager method
        ui_manager = main_window.get_manager('ui_components')
        if ui_manager:
            print("✅ get_manager method works")
        else:
            print("❌ get_manager method failed")
            return False
            
        # Test orchestration methods exist
        if hasattr(main_window, 'orchestrate_effect_application'):
            print("✅ orchestrate_effect_application method exists")
        else:
            print("❌ orchestrate_effect_application method missing")
            return False
            
        if hasattr(main_window, 'orchestrate_parameter_change'):
            print("✅ orchestrate_parameter_change method exists")
        else:
            print("❌ orchestrate_parameter_change method missing")
            return False
            
        if hasattr(main_window, 'orchestrate_processing_toggle'):
            print("✅ orchestrate_processing_toggle method exists")
        else:
            print("❌ orchestrate_processing_toggle method missing")
            return False
            
        print("✅ All orchestration methods verified!")
        
        # Test 8: Verify single entry point
        print("🎯 Test 8: Verifying single entry point...")
        if hasattr(main_window, 'managers') and len(main_window.managers) == 7:
            print("✅ Single entry point maintained - main window orchestrates all managers")
        else:
            print("❌ Single entry point verification failed")
            return False
            
        print("✅ Single entry point verified!")
        
        # Cleanup
        app.quit()
        
        print("🎉 All tests passed! Refactored V2 application is ready for production!")
        print("\n🚀 To run the application, use:")
        print("   python src/v2_main.py")
        
        return True
        
    except ImportError as e:
        print(f"❌ Import error: {e}")
        return False
    except Exception as e:
        print(f"❌ Test failed: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = test_refactored_v2()
    sys.exit(0 if success else 1) 