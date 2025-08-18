#!/usr/bin/env python3
"""
Basic Display Test - Command Line Version

This test checks basic display functionality without requiring the full GUI.
"""

import sys
import os
import logging
import numpy as np
import cv2

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

def test_numpy_opencv():
    """Test 1: Basic numpy and OpenCV functionality."""
    try:
        print("🧪 Test 1: NumPy and OpenCV")
        
        # Test numpy
        arr = np.zeros((100, 100, 3), dtype=np.uint8)
        print(f"✅ NumPy array created: {arr.shape}, dtype: {arr.dtype}")
        
        # Test OpenCV
        test_image = np.random.randint(0, 255, (100, 100, 3), dtype=np.uint8)
        gray = cv2.cvtColor(test_image, cv2.COLOR_BGR2GRAY)
        print(f"✅ OpenCV conversion successful: {gray.shape}")
        
        # Test text rendering
        test_text = np.zeros((100, 300, 3), dtype=np.uint8)
        cv2.putText(test_text, "Test", (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)
        print("✅ OpenCV text rendering successful")
        
        return True
        
    except Exception as e:
        print(f"❌ NumPy/OpenCV test failed: {e}")
        return False

def test_frame_generation():
    """Test 2: Frame generation."""
    try:
        print("🧪 Test 2: Frame Generation")
        
        # Generate test frame
        height, width = 480, 640
        frame = np.zeros((height, width, 3), dtype=np.uint8)
        
        # Create a pattern
        for y in range(height):
            for x in range(width):
                r = int(128 + 127 * (x / width))
                g = int(128 + 127 * (y / height))
                b = int(128 + 127 * ((x + y) / (width + height)))
                frame[y, x] = [r, g, b]
        
        # Add text
        cv2.putText(frame, "Test Frame", (width//2 - 100, height//2), 
                   cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)
        
        print(f"✅ Test frame generated: {frame.shape}")
        print(f"🔍 Frame data range: {frame.min()} to {frame.max()}")
        print(f"🔍 Frame size: {frame.nbytes} bytes")
        
        # Test BGR to RGB conversion
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        print(f"✅ BGR to RGB conversion: {rgb_frame.shape}")
        
        return True
        
    except Exception as e:
        print(f"❌ Frame generation test failed: {e}")
        return False

def test_camera_access():
    """Test 3: Camera access."""
    try:
        print("🧪 Test 3: Camera Access")
        
        # Try to open camera
        print("🔍 Attempting to open camera...")
        cap = cv2.VideoCapture(0)
        
        if cap.isOpened():
            print("✅ Camera opened successfully")
            
            # Try to read a frame
            ret, frame = cap.read()
            if ret and frame is not None:
                print(f"✅ Frame read successfully: {frame.shape}")
                print(f"🔍 Frame data range: {frame.min()} to {frame.max()}")
                
                # Test frame processing
                gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
                print(f"✅ Frame processing successful: {gray.shape}")
                
            else:
                print("⚠️ Camera opened but frame read failed")
            
            # Clean up
            cap.release()
            print("✅ Camera released")
            return True
        else:
            print("⚠️ Camera could not be opened")
            return False
            
    except Exception as e:
        print(f"❌ Camera test failed: {e}")
        return False

def test_file_operations():
    """Test 4: File operations."""
    try:
        print("🧪 Test 4: File Operations")
        
        # Create a test image
        test_image = np.random.randint(0, 255, (100, 100, 3), dtype=np.uint8)
        
        # Save image
        test_filename = "test_image.png"
        cv2.imwrite(test_filename, test_image)
        print(f"✅ Image saved: {test_filename}")
        
        # Load image
        loaded_image = cv2.imread(test_filename)
        if loaded_image is not None:
            print(f"✅ Image loaded: {loaded_image.shape}")
        else:
            print("❌ Image load failed")
            return False
        
        # Clean up
        if os.path.exists(test_filename):
            os.remove(test_filename)
            print("✅ Test file cleaned up")
        
        return True
        
    except Exception as e:
        print(f"❌ File operations test failed: {e}")
        return False

def main():
    """Run all tests."""
    print("🚀 Starting Basic Display Tests...")
    print("=" * 50)
    
    tests = [
        ("NumPy and OpenCV", test_numpy_opencv),
        ("Frame Generation", test_frame_generation),
        ("Camera Access", test_camera_access),
        ("File Operations", test_file_operations)
    ]
    
    passed = 0
    total = len(tests)
    
    for test_name, test_func in tests:
        print(f"\n{test_name}:")
        print("-" * 30)
        
        if test_func():
            passed += 1
            print(f"✅ {test_name} PASSED")
        else:
            print(f"❌ {test_name} FAILED")
    
    print("\n" + "=" * 50)
    print(f"📊 Test Results: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 All tests passed! Basic functionality is working.")
        return 0
    else:
        print("⚠️ Some tests failed. Check the output above for details.")
        return 1

if __name__ == "__main__":
    sys.exit(main())
