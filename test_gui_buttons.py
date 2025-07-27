#!/usr/bin/env python3
"""
Simple GUI Button Test Runner
Quick test to verify all buttons are functional
"""

import sys
import os

# Add the src directory to the path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

def run_gui_tests():
    """Run the comprehensive GUI tests."""
    print("Starting GUI Button Tests...")
    print("Following Single Responsibility Principle (SRP)")
    
    try:
        # Run the master test runner
        from tests.gui.run_all_gui_tests import MasterGUITestRunner
        runner = MasterGUITestRunner()
        success = runner.run_all_tests()
        
        if success:
            print("\nALL GUI TESTS PASSED!")
            print("All buttons are functional!")
            print("Application is ready for production!")
        else:
            print("\nSome GUI tests failed.")
            print("Please review the test results above.")
            
        return success
        
    except ImportError as e:
        print(f"Import error: {e}")
        print("Make sure you're running from the project root directory")
        return False
    except Exception as e:
        print(f"Test execution failed: {e}")
        return False

if __name__ == "__main__":
    success = run_gui_tests()
    sys.exit(0 if success else 1) 