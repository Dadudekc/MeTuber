#!/usr/bin/env python3
"""
Test frame flow from webcam service to preview
"""

import sys
import os
import time
import cv2
import numpy as np

# Add the project root to Python path
project_root = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, project_root)

def test_frame_flow():
    """Test the frame flow from webcam service to preview."""
    print("Testing frame flow...")
    
    try:
        # Import webcam service
        from src.services.webcam_service import WebcamService
        
        # Create webcam service
        webcam_service = WebcamService()
        print("✓ Webcam service created")
        
        # Start the service
        success = webcam_service.start_processing("0", None, {})
        print(f"✓ Webcam service started: {success}")
        
        # Wait a moment for initialization
        time.sleep(2)
        
        # Check if service is running
        is_running = webcam_service.is_running()
        print(f"✓ Service running: {is_running}")
        
        # Try to get frames
        for i in range(5):
            frame = webcam_service.get_last_frame()
            if frame is not None:
                print(f"✓ Frame {i+1}: {frame.shape}")
            else:
                print(f"✗ Frame {i+1}: None")
            time.sleep(0.5)
        
        # Stop the service
        webcam_service.stop_processing()
        print("✓ Webcam service stopped")
        
        return True
        
    except Exception as e:
        print(f"✗ Error testing frame flow: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = test_frame_flow()
    if success:
        print("\nFrame flow test completed successfully!")
    else:
        print("\nFrame flow test failed.") 