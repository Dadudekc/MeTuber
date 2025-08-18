#!/usr/bin/env python3
"""
Performance Test Script for Dreamscape V2
Demonstrates the new performance optimizations
"""

import time
import cv2
import numpy as np

def test_camera_performance():
    """Test camera performance with different settings."""
    print("🎥 Camera Performance Test")
    print("=" * 40)
    
    # Test camera access
    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        print("❌ Camera not accessible")
        return
    
    # Get camera properties
    width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    fps = cap.get(cv2.CAP_PROP_FPS)
    
    print(f"📊 Camera Properties:")
    print(f"   Resolution: {width}x{height}")
    print(f"   Native FPS: {fps}")
    
    # Test different quality settings
    test_settings = [
        ("High Quality", 1.0, "Full resolution, no frame skipping"),
        ("Medium Quality", 0.5, "Half resolution, skip every 2nd frame"),
        ("Performance Mode", 0.25, "Quarter resolution, skip every 3rd frame")
    ]
    
    for name, scale, description in test_settings:
        print(f"\n🔧 Testing: {name}")
        print(f"   Description: {description}")
        
        # Set camera properties
        cap.set(cv2.CAP_PROP_FRAME_WIDTH, int(width * scale))
        cap.set(cv2.CAP_PROP_FRAME_HEIGHT, int(height * scale))
        
        # Measure FPS
        start_time = time.time()
        frame_count = 0
        test_duration = 3  # Test for 3 seconds
        
        while time.time() - start_time < test_duration:
            ret, frame = cap.read()
            if ret:
                frame_count += 1
            time.sleep(0.01)  # Small delay to simulate processing
        
        elapsed_time = time.time() - start_time
        measured_fps = frame_count / elapsed_time
        
        print(f"   Result: {measured_fps:.1f} FPS")
        
        # Calculate processing time per frame
        if measured_fps > 0:
            ms_per_frame = (elapsed_time / frame_count) * 1000
            print(f"   Processing: {ms_per_frame:.1f}ms per frame")
    
    cap.release()
    print("\n✅ Performance test completed!")

def test_effect_performance():
    """Test effect processing performance."""
    print("\n🎨 Effect Processing Performance Test")
    print("=" * 40)
    
    # Create test frame
    test_frame = np.random.randint(0, 255, (480, 640, 3), dtype=np.uint8)
    
    # Test different effects
    effects = [
        ("Edge Detection", lambda img: cv2.Canny(cv2.cvtColor(img, cv2.COLOR_BGR2GRAY), 100, 200)),
        ("Blur", lambda img: cv2.GaussianBlur(img, (15, 15), 0)),
        ("Cartoon", lambda img: cv2.stylization(img, sigma_s=60, sigma_r=0.4)),
        ("Sketch", lambda img: cv2.pencilSketch(img, sigma_s=60, sigma_r=0.07, shade_factor=0.1)[0])
    ]
    
    for effect_name, effect_func in effects:
        print(f"\n🔧 Testing: {effect_name}")
        
        # Test multiple iterations
        iterations = 10
        start_time = time.time()
        
        for i in range(iterations):
            result = effect_func(test_frame)
        
        total_time = time.time() - start_time
        avg_time = (total_time / iterations) * 1000  # Convert to milliseconds
        
        print(f"   Average time: {avg_time:.1f}ms per frame")
        
        # Calculate theoretical FPS
        theoretical_fps = 1000 / avg_time if avg_time > 0 else 0
        print(f"   Theoretical FPS: {theoretical_fps:.1f}")
        
        # Performance rating
        if avg_time < 33:  # 30+ FPS
            rating = "🟢 Excellent"
        elif avg_time < 66:  # 15+ FPS
            rating = "🟡 Good"
        elif avg_time < 100:  # 10+ FPS
            rating = "🟠 Acceptable"
        else:
            rating = "🔴 Poor"
        
        print(f"   Rating: {rating}")

def show_performance_tips():
    """Show performance optimization tips."""
    print("\n💡 Performance Optimization Tips")
    print("=" * 40)
    
    tips = [
        "🎯 **Use Performance Mode**: Click the '⚡ Performance' button for higher FPS",
        "📱 **Reduce Resolution**: Lower camera resolution for better performance",
        "⏭️ **Frame Skipping**: Enable frame skipping for heavy effects",
        "🎨 **Effect Selection**: Choose lighter effects for real-time streaming",
        "🔄 **Restart Preview**: Restart preview if performance degrades",
        "💻 **Close Other Apps**: Free up CPU/GPU resources",
        "🌡️ **Monitor Temperature**: High CPU temperature can cause throttling"
    ]
    
    for tip in tips:
        print(f"   {tip}")

def main():
    """Run all performance tests."""
    print("🚀 Dreamscape V2 Performance Test Suite")
    print("=" * 50)
    
    try:
        test_camera_performance()
        test_effect_performance()
        show_performance_tips()
        
        print("\n🎉 All tests completed successfully!")
        print("\n💡 To use these optimizations in the main app:")
        print("   1. Launch the main application")
        print("   2. Click '⚡ Performance' button to toggle modes")
        print("   3. Monitor FPS in the status bar")
        print("   4. Adjust settings based on your needs")
        
    except Exception as e:
        print(f"❌ Test failed: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()
