#!/usr/bin/env python3
"""
Camera Information Test

This test shows all available cameras and their details.
"""

import cv2
import time

def list_available_cameras():
    """List all available cameras."""
    print("🔍 Scanning for Available Cameras...")
    print("=" * 50)
    
    available_cameras = []
    
    # Test camera indices 0-9
    for i in range(10):
        try:
            print(f"🔧 Testing camera index {i}...")
            cap = cv2.VideoCapture(i)
            
            if cap.isOpened():
                print(f"✅ Camera {i} is available!")
                
                # Get camera properties
                width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
                height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
                fps = cap.get(cv2.CAP_PROP_FPS)
                backend = cap.getBackendName()
                
                print(f"   📐 Resolution: {width}x{height}")
                print(f"   🎬 FPS: {fps}")
                print(f"   🔧 Backend: {backend}")
                
                # Try to read a frame
                ret, frame = cap.read()
                if ret and frame is not None:
                    print(f"   📸 Frame capture: ✅ {frame.shape}")
                    available_cameras.append({
                        'index': i,
                        'resolution': f"{width}x{height}",
                        'fps': fps,
                        'backend': backend,
                        'working': True
                    })
                else:
                    print(f"   📸 Frame capture: ❌ Failed")
                    available_cameras.append({
                        'index': i,
                        'resolution': f"{width}x{height}",
                        'fps': fps,
                        'backend': backend,
                        'working': False
                    })
                
                cap.release()
            else:
                print(f"❌ Camera {i} is not available")
                
        except Exception as e:
            print(f"❌ Error testing camera {i}: {e}")
    
    return available_cameras

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
    
    backend_results = []
    
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
                    backend_results.append((backend_name, True, True))
                else:
                    print(f"   ⚠️ Frame capture failed")
                    backend_results.append((backend_name, True, False))
                
                cap.release()
            else:
                print(f"❌ {backend_name} failed to open")
                backend_results.append((backend_name, False, False))
                
        except Exception as e:
            print(f"❌ {backend_name} error: {e}")
            backend_results.append((backend_name, False, False))
    
    return backend_results

def main():
    """Run camera information tests."""
    print("🔧 Camera Information Test")
    print("=" * 50)
    
    # List available cameras
    cameras = list_available_cameras()
    
    # Test backends
    backends = test_camera_backends()
    
    # Summary
    print("\n" + "=" * 50)
    print("📊 CAMERA INFORMATION SUMMARY")
    print("=" * 50)
    
    if cameras:
        print(f"🎉 Found {len(cameras)} available camera(s):")
        for cam in cameras:
            status = "✅ Working" if cam['working'] else "⚠️ Available but not working"
            print(f"   📷 Camera {cam['index']}: {cam['resolution']} @ {cam['fps']}fps ({status})")
        
        # Find the best camera
        working_cameras = [cam for cam in cameras if cam['working']]
        if working_cameras:
            best_camera = working_cameras[0]
            print(f"\n🎯 RECOMMENDED: Use Camera {best_camera['index']}")
            print(f"   - Resolution: {best_camera['resolution']}")
            print(f"   - FPS: {best_camera['fps']}")
            print(f"   - Backend: {best_camera['backend']}")
        else:
            print("\n⚠️ No working cameras found!")
            print("   - All cameras failed frame capture")
            print("   - This explains why preview isn't working")
    else:
        print("❌ No cameras found!")
        print("   - Check camera connections")
        print("   - Check camera permissions")
        print("   - Check if camera is used by another app")
    
    print(f"\n🔧 Backend Summary:")
    for backend_name, opened, working in backends:
        status = "✅ Working" if working else "⚠️ Opened but no frames" if opened else "❌ Failed to open"
        print(f"   - {backend_name}: {status}")
    
    print(f"\n💡 Current Configuration:")
    print(f"   - Main app uses: Camera 0 (cv2.VideoCapture(0))")
    print(f"   - Backend: CAP_ANY (default)")
    
    if cameras and any(cam['working'] for cam in cameras):
        print(f"\n🔧 To fix the main app:")
        print(f"   - Camera access is working ✅")
        print(f"   - Issue is in PyQt5 GUI display system")
        print(f"   - Need to check widget hierarchy and Z-order")
    else:
        print(f"\n🔧 To fix the main app:")
        print(f"   - Camera access is failing ❌")
        print(f"   - This is the root cause")
        print(f"   - Need to fix camera access first")
    
    return 0

if __name__ == "__main__":
    import sys
    sys.exit(main())
