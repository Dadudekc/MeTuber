"""
Plugin System for MeTuber Effects

This module provides a comprehensive plugin architecture for creating
and managing video effects with custom UI components and parameters.
"""

from .plugin_base import EffectPlugin, EffectUI, EffectParameter
from .plugin_registry import PluginRegistry
from .plugin_loader import PluginLoader
from .plugin_manager import PluginManager

__all__ = [
    'EffectPlugin',
    'EffectUI', 
    'EffectParameter',
    'PluginRegistry',
    'PluginLoader',
    'PluginManager'
]

__version__ = "1.0.0" 