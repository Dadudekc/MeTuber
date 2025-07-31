"""
Blur Effect UI Component

Custom UI components for the blur effect plugin with automatic styling.
"""

import sys
import os

# Add the project root to Python path for imports
project_root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))))
if project_root not in sys.path:
    sys.path.insert(0, project_root)

from PyQt5.QtWidgets import QWidget, QVBoxLayout, QGroupBox
from src.plugins.plugin_base import EffectUI

class BlurEffectUI(EffectUI):
    """UI component for the blur effect plugin with automatic styling."""
    
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
        
        # Create group box for blur controls
        group_box = QGroupBox("Blur Controls")
        group_layout = QVBoxLayout()
        
        # Blur Type Combo Box (using styled base class method)
        blur_type_control = self.create_combo_control(
            name="blur_type",
            options=["Gaussian", "Box", "Median"],
            default="Gaussian",
            label="Blur Type:"
        )
        group_layout.addWidget(blur_type_control)
        
        # Blur Strength Slider (using styled base class method)
        blur_strength_control = self.create_slider_control(
            name="blur_strength",
            min_val=1,
            max_val=50,
            default=5,
            label="Blur Strength:"
        )
        group_layout.addWidget(blur_strength_control)
        
        group_box.setLayout(group_layout)
        layout.addWidget(group_box)
        
        # Add some spacing
        layout.addStretch()
        
        widget.setLayout(layout)
        return widget 