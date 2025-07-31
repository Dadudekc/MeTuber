"""
Advanced Cartoon Effect UI

Demonstrates advanced UI features:
- Dynamic show/hide logic for dependent parameters
- Professional styling with dark theme
- All parameter types (sliders, dropdowns, checkboxes, file pickers, color pickers)
- Grouped parameters by category
"""

from PyQt5.QtWidgets import QVBoxLayout
from src.plugins.plugin_base import EffectUI
from .effect import AdvancedCartoonEffectPlugin

class AdvancedCartoonEffectUI(EffectUI):
    """Advanced cartoon effect UI with dynamic dependencies and professional styling."""
    
    def __init__(self, plugin: AdvancedCartoonEffectPlugin):
        super().__init__(plugin)
        
        # Setup dynamic dependencies for show/hide logic
        self.setup_dependencies()
    
    def setup_dependencies(self):
        """Setup dynamic parameter dependencies."""
        # Show texture file picker only when texture is enabled
        self.add_dependency("enable_texture", "texture_file", {"type": "is_true"})
        self.add_dependency("enable_texture", "texture_opacity", {"type": "is_true"})
        
        # Show custom color picker only when color mode is "Custom"
        self.add_dependency("color_mode", "custom_color", {"type": "equals", "value": "Custom"})
        
        # Show AI parameters only when AI edge detection is enabled
        self.add_dependency("ai_edge_detection", "edge_sensitivity", {"type": "is_true"})
        self.add_dependency("ai_edge_detection", "edge_thickness", {"type": "is_true"})
        
        # Show color saturation only when not in monochrome mode
        self.add_dependency("color_mode", "color_saturation", {"type": "not_equals", "value": "Monochrome"})
    
    def init_ui(self):
        """Initialize the UI with custom layout."""
        super().init_ui()
        
        # Add custom styling for this specific effect
        self.setObjectName("advancedCartoonEffectUI")
        self.setStyleSheet(self.styleSheet() + """
            #advancedCartoonEffectUI {
                background-color: #2a2a2a;
                border: 1px solid #444;
                border-radius: 6px;
                padding: 8px;
            }
            
            #advancedCartoonEffectUI QGroupBox {
                background-color: #333;
                border: 1px solid #555;
                border-radius: 4px;
                margin-top: 10px;
                padding-top: 10px;
            }
            
            #advancedCartoonEffectUI QGroupBox::title {
                color: #0096ff;
                font-weight: bold;
                font-size: 10pt;
            }
        """) 