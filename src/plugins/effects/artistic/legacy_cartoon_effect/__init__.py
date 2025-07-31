"""
Legacy Cartoon Effect Plugin Registration

This module registers the legacy cartoon effect plugin with the plugin system.
"""

from .effect import LegacyCartoonEffectPlugin
from .ui import LegacyCartoonEffectUI

def register_plugin(registry):
    """Register the legacy cartoon effect plugin."""
    plugin = LegacyCartoonEffectPlugin()
    ui = LegacyCartoonEffectUI(plugin)
    registry.register_plugin(plugin, ui)
    return plugin 