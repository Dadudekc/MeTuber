#!/usr/bin/env python3
"""
Test the working V2 version with direct camera access
"""

import sys
import os

# Add the project root to Python path
project_root = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, project_root)

def test_working_v2():
    """Test the working V2 version."""
    print("Testing working V2 version...")
    
    try:
        # Import the working V2 main window
        from src.gui.v2_main_window_working import main
        
        print("✓ Working V2 version imported successfully")
        print("Starting working V2 version...")
        
        # Run the working version
        return main()
        
    except Exception as e:
        print(f"✗ Error testing working V2 version: {e}")
        import traceback
        traceback.print_exc()
        return 1

if __name__ == "__main__":
    print("=== Testing Working V2 Version ===")
    result = test_working_v2()
    print(f"\nWorking V2 version test completed with result: {result}") 