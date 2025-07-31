#!/usr/bin/env python3
"""
Test Import

Test if the cartoon effect can be imported directly.
"""

import sys
import os
import importlib.util

# Add the project root to Python path
project_root = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, project_root)

def test_direct_import():
    """Test importing the cartoon effect directly."""
    print("=== Direct Import Test ===")
    
    # Path to the cartoon effect
    cartoon_dir = os.path.join(project_root, "src", "plugins", "effects", "artistic", "cartoon_effect")
    init_file = os.path.join(cartoon_dir, "__init__.py")
    
    print(f"Cartoon directory: {cartoon_dir}")
    print(f"Init file: {init_file}")
    print(f"Init file exists: {os.path.exists(init_file)}")
    
    try:
        # Try to load the module directly
        spec = importlib.util.spec_from_file_location("cartoon_effect", init_file)
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        
        print("✓ Module loaded successfully")
        
        # Check if register_plugin function exists
        if hasattr(module, 'register_plugin'):
            print("✓ register_plugin function found")
        else:
            print("✗ register_plugin function not found")
        
        # Check if plugin and ui exist
        if hasattr(module, 'plugin'):
            print("✓ plugin instance found")
        else:
            print("✗ plugin instance not found")
        
        if hasattr(module, 'ui'):
            print("✓ ui instance found")
        else:
            print("✗ ui instance not found")
        
        return True
        
    except Exception as e:
        print(f"✗ Error importing module: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = test_direct_import()
    if success:
        print("\n✓ Import test passed!")
    else:
        print("\n✗ Import test failed!") 