"""
Blur Effect Plugin Registration

This module registers the blur effect plugin with the plugin system.
"""

from .effect import BlurEffectPlugin
from .ui import BlurEffectUI

def register_plugin(registry):
    """Register the blur effect plugin."""
    plugin = BlurEffectPlugin()
    ui = BlurEffectUI(plugin)
    registry.register_plugin(plugin, ui)
    return plugin 