#!/usr/bin/env python3
"""
Systematic Debugging Script for Dreamscape V2
Tests each component with proper error handling and logging
"""

import sys
import logging
import traceback
import time
from pathlib import Path

def setup_logging():
    """Setup comprehensive logging."""
    log_dir = Path("logs")
    log_dir.mkdir(exist_ok=True)
    
    timestamp = time.strftime("%Y%m%d_%H%M%S")
    log_file = log_dir / f"debug_{timestamp}.log"
    
    logging.basicConfig(
        level=logging.DEBUG,
        format='%(asctime)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler(log_file),
            logging.StreamHandler(sys.stdout)
        ]
    )
    
    logger = logging.getLogger(__name__)
    logger.info(f"Debug logging initialized - Log: {log_file}")
    return logger

def test_component(name, test_func, logger):
    """Test a component with error handling."""
    logger.info(f"\n=== TESTING {name} ===")
    try:
        result = test_func(logger)
        if result:
            logger.info(f"[PASS] {name}")
        else:
            logger.error(f"[FAIL] {name}")
        return result
    except Exception as e:
        logger.error(f"[CRASH] {name}: {e}")
        logger.error(f"Traceback: {traceback.format_exc()}")
        return False

def test_imports(logger):
    """Test basic imports."""
    try:
        import cv2
        logger.info(f"OpenCV: {cv2.__version__}")
        
        import numpy as np
        logger.info(f"NumPy: {np.__version__}")
        
        from PyQt5.QtWidgets import QApplication
        logger.info("PyQt5: OK")
        
        return True
    except Exception as e:
        logger.error(f"Import error: {e}")
        return False

def test_camera(logger):
    """Test camera access."""
    try:
        import cv2
        
        # Test multiple camera indices
        for idx in range(3):
            logger.info(f"Testing camera {idx}...")
            cap = cv2.VideoCapture(idx)
            if cap.isOpened():
                ret, frame = cap.read()
                if ret and frame is not None:
                    logger.info(f"Camera {idx} working: {frame.shape}")
                    cap.release()
                    return True
                cap.release()
        
        logger.warning("No cameras accessible")
        return False
        
    except Exception as e:
        logger.error(f"Camera test error: {e}")
        return False

def test_style_system(logger):
    """Test style system."""
    try:
        sys.path.append("src")
        from gui.modules.style_manager import StyleManager
        
        sm = StyleManager(None)
        categories = sm.get_categories()
        logger.info(f"Style categories: {list(categories.keys())}")
        
        if categories:
            first_cat = list(categories.keys())[0]
            styles = categories[first_cat]
            if styles:
                first_style = styles[0]
                style = sm.get_style(first_style)
                if style and hasattr(style, 'apply'):
                    logger.info(f"Style '{first_style}' loaded with apply method")
                    return True
        
        logger.warning("No working styles found")
        return False
        
    except Exception as e:
        logger.error(f"Style test error: {e}")
        return False

def test_effect_system(logger):
    """Test effect system."""
    try:
        sys.path.append("src")
        from gui.modules.effect_manager import EffectManager
        
        em = EffectManager(None)
        logger.info("EffectManager created")
        
        if hasattr(em, 'get_available_effects'):
            effects = em.get_available_effects()
            logger.info(f"Available effects: {effects}")
            return True
        
        logger.warning("EffectManager missing get_available_effects")
        return False
        
    except Exception as e:
        logger.error(f"Effect test error: {e}")
        return False

def test_preview_system(logger):
    """Test preview system."""
    try:
        sys.path.append("src")
        from gui.modules.preview_manager import PreviewManager
        
        pm = PreviewManager(None)
        logger.info("PreviewManager created")
        
        pm.init_preview_timer()
        if pm.preview_timer:
            logger.info("Preview timer initialized")
            return True
        
        logger.warning("Preview timer not initialized")
        return False
        
    except Exception as e:
        logger.error(f"Preview test error: {e}")
        return False

def test_webcam_system(logger):
    """Test webcam system."""
    try:
        sys.path.append("src")
        from gui.modules.webcam_manager import WebcamManager
        
        wm = WebcamManager(None)
        logger.info("WebcamManager created")
        
        if wm.init_webcam_service():
            logger.info("Webcam service initialized")
            return True
        
        logger.warning("Webcam service not initialized")
        return False
        
    except Exception as e:
        logger.error(f"Webcam test error: {e}")
        return False

def main():
    """Run all tests."""
    logger = setup_logging()
    logger.info("Starting comprehensive system test...")
    
    tests = [
        ("Imports", test_imports),
        ("Camera", test_camera),
        ("Style System", test_style_system),
        ("Effect System", test_effect_system),
        ("Preview System", test_preview_system),
        ("Webcam System", test_webcam_system)
    ]
    
    results = {}
    for name, test_func in tests:
        results[name] = test_component(name, test_func, logger)
    
    # Summary
    logger.info("\n" + "="*50)
    logger.info("TEST RESULTS SUMMARY")
    logger.info("="*50)
    
    passed = sum(results.values())
    total = len(results)
    
    for name, result in results.items():
        status = "[PASS]" if result else "[FAIL]"
        logger.info(f"{status} {name}")
    
    logger.info(f"\nOverall: {passed}/{total} tests passed")
    
    if passed == total:
        logger.info("All systems working!")
    else:
        logger.error(f"{total - passed} systems have issues")
        logger.info("Check logs above for details")

if __name__ == "__main__":
    main()
