#!/usr/bin/env python3
"""
Comprehensive Debugging & Testing Script for Dreamscape V2
Systematically tests each component with proper error handling and logging
"""

import sys
import logging
import traceback
import time
from pathlib import Path

# Setup comprehensive logging
def setup_logging():
    """Setup comprehensive logging with file and console output."""
    # Create logs directory
    log_dir = Path("logs")
    log_dir.mkdir(exist_ok=True)
    
    # Create timestamped log file
    timestamp = time.strftime("%Y%m%d_%H%M%S")
    log_file = log_dir / f"debug_test_{timestamp}.log"
    
    # Configure logging
    logging.basicConfig(
        level=logging.DEBUG,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler(log_file),
            logging.StreamHandler(sys.stdout)
        ]
    )
    
    logger = logging.getLogger(__name__)
    logger.info(f"🔧 Debug logging initialized - Log file: {log_file}")
    return logger

def test_basic_imports(logger):
    """Test basic Python imports and dependencies."""
    logger.info("=== TESTING BASIC IMPORTS ===")
    
    try:
        import cv2
        logger.info(f"✅ OpenCV imported successfully - Version: {cv2.__version__}")
    except Exception as e:
        logger.error(f"❌ OpenCV import failed: {e}")
        return False
    
    try:
        import numpy as np
        logger.info(f"✅ NumPy imported successfully - Version: {np.__version__}")
    except Exception as e:
        logger.error(f"❌ NumPy import failed: {e}")
        return False
    
    try:
        from PyQt5.QtWidgets import QApplication, QLabel
        from PyQt5.QtCore import QTimer
        from PyQt5.QtGui import QPixmap, QImage
        logger.info("✅ PyQt5 imported successfully")
    except Exception as e:
        logger.error(f"❌ PyQt5 import failed: {e}")
        return False
    
    logger.info("✅ All basic imports successful")
    return True

def test_camera_access(logger):
    """Test camera access with detailed error reporting."""
    logger.info("=== TESTING CAMERA ACCESS ===")
    
    try:
        import cv2
        
        # Test camera 0
        logger.info("🔍 Testing camera index 0...")
        cap0 = cv2.VideoCapture(0)
        if cap0.isOpened():
            logger.info("✅ Camera 0 opened successfully")
            
            # Try to read a frame
            ret, frame = cap0.read()
            if ret and frame is not None:
                logger.info(f"✅ Camera 0 frame captured: {frame.shape}")
                cap0.release()
                return True
            else:
                logger.warning("⚠️ Camera 0 opened but no frame captured")
                cap0.release()
        else:
            logger.warning("⚠️ Camera 0 failed to open")
        
        # Test camera 1
        logger.info("🔍 Testing camera index 1...")
        cap1 = cv2.VideoCapture(1)
        if cap1.isOpened():
            logger.info("✅ Camera 1 opened successfully")
            ret, frame = cap1.read()
            if ret and frame is not None:
                logger.info(f"✅ Camera 1 frame captured: {frame.shape}")
                cap1.release()
                return True
            else:
                logger.warning("⚠️ Camera 1 opened but no frame captured")
                cap1.release()
        else:
            logger.warning("⚠️ Camera 1 failed to open")
        
        # Test camera 2
        logger.info("🔍 Testing camera index 2...")
        cap2 = cv2.VideoCapture(2)
        if cap2.isOpened():
            logger.info("✅ Camera 2 opened successfully")
            ret, frame = cap2.read()
            if ret and frame is not None:
                logger.info(f"✅ Camera 2 frame captured: {frame.shape}")
                cap2.release()
                return True
            else:
                logger.warning("⚠️ Camera 2 opened but no frame captured")
                cap2.release()
        else:
            logger.warning("⚠️ Camera 2 failed to open")
        
        logger.error("❌ No cameras accessible")
        return False
        
    except Exception as e:
        logger.error(f"❌ Camera access test failed: {e}")
        logger.error(f"Traceback: {traceback.format_exc()}")
        return False

def test_style_manager(logger):
    """Test style manager functionality."""
    logger.info("=== TESTING STYLE MANAGER ===")
    
    try:
        # Import style manager
        sys.path.append(str(Path("src")))
        from gui.modules.style_manager import StyleManager
        
        logger.info("✅ StyleManager imported successfully")
        
        # Test creating style manager
        logger.info("🔍 Creating StyleManager instance...")
        style_manager = StyleManager(None)  # Pass None for main_window
        logger.info("✅ StyleManager instance created")
        
        # Test getting categories
        try:
            categories = style_manager.get_categories()
            logger.info(f"✅ Categories retrieved: {list(categories.keys())}")
            
            # Test getting first available style
            if categories:
                first_category = list(categories.keys())[0]
                styles_in_category = categories[first_category]
                if styles_in_category:
                    first_style_name = styles_in_category[0]
                    logger.info(f"✅ First style found: {first_style_name}")
                    
                    # Test getting the style
                    style = style_manager.get_style(first_style_name)
                    if style:
                        logger.info(f"✅ Style '{first_style_name}' retrieved successfully")
                        
                        # Test style parameters
                        if hasattr(style, 'parameters'):
                            logger.info(f"✅ Style has parameters: {list(style.parameters.keys())}")
                        else:
                            logger.warning("⚠️ Style has no parameters attribute")
                        
                        # Test style apply method
                        if hasattr(style, 'apply') and callable(style.apply):
                            logger.info("✅ Style has apply method")
                        else:
                            logger.warning("⚠️ Style missing apply method")
                    else:
                        logger.error(f"❌ Failed to retrieve style '{first_style_name}'")
                else:
                    logger.warning(f"⚠️ No styles in category '{first_category}'")
            else:
                logger.warning("⚠️ No categories available")
                
        except Exception as e:
            logger.error(f"❌ Error testing style categories: {e}")
            logger.error(f"Traceback: {traceback.format_exc()}")
            return False
        
        return True
        
    except Exception as e:
        logger.error(f"❌ Style manager test failed: {e}")
        logger.error(f"Traceback: {traceback.format_exc()}")
        return False

def test_effect_manager(logger):
    """Test effect manager functionality."""
    logger.info("=== TESTING EFFECT MANAGER ===")
    
    try:
        # Import effect manager
        sys.path.append(str(Path("src")))
        from gui.modules.effect_manager import EffectManager
        
        logger.info("✅ EffectManager imported successfully")
        
        # Test creating effect manager
        logger.info("🔍 Creating EffectManager instance...")
        effect_manager = EffectManager(None)  # Pass None for main_window
        logger.info("✅ EffectManager instance created")
        
        # Test getting available effects
        try:
            if hasattr(effect_manager, 'get_available_effects'):
                effects = effect_manager.get_available_effects()
                logger.info(f"✅ Available effects: {effects}")
            else:
                logger.warning("⚠️ EffectManager has no get_available_effects method")
                
            # Test current effect
            if hasattr(effect_manager, 'current_effect'):
                current = effect_manager.current_effect
                logger.info(f"✅ Current effect: {current}")
            else:
                logger.warning("⚠️ EffectManager has no current_effect attribute")
                
        except Exception as e:
            logger.error(f"❌ Error testing effect manager methods: {e}")
            logger.error(f"Traceback: {traceback.format_exc()}")
            return False
        
        return True
        
    except Exception as e:
        logger.error(f"❌ Effect manager test failed: {e}")
        logger.error(f"Traceback: {traceback.format_exc()}")
        return False

def test_preview_manager(logger):
    """Test preview manager functionality."""
    logger.info("=== TESTING PREVIEW MANAGER ===")
    
    try:
        # Import preview manager
        sys.path.append(str(Path("src")))
        from gui.modules.preview_manager import PreviewManager
        
        logger.info("✅ PreviewManager imported successfully")
        
        # Test creating preview manager
        logger.info("🔍 Creating PreviewManager instance...")
        preview_manager = PreviewManager(None)  # Pass None for main_window
        logger.info("✅ PreviewManager instance created")
        
        # Test timer initialization
        try:
            logger.info("🔍 Testing timer initialization...")
            preview_manager.init_preview_timer()
            if preview_manager.preview_timer:
                logger.info("✅ Preview timer initialized successfully")
            else:
                logger.warning("⚠️ Preview timer not initialized")
        except Exception as e:
            logger.error(f"❌ Timer initialization failed: {e}")
            logger.error(f"Traceback: {traceback.format_exc()}")
            return False
        
        # Test frame generation
        try:
            logger.info("🔍 Testing frame generation...")
            if hasattr(preview_manager, '_generate_test_frame'):
                test_frame = preview_manager._generate_test_frame()
                if test_frame is not None:
                    logger.info(f"✅ Test frame generated: {test_frame.shape}")
                else:
                    logger.warning("⚠️ Test frame generation returned None")
            else:
                logger.warning("⚠️ PreviewManager has no _generate_test_frame method")
        except Exception as e:
            logger.error(f"❌ Frame generation test failed: {e}")
            logger.error(f"Traceback: {traceback.format_exc()}")
            return False
        
        return True
        
    except Exception as e:
        logger.error(f"❌ Preview manager test failed: {e}")
        logger.error(f"Traceback: {traceback.format_exc()}")
        return False

def test_webcam_manager(logger):
    """Test webcam manager functionality."""
    logger.info("=== TESTING WEBCAM MANAGER ===")
    
    try:
        # Import webcam manager
        sys.path.append(str(Path("src")))
        from gui.modules.webcam_manager import WebcamManager
        
        logger.info("✅ WebcamManager imported successfully")
        
        # Test creating webcam manager
        logger.info("🔍 Creating WebcamManager instance...")
        webcam_manager = WebcamManager(None)  # Pass None for main_window
        logger.info("✅ WebcamManager instance created")
        
        # Test webcam service initialization
        try:
            logger.info("🔍 Testing webcam service initialization...")
            if hasattr(webcam_manager, 'init_webcam_service'):
                success = webcam_manager.init_webcam_service()
                logger.info(f"✅ Webcam service initialization: {success}")
            else:
                logger.warning("⚠️ WebcamManager has no init_webcam_service method")
        except Exception as e:
            logger.error(f"❌ Webcam service initialization failed: {e}")
            logger.error(f"Traceback: {traceback.format_exc()}")
            return False
        
        # Test processing start
        try:
            logger.info("🔍 Testing processing start...")
            if hasattr(webcam_manager, 'start_processing'):
                success = webcam_manager.start_processing()
                logger.info(f"✅ Processing start: {success}")
                
                # Stop processing if started
                if success and hasattr(webcam_manager, 'stop_processing'):
                    webcam_manager.stop_processing()
                    logger.info("✅ Processing stopped")
            else:
                logger.warning("⚠️ WebcamManager has no start_processing method")
        except Exception as e:
            logger.error(f"❌ Processing start test failed: {e}")
            logger.error(f"Traceback: {traceback.format_exc()}")
            return False
        
        return True
        
    except Exception as e:
        logger.error(f"❌ Webcam manager test failed: {e}")
        logger.error(f"Traceback: {traceback.format_exc()}")
        return False

def test_ui_components(logger):
    """Test UI components functionality."""
    logger.info("=== TESTING UI COMPONENTS ===")
    
    try:
        # Import UI components
        sys.path.append(str(Path("src")))
        from gui.modules.ui_components import UIComponents
        
        logger.info("✅ UIComponents imported successfully")
        
        # Test creating UI components
        logger.info("🔍 Creating UIComponents instance...")
        ui_components = UIComponents(None)  # Pass None for main_window
        logger.info("✅ UIComponents instance created")
        
        # Test component creation methods
        try:
            logger.info("🔍 Testing component creation methods...")
            
            # Check if methods exist
            methods_to_test = [
                'create_central_preview',
                'create_effects_dock',
                'create_controls_dock',
                'create_status_bar'
            ]
            
            for method_name in methods_to_test:
                if hasattr(ui_components, method_name):
                    logger.info(f"✅ Method '{method_name}' exists")
                else:
                    logger.warning(f"⚠️ Method '{method_name}' missing")
                    
        except Exception as e:
            logger.error(f"❌ UI components method test failed: {e}")
            logger.error(f"Traceback: {traceback.format_exc()}")
            return False
        
        return True
        
    except Exception as e:
        logger.error(f"❌ UI components test failed: {e}")
        logger.error(f"Traceback: {traceback.format_exc()}")
        return False

def test_main_window_creation(logger):
    """Test main window creation."""
    logger.info("=== TESTING MAIN WINDOW CREATION ===")
    
    try:
        # Import main window
        sys.path.append(str(Path("src")))
        from gui.v2_main_window import ProfessionalV2MainWindow
        
        logger.info("✅ ProfessionalV2MainWindow imported successfully")
        
        # Test creating main window
        logger.info("🔍 Creating main window instance...")
        try:
            main_window = ProfessionalV2MainWindow()
            logger.info("✅ Main window instance created successfully")
            
            # Test manager initialization
            managers_to_check = [
                'ui_components',
                'parameter_manager', 
                'effect_manager',
                'preview_manager',
                'webcam_manager',
                'style_manager',
                'widget_manager'
            ]
            
            for manager_name in managers_to_check:
                if hasattr(main_window, manager_name):
                    manager = getattr(main_window, manager_name)
                    if manager:
                        logger.info(f"✅ Manager '{manager_name}' initialized")
                    else:
                        logger.warning(f"⚠️ Manager '{manager_name}' is None")
                else:
                    logger.warning(f"⚠️ Manager '{manager_name}' not found")
            
            return True
            
        except Exception as e:
            logger.error(f"❌ Main window creation failed: {e}")
            logger.error(f"Traceback: {traceback.format_exc()}")
            return False
        
    except Exception as e:
        logger.error(f"❌ Main window import test failed: {e}")
        logger.error(f"Traceback: {traceback.format_exc()}")
        return False

def run_comprehensive_test():
    """Run all comprehensive tests."""
    logger = setup_logging()
    
    logger.info("🚀 STARTING COMPREHENSIVE DEBUG TESTING")
    logger.info("=" * 60)
    
    test_results = {}
    
    # Run all tests
    tests = [
        ("Basic Imports", test_basic_imports),
        ("Camera Access", test_camera_access),
        ("Style Manager", test_style_manager),
        ("Effect Manager", test_effect_manager),
        ("Preview Manager", test_preview_manager),
        ("Webcam Manager", test_webcam_manager),
        ("UI Components", test_ui_components),
        ("Main Window", test_main_window_creation)
    ]
    
    for test_name, test_func in tests:
        logger.info(f"\n{'='*20} {test_name} {'='*20}")
        try:
            result = test_func(logger)
            test_results[test_name] = result
            if result:
                logger.info(f"✅ {test_name} PASSED")
            else:
                logger.error(f"❌ {test_name} FAILED")
        except Exception as e:
            logger.error(f"❌ {test_name} CRASHED: {e}")
            logger.error(f"Traceback: {traceback.format_exc()}")
            test_results[test_name] = False
    
    # Summary
    logger.info("\n" + "=" * 60)
    logger.info("📊 TEST RESULTS SUMMARY")
    logger.info("=" * 60)
    
    passed = sum(1 for result in test_results.values() if result)
    total = len(test_results)
    
    for test_name, result in test_results.items():
        status = "✅ PASS" if result else "❌ FAIL"
        logger.info(f"{status} {test_name}")
    
    logger.info(f"\nOverall: {passed}/{total} tests passed")
    
    if passed == total:
        logger.info("🎉 ALL TESTS PASSED - System appears to be working!")
    else:
        logger.error(f"⚠️ {total - passed} tests failed - System has issues")
        logger.info("Check the log file above for detailed error information")
    
    return test_results

if __name__ == "__main__":
    results = run_comprehensive_test()
    
    # Exit with error code if any tests failed
    if not all(results.values()):
        sys.exit(1) 