"""
Advanced Cartoon Effect Plugin Registration

This module registers the advanced cartoon effect plugin with the plugin system.
"""

from .effect import AdvancedCartoonEffectPlugin
from .ui import AdvancedCartoonEffectUI

def register_plugin(registry):
    """Register the advanced cartoon effect plugin."""
    plugin = AdvancedCartoonEffectPlugin()
    ui = AdvancedCartoonEffectUI(plugin)
    registry.register_plugin(plugin, ui)
    return plugin 