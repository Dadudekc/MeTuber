#!/usr/bin/env python3
"""
Logitech C270 HD Webcam Resolution Test

This test checks what resolutions your C270 HD webcam actually supports.
"""

import cv2
import time

def test_c270_resolutions():
    """Test different resolutions for C270 HD webcam."""
    print("🔍 Testing Logitech C270 HD Webcam Resolutions")
    print("=" * 60)
    
    # Common HD resolutions to test
    resolutions = [
        (1280, 720),   # 720p HD
        (1280, 800),   # WXGA
        (1024, 768),   # XGA
        (800, 600),    # SVGA
        (640, 480),    # VGA
        (1280, 960),   # SXGA
        (1600, 900),   # HD+
        (1920, 1080),  # 1080p Full HD
    ]
    
    working_resolutions = []
    
    for width, height in resolutions:
        try:
            print(f"🔧 Testing {width}x{height}...")
            
            # Open camera
            cap = cv2.VideoCapture(0)
            if not cap.isOpened():
                print(f"   ❌ Failed to open camera")
                continue
            
            # Set resolution
            cap.set(cv2.CAP_PROP_FRAME_WIDTH, width)
            cap.set(cv2.CAP_PROP_FRAME_HEIGHT, height)
            
            # Wait a moment for settings to apply
            time.sleep(0.5)
            
            # Get actual resolution
            actual_width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
            actual_height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
            
            print(f"   📐 Requested: {width}x{height}")
            print(f"   📐 Actual: {actual_width}x{actual_height}")
            
            # Test frame capture
            ret, frame = cap.read()
            if ret and frame is not None:
                frame_shape = frame.shape
                print(f"   📸 Frame captured: ✅ {frame_shape}")
                
                if frame_shape[1] == actual_width and frame_shape[0] == actual_height:
                    print(f"   ✅ Resolution match: {actual_width}x{actual_height}")
                    working_resolutions.append({
                        'requested': (width, height),
                        'actual': (actual_width, actual_height),
                        'working': True
                    })
                else:
                    print(f"   ⚠️ Shape mismatch: {frame_shape[1]}x{frame_shape[0]}")
                    working_resolutions.append({
                        'requested': (width, height),
                        'actual': (actual_width, actual_height),
                        'working': False
                    })
            else:
                print(f"   ❌ Frame capture failed")
                working_resolutions.append({
                    'requested': (width, height),
                    'actual': (actual_width, actual_height),
                    'working': False
                })
            
            cap.release()
            
        except Exception as e:
            print(f"   ❌ Error: {e}")
            working_resolutions.append({
                'requested': (width, height),
                'actual': (0, 0),
                'working': False
            })
    
    return working_resolutions

def test_c270_properties():
    """Test C270 HD webcam properties."""
    print("\n🔧 Testing C270 HD Webcam Properties")
    print("=" * 50)
    
    try:
        cap = cv2.VideoCapture(0)
        if cap.isOpened():
            print("✅ Camera opened successfully")
            
            # Get all available properties
            properties = [
                (cv2.CAP_PROP_FRAME_WIDTH, "Frame Width"),
                (cv2.CAP_PROP_FRAME_HEIGHT, "Frame Height"),
                (cv2.CAP_PROP_FPS, "FPS"),
                (cv2.CAP_PROP_BRIGHTNESS, "Brightness"),
                (cv2.CAP_PROP_CONTRAST, "Contrast"),
                (cv2.CAP_PROP_SATURATION, "Saturation"),
                (cv2.CAP_PROP_HUE, "Hue"),
                (cv2.CAP_PROP_GAIN, "Gain"),
                (cv2.CAP_PROP_EXPOSURE, "Exposure"),
                (cv2.CAP_PROP_BACKEND, "Backend"),
                (cv2.CAP_PROP_FORMAT, "Format"),
                (cv2.CAP_PROP_MODE, "Mode"),
                (cv2.CAP_PROP_BUFFERSIZE, "Buffer Size"),
            ]
            
            for prop_id, prop_name in properties:
                try:
                    value = cap.get(prop_id)
                    print(f"   {prop_name}: {value}")
                except:
                    print(f"   {prop_name}: Not supported")
            
            cap.release()
        else:
            print("❌ Failed to open camera")
            
    except Exception as e:
        print(f"❌ Error testing properties: {e}")

def test_c270_backends():
    """Test different backends for C270 HD webcam."""
    print("\n🔧 Testing C270 HD Webcam Backends")
    print("=" * 50)
    
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
                
                # Try to set HD resolution
                cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
                cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)
                time.sleep(0.5)
                
                actual_width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
                actual_height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
                
                print(f"   📐 Resolution: {actual_width}x{actual_height}")
                
                # Try to read a frame
                ret, frame = cap.read()
                if ret and frame is not None:
                    print(f"   📸 Frame captured: ✅ {frame.shape}")
                else:
                    print(f"   ❌ Frame capture failed")
                
                cap.release()
            else:
                print(f"❌ {backend_name} failed to open")
                
        except Exception as e:
            print(f"❌ {backend_name} error: {e}")

def main():
    """Run C270 HD webcam tests."""
    print("🔧 Logitech C270 HD Webcam Test")
    print("=" * 60)
    
    # Test different resolutions
    resolutions = test_c270_resolutions()
    
    # Test properties
    test_c270_properties()
    
    # Test backends
    test_c270_backends()
    
    # Summary
    print("\n" + "=" * 60)
    print("📊 C270 HD WEBCAM TEST SUMMARY")
    print("=" * 60)
    
    if resolutions:
        print(f"🎯 Resolution Test Results:")
        for res in resolutions:
            status = "✅ Working" if res['working'] else "❌ Failed"
            print(f"   📐 {res['requested'][0]}x{res['requested'][1]} → {res['actual'][0]}x{res['actual'][1]} ({status})")
        
        # Find best working resolution
        working_res = [r for r in resolutions if r['working']]
        if working_res:
            best_res = max(working_res, key=lambda x: x['actual'][0] * x['actual'][1])
            print(f"\n🎉 BEST WORKING RESOLUTION: {best_res['actual'][0]}x{best_res['actual'][1]}")
            
            if best_res['actual'][0] >= 1280 and best_res['actual'][1] >= 720:
                print("✅ Your C270 HD webcam is working at HD resolution!")
            else:
                print("⚠️ Your C270 HD webcam is not achieving HD resolution")
                print("   - This might be a driver issue")
                print("   - Try updating Logitech drivers")
        else:
            print("\n❌ No resolutions are working properly!")
            print("   - This explains the preview issues")
            print("   - Need to fix camera configuration")
    
    print(f"\n💡 Recommendations:")
    print(f"   - Update Logitech C270 HD drivers")
    print(f"   - Check Windows camera privacy settings")
    print(f"   - Try different USB ports")
    print(f"   - Check if other apps can use the camera")
    
    return 0

if __name__ == "__main__":
    import sys
    sys.exit(main())
