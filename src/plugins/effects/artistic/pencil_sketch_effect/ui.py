"""
Pencil Sketch Effect UI

UI component for the pencil sketch effect plugin with dynamic dependencies.
"""

from src.plugins.plugin_base import EffectUI
from .effect import PencilSketchEffectPlugin

class PencilSketchEffectUI(EffectUI):
    """UI for Pencil Sketch Effect Plugin."""
    
    def __init__(self, plugin: PencilSketchEffectPlugin):
        super().__init__(plugin)
        
        # Setup dynamic dependencies for show/hide logic
        self.setup_dependencies()
    
    def setup_dependencies(self):
        """Setup dynamic parameter dependencies."""
        # Show texture strength only when paper texture is enabled
        self.add_dependency("paper_texture", "texture_strength", {
            "type": "is_true"
        })
        
        # Show line thickness only when blur intensity is high enough
        self.add_dependency("blur_intensity", "line_thickness", {
            "type": "greater_than", "value": 10
        }) 