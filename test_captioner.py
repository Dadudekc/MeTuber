#!/usr/bin/env python3
"""
Captioner Test Script

Demonstrates the speech-to-text captioner functionality with a simple video feed.
"""

import sys
import os
import cv2
import numpy as np
import time
import logging

# Add project root to Python path
project_root = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, project_root)

from src.captioner import CaptionerManager, CaptionerConfig

def setup_logging():
    """Setup logging for the test."""
    logging.basicConfig(
        level=logging.WARNING,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )

def create_test_frame(width=640, height=480):
    """Create a test video frame."""
    # Create a gradient background
    frame = np.zeros((height, width, 3), dtype=np.uint8)
    
    # Add gradient
    for y in range(height):
        for x in range(width):
            frame[y, x] = [
                int(255 * x / width),  # Red gradient
                int(255 * y / height), # Green gradient
                128                     # Blue constant
            ]
    
    # Add some text to show it's working
    cv2.putText(frame, "Captioner Test", (50, 50), 
                cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)
    cv2.putText(frame, "Speak into your microphone", (50, 100), 
                cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)
    cv2.putText(frame, "Press 'q' to quit", (50, 150), 
                cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)
    
    return frame

def main():
    """Main test function."""
    setup_logging()
    logger = logging.getLogger(__name__)
    
    # Create captioner configuration
    config = CaptionerConfig(
        enabled=True,
        engine="dummy",  # Use dummy engine for testing
        language="en",
        font_size=24,
        font_color=(255, 255, 255),  # White text
        background_color=(0, 0, 0),  # Black background
        background_opacity=0.8,
        outline_color=(0, 0, 0),     # Black outline
        outline_width=2,
        typing_speed=0.03,           # Faster typing for demo
        fade_in_duration=0.2,
        fade_out_duration=0.3
    )
    
    # Create captioner manager
    captioner = CaptionerManager(config)
    
    # Set up callbacks
    def on_text_update(text):
        print(f"🎤 {text}")
    
    def on_error(error):
        logger.error(f"Captioner error: {error}")
    
    def on_status_change(status):
        print(f"📊 Status: {status}")
    
    captioner.set_text_callback(on_text_update)
    captioner.set_error_callback(on_error)
    captioner.set_status_callback(on_status_change)
    
    # Initialize and start captioner
    if not captioner.initialize():
        logger.error("Failed to initialize captioner")
        return
    
    if not captioner.start():
        logger.error("Failed to start captioner")
        return
    
    print("🎬 Captioner Test Started!")
    print("🎤 Speak into your microphone to see live captions!")
    print("⌨️  Press 'q' to quit, 'c' to clear text, 's' for status, 'h' for history")
    
    # Create video window
    cv2.namedWindow("Captioner Test", cv2.WINDOW_NORMAL)
    cv2.resizeWindow("Captioner Test", 800, 600)
    
    try:
        frame_count = 0
        start_time = time.time()
        
        while True:
            # Create test frame
            frame = create_test_frame()
            
            # Add frame counter
            frame_count += 1
            fps = frame_count / (time.time() - start_time)
            cv2.putText(frame, f"FPS: {fps:.1f}", (50, 200), 
                       cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)
            
            # Render captioner overlay
            frame_with_captions = captioner.render_frame(frame)
            
            # Display frame
            cv2.imshow("Captioner Test", frame_with_captions)
            
            # Check for key press
            key = cv2.waitKey(1) & 0xFF
            if key == ord('q'):
                break
            elif key == ord('c'):
                # Clear text
                captioner.clear_text()
                print("Text cleared")
            elif key == ord('s'):
                # Show status
                status = captioner.get_status()
                print(f"Status: {status}")
            elif key == ord('h'):
                # Show text history
                history = captioner.get_text_history()
                print(f"Text history: {history}")
            
            # Small delay to control frame rate
            time.sleep(0.03)  # ~30 FPS
            
    except KeyboardInterrupt:
        print("Interrupted by user")
    except Exception as e:
        logger.error(f"Error in main loop: {e}")
    finally:
        # Cleanup
        cv2.destroyAllWindows()
        captioner.stop()
        captioner.cleanup()
        print("Test completed")

if __name__ == "__main__":
    main() 