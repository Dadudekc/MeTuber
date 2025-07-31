"""
Brightness Effect Plugin Registration

This module registers the brightness effect plugin with the plugin system.
"""

from .effect import BrightnessEffectPlugin
from .ui import BrightnessEffectUI

def register_plugin(registry):
    """Register the brightness effect plugin."""
    plugin = BrightnessEffectPlugin()
    ui = BrightnessEffectUI(plugin)
    registry.register_plugin(plugin, ui)
    return plugin 