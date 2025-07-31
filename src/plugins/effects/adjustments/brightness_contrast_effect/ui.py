"""
Brightness & Contrast Effect UI

UI component for the brightness/contrast effect plugin with dynamic dependencies.
"""

from src.plugins.plugin_base import EffectUI
from .effect import BrightnessContrastEffectPlugin

class BrightnessContrastEffectUI(EffectUI):
    """UI for Brightness & Contrast Effect Plugin."""
    
    def __init__(self, plugin: BrightnessContrastEffectPlugin):
        super().__init__(plugin)
        
        # Setup dynamic dependencies for show/hide logic
        self.setup_dependencies()
    
    def setup_dependencies(self):
        """Setup dynamic parameter dependencies."""
        # Show advanced options only when auto adjust is disabled
        self.add_dependency("auto_adjust", "gamma", {
            "type": "is_false"
        })
        self.add_dependency("auto_adjust", "preserve_highlights", {
            "type": "is_false"
        })
        self.add_dependency("auto_adjust", "preserve_shadows", {
            "type": "is_false"
        })
        
        # Show preserve options only when contrast is not extreme
        self.add_dependency("contrast", "preserve_highlights", {
            "type": "less_than", "value": 2.5
        })
        self.add_dependency("contrast", "preserve_shadows", {
            "type": "greater_than", "value": 0.7
        }) 