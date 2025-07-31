#!/usr/bin/env python3
"""
Summary of all available versions
"""

import os
import sys

def show_all_versions():
    """Show all available versions."""
    print("=== ALL AVAILABLE VERSIONS ===")
    print()
    print("🎯 RECOMMENDED ORDER TO TEST:")
    print()
    print("1. 🚀 WORKING V2 VERSION (NEW!)")
    print("   - Based on original backup with working camera")
    print("   - Direct camera access (no complex async)")
    print("   - Professional UI with working preview")
    print("   - Command: python test_working_v2.py")
    print()
    print("2. 📱 ORIGINAL VERSION")
    print("   - Simple, straightforward implementation")
    print("   - Direct camera access")
    print("   - Basic UI with working preview")
    print("   - Command: python src/main.py")
    print()
    print("3. 🔧 CURRENT V2 VERSION (with our fixes)")
    print("   - Complex modular architecture")
    print("   - Performance optimizations")
    print("   - Advanced UI with multiple docks")
    print("   - Command: python src/v2_main.py")
    print()
    print("4. 🧪 TEST VERSIONS")
    print("   - Camera test: python simple_camera_test.py")
    print("   - Frame flow test: python test_frame_flow.py")
    print()
    print("=== RECOMMENDATION ===")
    print("Try the WORKING V2 VERSION first - it combines the best of both worlds!")
    print("Command: python test_working_v2.py")
    print()
    print("=== WHAT CHANGED ===")
    print("The working V2 version:")
    print("- Uses direct cv2.VideoCapture instead of complex WebcamService")
    print("- Has simpler, more reliable camera initialization")
    print("- Maintains the professional V2 UI")
    print("- Should show camera preview immediately")

if __name__ == "__main__":
    show_all_versions()
    
    print("\n" + "="*50)
    print("Would you like to test the working V2 version? (y/n)")
    response = input().lower()
    
    if response == 'y':
        print("\nStarting working V2 version...")
        try:
            from test_working_v2 import test_working_v2
            result = test_working_v2()
            print(f"Working V2 version completed with result: {result}")
        except Exception as e:
            print(f"Error: {e}")
    else:
        print("\nYou can test the versions manually:")
        print("- Working V2: python test_working_v2.py")
        print("- Original: python src/main.py")
        print("- Current V2: python src/v2_main.py")
        print("- Camera test: python simple_camera_test.py") 