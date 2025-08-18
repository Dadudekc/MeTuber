"""
Style Manager Module for Dreamscape V2 Professional

Handles all style-related functionality including style loading,
parameter extraction, style instance management, and style registry.
"""

import logging
from PyQt5.QtWidgets import QSlider, QLabel


class StyleManager:
    """Manages all style-related functionality."""
    
    def __init__(self, main_window):
        """Initialize style manager with reference to main window."""
        self.main_window = main_window
        self.logger = logging.getLogger(__name__)
        
        # Style management
        self.style_manager_ready = None
        self.loaded_styles = {}
        self.style_registry = {}
        
        # CRITICAL FIX: Initialize core style manager immediately
        try:
            self.logger.info("Initializing core style manager...")
            from core.style_manager import StyleManager as CoreStyleManager
            self.style_manager_ready = CoreStyleManager()
            self.logger.info("Core style manager initialized successfully")
        except Exception as e:
            self.logger.error(f"Failed to initialize core style manager: {e}")
            self.style_manager_ready = None
    
    def pre_load_styles_lazy(self):
        """Pre-load styles lazily (called by main window)."""
        try:
            self.logger.info("PRE-LOADING STYLES (LAZY)...")
            
            # Import style manager - FIXED: Use absolute import
            from core.style_manager import StyleManager as CoreStyleManager
            
            # Create style manager instance
            self.style_manager_ready = CoreStyleManager()
            
            # Store reference in main window for easy access
            self.main_window.style_manager = self.style_manager_ready
            
            self.logger.info("Style manager ready for lazy loading!")
            
        except Exception as e:
            self.logger.error(f"Error pre-loading styles (lazy): {e}")
            import traceback
            self.logger.error(f"Traceback: {traceback.format_exc()}")
    
    def pre_load_styles(self):
        """Pre-load all styles for instant access."""
        try:
            self.logger.info("PRE-LOADING STYLES...")
            
            # Import style manager - FIXED: Use absolute import
            from core.style_manager import StyleManager as CoreStyleManager
            
            # Create style manager instance
            self.style_manager_ready = CoreStyleManager()
            
            # Load all styles (styles are loaded automatically when accessed)
            # The style manager loads styles on demand, so we don't need to call load_all_styles()
            
            # Store loaded styles (styles are loaded on demand)
            self.loaded_styles = {}  # Will be populated as styles are accessed
            
            # Create style registry for quick lookup
            for style_name, style_instance in self.loaded_styles.items():
                self.style_registry[style_name] = style_instance
                
            # Pre-load specific styles for instant access
            self.pre_load_specific_styles()
            
            # Store reference in main window for easy access
            self.main_window.style_manager = self.style_manager_ready
            
            self.logger.info("All styles pre-loaded and ready!")
            
        except Exception as e:
            self.logger.error(f"Error pre-loading styles: {e}")
            import traceback
            self.logger.error(f"Traceback: {traceback.format_exc()}")
            
    def pre_load_specific_styles(self):
        """Pre-load specific commonly used styles."""
        try:
            # Pre-load Edge Detection for instant access
            edge_detection = self.style_manager_ready.get_style("Edge Detection")
            if edge_detection:
                self.logger.info("Edge Detection pre-loaded!")
                
            # Pre-load other popular styles
            popular_styles = [
                "Cartoon", "Pencil Sketch", "Watercolor", "Glitch",
                "Color Balance", "Brightness Only", "Contrast Only"
            ]
            
            for style_name in popular_styles:
                style_instance = self.style_manager_ready.get_style(style_name)
                if style_instance:
                    self.logger.info(f"{style_name} pre-loaded!")
                    
        except Exception as e:
            self.logger.error(f"Error pre-loading specific styles: {e}")
            
    def get_style(self, style_name):
        """Get a style instance by name."""
        try:
            if self.style_manager_ready:
                return self.style_manager_ready.get_style(style_name)
            return None
            
        except Exception as e:
            self.logger.error(f"Error getting style {style_name}: {e}")
            return None
    
    def get_categories(self):
        """Get style categories from the core style manager."""
        try:
            if self.style_manager_ready:
                return self.style_manager_ready.get_categories()
            return {}
            
        except Exception as e:
            self.logger.error(f"Error getting style categories: {e}")
            return {}
            
    def get_all_styles(self):
        """Get all loaded styles."""
        try:
            if self.style_manager_ready:
                return self.style_manager_ready.get_all_styles()
            return {}
            
        except Exception as e:
            self.logger.error(f"Error getting all styles: {e}")
            return {}
            
    def get_style_specific_parameters(self, effect_name):
        """Get style-specific parameters for an effect."""
        try:
            # Map UI effect names to actual style names
            style_mapping = {
                "🔍 Edge Detection": "Edge Detection",
                "🎭 Cartoon Effects": "Cartoon",
                "✏️ Sketch Effects": "Pencil Sketch",
                "🎨 Color Effects": "Color Balance",
                "💧 Watercolor": "Watercolor",
                "⚡ Glitch Effect": "Glitch",
                "🌟 Glow Effect": "Glowing Edges",
                "🎬 Motion Blur": "Motion Blur",
                "🌈 Color Grading": "Color Balance",
                "📸 Portrait Mode": "Brightness Only",
                "🎪 Vintage": "Sepia Vibrant",
                "🌌 Cyberpunk": "Negative Vintage"
            }
            
            # Get actual style name
            actual_style_name = style_mapping.get(effect_name, effect_name)
            
            # Get style instance
            style_instance = self.get_style(actual_style_name)
            if not style_instance:
                return {}
                
            # Get parameters from style
            if hasattr(style_instance, 'define_parameters'):
                try:
                    return style_instance.define_parameters()
                except Exception as param_error:
                    self.logger.warning(f"Error getting parameters for {actual_style_name}: {param_error}")
                    
            return {}
            
        except Exception as e:
            self.logger.error(f"Error getting style-specific parameters: {e}")
            return {}
            
    def update_parameters_for_effect(self, effect_name):
        """Update parameter controls for a specific effect."""
        try:
            self.logger.info(f"Updating parameters for effect: {effect_name}")
            
            # Get style-specific parameters
            parameters = self.get_style_specific_parameters(effect_name)
            
            # Update parameter controls based on effect type
            if "🔍 Edge Detection" in effect_name:
                self.update_edge_detection_parameters()
            elif "🎭 Cartoon Effects" in effect_name:
                self.update_cartoon_parameters()
            elif "✏️ Sketch Effects" in effect_name:
                self.update_sketch_parameters()
            elif "🎨 Color Effects" in effect_name:
                self.update_color_parameters()
            else:
                self.update_generic_parameters()
                
        except Exception as e:
            self.logger.error(f"Error updating parameters for effect: {e}")
            
    def update_edge_detection_parameters(self):
        """Update parameters for Edge Detection effect."""
        try:
            # Update parameter sliders for Edge Detection
            if hasattr(self.main_window, 'param1_slider'):
                self.main_window.param1_slider.setRange(0, 255)
                self.main_window.param1_slider.setValue(100)
                if hasattr(self.main_window, 'param1_label'):
                    self.main_window.param1_label.setText("Lower Threshold")
                    
            if hasattr(self.main_window, 'param2_slider'):
                self.main_window.param2_slider.setRange(0, 255)
                self.main_window.param2_slider.setValue(200)
                if hasattr(self.main_window, 'param2_label'):
                    self.main_window.param2_label.setText("Upper Threshold")
                    
            if hasattr(self.main_window, 'param3_slider'):
                self.main_window.param3_slider.setRange(1, 15)
                self.main_window.param3_slider.setValue(5)
                if hasattr(self.main_window, 'param3_label'):
                    self.main_window.param3_label.setText("Blur Kernel")
                    
            if hasattr(self.main_window, 'param4_slider'):
                self.main_window.param4_slider.setRange(0, 2)
                self.main_window.param4_slider.setValue(0)
                if hasattr(self.main_window, 'param4_label'):
                    self.main_window.param4_label.setText("Algorithm")
                    
            self.logger.info("Edge Detection parameters configured")
            
        except Exception as e:
            self.logger.error(f"Error updating Edge Detection parameters: {e}")
            
    def update_cartoon_parameters(self):
        """Update parameters for Cartoon effect."""
        try:
            # Update parameter sliders for Cartoon
            if hasattr(self.main_window, 'param1_slider'):
                self.main_window.param1_slider.setRange(0, 255)
                self.main_window.param1_slider.setValue(50)
                if hasattr(self.main_window, 'param1_label'):
                    self.main_window.param1_label.setText("Edge Threshold")
                    
            if hasattr(self.main_window, 'param2_slider'):
                self.main_window.param2_slider.setRange(10, 300)
                self.main_window.param2_slider.setValue(150)
                if hasattr(self.main_window, 'param2_label'):
                    self.main_window.param2_label.setText("Color Saturation")
                    
            if hasattr(self.main_window, 'param3_slider'):
                self.main_window.param3_slider.setRange(1, 15)
                self.main_window.param3_slider.setValue(5)
                if hasattr(self.main_window, 'param3_label'):
                    self.main_window.param3_label.setText("Blur Strength")
                    
            if hasattr(self.main_window, 'param4_slider'):
                self.main_window.param4_slider.setRange(0, 3)
                self.main_window.param4_slider.setValue(0)
                if hasattr(self.main_window, 'param4_label'):
                    self.main_window.param4_label.setText("Cartoon Mode")
                    
            self.logger.info("Cartoon parameters configured")
            
        except Exception as e:
            self.logger.error(f"Error updating Cartoon parameters: {e}")
            
    def update_sketch_parameters(self):
        """Update parameters for Sketch effect."""
        try:
            # Update parameter sliders for Sketch
            if hasattr(self.main_window, 'param1_slider'):
                self.main_window.param1_slider.setRange(1, 10)
                self.main_window.param1_slider.setValue(3)
                if hasattr(self.main_window, 'param1_label'):
                    self.main_window.param1_label.setText("Line Thickness")
                    
            if hasattr(self.main_window, 'param2_slider'):
                self.main_window.param2_slider.setRange(0, 100)
                self.main_window.param2_slider.setValue(50)
                if hasattr(self.main_window, 'param2_label'):
                    self.main_window.param2_label.setText("Detail Level")
                    
            if hasattr(self.main_window, 'param3_slider'):
                self.main_window.param3_slider.setRange(0, 1)
                self.main_window.param3_slider.setValue(0)
                if hasattr(self.main_window, 'param3_label'):
                    self.main_window.param3_label.setText("Preserve Colors")
                    
            if hasattr(self.main_window, 'param4_slider'):
                self.main_window.param4_slider.setRange(0, 4)
                self.main_window.param4_slider.setValue(0)
                if hasattr(self.main_window, 'param4_label'):
                    self.main_window.param4_label.setText("Sketch Type")
                    
            self.logger.info("Sketch parameters configured")
            
        except Exception as e:
            self.logger.error(f"Error updating Sketch parameters: {e}")
            
    def update_color_parameters(self):
        """Update parameters for Color effect."""
        try:
            # Update parameter sliders for Color
            if hasattr(self.main_window, 'param1_slider'):
                self.main_window.param1_slider.setRange(-100, 100)
                self.main_window.param1_slider.setValue(0)
                if hasattr(self.main_window, 'param1_label'):
                    self.main_window.param1_label.setText("Brightness")
                    
            if hasattr(self.main_window, 'param2_slider'):
                self.main_window.param2_slider.setRange(50, 300)
                self.main_window.param2_slider.setValue(100)
                if hasattr(self.main_window, 'param2_label'):
                    self.main_window.param2_label.setText("Contrast")
                    
            if hasattr(self.main_window, 'param3_slider'):
                self.main_window.param3_slider.setRange(0, 200)
                self.main_window.param3_slider.setValue(100)
                if hasattr(self.main_window, 'param3_label'):
                    self.main_window.param3_label.setText("Saturation")
                    
            if hasattr(self.main_window, 'param4_slider'):
                self.main_window.param4_slider.setRange(0, 7)
                self.main_window.param4_slider.setValue(0)
                if hasattr(self.main_window, 'param4_label'):
                    self.main_window.param4_label.setText("Color Effect")
                    
            self.logger.info("Color parameters configured")
            
        except Exception as e:
            self.logger.error(f"Error updating Color parameters: {e}")
            
    def update_generic_parameters(self):
        """Update parameters for generic effects."""
        try:
            # Update parameter sliders for generic effects
            if hasattr(self.main_window, 'param1_slider'):
                self.main_window.param1_slider.setRange(0, 100)
                self.main_window.param1_slider.setValue(50)
                if hasattr(self.main_window, 'param1_label'):
                    self.main_window.param1_label.setText("Intensity")
                    
            if hasattr(self.main_window, 'param2_slider'):
                self.main_window.param2_slider.setRange(0, 100)
                self.main_window.param2_slider.setValue(50)
                if hasattr(self.main_window, 'param2_label'):
                    self.main_window.param2_label.setText("Quality")
                    
            if hasattr(self.main_window, 'param3_slider'):
                self.main_window.param3_slider.setRange(0, 1)
                self.main_window.param3_slider.setValue(1)
                if hasattr(self.main_window, 'param3_label'):
                    self.main_window.param3_label.setText("Enable")
                    
            if hasattr(self.main_window, 'param4_slider'):
                self.main_window.param4_slider.setRange(0, 100)
                self.main_window.param4_slider.setValue(0)
                if hasattr(self.main_window, 'param4_label'):
                    self.main_window.param4_label.setText("Advanced")
                    
            self.logger.info("Generic parameters configured")
            
        except Exception as e:
            self.logger.error(f"Error updating generic parameters: {e}")
            
    def create_default_sliders(self):
        """Create default parameter sliders."""
        try:
            # Create default parameter sliders if they don't exist
            if not hasattr(self.main_window, 'param1_slider'):
                self.main_window.param1_slider = QSlider()
                self.main_window.param1_label = QLabel("Parameter 1")
                
            if not hasattr(self.main_window, 'param2_slider'):
                self.main_window.param2_slider = QSlider()
                self.main_window.param2_label = QLabel("Parameter 2")
                
            if not hasattr(self.main_window, 'param3_slider'):
                self.main_window.param3_slider = QSlider()
                self.main_window.param3_label = QLabel("Parameter 3")
                
            if not hasattr(self.main_window, 'param4_slider'):
                self.main_window.param4_slider = QSlider()
                self.main_window.param4_label = QLabel("Parameter 4")
                
            # Set default ranges and values
            for i in range(1, 5):
                slider = getattr(self.main_window, f'param{i}_slider')
                label = getattr(self.main_window, f'param{i}_label')
                
                slider.setRange(0, 100)
                slider.setValue(50)
                label.setText(f"Parameter {i}")
                
        except Exception as e:
            self.logger.error(f"Error creating default sliders: {e}")
            
    def get_styles_by_category(self, category):
        """Get all styles in a specific category."""
        try:
            if self.style_manager_ready:
                return self.style_manager_ready.get_styles_by_category(category)
            return []
            
        except Exception as e:
            self.logger.error(f"Error getting styles by category: {e}")
            return []
            
    def reload_styles(self):
        """Reload all styles."""
        try:
            self.logger.info("Reloading all styles...")
            
            if self.style_manager_ready:
                self.style_manager_ready.load_all_styles()
                self.loaded_styles = self.style_manager_ready.get_all_styles()
                
            self.logger.info("Styles reloaded successfully")
            
        except Exception as e:
            self.logger.error(f"Error reloading styles: {e}")
            
    def get_style_info(self, style_name):
        """Get detailed information about a style."""
        try:
            style_instance = self.get_style(style_name)
            if not style_instance:
                return {}
                
            info = {
                'name': style_name,
                'class': style_instance.__class__.__name__,
                'module': style_instance.__class__.__module__,
                'has_parameters': hasattr(style_instance, 'define_parameters'),
                'has_apply': hasattr(style_instance, 'apply')
            }
            
            # Get parameters if available
            if info['has_parameters']:
                try:
                    info['parameters'] = style_instance.define_parameters()
                except Exception:
                    info['parameters'] = {}
                    
            return info
            
        except Exception as e:
            self.logger.error(f"Error getting style info: {e}")
            return {} 