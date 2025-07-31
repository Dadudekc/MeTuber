"""
Cartoon Effect Plugin Registration

This module registers the cartoon effect plugin with the plugin system.
"""

from .effect import CartoonEffectPlugin
from .ui import CartoonEffectUI

def register_plugin(registry):
    """Register the cartoon effect plugin."""
    plugin = CartoonEffectPlugin()
    ui = CartoonEffectUI(plugin)
    registry.register_plugin(plugin, ui)
    return plugin 