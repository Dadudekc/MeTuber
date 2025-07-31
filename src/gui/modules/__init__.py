"""
GUI Modules Package for Dreamscape V2 Professional

This package contains modularized components of the main window,
organized by functionality while preserving the exact UI appearance.
"""

from .ui_components import UIComponents
from .parameter_manager import ParameterManager
from .effect_manager import EffectManager
from .preview_manager import PreviewManager
from .webcam_manager import WebcamManager
from .style_manager import StyleManager
from .widget_manager import WidgetManager

__all__ = [
    'UIComponents',
    'ParameterManager', 
    'EffectManager',
    'PreviewManager',
    'WebcamManager',
    'StyleManager',
    'WidgetManager'
] 