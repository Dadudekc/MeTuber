"""
Brightness & Contrast Effect Plugin Registration

This module registers the brightness/contrast effect plugin with the plugin system.
"""

from .effect import BrightnessContrastEffectPlugin
from .ui import BrightnessContrastEffectUI

def register_plugin(registry):
    """Register the brightness/contrast effect plugin."""
    plugin = BrightnessContrastEffectPlugin()
    ui = BrightnessContrastEffectUI(plugin)
    registry.register_plugin(plugin, ui)
    return plugin 