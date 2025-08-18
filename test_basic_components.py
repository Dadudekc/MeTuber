#!/usr/bin/env python3
"""
Basic Component Test - Command Line Version

This test checks basic functionality without requiring the full GUI.
"""

import sys
import os
import logging

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

def test_imports():
    """Test 1: Basic imports."""
    print("🧪 Test 1: Basic Imports")
    
    try:
        import numpy as np
        print(f"✅ NumPy imported: {np.__version__}")
    except ImportError as e:
        print(f"❌ NumPy import failed: {e}")
        return False
        
    try:
        import cv2
        print(f"✅ OpenCV imported: {cv2.__version__}")
    except ImportError as e:
        print(f"❌ OpenCV import failed: {e}")
        return False
        
    try:
        from PyQt5.QtWidgets import QApplication
        print("✅ PyQt5.QtWidgets imported")
    except ImportError as e:
        print(f"❌ PyQt5.QtWidgets import failed: {e}")
        return False
        
    try:
        from PyQt5.QtCore import Qt
        print("✅ PyQt5.QtCore imported")
    except ImportError as e:
        print(f"❌ PyQt5.QtCore import failed: {e}")
        return False
        
    try:
        from PyQt5.QtGui import QImage, QPixmap
        print("✅ PyQt5.QtGui imported")
    except ImportError as e:
        print(f"❌ PyQt5.QtGui import failed: {e}")
        return False
        
    return True

def test_numpy_opencv():
    """Test 2: NumPy and OpenCV functionality."""
    print("\n🧪 Test 2: NumPy and OpenCV")
    
    try:
        import numpy as np
        import cv2
        
        # Test numpy
        arr = np.zeros((100, 100, 3), dtype=np.uint8)
        print(f"✅ NumPy array created: {arr.shape}, dtype: {arr.dtype}")
        
        # Test OpenCV
        test_image = np.random.randint(0, 255, (100, 100, 3), dtype=np.uint8)
        gray = cv2.cvtColor(test_image, cv2.COLOR_BGR2GRAY)
        print(f"✅ OpenCV color conversion: {gray.shape}")
        
        # Test effects
        blurred = cv2.GaussianBlur(test_image, (5, 5), 0)
        print(f"✅ OpenCV blur effect: {blurred.shape}")
        
        return True
        
    except Exception as e:
        print(f"❌ NumPy/OpenCV test failed: {e}")
        import traceback
        print(f"Traceback: {traceback.format_exc()}")
        return False

def test_camera_access():
    """Test 3: Camera access."""
    print("\n🧪 Test 3: Camera Access")
    
    try:
        import cv2
        
        # Try to open camera
        cap = cv2.VideoCapture(0)
        if cap.isOpened():
            print("✅ Camera opened successfully")
            
            # Try to read a frame
            ret, frame = cap.read()
            if ret and frame is not None:
                print(f"✅ Frame captured: {frame.shape}")
                cap.release()
                return True
            else:
                print("❌ Failed to capture frame from camera")
                cap.release()
                return False
        else:
            print("❌ Failed to open camera")
            return False
            
    except Exception as e:
        print(f"❌ Camera test failed: {e}")
        import traceback
        print(f"Traceback: {traceback.format_exc()}")
        return False

def test_pyqt_basic():
    """Test 4: Basic PyQt functionality."""
    print("\n🧪 Test 4: Basic PyQt")
    
    try:
        from PyQt5.QtWidgets import QApplication
        from PyQt5.QtCore import Qt
        from PyQt5.QtGui import QImage, QPixmap
        
        # Create QApplication instance for testing
        app = QApplication.instance()
        if app is None:
            app = QApplication([])
            print("✅ QApplication created for testing")
        
        # Test QImage creation
        test_data = bytes([255] * (100 * 100 * 3))  # White image
        q_image = QImage(test_data, 100, 100, 300, QImage.Format_RGB888)
        print(f"✅ QImage created: {q_image.size()}")
        
        # Test QPixmap creation
        pixmap = QPixmap.fromImage(q_image)
        print(f"✅ QPixmap created: {pixmap.size()}")
        
        return True
        
    except Exception as e:
        print(f"❌ PyQt test failed: {e}")
        import traceback
        print(f"Traceback: {traceback.format_exc()}")
        return False

def test_file_access():
    """Test 5: File access and paths."""
    print("\n🧪 Test 5: File Access")
    
    try:
        # Check current directory
        current_dir = os.getcwd()
        print(f"✅ Current directory: {current_dir}")
        
        # Check if key files exist
        key_files = [
            "run_v2.py",
            "src/gui/v2_main_window.py",
            "src/gui/modules/preview_manager.py"
        ]
        
        for file_path in key_files:
            if os.path.exists(file_path):
                print(f"✅ File exists: {file_path}")
            else:
                print(f"❌ File missing: {file_path}")
                
        return True
        
    except Exception as e:
        print(f"❌ File access test failed: {e}")
        return False

def main():
    """Run all tests."""
    print("🔧 Starting Basic Component Tests")
    print("=" * 50)
    
    tests = [
        ("Basic Imports", test_imports),
        ("NumPy/OpenCV", test_numpy_opencv),
        ("Camera Access", test_camera_access),
        ("PyQt Basic", test_pyqt_basic),
        ("File Access", test_file_access)
    ]
    
    results = []
    for test_name, test_func in tests:
        try:
            result = test_func()
            results.append((test_name, result))
        except Exception as e:
            print(f"❌ {test_name} test crashed: {e}")
            results.append((test_name, False))
    
    # Summary
    print("\n" + "=" * 50)
    print("📊 TEST SUMMARY")
    print("=" * 50)
    
    passed = 0
    total = len(results)
    
    for test_name, result in results:
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{status}: {test_name}")
        if result:
            passed += 1
    
    print(f"\nOverall: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 All tests passed! Basic components are working.")
        return 0
    else:
        print("⚠️ Some tests failed. Check the output above for details.")
        return 1

if __name__ == "__main__":
    sys.exit(main())
