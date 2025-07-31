"""
Cartoon Effect UI Component

Custom UI components for the cartoon effect plugin with automatic styling.
"""

import sys
import os

# Add the project root to Python path for imports
project_root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))))
if project_root not in sys.path:
    sys.path.insert(0, project_root)

from PyQt5.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLabel, QSlider, QGroupBox
from PyQt5.QtCore import Qt
from src.plugins.plugin_base import EffectUI

class CartoonEffectUI(EffectUI):
    """UI component for the cartoon effect plugin with automatic styling."""
    
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
        
        # Create group box for cartoon effect controls
        group_box = QGroupBox("Cartoon Effect Controls")
        group_layout = QVBoxLayout()
        
        # Edge Strength Slider (using styled base class method)
        edge_control = self.create_slider_control(
            name="edge_strength",
            min_val=0,
            max_val=200,  # 0.0 to 2.0 * 100
            default=100,   # Default 1.0
            label="Edge Strength:"
        )
        group_layout.addWidget(edge_control)
        
        # Color Reduction Slider (using styled base class method)
        color_control = self.create_slider_control(
            name="color_reduction",
            min_val=2,
            max_val=32,
            default=8,
            label="Color Reduction:"
        )
        group_layout.addWidget(color_control)
        
        # Blur Strength Slider (using styled base class method)
        blur_control = self.create_slider_control(
            name="blur_strength",
            min_val=1,
            max_val=15,
            default=5,
            label="Blur Strength:"
        )
        group_layout.addWidget(blur_control)
        
        # Override the slider change handlers to convert values properly
        self.widgets['edge_strength_slider'].valueChanged.disconnect()
        self.widgets['edge_strength_slider'].valueChanged.connect(self._on_edge_strength_changed)
        
        self.widgets['color_reduction_slider'].valueChanged.disconnect()
        self.widgets['color_reduction_slider'].valueChanged.connect(self._on_color_reduction_changed)
        
        self.widgets['blur_strength_slider'].valueChanged.disconnect()
        self.widgets['blur_strength_slider'].valueChanged.connect(self._on_blur_strength_changed)
        
        group_box.setLayout(group_layout)
        layout.addWidget(group_box)
        
        # Add some spacing
        layout.addStretch()
        
        widget.setLayout(layout)
        return widget
    
    def _on_edge_strength_changed(self, value):
        """Handle edge strength slider change with proper value conversion."""
        float_value = value / 100.0
        self.widgets['edge_strength_label'].setText(f"{float_value:.2f}")
        self.update_parameter('edge_strength', float_value)
    
    def _on_color_reduction_changed(self, value):
        """Handle color reduction slider change."""
        self.widgets['color_reduction_label'].setText(str(value))
        self.update_parameter('color_reduction', value)
    
    def _on_blur_strength_changed(self, value):
        """Handle blur strength slider change."""
        self.widgets['blur_strength_label'].setText(str(value))
        self.update_parameter('blur_strength', value)
    
    def update_parameter_widget(self, name, value):
        """Update a parameter widget with a new value."""
        if name == 'edge_strength':
            int_value = int(value * 100)
            self.widgets['edge_strength_slider'].setValue(int_value)
            self.widgets['edge_strength_label'].setText(f"{value:.2f}")
        elif name == 'color_reduction':
            self.widgets['color_reduction_slider'].setValue(value)
            self.widgets['color_reduction_label'].setText(str(value))
        elif name == 'blur_strength':
            self.widgets['blur_strength_slider'].setValue(value)
            self.widgets['blur_strength_label'].setText(str(value)) 