#!/usr/bin/env python3
"""
Simple camera test script to verify camera functionality
"""

import cv2
import sys
import time

def test_camera():
    """Test camera functionality."""
    print("Testing camera functionality...")
    
    # Try different camera indices
    for camera_index in [0, 1, 2]:
        print(f"Trying camera index: {camera_index}")
        
        try:
            # Open camera
            cap = cv2.VideoCapture(camera_index)
            
            if cap.isOpened():
                print(f"✓ Camera {camera_index} opened successfully")
                
                # Set properties
                cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
                cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
                cap.set(cv2.CAP_PROP_FPS, 30)
                
                # Try to read a frame
                ret, frame = cap.read()
                if ret and frame is not None:
                    print(f"✓ Camera {camera_index} can read frames: {frame.shape}")
                    
                    # Show frame briefly
                    cv2.imshow(f'Camera {camera_index} Test', frame)
                    cv2.waitKey(2000)  # Show for 2 seconds
                    cv2.destroyAllWindows()
                    
                    cap.release()
                    print(f"✓ Camera {camera_index} test completed successfully")
                    return True
                else:
                    print(f"✗ Camera {camera_index} opened but failed to read frame")
                    cap.release()
            else:
                print(f"✗ Failed to open camera {camera_index}")
                
        except Exception as e:
            print(f"✗ Error testing camera {camera_index}: {e}")
    
    print("No working camera found")
    return False

if __name__ == "__main__":
    success = test_camera()
    if success:
        print("\nCamera test completed successfully!")
    else:
        print("\nCamera test failed. Check your camera connection.") 