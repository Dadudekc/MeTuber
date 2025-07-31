"""
Watercolor Effect Plugin Registration

This module registers the watercolor effect plugin with the plugin system.
"""

from .effect import WatercolorEffectPlugin
from .ui import WatercolorEffectUI

def register_plugin(registry):
    """Register the watercolor effect plugin."""
    plugin = WatercolorEffectPlugin()
    ui = WatercolorEffectUI(plugin)
    registry.register_plugin(plugin, ui)
    return plugin 