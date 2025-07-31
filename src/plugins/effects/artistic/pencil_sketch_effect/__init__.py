"""
Pencil Sketch Effect Plugin Registration

This module registers the pencil sketch effect plugin with the plugin system.
"""

from .effect import PencilSketchEffectPlugin
from .ui import PencilSketchEffectUI

def register_plugin(registry):
    """Register the pencil sketch effect plugin."""
    plugin = PencilSketchEffectPlugin()
    ui = PencilSketchEffectUI(plugin)
    registry.register_plugin(plugin, ui)
    return plugin 