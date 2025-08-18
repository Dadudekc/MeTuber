#!/usr/bin/env python3
"""
Simple Camera Test - Command Line Only

This test isolates the camera issue without any GUI components.
"""

import cv2
import time

def test_camera_step_by_step():
    """Test camera access step by step."""
    print("🧪 Simple Camera Test - Step by Step")
    print("=" * 40)
    
    try:
        print("🔧 Step 1: Importing OpenCV...")
        print(f"✅ OpenCV version: {cv2.__version__}")
        
        print("\n🔧 Step 2: Creating VideoCapture object...")
        cap = cv2.VideoCapture(0)
        print("✅ VideoCapture object created")
        
        print("\n🔧 Step 3: Checking if camera is opened...")
        if cap.isOpened():
            print("✅ Camera opened successfully")
        else:
            print("❌ Camera failed to open")
            return False
            
        print("\n🔧 Step 4: Getting camera properties...")
        width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
        height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
        fps = cap.get(cv2.CAP_PROP_FPS)
        print(f"✅ Camera properties: {width}x{height} @ {fps} FPS")
        
        print("\n🔧 Step 5: Testing frame capture...")
        print("   - Attempting to read first frame...")
        ret, frame = cap.read()
        
        if ret and frame is not None:
            print(f"✅ First frame captured: {frame.shape}")
            print(f"   - Frame size: {frame.size}")
            print(f"   - Data type: {frame.dtype}")
            print(f"   - Min/Max values: {frame.min()}/{frame.max()}")
        else:
            print("❌ Failed to capture first frame")
            cap.release()
            return False
            
        print("\n🔧 Step 6: Testing multiple frames...")
        frames_captured = 0
        for i in range(5):
            ret, frame = cap.read()
            if ret and frame is not None:
                frames_captured += 1
                print(f"   ✅ Frame {i+1}: {frame.shape}")
            else:
                print(f"   ❌ Frame {i+1}: Failed")
            time.sleep(0.1)
            
        print(f"\n📊 Frame capture summary: {frames_captured}/5 frames captured")
        
        print("\n🔧 Step 7: Releasing camera...")
        cap.release()
        print("✅ Camera released")
        
        if frames_captured > 0:
            print("\n🎉 Camera test PASSED!")
            print("✅ Camera is working correctly")
            print("✅ The issue is likely in the GUI/preview system")
        else:
            print("\n❌ Camera test FAILED!")
            print("❌ Camera cannot capture frames")
            print("❌ This is the root cause")
            
        return frames_captured > 0
        
    except Exception as e:
        print(f"\n❌ Camera test failed with error: {e}")
        import traceback
        print(f"Traceback: {traceback.format_exc()}")
        return False

def test_camera_backends():
    """Test different camera backends."""
    print("\n🧪 Testing Camera Backends")
    print("=" * 40)
    
    backends = [
        (cv2.CAP_ANY, "CAP_ANY"),
        (cv2.CAP_DSHOW, "CAP_DSHOW (DirectShow)"),
        (cv2.CAP_MSMF, "CAP_MSMF (Media Foundation)"),
    ]
    
    for backend_id, backend_name in backends:
        try:
            print(f"🔧 Testing {backend_name}...")
            cap = cv2.VideoCapture(0, backend_id)
            
            if cap.isOpened():
                print(f"✅ {backend_name} opened successfully")
                
                # Try to read a frame
                ret, frame = cap.read()
                if ret and frame is not None:
                    print(f"   ✅ Frame captured: {frame.shape}")
                else:
                    print(f"   ⚠️ Frame capture failed")
                
                cap.release()
            else:
                print(f"❌ {backend_name} failed to open")
                
        except Exception as e:
            print(f"❌ {backend_name} error: {e}")

def main():
    """Run camera tests."""
    print("🔧 Starting Simple Camera Tests")
    print("=" * 50)
    
    # Test basic camera access
    camera_working = test_camera_step_by_step()
    
    # Test different backends
    test_camera_backends()
    
    # Summary
    print("\n" + "=" * 50)
    print("📊 CAMERA TEST SUMMARY")
    print("=" * 50)
    
    if camera_working:
        print("🎉 Camera access test PASSED!")
        print("✅ Camera is working and can capture frames")
        print("✅ This means the issue is in the GUI/preview system, not the camera")
        print("\n🔍 Next steps:")
        print("   - Check PyQt5 installation")
        print("   - Check widget hierarchy in main app")
        print("   - Check for Z-order/transparency issues")
    else:
        print("❌ Camera access test FAILED!")
        print("❌ Camera cannot be accessed or capture frames")
        print("❌ This is the root cause of the preview not working")
        print("\n🔍 Possible solutions:")
        print("   - Check camera permissions")
        print("   - Try different camera index (1, 2, etc.)")
        print("   - Check if camera is used by another application")
    
    return 0 if camera_working else 1

if __name__ == "__main__":
    import sys
    sys.exit(main())
