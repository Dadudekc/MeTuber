"""
Effect Manager Module for MeTuber V2 Professional

Handles all effect-related functionality including effect application,
style management, and effect history tracking.
"""

import logging
from PyQt5.QtWidgets import QPushButton, QLabel
from PyQt5.QtCore import pyqtSignal


class EffectManager:
    """Manages all effect-related functionality."""
    
    def __init__(self, main_window):
        """Initialize effect manager with reference to main window."""
        self.main_window = main_window
        self.logger = logging.getLogger(__name__)
        
        # Effect tracking
        self.effects_history = []
        self.current_effect = None
        
        # Signals
        self.effect_applied = pyqtSignal(str)
        
    def create_effect_buttons(self):
        """Create effect buttons in the effects dock."""
        self.logger.info("Creating effect buttons")
        
        # Popular effects list
        effects = [
            "🔍 Edge Detection",
            "🎭 Cartoon Effects", 
            "✏️ Sketch Effects",
            "🎨 Color Effects",
            "💧 Watercolor",
            "⚡ Glitch Effect",
            "🌟 Glow Effect",
            "🎬 Motion Blur",
            "🌈 Color Grading",
            "📸 Portrait Mode",
            "🎪 Vintage",
            "🌌 Cyberpunk"
        ]
        
        # Create effect buttons
        for effect in effects:
            effect_btn = QPushButton(effect)
            effect_btn.setMinimumHeight(40)
            effect_btn.setStyleSheet("""
                QPushButton {
                    background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                        stop:0 #404040, stop:1 #2d2d2d);
                    border: 1px solid #404040;
                    border-radius: 6px;
                    padding: 8px;
                    text-align: left;
                    font-size: 11px;
                    font-weight: bold;
                }
                QPushButton:hover {
                    background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                        stop:0 #505050, stop:1 #404040);
                    border: 1px solid #0096ff;
                }
                QPushButton:pressed {
                    background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                        stop:0 #2d2d2d, stop:1 #404040);
                }
            """)
            
            # Connect button to effect application
            effect_btn.clicked.connect(lambda checked, e=effect: self.apply_effect(e))
            
            # Add to effects layout
            self.main_window.effects_layout.addWidget(effect_btn)
            
        # Add stretch to push buttons to top
        self.main_window.effects_layout.addStretch()
        
    def apply_effect(self, effect_name):
        """Apply an effect to the preview and embed draggable widget content into parameter panel."""
        # Update current effect label
        if hasattr(self.main_window, 'current_effect_label'):
            self.main_window.current_effect_label.setText(effect_name)
            
        self.effects_history.append(effect_name)
        # Note: We'll handle effect application through direct method calls instead of signals
        self.update_status(f"Applied effect: {effect_name}")
        
        # HIDE THE OLD PARAMETER CONTROLS - REPLACE WITH EMBEDDED WIDGET CONTENT!
        self.main_window.parameter_manager.hide_old_parameter_controls()
        
        # EMBED DRAGGABLE WIDGET CONTENT INTO THE EXISTING PARAMETER PANEL!
        try:
            # Clean up the effect name (remove emojis for style lookup)
            clean_effect_name = effect_name
            if "🔍 Edge Detection" in effect_name:
                clean_effect_name = "Edge Detection"
            elif "🎭 Cartoon Effects" in effect_name:
                clean_effect_name = "Cartoon"
            elif "✏️ Sketch Effects" in effect_name:
                clean_effect_name = "Sketch"
            elif "🎨 Color Effects" in effect_name:
                clean_effect_name = "Color Balance"
            elif "💧 Watercolor" in effect_name:
                clean_effect_name = "Watercolor"
            elif "⚡ Glitch Effect" in effect_name:
                clean_effect_name = "Glitch"
            
            # Embed the widget content into the existing parameter panel
            self.embed_widget_content_into_panel(clean_effect_name)
            # Use clean effect name for logging to avoid emoji encoding issues
            self.logger.info(f"Embedded widget content for: {clean_effect_name}")
                
        except Exception as e:
            self.logger.error(f"Error embedding widget content: {e}")
            import traceback
            self.logger.error(f"Traceback: {traceback.format_exc()}")
            # Show old controls as fallback
            self.main_window.parameter_manager.show_old_parameter_controls()
            
    def embed_widget_content_into_panel(self, filter_name):
        """Embed draggable widget content into the existing parameter panel."""
        try:
            # Clear existing parameter widgets
            self.main_window.parameter_manager.clear_embedded_parameter_widgets()
            
            # Get style manager
            if hasattr(self.main_window, 'style_manager'):
                style_manager = self.main_window.style_manager
            else:
                from src.core.style_manager import StyleManager
                style_manager = StyleManager()
                
            # Get style instance
            style_instance = style_manager.get_style(filter_name)
            if not style_instance:
                self.logger.warning(f"No style found for filter: {filter_name}")
                # Use fallback parameters
                parameters = self.main_window.parameter_manager.create_fallback_parameters(filter_name)
            else:
                # Get parameter definitions
                parameters = []
                if hasattr(style_instance, 'define_parameters'):
                    try:
                        style_params = style_instance.define_parameters()
                        
                        # Convert to widget format
                        if isinstance(style_params, dict):
                            for name, props in style_params.items():
                                param = {
                                    'name': name,
                                    'label': props.get('label', name.replace('_', ' ').title()),
                                    'type': self.main_window.parameter_manager.get_widget_type(props),
                                    'default': props.get('default', 0),
                                    'category': 'Parameters'
                                }
                                
                                # Add type-specific properties
                                if 'min' in props:
                                    param['min'] = props['min']
                                if 'max' in props:
                                    param['max'] = props['max']
                                if 'step' in props:
                                    param['step'] = props['step']
                                if 'options' in props:
                                    param['options'] = props['options']
                                    
                                parameters.append(param)
                                
                        elif isinstance(style_params, list):
                            parameters = style_params
                            
                    except Exception as param_error:
                        self.logger.warning(f"Error extracting parameters: {param_error}")
                        
                # Create comprehensive fallback parameters based on filter type
                if not parameters:
                    parameters = self.main_window.parameter_manager.create_fallback_parameters(filter_name)
            
            # Store the current style for parameter updates
            self.main_window.current_style = style_instance
            self.main_window.parameter_manager.current_filter_name = filter_name
            
            # Create and embed parameter widgets into the existing layout
            self.main_window.parameter_manager.create_embedded_parameter_widgets(parameters)
            
            # Apply the effect immediately
            self.main_window.parameter_manager.apply_embedded_effect(filter_name, parameters)
            
        except Exception as e:
            self.logger.error(f"Error embedding widget content: {e}")
            import traceback
            self.logger.error(f"Traceback: {traceback.format_exc()}")
            
    def update_variant_combo(self, effect_name):
        """Update the variant combo box based on the selected effect."""
        self.main_window.effect_variant_combo.clear()
        
        if "Cartoon Effects" in effect_name:
            self.main_window.effect_variant_combo.addItems(["Classic", "Fast", "Anime", "Advanced", "Whole Image"])
        elif "Sketch Effects" in effect_name:
            self.main_window.effect_variant_combo.addItems(["Pencil", "Advanced Pencil", "Color Sketch", "Line Art", "Stippling"])
        elif "Color Effects" in effect_name:
            self.main_window.effect_variant_combo.addItems(["Brightness", "Contrast", "Color Balance", "Vibrant", "Sepia", "Black & White", "Negative", "Invert"])
        else:
            self.main_window.effect_variant_combo.addItems(["Standard", "Enhanced", "Pro", "Custom"])
            
    def load_and_apply_style(self, style_name):
        """Load a style and apply it to the webcam service."""
        try:
            # Use pre-loaded style manager for instant access
            if hasattr(self.main_window, 'style_manager_ready'):
                style_manager = self.main_window.style_manager_ready
            else:
                # Fallback if pre-load failed
                from src.core.style_manager import StyleManager
                style_manager = StyleManager()
            
            # Map UI effect names to actual style names
            style_mapping = {
                # Consolidated styles
                "🎭 Cartoon Effects": "ConsolidatedCartoon",
                "✏️ Sketch Effects": "ConsolidatedSketch", 
                "🎨 Color Effects": "ConsolidatedColor",
                
                # Individual styles
                "💧 Watercolor": "Watercolor",
                "⚡ Glitch Effect": "Glitch",
                "🌟 Glow Effect": "Glowing Edges",
                "🎬 Motion Blur": "Motion Blur",
                "🔍 Edge Detection": "Edge Detection",
                "🌈 Color Grading": "Color Balance",
                "📸 Portrait Mode": "Brightness Only",
                "🎪 Vintage": "Sepia Vibrant",
                "🌌 Cyberpunk": "Negative Vintage",
                
                # Legacy mappings
                "Cartoon (Fast)": "Cartoon",
                "Cartoon (Anime)": "Advanced Cartoon (Anime)",
                "Cartoon (Advanced)": "Advanced Cartoon",
                "Pencil Sketch": "Pencil Sketch",
                "Advanced Sketch": "Advanced Edge Detection",
                "Color Sketch": "Sketch & Color",
                "Oil Painting": "Oil Painting",
                "Line Art": "Line Art",
                "Stippling": "Stippling",
                "Glitch": "Glitch",
                "Mosaic": "Mosaic",
                "Light Leak": "Light Leak",
                "Halftone": "Halftone",
                "Invert": "Invert Colors",
                "Negative": "Negative",
                "Sepia": "Sepia Vibrant",
                "Black & White": "Black & White",
                "Brightness": "Brightness Only",
                "Contrast": "Contrast Only",
                "Color Balance": "Color Balance",
                "Vibrant Color": "Vibrant Color",
                "Edge Detection": "Edge Detection",
                "Cartoon": "Cartoon",
                "Pencil Sketch": "Pencil Sketch",
                "Advanced Edge Detection": "Advanced Edge Detection",
                "Oil Painting": "Oil Painting",
                "Line Art": "Line Art",
                "Stippling": "Stippling",
                "Watercolor": "Watercolor",
                "Motion Blur": "Motion Blur",
                "Glowing Edges": "Glowing Edges",
                "Color Quantization": "Color Quantization",
                "Emboss & Contrast": "Emboss & Contrast",
                "Canny Edge": "Canny Edge",
                "Hough Lines": "Hough Lines",
                "Negative Vintage": "Negative Vintage",
                "Original": "Original"
            }
            
            # Get the actual style name
            actual_style_name = style_mapping.get(style_name, style_name)
            
            # Load the style
            style_instance = style_manager.get_style(actual_style_name)
            if not style_instance:
                self.logger.warning(f"Style not found: {actual_style_name}")
                return
                
            # Apply the style
            self.main_window.current_style = style_instance
            self.main_window.pending_params = {}
            
            # Update webcam service if running
            if hasattr(self.main_window, 'webcam_service') and self.main_window.webcam_service:
                self.main_window.webcam_service.update_style(style_instance, {})
                
            self.logger.info(f"Applied style: {actual_style_name}")
            
        except Exception as e:
            self.logger.error(f"Error loading and applying style: {e}")
            import traceback
            self.logger.error(f"Traceback: {traceback.format_exc()}")
            
    def add_to_favorites(self):
        """Add current effect to favorites."""
        if self.current_effect:
            # Implementation for adding to favorites
            self.logger.info(f"Added {self.current_effect} to favorites")
            
    def update_status(self, message):
        """Update the status bar with a message."""
        if hasattr(self.main_window, 'status_label'):
            self.main_window.status_label.setText(message)
        self.logger.info(message) 