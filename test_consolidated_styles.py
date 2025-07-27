#!/usr/bin/env python3
"""
Test script to verify that consolidated styles are working correctly.
"""

import cv2
import numpy as np
import sys
import os

# Add the project root to the path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def test_consolidated_cartoon():
    """Test the ConsolidatedCartoon effect."""
    print("Testing ConsolidatedCartoon effect...")
    
    try:
        from styles.consolidated.consolidated_styles import ConsolidatedCartoon
        
        # Create test image
        test_image = np.random.randint(0, 255, (480, 640, 3), dtype=np.uint8)
        
        # Test each variant
        variants = ["Classic", "Fast", "Anime", "Advanced", "Whole Image"]
        
        for variant in variants:
            print(f"  Testing variant: {variant}")
            
            # Create style instance
            cartoon_style = ConsolidatedCartoon()
            cartoon_style.current_variant = variant
            
            # Test parameters
            params = {
                "intensity": 50,
                "smoothing": 50,
                "edge_strength": 50,
                "color_levels": 8
            }
            
            # Apply effect
            result = cartoon_style.apply(test_image, params)
            
            # Verify output
            if result.shape == test_image.shape and result.dtype == np.uint8:
                print(f"    ✅ {variant} variant working correctly!")
            else:
                print(f"    ❌ {variant} variant failed - wrong output format")
                return False
                
        print("✅ All ConsolidatedCartoon variants working!")
        return True
        
    except Exception as e:
        print(f"❌ Error testing ConsolidatedCartoon: {e}")
        return False

def test_consolidated_sketch():
    """Test the ConsolidatedSketch effect."""
    print("\nTesting ConsolidatedSketch effect...")
    
    try:
        from styles.consolidated.consolidated_styles import ConsolidatedSketch
        
        # Create test image
        test_image = np.random.randint(0, 255, (480, 640, 3), dtype=np.uint8)
        
        # Test each variant
        variants = ["Pencil", "Advanced Pencil", "Color Sketch", "Line Art", "Stippling"]
        
        for variant in variants:
            print(f"  Testing variant: {variant}")
            
            # Create style instance
            sketch_style = ConsolidatedSketch()
            sketch_style.current_variant = variant
            
            # Test parameters
            params = {
                "intensity": 50,
                "detail": 50,
                "contrast": 50,
                "color_preservation": 0
            }
            
            # Apply effect
            result = sketch_style.apply(test_image, params)
            
            # Verify output
            if result.shape == test_image.shape and result.dtype == np.uint8:
                print(f"    ✅ {variant} variant working correctly!")
            else:
                print(f"    ❌ {variant} variant failed - wrong output format")
                return False
                
        print("✅ All ConsolidatedSketch variants working!")
        return True
        
    except Exception as e:
        print(f"❌ Error testing ConsolidatedSketch: {e}")
        return False

def test_consolidated_color():
    """Test the ConsolidatedColor effect."""
    print("\nTesting ConsolidatedColor effect...")
    
    try:
        from styles.consolidated.consolidated_styles import ConsolidatedColor
        
        # Create test image
        test_image = np.random.randint(0, 255, (480, 640, 3), dtype=np.uint8)
        
        # Test each variant
        variants = ["Brightness", "Contrast", "Color Balance", "Vibrant", "Sepia", "Black & White", "Negative", "Invert"]
        
        for variant in variants:
            print(f"  Testing variant: {variant}")
            
            # Create style instance
            color_style = ConsolidatedColor()
            color_style.current_variant = variant
            
            # Test parameters
            params = {
                "intensity": 50,
                "red": 50,
                "green": 50,
                "blue": 50
            }
            
            # Apply effect
            result = color_style.apply(test_image, params)
            
            # Verify output
            if result.shape == test_image.shape and result.dtype == np.uint8:
                print(f"    ✅ {variant} variant working correctly!")
            else:
                print(f"    ❌ {variant} variant failed - wrong output format")
                return False
                
        print("✅ All ConsolidatedColor variants working!")
        return True
        
    except Exception as e:
        print(f"❌ Error testing ConsolidatedColor: {e}")
        return False

def test_style_manager_integration():
    """Test that consolidated styles are properly loaded by the style manager."""
    print("\nTesting Style Manager Integration...")
    
    try:
        from src.core.style_manager import StyleManager
        
        style_manager = StyleManager()
        
        # Check if consolidated styles are loaded
        consolidated_styles = [
            "Cartoon Effects",
            "Sketch Effects", 
            "Color Effects"
        ]
        
        for style_name in consolidated_styles:
            if style_name in style_manager.style_instances:
                style_instance = style_manager.style_instances[style_name]
                variants = style_instance.get_available_variants()
                print(f"  ✅ {style_name} loaded with {len(variants)} variants: {variants}")
            else:
                print(f"  ❌ {style_name} not found in style manager")
                return False
                
        print("✅ All consolidated styles properly integrated!")
        return True
        
    except Exception as e:
        print(f"❌ Error testing style manager integration: {e}")
        return False

def main():
    """Run all tests."""
    print("🧪 Testing Consolidated Styles System")
    print("=" * 60)
    
    tests = [
        test_consolidated_cartoon,
        test_consolidated_sketch,
        test_consolidated_color,
        test_style_manager_integration
    ]
    
    passed = 0
    total = len(tests)
    
    for test in tests:
        if test():
            passed += 1
        print()
    
    print("=" * 60)
    print(f"Tests passed: {passed}/{total}")
    
    if passed == total:
        print("🎉 All tests passed! Consolidated styles system is working correctly.")
        print("\n📋 Summary:")
        print("  • Cartoon Effects: 5 variants (Classic, Fast, Anime, Advanced, Whole Image)")
        print("  • Sketch Effects: 5 variants (Pencil, Advanced Pencil, Color Sketch, Line Art, Stippling)")
        print("  • Color Effects: 8 variants (Brightness, Contrast, Color Balance, Vibrant, Sepia, B&W, Negative, Invert)")
        print("  • Total: 18 effects consolidated into 3 unified style classes")
    else:
        print("⚠️  Some tests failed. Check the output above.")

if __name__ == "__main__":
    main() 