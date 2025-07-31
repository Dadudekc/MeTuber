"""
Legacy Cartoon Effect UI

UI component for the legacy cartoon effect plugin.
"""

from src.plugins.plugin_base import EffectUI
from .effect import LegacyCartoonEffectPlugin

class LegacyCartoonEffectUI(EffectUI):
    """UI for Legacy Cartoon Effect Plugin."""
    
    def __init__(self, plugin: LegacyCartoonEffectPlugin):
        super().__init__(plugin)
        
        # Setup dynamic dependencies for show/hide logic
        self.setup_dependencies()
    
    def setup_dependencies(self):
        """Setup dynamic parameter dependencies."""
        # Show edge detection parameters only when thresholds are high enough
        self.add_dependency("canny_threshold1", "canny_threshold2", {"type": "greater_than", "value": 50}) 