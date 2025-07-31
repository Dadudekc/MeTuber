"""
Neural Style Effect Plugin Registration

This module registers the neural style effect plugin with the plugin system.
"""

from .effect import NeuralStyleEffectPlugin
from .ui import NeuralStyleEffectUI

def register_plugin(registry):
    """Register the neural style effect plugin."""
    plugin = NeuralStyleEffectPlugin()
    ui = NeuralStyleEffectUI(plugin)
    registry.register_plugin(plugin, ui)
    return plugin 