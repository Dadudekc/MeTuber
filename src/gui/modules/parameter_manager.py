"""
Parameter Manager Module for MeTuber V2 Professional

Handles all parameter-related functionality including embedded widgets,
parameter updates, and fallback parameter creation.
"""

import logging
from PyQt5.QtWidgets import (
    QSlider, QDoubleSpinBox, QSpinBox, QCheckBox, QComboBox, QLabel
)
from PyQt5.QtCore import Qt


class ParameterManager:
    """Manages all parameter-related functionality."""
    
    def __init__(self, main_window):
        """Initialize parameter manager with reference to main window."""
        self.main_window = main_window
        self.logger = logging.getLogger(__name__)
        
        # Parameter storage
        self.current_embedded_params = {}
        self.current_filter_name = None
        self.current_style = None
        
    def clear_embedded_parameter_widgets(self):
        """Clear existing embedded parameter widgets."""
        try:
            # Clear the existing parameter layout
            if hasattr(self.main_window, 'params_layout'):
                # Remove all widgets from the layout
                while self.main_window.params_layout.rowCount() > 0:
                    self.main_window.params_layout.removeRow(0)
                    
            # Clear stored widget references
            if hasattr(self.main_window, 'embedded_param_widgets'):
                for widget in self.main_window.embedded_param_widgets.values():
                    if widget:
                        widget.deleteLater()
                self.main_window.embedded_param_widgets.clear()
            else:
                self.main_window.embedded_param_widgets = {}
                
        except Exception as e:
            self.logger.error(f"Error clearing embedded widgets: {e}")
            
    def create_embedded_parameter_widgets(self, parameters):
        """Create parameter widgets and embed them into the existing layout."""
        try:
            # Group parameters by category
            grouped_params = {}
            for param in parameters:
                category = param.get('category', 'Basic')
                if category not in grouped_params:
                    grouped_params[category] = []
                grouped_params[category].append(param)
            
            # Create widgets for each group
            for category, params in grouped_params.items():
                # Add category label
                category_label = QLabel(category)
                category_label.setStyleSheet("color: #0096ff; font-weight: bold; font-size: 12px; margin-top: 10px;")
                self.main_window.params_layout.addRow(category_label)
                
                # Create widgets for each parameter in this category
                for param in params:
                    widget = self.create_embedded_parameter_widget(param)
                    if widget:
                        self.main_window.embedded_param_widgets[param['name']] = widget
                        self.main_window.params_layout.addRow(param['label'], widget)
                        
        except Exception as e:
            self.logger.error(f"Error creating embedded parameter widgets: {e}")
            
    def create_embedded_parameter_widget(self, param):
        """Create a single embedded parameter widget."""
        try:
            param_type = param.get('type', 'slider')
            param_name = param['name']
            default_value = param.get('default', 0)
            
            if param_type == 'slider':
                widget = QSlider(Qt.Horizontal)
                min_val = param.get('min', 0)
                max_val = param.get('max', 100)
                widget.setRange(min_val, max_val)
                widget.setValue(default_value)
                
                # Connect to parameter update
                widget.valueChanged.connect(lambda value, name=param_name: self.on_embedded_parameter_changed(name, value))
                
            elif param_type == 'float':
                widget = QDoubleSpinBox()
                min_val = param.get('min', 0.0)
                max_val = param.get('max', 100.0)
                step = param.get('step', 0.1)
                widget.setRange(min_val, max_val)
                widget.setSingleStep(step)
                widget.setValue(default_value)
                
                # Connect to parameter update
                widget.valueChanged.connect(lambda value, name=param_name: self.on_embedded_parameter_changed(name, value))
                
            elif param_type == 'int':
                widget = QSpinBox()
                min_val = param.get('min', 0)
                max_val = param.get('max', 100)
                widget.setRange(min_val, max_val)
                widget.setValue(default_value)
                
                # Connect to parameter update
                widget.valueChanged.connect(lambda value, name=param_name: self.on_embedded_parameter_changed(name, value))
                
            elif param_type == 'bool':
                widget = QCheckBox()
                widget.setChecked(default_value)
                
                # Connect to parameter update
                widget.toggled.connect(lambda checked, name=param_name: self.on_embedded_parameter_changed(name, checked))
                
            elif param_type == 'str':
                widget = QComboBox()
                options = param.get('options', ['Option 1', 'Option 2'])
                widget.addItems(options)
                if default_value in options:
                    widget.setCurrentText(default_value)
                
                # Connect to parameter update
                widget.currentTextChanged.connect(lambda text, name=param_name: self.on_embedded_parameter_changed(name, text))
                
            else:
                # Default to slider
                widget = QSlider(Qt.Horizontal)
                widget.setRange(0, 100)
                widget.setValue(default_value)
                widget.valueChanged.connect(lambda value, name=param_name: self.on_embedded_parameter_changed(name, value))
                
            return widget
            
        except Exception as e:
            self.logger.error(f"Error creating embedded parameter widget: {e}")
            return None
            
    def on_embedded_parameter_changed(self, param_name, value):
        """Handle parameter changes from embedded widgets."""
        try:
            # Ensure current_embedded_params is a dictionary
            if not isinstance(self.current_embedded_params, dict):
                self.current_embedded_params = {}
                self.logger.warning("Reset current_embedded_params to dictionary")
            
            # Update the current parameters
            self.current_embedded_params[param_name] = value
            
            # Apply the effect with updated parameters
            if self.current_filter_name:
                self.apply_embedded_effect(self.current_filter_name, self.current_embedded_params)
                
            self.logger.info(f"Embedded parameter changed: {param_name} = {value}")
            
        except Exception as e:
            self.logger.error(f"Error handling embedded parameter change: {e}")
            
    def apply_embedded_effect(self, filter_name, parameters):
        """Apply effect using embedded widget parameters."""
        try:
            # Load and apply the style with parameters
            if hasattr(self.main_window, 'style_manager'):
                style_manager = self.main_window.style_manager
            else:
                from src.core.style_manager import StyleManager
                style_manager = StyleManager()
                
            # Get the style instance
            style_instance = style_manager.get_style(filter_name)
            if not style_instance:
                self.logger.warning(f"Style not found: {filter_name}")
                return
                
            # Apply the style with parameters
            self.main_window.pending_params = parameters
            self.current_style = style_instance
            
            # Update webcam service if running
            if hasattr(self.main_window, 'webcam_manager') and self.main_window.webcam_manager:
                self.main_window.webcam_manager.update_style(style_instance, parameters)
                
            self.logger.info(f"Applied {filter_name} with embedded parameters: {parameters}")
            
        except Exception as e:
            self.logger.error(f"Error applying embedded effect: {e}")
            import traceback
            self.logger.error(f"Traceback: {traceback.format_exc()}")
            
    def create_fallback_parameters(self, filter_name):
        """Create fallback parameters when style parameters can't be loaded."""
        filter_name_lower = filter_name.lower()
        
        if "edge" in filter_name_lower or "detection" in filter_name_lower:
            return [
                {
                    'name': 'threshold1',
                    'type': 'slider',
                    'min': 0,
                    'max': 255,
                    'default': 100,
                    'label': 'Lower Threshold',
                    'category': 'Edge Detection'
                },
                {
                    'name': 'threshold2',
                    'type': 'slider',
                    'min': 0,
                    'max': 255,
                    'default': 200,
                    'label': 'Upper Threshold',
                    'category': 'Edge Detection'
                },
                {
                    'name': 'blur_kernel',
                    'type': 'slider',
                    'min': 1,
                    'max': 15,
                    'default': 5,
                    'label': 'Blur Kernel Size',
                    'category': 'Preprocessing'
                },
                {
                    'name': 'algorithm',
                    'type': 'str',
                    'options': ['Canny', 'Sobel', 'Laplacian'],
                    'default': 'Canny',
                    'label': 'Algorithm',
                    'category': 'Advanced'
                }
            ]
        elif "cartoon" in filter_name_lower:
            return [
                {
                    'name': 'edge_threshold',
                    'type': 'slider',
                    'min': 0,
                    'max': 255,
                    'default': 50,
                    'label': 'Edge Threshold',
                    'category': 'Basic'
                },
                {
                    'name': 'color_saturation',
                    'type': 'float',
                    'min': 0.1,
                    'max': 3.0,
                    'default': 1.5,
                    'label': 'Color Saturation',
                    'category': 'Basic'
                },
                {
                    'name': 'blur_strength',
                    'type': 'slider',
                    'min': 1,
                    'max': 15,
                    'default': 5,
                    'label': 'Blur Strength',
                    'category': 'Basic'
                },
                {
                    'name': 'mode',
                    'type': 'str',
                    'options': ['Basic', 'Advanced', 'Anime'],
                    'default': 'Basic',
                    'label': 'Cartoon Mode',
                    'category': 'Advanced'
                }
            ]
        elif "sketch" in filter_name_lower:
            return [
                {
                    'name': 'line_thickness',
                    'type': 'slider',
                    'min': 1,
                    'max': 10,
                    'default': 3,
                    'label': 'Line Thickness',
                    'category': 'Basic'
                },
                {
                    'name': 'detail_level',
                    'type': 'slider',
                    'min': 0,
                    'max': 100,
                    'default': 50,
                    'label': 'Detail Level',
                    'category': 'Basic'
                },
                {
                    'name': 'preserve_colors',
                    'type': 'bool',
                    'default': False,
                    'label': 'Preserve Colors',
                    'category': 'Advanced'
                }
            ]
        elif "color" in filter_name_lower:
            return [
                {
                    'name': 'brightness',
                    'type': 'slider',
                    'min': -100,
                    'max': 100,
                    'default': 0,
                    'label': 'Brightness',
                    'category': 'Basic'
                },
                {
                    'name': 'contrast',
                    'type': 'float',
                    'min': 0.5,
                    'max': 3.0,
                    'default': 1.0,
                    'label': 'Contrast',
                    'category': 'Basic'
                },
                {
                    'name': 'saturation',
                    'type': 'float',
                    'min': 0.0,
                    'max': 2.0,
                    'default': 1.0,
                    'label': 'Saturation',
                    'category': 'Basic'
                }
            ]
        else:
            # Generic fallback
            return [
                {
                    'name': 'intensity',
                    'type': 'slider',
                    'min': 0,
                    'max': 100,
                    'default': 50,
                    'label': 'Effect Intensity',
                    'category': 'Basic'
                },
                {
                    'name': 'quality',
                    'type': 'str',
                    'options': ['Low', 'Medium', 'High'],
                    'default': 'Medium',
                    'label': 'Quality',
                    'category': 'Advanced'
                },
                {
                    'name': 'enable_effect',
                    'type': 'bool',
                    'default': True,
                    'label': 'Enable Effect',
                    'category': 'Basic'
                }
            ]
            
    def get_widget_type(self, props):
        """Determine widget type from parameter properties."""
        param_type = props.get('type', 'slider')
        
        if param_type == 'float':
            return 'float'
        elif param_type == 'int':
            return 'int'
        elif param_type == 'bool':
            return 'bool'
        elif param_type == 'str' or 'options' in props:
            return 'str'
        else:
            return 'slider'
            
    def hide_old_parameter_controls(self):
        """Hide the old static parameter controls when using draggable widgets."""
        try:
            # Hide the old parameter sliders and labels
            if hasattr(self.main_window, 'param1_slider'):
                self.main_window.param1_slider.hide()
                self.main_window.param1_label.hide()
            if hasattr(self.main_window, 'param2_slider'):
                self.main_window.param2_slider.hide()
                self.main_window.param2_label.hide()
            if hasattr(self.main_window, 'param3_slider'):
                self.main_window.param3_slider.hide()
                self.main_window.param3_label.hide()
            if hasattr(self.main_window, 'param4_slider'):
                self.main_window.param4_slider.hide()
                self.main_window.param4_label.hide()
                
            # Hide the old effect variant combo
            if hasattr(self.main_window, 'effect_variant_combo'):
                self.main_window.effect_variant_combo.hide()
                
            self.logger.info("Hidden old parameter controls - using draggable widgets")
        except Exception as e:
            self.logger.error(f"Error hiding old controls: {e}")
            
    def show_old_parameter_controls(self):
        """Show the old static parameter controls as fallback."""
        try:
            # Show the old parameter sliders and labels
            if hasattr(self.main_window, 'param1_slider'):
                self.main_window.param1_slider.show()
                self.main_window.param1_label.show()
            if hasattr(self.main_window, 'param2_slider'):
                self.main_window.param2_slider.show()
                self.main_window.param2_label.show()
            if hasattr(self.main_window, 'param3_slider'):
                self.main_window.param3_slider.show()
                self.main_window.param3_label.show()
            if hasattr(self.main_window, 'param4_slider'):
                self.main_window.param4_slider.show()
                self.main_window.param4_label.show()
                
            # Show the old effect variant combo
            if hasattr(self.main_window, 'effect_variant_combo'):
                self.main_window.effect_variant_combo.show()
                
            self.logger.info("Showed old parameter controls as fallback")
        except Exception as e:
            self.logger.error(f"Error showing old controls: {e}") 