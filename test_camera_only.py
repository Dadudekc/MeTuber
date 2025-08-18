#!/usr/bin/env python3
"""
Camera Access Test Only

This test focuses solely on testing camera access without any GUI components.
"""

import cv2
import time

def test_camera_access():
    """Test camera access and frame capture."""
    print("🧪 Testing Camera Access")
    print("=" * 40)
    
    try:
        print("🔧 Attempting to open camera...")
        cap = cv2.VideoCapture(0)
        
        if cap.isOpened():
            print("✅ Camera opened successfully")
            
            # Get camera properties
            width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
            height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
            fps = cap.get(cv2.CAP_PROP_FPS)
            
            print(f"📐 Camera resolution: {width}x{height}")
            print(f"🎬 Camera FPS: {fps}")
            
            # Try to read a few frames
            print("📸 Testing frame capture...")
            frames_captured = 0
            
            for i in range(5):  # Try 5 frames
                ret, frame = cap.read()
                if ret and frame is not None:
                    frames_captured += 1
                    print(f"✅ Frame {i+1} captured: {frame.shape}")
                    
                    # Check frame data
                    if frame.size > 0:
                        print(f"   - Frame size: {frame.size}")
                        print(f"   - Data type: {frame.dtype}")
                        print(f"   - Min/Max values: {frame.min()}/{frame.max()}")
                    else:
                        print(f"   ⚠️ Frame {i+1} has zero size")
                else:
                    print(f"❌ Frame {i+1} capture failed")
                
                time.sleep(0.1)  # Small delay between frames
            
            print(f"\n📊 Frame capture summary: {frames_captured}/5 frames captured")
            
            if frames_captured > 0:
                print("✅ Camera is working and capturing frames!")
            else:
                print("❌ Camera opened but failed to capture any frames")
            
            # Release camera
            cap.release()
            print("✅ Camera released")
            
            return frames_captured > 0
            
        else:
            print("❌ Failed to open camera")
            return False
            
    except Exception as e:
        print(f"❌ Camera test failed with error: {e}")
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
        (cv2.CAP_V4L2, "CAP_V4L2 (Linux)"),
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
    print("🔧 Starting Camera Access Tests")
    print("=" * 50)
    
    # Test basic camera access
    camera_working = test_camera_access()
    
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
    else:
        print("❌ Camera access test FAILED!")
        print("❌ Camera cannot be accessed or capture frames")
        print("❌ This is the root cause of the preview not working")
    
    return 0 if camera_working else 1

if __name__ == "__main__":
    import sys
    sys.exit(main())
