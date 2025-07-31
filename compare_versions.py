#!/usr/bin/env python3
"""
Compare different versions of the application
"""

import os
import sys

def show_version_options():
    """Show the different version options available."""
    print("=== Available Versions ===")
    print()
    print("1. ORIGINAL VERSION (src/main.py)")
    print("   - Simple, straightforward implementation")
    print("   - Direct camera access")
    print("   - Basic UI with working preview")
    print("   - Command: python src/main.py")
    print()
    print("2. V2 VERSION (src/v2_main.py)")
    print("   - Complex modular architecture")
    print("   - Performance optimizations")
    print("   - Advanced UI with multiple docks")
    print("   - Command: python src/v2_main.py")
    print()
    print("3. SIMPLE TEST VERSION")
    print("   - Direct camera test")
    print("   - Command: python simple_camera_test.py")
    print()
    print("=== Recommendation ===")
    print("Try the ORIGINAL VERSION first - it's simpler and more likely to work!")
    print("Command: python src/main.py")

def test_original_version():
    """Test the original version."""
    print("\n=== Testing Original Version ===")
    try:
        from src.main import main
        print("✓ Original version imported successfully")
        print("Starting original version...")
        return main()
    except Exception as e:
        print(f"✗ Error with original version: {e}")
        return 1

if __name__ == "__main__":
    show_version_options()
    
    print("\n" + "="*50)
    print("Would you like to test the original version? (y/n)")
    response = input().lower()
    
    if response == 'y':
        test_original_version()
    else:
        print("You can test the versions manually:")
        print("- Original: python src/main.py")
        print("- V2: python src/v2_main.py")
        print("- Camera test: python simple_camera_test.py") 