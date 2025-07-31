"""
Edge Detection Effect Plugin Registration

This module registers the edge detection effect plugin with the plugin system.
"""

from .effect import EdgeDetectionEffectPlugin
from .ui import EdgeDetectionEffectUI

def register_plugin(registry):
    """Register the edge detection effect plugin."""
    plugin = EdgeDetectionEffectPlugin()
    ui = EdgeDetectionEffectUI(plugin)
    registry.register_plugin(plugin, ui)
    return plugin 