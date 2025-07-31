"""
Neural Style Effect UI

UI component for the neural style effect plugin with dynamic dependencies.
"""

from src.plugins.plugin_base import EffectUI
from .effect import NeuralStyleEffectPlugin

class NeuralStyleEffectUI(EffectUI):
    """UI for Neural Style Effect Plugin."""
    
    def __init__(self, plugin: NeuralStyleEffectPlugin):
        super().__init__(plugin)
        
        # Setup dynamic dependencies for show/hide logic
        self.setup_dependencies()
    
    def setup_dependencies(self):
        """Setup dynamic parameter dependencies."""
        # Show brush stroke size only for certain styles
        self.add_dependency("artistic_style", "brush_stroke_size", {
            "type": "contains", "value": "Van Gogh"
        })
        self.add_dependency("artistic_style", "brush_stroke_size", {
            "type": "contains", "value": "Oil Painting"
        })
        
        # Show saturation boost only for non-monochrome palettes
        self.add_dependency("color_palette", "saturation_boost", {
            "type": "not_equals", "value": "Monochrome"
        })
        
        # Show AI quality only when AI enhancement is enabled
        self.add_dependency("enable_ai_enhancement", "ai_quality", {
            "type": "is_true"
        })
        
        # Show texture strength only when detail preservation is low
        self.add_dependency("detail_preservation", "texture_strength", {
            "type": "less_than", "value": 0.9
        }) 