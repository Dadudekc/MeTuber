#!/usr/bin/env python3
"""
Diagnostic script for Dreamscape Virtual Camera
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

def diagnose_virtual_camera():
    """Diagnose virtual camera issues."""
    print("🔍 Dreamscape Virtual Camera Diagnostics")
    print("=" * 50)
    
    # Check pyvirtualcam installation
    print("\n1. Checking pyvirtualcam installation...")
    try:
        import pyvirtualcam
        print("  ✅ pyvirtualcam is installed")
        print(f"    Version: {pyvirtualcam.__version__}")
    except ImportError:
        print("  ❌ pyvirtualcam is not installed")
        print("    Install with: pip install pyvirtualcam")
        return
    
    # Check available backends
    print("\n2. Checking available virtual camera backends...")
    try:
        from pyvirtualcam import Camera, Backend
        
        available_backends = []
        for backend_name in ['OBS_VIRTUAL_CAM', 'OBS_VIRTUAL_CAM_LEGACY', 'OBS_VIRTUAL_CAM_DEVICE']:
            try:
                backend = getattr(Backend, backend_name)
                test_camera = Camera(width=640, height=480, fps=30, backend=backend)
                test_camera.close()
                available_backends.append(backend_name)
                print(f"  ✅ {backend_name} is available")
            except Exception as e:
                print(f"  ❌ {backend_name} failed: {e}")
        
        if available_backends:
            print(f"  ✅ {len(available_backends)} backend(s) available")
        else:
            print("  ❌ No virtual camera backends available")
            
    except Exception as e:
        print(f"  ❌ Error checking backends: {e}")
    
    # Check OBS Virtual Camera installation
    print("\n3. Checking OBS Virtual Camera...")
    try:
        import subprocess
        result = subprocess.run(['obs-virtualcam', '--version'], 
                              capture_output=True, text=True, timeout=5)
        if result.returncode == 0:
            print("  ✅ OBS Virtual Camera is installed")
            print(f"    Version: {result.stdout.strip()}")
        else:
            print("  ⚠️ OBS Virtual Camera not found in PATH")
            print("    Install OBS Studio to get virtual camera support")
    except Exception as e:
        print(f"  ⚠️ Could not check OBS Virtual Camera: {e}")
    
    # Test creating a virtual camera
    print("\n4. Testing virtual camera creation...")
    try:
        from pyvirtualcam import Camera, PixelFormat
        
        # Try with Dreamscape branding
        camera = Camera(
            width=640, 
            height=480, 
            fps=30, 
            fmt=PixelFormat.BGR,
            device="Dreamscape Virtual Camera"
        )
        print("  ✅ Successfully created Dreamscape Virtual Camera")
        print(f"    Device name: {camera.device}")
        print(f"    Backend: {camera.backend}")
        camera.close()
        
    except Exception as e:
        print(f"  ❌ Failed to create virtual camera: {e}")
    
    # Provide recommendations
    print("\n5. Recommendations:")
    print("  📹 To use Dreamscape Virtual Camera in OBS:")
    print("    1. Start the MeTuber application")
    print("    2. Click '📹 Enable Dreamscape Virtual Camera'")
    print("    3. Open OBS Studio")
    print("    4. Add 'Video Capture Device' source")
    print("    5. Select 'Dreamscape Virtual Camera' from device list")
    print("    6. Your processed video with effects will appear in OBS!")
    
    print("\n  🔧 If virtual camera doesn't appear:")
    print("    - Restart OBS Studio")
    print("    - Check Windows Camera privacy settings")
    print("    - Ensure OBS Studio is installed")
    print("    - Try running as administrator")
    
    print("\n  🛠️ Troubleshooting:")
    print("    - Install OBS Studio: https://obsproject.com/")
    print("    - Check Windows Camera settings in Privacy & Security")
    print("    - Ensure pyvirtualcam is up to date: pip install --upgrade pyvirtualcam")

if __name__ == "__main__":
    diagnose_virtual_camera() 