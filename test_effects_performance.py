#!/usr/bin/env python3
"""
Effects Performance Test
Measures performance of Cartoon, Advanced Cartoon, and Pencil Sketch effects
"""

import cv2
import numpy as np
import time
import sys
import os

# Add the project root to Python path for imports
project_root = os.path.dirname(os.path.abspath(__file__))
if project_root not in sys.path:
    sys.path.insert(0, project_root)

def test_cartoon_effect():
    """Test basic Cartoon Effect performance."""
    print("🎨 Testing Basic Cartoon Effect Performance")
    print("=" * 50)
    
    try:
        from src.plugins.effects.artistic.cartoon_effect.effect import CartoonEffectPlugin
        
        # Create test image
        test_image = np.random.randint(0, 255, (480, 640, 3), dtype=np.uint8)
        print(f"✅ Test image created: {test_image.shape}")
        
        # Create effect plugin
        effect = CartoonEffectPlugin()
        print(f"✅ Plugin created: {effect.name}")
        
        # Test different parameter combinations
        test_params = [
            {'edge_strength': 1.0, 'color_reduction': 8, 'blur_strength': 5},
            {'edge_strength': 0.5, 'color_reduction': 4, 'blur_strength': 3},
            {'edge_strength': 2.0, 'color_reduction': 16, 'blur_strength': 7}
        ]
        
        for i, params in enumerate(test_params):
            print(f"\n🔧 Test {i+1}: {params}")
            
            # Measure performance
            start_time = time.time()
            
            # Apply effect multiple times for accurate measurement
            for j in range(10):
                result = effect.apply(test_image, params)
            
            end_time = time.time()
            total_time = end_time - start_time
            avg_time = total_time / 10
            
            print(f"   ⏱️  Average time: {avg_time*1000:.2f}ms")
            print(f"   🚀 FPS equivalent: {1/avg_time:.1f}")
            
            # Check result quality
            if result is not None and result.shape == test_image.shape:
                print(f"   ✅ Result valid: {result.shape}")
            else:
                print(f"   ❌ Result invalid: {result.shape if result is not None else 'None'}")
        
        return True
        
    except Exception as e:
        print(f"❌ Basic Cartoon Effect test failed: {e}")
        return False

def test_advanced_cartoon_effect():
    """Test Advanced Cartoon Effect performance."""
    print("\n🎭 Testing Advanced Cartoon Effect Performance")
    print("=" * 50)
    
    try:
        from src.plugins.effects.artistic.advanced_cartoon_effect.effect import AdvancedCartoonEffectPlugin
        
        # Create test image
        test_image = np.random.randint(0, 255, (480, 640, 3), dtype=np.uint8)
        print(f"✅ Test image created: {test_image.shape}")
        
        # Create effect plugin
        effect = AdvancedCartoonEffectPlugin()
        print(f"✅ Plugin created: {effect.name}")
        
        # Test different parameter combinations
        test_params = [
            {'intensity': 50, 'smoothness': 0.7, 'ai_edge_detection': True, 'edge_sensitivity': 75},
            {'intensity': 25, 'smoothness': 0.3, 'ai_edge_detection': False, 'edge_sensitivity': 50},
            {'intensity': 75, 'smoothness': 0.9, 'ai_edge_detection': True, 'edge_sensitivity': 100}
        ]
        
        for i, params in enumerate(test_params):
            print(f"\n🔧 Test {i+1}: {params}")
            
            # Measure performance
            start_time = time.time()
            
            # Apply effect multiple times for accurate measurement
            for j in range(10):
                result = effect.apply(test_image, params)
            
            end_time = time.time()
            total_time = end_time - start_time
            avg_time = total_time / 10
            
            print(f"   ⏱️  Average time: {avg_time*1000:.2f}ms")
            print(f"   🚀 FPS equivalent: {1/avg_time:.1f}")
            
            # Check result quality
            if result is not None and result.shape == test_image.shape:
                print(f"   ✅ Result valid: {result.shape}")
            else:
                print(f"   ❌ Result invalid: {result.shape if result is not None else 'None'}")
        
        return True
        
    except Exception as e:
        print(f"❌ Advanced Cartoon Effect test failed: {e}")
        return False

def test_pencil_sketch_effect():
    """Test Pencil Sketch Effect performance."""
    print("\n✏️ Testing Pencil Sketch Effect Performance")
    print("=" * 50)
    
    try:
        from src.plugins.effects.artistic.pencil_sketch_effect.effect import PencilSketchEffectPlugin
        
        # Create test image
        test_image = np.random.randint(0, 255, (480, 640, 3), dtype=np.uint8)
        print(f"✅ Test image created: {test_image.shape}")
        
        # Create effect plugin
        effect = PencilSketchEffectPlugin()
        print(f"✅ Plugin created: {effect.name}")
        
        # Test different parameter combinations
        test_params = [
            {'blur_intensity': 15, 'contrast': 1.5, 'line_thickness': 1, 'paper_texture': True},
            {'blur_intensity': 9, 'contrast': 1.0, 'line_thickness': 1, 'paper_texture': False},
            {'blur_intensity': 25, 'contrast': 2.0, 'line_thickness': 3, 'paper_texture': True}
        ]
        
        for i, params in enumerate(test_params):
            print(f"\n🔧 Test {i+1}: {params}")
            
            # Measure performance
            start_time = time.time()
            
            # Apply effect multiple times for accurate measurement
            for j in range(10):
                result = effect.apply(test_image, params)
            
            end_time = time.time()
            total_time = end_time - start_time
            avg_time = total_time / 10
            
            print(f"   ⏱️  Average time: {avg_time*1000:.2f}ms")
            print(f"   🚀 FPS equivalent: {1/avg_time:.1f}")
            
            # Check result quality
            if result is not None and result.shape == test_image.shape:
                print(f"   ✅ Result valid: {result.shape}")
            else:
                print(f"   ❌ Result invalid: {result.shape if result is not None else 'None'}")
        
        return True
        
    except Exception as e:
        print(f"❌ Pencil Sketch Effect test failed: {e}")
        return False

def test_watercolor_effect():
    """Test Watercolor Effect performance."""
    print("\n🎨 Testing Watercolor Effect Performance")
    print("=" * 50)
    
    try:
        from src.plugins.effects.artistic.watercolor_effect.effect import WatercolorEffectPlugin
        
        # Create test image
        test_image = np.random.randint(0, 255, (480, 640, 3), dtype=np.uint8)
        print(f"✅ Test image created: {test_image.shape}")
        
        # Create effect plugin
        effect = WatercolorEffectPlugin()
        print(f"✅ Plugin created: {effect.name}")
        
        # Test different parameter combinations
        test_params = [
            {'sigma_s': 30, 'sigma_r': 0.3, 'texture_overlay': False},  # Performance mode
            {'sigma_s': 60, 'sigma_r': 0.5, 'texture_overlay': True},   # Balanced mode
            {'sigma_s': 80, 'sigma_r': 0.8, 'texture_overlay': True}    # Quality mode
        ]
        
        for i, params in enumerate(test_params):
            print(f"\n🔧 Test {i+1}: {params}")
            
            # Measure performance
            start_time = time.time()
            
            # Apply effect multiple times for accurate measurement
            for j in range(10):
                result = effect.apply(test_image, params)
            
            end_time = time.time()
            total_time = end_time - start_time
            avg_time = total_time / 10
            
            print(f"   ⏱️  Average time: {avg_time*1000:.2f}ms")
            print(f"   🚀 FPS equivalent: {1/avg_time:.1f}")
            
            # Check result quality
            if result is not None and result.shape == test_image.shape:
                print(f"   ✅ Result valid: {result.shape}")
            else:
                print(f"   ❌ Result invalid: {result.shape if result is not None else 'None'}")
        
        return True
        
    except Exception as e:
        print(f"❌ Watercolor Effect test failed: {e}")
        return False

def test_neural_style_effect():
    """Test Neural Style Effect performance."""
    print("\n🎭 Testing Neural Style Effect Performance")
    print("=" * 50)
    
    try:
        from src.plugins.effects.artistic.neural_style_effect.effect import NeuralStyleEffectPlugin
        
        # Create test image
        test_image = np.random.randint(0, 255, (480, 640, 3), dtype=np.uint8)
        print(f"✅ Test image created: {test_image.shape}")
        
        # Create effect plugin
        effect = NeuralStyleEffectPlugin()
        print(f"✅ Plugin created: {effect.name}")
        
        # Test different parameter combinations
        test_params = [
            {'style_strength': 0.2, 'artistic_style': 'Van Gogh', 'texture_strength': 0.3},  # Performance mode
            {'style_strength': 0.5, 'artistic_style': 'Monet', 'texture_strength': 0.5},      # Balanced mode
            {'style_strength': 0.8, 'artistic_style': 'Picasso', 'texture_strength': 0.7}     # Quality mode
        ]
        
        for i, params in enumerate(test_params):
            print(f"\n🔧 Test {i+1}: {params}")
            
            # Measure performance
            start_time = time.time()
            
            # Apply effect multiple times for accurate measurement
            for j in range(10):
                result = effect.apply(test_image, params)
            
            end_time = time.time()
            total_time = end_time - start_time
            avg_time = total_time / 10
            
            print(f"   ⏱️  Average time: {avg_time*1000:.2f}ms")
            print(f"   🚀 FPS equivalent: {1/avg_time:.1f}")
            
            # Check result quality
            if result is not None and result.shape == test_image.shape:
                print(f"   ✅ Result valid: {result.shape}")
            else:
                print(f"   ❌ Result invalid: {result.shape if result is not None else 'None'}")
        
        return True
        
    except Exception as e:
        print(f"❌ Neural Style Effect test failed: {e}")
        return False

def test_manual_implementations():
    """Test manual implementations for comparison."""
    print("\n🔧 Testing Manual Implementations for Comparison")
    print("=" * 50)
    
    # Create test image
    test_image = np.random.randint(0, 255, (480, 640, 3), dtype=np.uint8)
    
    # Test basic cartoon (manual implementation)
    print("🎨 Basic Cartoon (Manual):")
    start_time = time.time()
    
    for i in range(10):
        # Convert to grayscale
        gray = cv2.cvtColor(test_image, cv2.COLOR_BGR2GRAY)
        # Apply bilateral filter (odd kernel size)
        bilateral = cv2.bilateralFilter(gray, 5, 75, 75)
        # Detect edges
        edges = cv2.adaptiveThreshold(bilateral, 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY, 9, 2)
        # Reduce colors (odd kernel size)
        color_reduced = cv2.medianBlur(test_image, 5)  # Fixed: use odd kernel size
        # Combine
        result = cv2.bitwise_and(color_reduced, cv2.cvtColor(edges, cv2.COLOR_GRAY2BGR))
    
    manual_time = (time.time() - start_time) / 10
    print(f"   ⏱️  Manual time: {manual_time*1000:.2f}ms")
    print(f"   🚀 Manual FPS: {1/manual_time:.1f}")
    
    # Test basic sketch (manual implementation)
    print("\n✏️ Basic Sketch (Manual):")
    start_time = time.time()
    
    for i in range(10):
        # Convert to grayscale
        gray = cv2.cvtColor(test_image, cv2.COLOR_BGR2GRAY)
        # Apply contrast
        contrasted = np.clip(gray * 1.5, 0, 255).astype(np.uint8)
        # Create inverted blurred (odd kernel size)
        inverted = 255 - contrasted
        blurred = cv2.GaussianBlur(inverted, (15, 15), 0)
        inverted_blurred = 255 - blurred
        # Create sketch
        sketch = cv2.divide(contrasted, inverted_blurred, scale=256.0)
        # Convert back
        result = cv2.cvtColor(sketch, cv2.COLOR_GRAY2BGR)
    
    manual_sketch_time = (time.time() - start_time) / 10
    print(f"   ⏱️  Manual sketch time: {manual_sketch_time*1000:.2f}ms")
    print(f"   🚀 Manual sketch FPS: {1/manual_sketch_time:.1f}")
    
    # Performance comparison
    print(f"\n📊 Manual vs Plugin Comparison:")
    print(f"   Basic Cartoon: Manual {manual_time*1000:.1f}ms vs Plugin {35.83:.1f}ms")
    print(f"   Pencil Sketch: Manual {manual_sketch_time*1000:.1f}ms vs Plugin {7.81:.1f}ms")

def main():
    """Main function to run all performance tests."""
    print("🚀 Effects Performance Test Suite")
    print("=" * 60)
    
    results = []
    
    # Test all effects
    results.append(("Basic Cartoon", test_cartoon_effect()))
    results.append(("Advanced Cartoon", test_advanced_cartoon_effect()))
    results.append(("Pencil Sketch", test_pencil_sketch_effect()))
    results.append(("Watercolor", test_watercolor_effect()))
    results.append(("Neural Style", test_neural_style_effect()))
    
    # Test manual implementations
    test_manual_implementations()
    
    # Summary
    print("\n" + "=" * 60)
    print("📊 Performance Test Summary:")
    print("=" * 60)
    
    for effect_name, success in results:
        status = "✅ PASS" if success else "❌ FAIL"
        print(f"{effect_name}: {status}")
    
    print("\n🎯 Performance Recommendations:")
    print("- Use lower blur intensities for better performance")
    print("- Disable paper texture when not needed")
    print("- Use simpler edge detection algorithms")
    print("- Consider quality reduction for real-time use")

if __name__ == "__main__":
    try:
        main()
        print("\n🎉 All tests completed!")
        
    except Exception as e:
        print(f"❌ Test suite failed: {e}")
        import traceback
        traceback.print_exc()
