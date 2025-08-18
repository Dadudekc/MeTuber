#!/usr/bin/env python3
"""
Dependency checker for MeTuber webcam filter application.
This script checks if all required dependencies are installed and provides helpful error messages.
"""

import sys
import importlib
import subprocess
from typing import Dict, List, Tuple

# Core dependencies that are absolutely required
CORE_DEPS = {
    'PyQt5': 'PyQt5',
    'cv2': 'opencv-python',
    'numpy': 'numpy',
    'pyvirtualcam': 'pyvirtualcam'
}

# Optional dependencies that provide additional features
OPTIONAL_DEPS = {
    'av': 'av',  # PyAV for advanced video processing
    'PIL': 'pillow',  # Pillow for image processing
    'skimage': 'scikit-image',  # Advanced image processing
    'sklearn': 'scikit-learn',  # Machine learning features
    'pyaudio': 'pyaudio',  # Audio processing
    'whisper': 'whisper',  # Speech recognition
    'speech_recognition': 'speech-recognition'  # Speech recognition
}

def check_package(package_name: str, pip_name: str = None) -> Tuple[bool, str]:
    """
    Check if a package is available for import.
    
    Args:
        package_name: The name to use in import statement
        pip_name: The name to use with pip install (if different)
    
    Returns:
        Tuple of (is_available, error_message)
    """
    try:
        importlib.import_module(package_name)
        return True, ""
    except ImportError as e:
        pip_package = pip_name or package_name
        return False, f"Package '{pip_package}' not found. Install with: pip install {pip_package}"

def check_system_requirements() -> List[str]:
    """Check system-level requirements."""
    issues = []
    
    # Check Python version
    if sys.version_info < (3, 8):
        issues.append(f"Python 3.8+ required, found {sys.version}")
    
    # Check if we're on Windows (for virtual camera support)
    if sys.platform == "win32":
        try:
            # Check if OBS Virtual Camera is available
            result = subprocess.run(['obs-virtualcam', '--version'], 
                                  capture_output=True, text=True, timeout=5)
            if result.returncode != 0:
                issues.append("OBS Virtual Camera not found. Install OBS Studio for virtual camera support.")
        except FileNotFoundError:
            issues.append("OBS Virtual Camera not found. Install OBS Studio for virtual camera support.")
    
    return issues

def main():
    """Main dependency checking function."""
    print("MeTuber Dependency Checker")
    print("=" * 40)
    
    # Check system requirements
    system_issues = check_system_requirements()
    if system_issues:
        print("\n❌ System Requirements Issues:")
        for issue in system_issues:
            print(f"  - {issue}")
    
    # Check core dependencies
    print("\n🔍 Checking Core Dependencies:")
    core_issues = []
    for package, pip_name in CORE_DEPS.items():
        available, error = check_package(package, pip_name)
        if available:
            print(f"  ✅ {package}")
        else:
            print(f"  ❌ {package}: {error}")
            core_issues.append(error)
    
    # Check optional dependencies
    print("\n🔍 Checking Optional Dependencies:")
    optional_issues = []
    for package, pip_name in OPTIONAL_DEPS.items():
        available, error = check_package(package, pip_name)
        if available:
            print(f"  ✅ {package}")
        else:
            print(f"  ⚠️  {package}: {error}")
            optional_issues.append(error)
    
    # Summary
    print("\n" + "=" * 40)
    if core_issues:
        print("❌ CRITICAL: Core dependencies missing!")
        print("The application cannot run without these packages.")
        print("\nInstall core dependencies with:")
        print("pip install -r requirements-core.txt")
        return False
    elif system_issues:
        print("⚠️  WARNING: System requirements not met.")
        print("Some features may not work properly.")
        return False
    else:
        print("✅ All core dependencies are available!")
        if optional_issues:
            print("⚠️  Some optional features may not be available.")
            print("Install optional dependencies with:")
            print("pip install -r requirements.txt")
        return True

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)


