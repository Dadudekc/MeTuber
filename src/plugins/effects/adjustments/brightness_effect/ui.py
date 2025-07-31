"""
Brightness Effect UI Component

Custom UI components for the brightness effect plugin with automatic styling.
"""

import sys
import os

# Add the project root to Python path for imports
project_root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))))
if project_root not in sys.path:
    sys.path.insert(0, project_root)

from PyQt5.QtWidgets import QWidget, QVBoxLayout, QGroupBox
from src.plugins.plugin_base import EffectUI

class BrightnessEffectUI(EffectUI):
    """UI component for the brightness effect plugin with automatic styling."""
    
    def __init__(self, effect_plugin):
        super().__init__(effect_plugin)
    
    def create_ui_components(self):
        """
        Create the UI components for this effect with beautiful styling.
        
        Returns:
            QWidget containing the effect's UI components
        """
        # Create main widget
        widget = QWidget()
        layout = QVBoxLayout()
        
        # Create group box for brightness controls
        group_box = QGroupBox("Brightness Controls")
        group_layout = QVBoxLayout()
        
        # Brightness Slider (using styled base class method)
        brightness_control = self.create_slider_control(
            name="brightness",
            min_val=-100,
            max_val=100,
            default=0,
            label="Brightness:"
        )
        group_layout.addWidget(brightness_control)
        
        group_box.setLayout(group_layout)
        layout.addWidget(group_box)
        
        # Add some spacing
        layout.addStretch()
        
        widget.setLayout(layout)
        return widget 