#!/usr/bin/env python3
"""
Dependency Manager for MeTuber webcam filter application.
This module provides graceful handling of missing dependencies and feature detection.
"""

import importlib
import logging
from typing import Dict, List, Tuple, Optional
import sys

class DependencyManager:
    """
    Manages dependencies and provides graceful fallbacks for missing packages.
    """
    
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self._available_packages = {}
        self._check_dependencies()
    
    def _check_dependencies(self):
        """Check which packages are available."""
        packages_to_check = {
            # Core packages
            'PyQt5': 'PyQt5',
            'cv2': 'opencv-python',
            'numpy': 'numpy',
            'pyvirtualcam': 'pyvirtualcam',
            
            # Optional packages
            'av': 'av',
            'PIL': 'pillow',
            'skimage': 'scikit-image',
            'sklearn': 'scikit-learn',
            'pyaudio': 'pyaudio',
            'whisper': 'whisper',
            'speech_recognition': 'speech-recognition'
        }
        
        for package_name, pip_name in packages_to_check.items():
            try:
                importlib.import_module(package_name)
                self._available_packages[package_name] = True
                self.logger.debug(f"Package {package_name} is available")
            except ImportError:
                self._available_packages[package_name] = False
                self.logger.debug(f"Package {package_name} is not available")
    
    def is_available(self, package_name: str) -> bool:
        """Check if a specific package is available."""
        return self._available_packages.get(package_name, False)
    
    def get_missing_core_deps(self) -> List[str]:
        """Get list of missing core dependencies."""
        core_deps = ['PyQt5', 'cv2', 'numpy', 'pyvirtualcam']
        missing = []
        for dep in core_deps:
            if not self.is_available(dep):
                missing.append(dep)
        return missing
    
    def get_missing_optional_deps(self) -> List[str]:
        """Get list of missing optional dependencies."""
        optional_deps = ['av', 'PIL', 'skimage', 'sklearn', 'pyaudio', 'whisper', 'speech_recognition']
        missing = []
        for dep in optional_deps:
            if not self.is_available(dep):
                missing.append(dep)
        return missing
    
    def can_run_basic(self) -> bool:
        """Check if the basic application can run."""
        return len(self.get_missing_core_deps()) == 0
    
    def can_run_advanced(self) -> bool:
        """Check if advanced features are available."""
        return self.is_available('av') and self.is_available('skimage')
    
    def can_run_audio(self) -> bool:
        """Check if audio features are available."""
        return self.is_available('pyaudio') and self.is_available('whisper')
    
    def get_feature_status(self) -> Dict[str, bool]:
        """Get status of all features."""
        return {
            'basic_webcam': self.can_run_basic(),
            'advanced_video': self.can_run_advanced(),
            'audio_captioning': self.can_run_audio(),
            'virtual_camera': self.is_available('pyvirtualcam'),
            'image_processing': self.is_available('PIL') or self.is_available('skimage'),
            'machine_learning': self.is_available('sklearn')
        }
    
    def get_installation_commands(self) -> Dict[str, str]:
        """Get pip install commands for missing packages."""
        missing_core = self.get_missing_core_deps()
        missing_optional = self.get_missing_optional_deps()
        
        commands = {}
        
        if missing_core:
            commands['core'] = f"pip install {' '.join(missing_core)}"
        
        if missing_optional:
            commands['optional'] = f"pip install {' '.join(missing_optional)}"
        
        return commands
    
    def log_dependency_status(self):
        """Log the current dependency status."""
        self.logger.info("=== Dependency Status ===")
        
        # Core dependencies
        missing_core = self.get_missing_core_deps()
        if missing_core:
            self.logger.error(f"Missing core dependencies: {', '.join(missing_core)}")
        else:
            self.logger.info("✅ All core dependencies are available")
        
        # Optional dependencies
        missing_optional = self.get_missing_optional_deps()
        if missing_optional:
            self.logger.warning(f"Missing optional dependencies: {', '.join(missing_optional)}")
        else:
            self.logger.info("✅ All optional dependencies are available")
        
        # Feature status
        features = self.get_feature_status()
        self.logger.info("=== Feature Status ===")
        for feature, available in features.items():
            status = "✅" if available else "❌"
            self.logger.info(f"{status} {feature}")
    
    def get_import_safe(self, package_name: str, fallback=None):
        """
        Safely import a package with fallback.
        
        Args:
            package_name: Name of the package to import
            fallback: Fallback value if import fails
            
        Returns:
            The imported module or fallback value
        """
        if self.is_available(package_name):
            try:
                return importlib.import_module(package_name)
            except ImportError:
                self.logger.warning(f"Failed to import {package_name} despite availability check")
                return fallback
        else:
            self.logger.debug(f"Package {package_name} not available, using fallback")
            return fallback

# Global instance
dependency_manager = DependencyManager()

def get_dependency_manager() -> DependencyManager:
    """Get the global dependency manager instance."""
    return dependency_manager

# Convenience functions
def is_package_available(package_name: str) -> bool:
    """Check if a package is available."""
    return dependency_manager.is_available(package_name)

def can_run_basic_app() -> bool:
    """Check if basic application can run."""
    return dependency_manager.can_run_basic()

def get_feature_status() -> Dict[str, bool]:
    """Get status of all features."""
    return dependency_manager.get_feature_status()


