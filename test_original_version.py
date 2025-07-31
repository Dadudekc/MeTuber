#!/usr/bin/env python3
"""
Test the original simpler version of the application
"""

import sys
import os

# Add the project root to Python path
project_root = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, project_root)

def test_original_version():
    """Test the original simpler version."""
    print("Testing original version...")
    
    try:
        # Import the original main
        from src.main import main
        
        print("✓ Original main imported successfully")
        print("Starting original version...")
        
        # Run the original version
        return main()
        
    except Exception as e:
        print(f"✗ Error testing original version: {e}")
        import traceback
        traceback.print_exc()
        return 1

if __name__ == "__main__":
    print("=== Testing Original Version ===")
    result = test_original_version()
    print(f"\nOriginal version test completed with result: {result}") 