"""
Watercolor Effect UI

UI component for the watercolor effect plugin with dynamic dependencies.
"""

from src.plugins.plugin_base import EffectUI
from .effect import WatercolorEffectPlugin

class WatercolorEffectUI(EffectUI):
    """UI for Watercolor Effect Plugin."""
    
    def __init__(self, plugin: WatercolorEffectPlugin):
        super().__init__(plugin)
        
        # Setup dynamic dependencies for show/hide logic
        self.setup_dependencies()
    
    def setup_dependencies(self):
        """Setup dynamic parameter dependencies."""
        # Show texture strength only when texture overlay is enabled
        self.add_dependency("texture_overlay", "texture_strength", {
            "type": "is_true"
        })
        
        # Show edge preservation only when sigma_s is high enough
        self.add_dependency("sigma_s", "edge_preservation", {
            "type": "greater_than", "value": 30
        })
        
        # Show color intensity only when sigma_r is not too low
        self.add_dependency("sigma_r", "color_intensity", {
            "type": "greater_than", "value": 0.3
        }) 