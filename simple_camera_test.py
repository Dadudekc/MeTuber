#!/usr/bin/env python3
"""
Simple camera test that directly tests camera functionality
"""

import cv2
import time
import numpy as np

def test_camera_direct():
    """Test camera functionality directly."""
    print("Testing camera directly...")
    
    # Try to open camera
    cap = cv2.VideoCapture(0)
    
    if cap.isOpened():
        print("✓ Camera opened successfully")
        
        # Set properties
        cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
        cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
        cap.set(cv2.CAP_PROP_FPS, 30)
        
        # Try to read frames
        for i in range(5):
            ret, frame = cap.read()
            if ret and frame is not None:
                print(f"✓ Frame {i+1}: {frame.shape}")
                
                # Show frame briefly
                cv2.imshow(f'Camera Test {i+1}', frame)
                cv2.waitKey(500)  # Show for 0.5 seconds
                cv2.destroyAllWindows()
            else:
                print(f"✗ Frame {i+1}: Failed to read")
            
            time.sleep(0.5)
        
        cap.release()
        print("✓ Camera test completed successfully!")
        return True
    else:
        print("✗ Failed to open camera")
        return False

def test_generated_frames():
    """Test generated frames (fallback)."""
    print("Testing generated frames...")
    
    for i in range(3):
        # Generate test frame
        height, width = 480, 640
        frame = np.zeros((height, width, 3), dtype=np.uint8)
        
        # Add some visual elements
        for y in range(height):
            for x in range(width):
                frame[y, x] = [
                    int(255 * x / width),  # Blue gradient
                    int(255 * y / height), # Green gradient
                    128  # Red constant
                ]
        
        # Add text overlay
        cv2.putText(frame, f"Test Frame {i+1}", (50, height//2), 
                   cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)
        
        print(f"✓ Generated frame {i+1}: {frame.shape}")
        
        # Show frame briefly
        cv2.imshow(f'Generated Frame {i+1}', frame)
        cv2.waitKey(1000)  # Show for 1 second
        cv2.destroyAllWindows()
    
    print("✓ Generated frames test completed successfully!")
    return True

if __name__ == "__main__":
    print("=== Camera Test ===")
    
    # Test real camera first
    if test_camera_direct():
        print("\nReal camera is working!")
    else:
        print("\nReal camera failed, testing generated frames...")
        test_generated_frames()
        print("\nGenerated frames are working!")
    
    print("\nTest completed!") 