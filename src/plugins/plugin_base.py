"""
Plugin Base Classes

Base classes for creating effects plugins with consistent styling.
"""

import logging
from abc import ABC, abstractmethod
from typing import Dict, Any, List, Optional
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QFormLayout, QLabel, QSlider, QComboBox, QSpinBox, QDoubleSpinBox, QGroupBox, QCheckBox, QPushButton
from PyQt5.QtCore import Qt, pyqtSignal
from PyQt5.QtGui import QPalette, QColor

class EffectPlugin(ABC):
    """Base class for all effect plugins."""
    
    def __init__(self, name: str, category: str, description: str = ""):
        self.name = name
        self.category = category
        self.description = description
        self.parameters = {}
        self.logger = logging.getLogger(f"Plugin.{name}")
        
        # Add required attributes for compatibility
        self.version = "1.0.0"
        self.author = "MeTuber Team"
        self.tags = []
        self.is_enabled = True
    
    @abstractmethod
    def apply(self, frame, parameters: Optional[Dict[str, Any]] = None):
        """Apply the effect to a frame."""
        pass
    
    def apply_effect(self, frame, parameters: Dict[str, Any]):
        """Legacy method for backward compatibility."""
        return self.apply(frame, parameters)
    
    def get_parameters(self) -> Dict[str, Any]:
        """Get current parameter values."""
        return self.parameters.copy()
    
    def set_parameters(self, parameters: Dict[str, Any]):
        """Set parameter values."""
        self.parameters.update(parameters)
    
    def get_metadata(self) -> Dict[str, Any]:
        """Get metadata about this effect."""
        return {
            'name': self.name,
            'description': self.description,
            'category': self.category,
            'version': self.version,
            'author': self.author,
            'tags': self.tags
        }
    
    def cleanup(self):
        """Clean up any resources used by this plugin."""
        # Default implementation - override in subclasses if needed
        pass
    
    def enable(self):
        """Enable this plugin."""
        self.is_enabled = True
    
    def disable(self):
        """Disable this plugin."""
        self.is_enabled = False

class EffectParameter:
    """Represents a parameter for an effect."""
    
    def __init__(self, name: str, param_type: str, default: Any, min_val: Any = None, max_val: Any = None, options: List[str] = None, description: str = ""):
        self.name = name
        self.type = param_type
        self.default = default
        self.min = min_val
        self.max = max_val
        self.options = options or []
        self.description = description

class EffectUI(QWidget):
    """
    Base class for effect UI components with professional styling and advanced controls.
    Supports all parameter types: sliders, dropdowns, checkboxes, file pickers, color pickers,
    grouped controls, and dynamic show/hide logic.
    """
    
    parameter_changed = pyqtSignal(str, object)  # parameter_name, value
    
    def __init__(self, plugin: EffectPlugin):
        super().__init__()
        self.plugin = plugin
        self.parameter_widgets = {}
        self.parameter_groups = {}
        self.dependent_parameters = {}  # Track parameter dependencies for show/hide logic
        
        # Apply professional styling
        self.apply_professional_styling()
        
        # Initialize UI
        self.init_ui()
    
    def init_ui(self):
        """Initialize the UI layout."""
        self.layout = QVBoxLayout(self)
        self.layout.setContentsMargins(8, 8, 8, 8)
        self.layout.setSpacing(6)
        
        # Create parameter controls
        self.create_parameter_controls()
    
    def create_parameter_controls(self):
        """Create controls for all plugin parameters."""
        # Group parameters by category if specified
        grouped_params = self.group_parameters()
        
        for group_name, params in grouped_params.items():
            if group_name == "General" and len(grouped_params) == 1:
                # No grouping needed
                for param in params:
                    self.create_parameter_widget(param)
            else:
                # Create group box
                group_box = self.create_group_box(group_name, params)
                self.layout.addWidget(group_box)
    
    def group_parameters(self):
        """Group parameters by category."""
        grouped = {}
        for param_name, param_def in self.plugin.parameters.items():
            category = param_def.get('category', 'General')
            if category not in grouped:
                grouped[category] = []
            # Add param_name to the param_def for reference
            param_def['name'] = param_name
            grouped[category].append(param_def)
        return grouped
    
    def create_group_box(self, title: str, params: list):
        """Create a group box for parameters."""
        group_box = QGroupBox(title)
        group_box.setObjectName("parameterGroup")
        
        layout = QFormLayout(group_box)
        layout.setSpacing(8)
        
        for param in params:
            widget = self.create_parameter_widget(param)
            if widget:
                label = QLabel(param.get('label', param['name']))
                label.setObjectName("parameterLabel")
                layout.addRow(label, widget)
        
        return group_box
    
    def create_parameter_widget(self, param: dict):
        """Create appropriate widget for parameter type."""
        param_type = param.get('type', 'int')
        param_name = param['name']
        
        if param_type == 'int':
            return self.create_slider_control(param)
        elif param_type == 'float':
            return self.create_float_control(param)
        elif param_type == 'bool':
            return self.create_checkbox_control(param)
        elif param_type == 'str' and 'options' in param:
            return self.create_combo_control(param)
        elif param_type == 'file':
            return self.create_file_picker_control(param)
        elif param_type == 'color':
            return self.create_color_picker_control(param)
        else:
            # Fallback to spinbox for unknown types
            return self.create_spin_control(param)
    
    def create_slider_control(self, param: dict):
        """Create a slider control for integer parameters."""
        slider = QSlider(Qt.Horizontal)
        slider.setMinimum(param.get('min', 0))
        slider.setMaximum(param.get('max', 100))
        slider.setValue(param.get('default', 0))
        slider.setTickPosition(QSlider.TicksBelow)
        slider.setTickInterval(param.get('step', 10))
        slider.setObjectName("parameterSlider")
        
        # Connect signal
        slider.valueChanged.connect(
            lambda value, name=param['name']: self.on_parameter_changed(name, value)
        )
        
        self.parameter_widgets[param['name']] = slider
        return slider
    
    def create_float_control(self, param: dict):
        """Create a float control (slider + spinbox)."""
        container = QWidget()
        layout = QHBoxLayout(container)
        layout.setContentsMargins(0, 0, 0, 0)
        
        # Slider
        slider = QSlider(Qt.Horizontal)
        slider.setMinimum(int(param.get('min', 0) * 100))
        slider.setMaximum(int(param.get('max', 1) * 100))
        slider.setValue(int(param.get('default', 0) * 100))
        slider.setObjectName("parameterSlider")
        
        # Spinbox
        spinbox = QDoubleSpinBox()
        spinbox.setMinimum(param.get('min', 0))
        spinbox.setMaximum(param.get('max', 1))
        spinbox.setValue(param.get('default', 0))
        spinbox.setDecimals(param.get('decimals', 2))
        spinbox.setSingleStep(param.get('step', 0.1))
        spinbox.setObjectName("parameterSpinBox")
        
        # Connect signals
        slider.valueChanged.connect(
            lambda value, sb=spinbox: sb.setValue(value / 100.0)
        )
        spinbox.valueChanged.connect(
            lambda value, s=slider: s.setValue(int(value * 100))
        )
        spinbox.valueChanged.connect(
            lambda value, name=param['name']: self.on_parameter_changed(name, value)
        )
        
        layout.addWidget(slider)
        layout.addWidget(spinbox)
        
        self.parameter_widgets[param['name']] = (slider, spinbox)
        return container
    
    def create_checkbox_control(self, param: dict):
        """Create a checkbox control."""
        checkbox = QCheckBox()
        checkbox.setChecked(param.get('default', False))
        checkbox.setObjectName("parameterCheckBox")
        
        # Connect signal
        checkbox.toggled.connect(
            lambda checked, name=param['name']: self.on_parameter_changed(name, checked)
        )
        
        self.parameter_widgets[param['name']] = checkbox
        return checkbox
    
    def create_combo_control(self, param: dict):
        """Create a combo box control."""
        combo = QComboBox()
        combo.addItems(param['options'])
        combo.setCurrentText(param.get('default', param['options'][0]))
        combo.setObjectName("parameterComboBox")
        
        # Connect signal
        combo.currentTextChanged.connect(
            lambda text, name=param['name']: self.on_parameter_changed(name, text)
        )
        
        self.parameter_widgets[param['name']] = combo
        return combo
    
    def create_file_picker_control(self, param: dict):
        """Create a file picker control."""
        container = QWidget()
        layout = QHBoxLayout(container)
        layout.setContentsMargins(0, 0, 0, 0)
        
        # File path display
        path_label = QLabel(param.get('default', ''))
        path_label.setObjectName("filePathLabel")
        path_label.setStyleSheet("color: #888; font-style: italic;")
        
        # Browse button
        browse_btn = QPushButton("Browse...")
        browse_btn.setObjectName("browseButton")
        browse_btn.clicked.connect(
            lambda: self.browse_file(param, path_label)
        )
        
        layout.addWidget(path_label)
        layout.addWidget(browse_btn)
        
        self.parameter_widgets[param['name']] = (path_label, browse_btn)
        return container
    
    def create_color_picker_control(self, param: dict):
        """Create a color picker control."""
        container = QWidget()
        layout = QHBoxLayout(container)
        layout.setContentsMargins(0, 0, 0, 0)
        
        # Color preview button
        color_btn = QPushButton()
        color_btn.setFixedSize(32, 24)
        color_btn.setObjectName("colorPreviewButton")
        color_btn.clicked.connect(
            lambda: self.pick_color(param, color_btn)
        )
        
        # Set initial color
        default_color = param.get('default', '#ffffff')
        color_btn.setStyleSheet(f"background-color: {default_color}; border: 1px solid #555;")
        
        # RGB spinboxes
        rgb_container = QWidget()
        rgb_layout = QHBoxLayout(rgb_container)
        rgb_layout.setContentsMargins(0, 0, 0, 0)
        
        r_spin = QSpinBox()
        g_spin = QSpinBox()
        b_spin = QSpinBox()
        
        for spin, label in [(r_spin, 'R'), (g_spin, 'G'), (b_spin, 'B')]:
            spin.setRange(0, 255)
            spin.setValue(255)  # Default white
            spin.setFixedWidth(50)
            spin.setObjectName("colorSpinBox")
            rgb_layout.addWidget(QLabel(label))
            rgb_layout.addWidget(spin)
        
        # Connect RGB changes to color button
        def update_color():
            r, g, b = r_spin.value(), g_spin.value(), b_spin.value()
            color_btn.setStyleSheet(f"background-color: rgb({r},{g},{b}); border: 1px solid #555;")
            self.on_parameter_changed(param['name'], {'r': r, 'g': g, 'b': b})
        
        r_spin.valueChanged.connect(update_color)
        g_spin.valueChanged.connect(update_color)
        b_spin.valueChanged.connect(update_color)
        
        layout.addWidget(color_btn)
        layout.addWidget(rgb_container)
        
        self.parameter_widgets[param['name']] = (color_btn, r_spin, g_spin, b_spin)
        return container
    
    def create_spin_control(self, param: dict):
        """Create a spinbox control (fallback)."""
        spinbox = QSpinBox()
        spinbox.setMinimum(param.get('min', 0))
        spinbox.setMaximum(param.get('max', 100))
        spinbox.setValue(param.get('default', 0))
        spinbox.setSingleStep(param.get('step', 1))
        spinbox.setObjectName("parameterSpinBox")
        
        # Connect signal
        spinbox.valueChanged.connect(
            lambda value, name=param['name']: self.on_parameter_changed(name, value)
        )
        
        self.parameter_widgets[param['name']] = spinbox
        return spinbox
    
    def browse_file(self, param: dict, path_label: QLabel):
        """Open file dialog for file picker."""
        from PyQt5.QtWidgets import QFileDialog
        
        file_filter = param.get('file_filter', 'All Files (*.*)')
        file_path, _ = QFileDialog.getOpenFileName(
            self, 
            f"Select {param.get('label', param['name'])}", 
            "", 
            file_filter
        )
        
        if file_path:
            path_label.setText(file_path)
            self.on_parameter_changed(param['name'], file_path)
    
    def pick_color(self, param: dict, color_btn: QPushButton):
        """Open color dialog for color picker."""
        from PyQt5.QtWidgets import QColorDialog
        from PyQt5.QtGui import QColor
        
        current_color = QColor(255, 255, 255)  # Default white
        color = QColorDialog.getColor(current_color, self, f"Select {param.get('label', param['name'])}")
        
        if color.isValid():
            color_btn.setStyleSheet(f"background-color: {color.name()}; border: 1px solid #555;")
            self.on_parameter_changed(param['name'], {
                'r': color.red(),
                'g': color.green(), 
                'b': color.blue()
            })
    
    def on_parameter_changed(self, name: str, value):
        """Handle parameter value changes."""
        self.parameter_changed.emit(name, value)
        
        # Handle dependent parameters (show/hide logic)
        self.update_dependent_parameters(name, value)
    
    def update_dependent_parameters(self, changed_param: str, value):
        """Update visibility of dependent parameters."""
        if changed_param in self.dependent_parameters:
            for dependent_param, condition in self.dependent_parameters[changed_param].items():
                should_show = self.evaluate_condition(condition, value)
                self.set_parameter_visibility(dependent_param, should_show)
    
    def evaluate_condition(self, condition: dict, value) -> bool:
        """Evaluate a condition for showing/hiding parameters."""
        condition_type = condition.get('type', 'equals')
        
        if condition_type == 'equals':
            return value == condition['value']
        elif condition_type == 'not_equals':
            return value != condition['value']
        elif condition_type == 'contains':
            return condition['value'] in str(value)
        elif condition_type == 'greater_than':
            return value > condition['value']
        elif condition_type == 'less_than':
            return value < condition['value']
        elif condition_type == 'is_true':
            return bool(value)
        elif condition_type == 'is_false':
            return not bool(value)
        
        return True
    
    def set_parameter_visibility(self, param_name: str, visible: bool):
        """Show or hide a parameter widget."""
        if param_name in self.parameter_widgets:
            widget = self.parameter_widgets[param_name]
            
            # Handle different widget types
            if isinstance(widget, tuple):
                # Multiple widgets (like file picker or color picker)
                for w in widget:
                    if hasattr(w, 'setVisible'):
                        w.setVisible(visible)
                    if hasattr(w, 'parent') and w.parent():
                        w.parent().setVisible(visible)
            else:
                # Single widget
                if hasattr(widget, 'setVisible'):
                    widget.setVisible(visible)
                if hasattr(widget, 'parent') and widget.parent():
                    widget.parent().setVisible(visible)
    
    def add_dependency(self, controlling_param: str, dependent_param: str, condition: dict):
        """Add a dependency between parameters for show/hide logic."""
        if controlling_param not in self.dependent_parameters:
            self.dependent_parameters[controlling_param] = {}
        self.dependent_parameters[controlling_param][dependent_param] = condition
    
    def apply_professional_styling(self):
        """Apply comprehensive professional dark theme styling."""
        self.setStyleSheet("""
            QWidget {
                background-color: #2d2d2d;
                color: #ffffff;
                font-family: 'Segoe UI', Arial, sans-serif;
                font-size: 9pt;
            }
            
            QGroupBox {
                color: #ffffff;
                font-weight: bold;
                border: 1px solid #444;
                border-radius: 4px;
                margin-top: 8px;
                padding-top: 8px;
                background-color: #333;
            }
            
            QGroupBox::title {
                subcontrol-origin: margin;
                subcontrol-position: top left;
                padding: 0 8px;
                color: #0096ff;
            }
            
            QLabel {
                color: #ffffff;
                background-color: transparent;
            }
            
            QSlider::groove:horizontal {
                background-color: #444;
                height: 6px;
                border-radius: 3px;
            }
            
            QSlider::handle:horizontal {
                background-color: #0096ff;
                width: 16px;
                border-radius: 8px;
                margin: -5px 0;
            }
            
            QSlider::handle:horizontal:hover {
                background-color: #1aa3ff;
            }
            
            QComboBox, QSpinBox, QDoubleSpinBox {
                background-color: #333;
                border: 1px solid #555;
                border-radius: 3px;
                padding: 4px;
                color: white;
                min-height: 20px;
            }
            
            QComboBox:hover, QSpinBox:hover, QDoubleSpinBox:hover {
                border-color: #0096ff;
            }
            
            QComboBox::drop-down {
                border: none;
                width: 20px;
            }
            
            QComboBox::down-arrow {
                image: none;
                border-left: 5px solid transparent;
                border-right: 5px solid transparent;
                border-top: 5px solid #0096ff;
            }
            
            QCheckBox {
                color: white;
                background-color: transparent;
            }
            
            QCheckBox::indicator {
                width: 16px;
                height: 16px;
                border: 1px solid #555;
                border-radius: 3px;
                background-color: #333;
            }
            
            QCheckBox::indicator:checked {
                background-color: #0096ff;
                image: url(data:image/svg+xml;base64,PHN2ZyB3aWR0aD0iMTIiIGhlaWdodD0iMTIiIHZpZXdCb3g9IjAgMCAxMiAxMiIgZmlsbD0ibm9uZSIgeG1sbnM9Imh0dHA6Ly93d3cudzMub3JnLzIwMDAvc3ZnIj4KPHBhdGggZD0iTTEwIDNMNC41IDguNUwyIDYiIHN0cm9rZT0id2hpdGUiIHN0cm9rZS13aWR0aD0iMiIgc3Ryb2tlLWxpbmVjYXA9InJvdW5kIiBzdHJva2UtbGluZWpvaW49InJvdW5kIi8+Cjwvc3ZnPgo=);
            }
            
            QPushButton {
                background-color: #0096ff;
                border: 1px solid #0096ff;
                border-radius: 3px;
                color: white;
                padding: 4px 8px;
                font-weight: bold;
            }
            
            QPushButton:hover {
                background-color: #1aa3ff;
                border-color: #1aa3ff;
            }
            
            QPushButton:pressed {
                background-color: #007acc;
                border-color: #007acc;
            }
            
            #browseButton {
                background-color: #555;
                border-color: #555;
                font-size: 8pt;
            }
            
            #browseButton:hover {
                background-color: #666;
                border-color: #666;
            }
            
            #colorPreviewButton {
                border: 1px solid #555;
                border-radius: 2px;
            }
            
            #filePathLabel {
                color: #888;
                font-style: italic;
                background-color: transparent;
            }
            
            #parameterLabel {
                color: #ffffff;
                background-color: transparent;
                font-weight: normal;
            }
        """) 