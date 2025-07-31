#!/usr/bin/env python3
"""
Test script to list all available styles and their parameters.
"""

import sys
import logging
from PyQt5.QtWidgets import QApplication

# Add the src directory to the path
sys.path.insert(0, 'src')

from core.style_manager import StyleManager

# Set up logging
logging.basicConfig(level=logging.INFO)

def test_available_styles():
    """Test to see what styles are available."""
    app = QApplication(sys.argv)
    
    # Create style manager
    style_manager = StyleManager()
    
    print("=== AVAILABLE STYLES ===")
    
    # Get all styles
    all_styles = style_manager.style_instances
    categories = style_manager.get_categories()
    
    print(f"\nTotal styles loaded: {len(all_styles)}")
    print(f"Categories: {list(categories.keys())}")
    
    # List all styles by category
    for category, styles in categories.items():
        print(f"\n--- {category} ---")
        for style_name in styles:
            style_instance = style_manager.get_style(style_name)
            if style_instance:
                # Get parameters
                if hasattr(style_instance, 'define_parameters'):
                    try:
                        params = style_instance.define_parameters()
                        param_count = len(params) if isinstance(params, (list, dict)) else 0
                        print(f"  {style_name} ({param_count} parameters)")
                        
                        # Show parameter details
                        if isinstance(params, dict):
                            for param_name, param_def in params.items():
                                default = param_def.get('default', 'N/A')
                                min_val = param_def.get('min', 'N/A')
                                max_val = param_def.get('max', 'N/A')
                                print(f"    - {param_name}: {default} ({min_val}-{max_val})")
                        elif isinstance(params, list):
                            for param in params:
                                name = param.get('name', 'Unknown')
                                default = param.get('default', 'N/A')
                                min_val = param.get('min', 'N/A')
                                max_val = param.get('max', 'N/A')
                                print(f"    - {name}: {default} ({min_val}-{max_val})")
                    except Exception as e:
                        print(f"  {style_name} (Error getting parameters: {e})")
                else:
                    print(f"  {style_name} (No parameters)")
            else:
                print(f"  {style_name} (Not found)")
    
    # Test specific styles
    print("\n=== TESTING SPECIFIC STYLES ===")
    test_styles = ["Cartoon", "EdgeDetection", "PencilSketch", "Watercolor"]
    
    for style_name in test_styles:
        style_instance = style_manager.get_style(style_name)
        if style_instance:
            print(f"\n✅ {style_name} found!")
            if hasattr(style_instance, 'define_parameters'):
                try:
                    params = style_instance.define_parameters()
                    print(f"  Parameters: {params}")
                except Exception as e:
                    print(f"  Error getting parameters: {e}")
        else:
            print(f"\n❌ {style_name} NOT FOUND")
    
    print("\n=== STYLE MAPPING TEST ===")
    # Test the mapping we're using
    test_mappings = {
        "🎭 Cartoon Effects": "Cartoon",
        "✏️ Sketch Effects": "PencilSketch", 
        "🔍 Edge Detection": "EdgeDetection",
        "🌊 Watercolor": "Watercolor"
    }
    
    for ui_name, style_name in test_mappings.items():
        style_instance = style_manager.get_style(style_name)
        if style_instance:
            print(f"✅ {ui_name} -> {style_name} (FOUND)")
            if hasattr(style_instance, 'define_parameters'):
                try:
                    params = style_instance.define_parameters()
                    param_count = len(params) if isinstance(params, (list, dict)) else 0
                    print(f"   Parameters: {param_count}")
                except Exception as e:
                    print(f"   Error: {e}")
        else:
            print(f"❌ {ui_name} -> {style_name} (NOT FOUND)")
    
    app.quit()

if __name__ == "__main__":
    test_available_styles() 