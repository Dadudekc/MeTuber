"""
Edge Detection Effect UI

UI component for the edge detection effect plugin with dynamic dependencies.
"""

from src.plugins.plugin_base import EffectUI
from .effect import EdgeDetectionEffectPlugin

class EdgeDetectionEffectUI(EffectUI):
    """UI for Edge Detection Effect Plugin."""
    
    def __init__(self, plugin: EdgeDetectionEffectPlugin):
        super().__init__(plugin)
        
        # Setup dynamic dependencies for show/hide logic
        self.setup_dependencies()
    
    def setup_dependencies(self):
        """Setup dynamic parameter dependencies."""
        # Show thresholds only for Canny algorithm
        self.add_dependency("algorithm", "threshold1", {
            "type": "equals", "value": "Canny"
        })
        self.add_dependency("algorithm", "threshold2", {
            "type": "equals", "value": "Canny"
        })
        
        # Show blur strength only when blur preprocessing is enabled
        self.add_dependency("blur_preprocessing", "blur_strength", {
            "type": "is_true"
        })
        
        # Show line thickness only when not using extreme settings
        self.add_dependency("threshold1", "line_thickness", {
            "type": "less_than", "value": 300
        })
        
        # Show invert edges only for certain background colors
        self.add_dependency("background_color", "invert_edges", {
            "type": "not_equals", "value": "Gray"
        }) 