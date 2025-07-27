#!/usr/bin/env python3
"""
MeTuber V2 - Professional Webcam Effects Studio (Modular Version)
A next-generation interface designed to rival OBS Studio
"""

import sys
import logging
from PyQt5.QtWidgets import QApplication, QMainWindow
from PyQt5.QtCore import pyqtSignal

# Import our modular components
from .modules import (
    UIComponents,
    ParameterManager,
    EffectManager,
    PreviewManager,
    WebcamManager,
    StyleManager,
    WidgetManager
)


class ProfessionalV2MainWindow(QMainWindow):
    """Professional V2 main window designed to rival OBS Studio (Modular Version)."""
    
    # Signals
    style_changed = pyqtSignal(str)
    device_changed = pyqtSignal(str)
    parameters_changed = pyqtSignal(dict)
    start_processing = pyqtSignal()
    stop_processing = pyqtSignal()
    effect_applied = pyqtSignal(str)
    
    def __init__(self):
        super().__init__()
        self.logger = logging.getLogger(__name__)
        
        # Initialize state variables
        self.is_processing = False
        self.current_style = None
        self.effects_history = []
        self.favorite_effects = []
        self.current_frame = None
        self.preview_pixmap = None
        self.pending_style = None
        self.pending_params = {}  # Ensure this is always a dictionary
        
        # Initialize all managers
        self.init_managers()
        
        # Setup UI using UI Components manager
        self.ui_components.setup_professional_theme()
        self.init_ui()
        
        # Expose UI components after UI is initialized
        self._expose_ui_components()
        
        self.setup_connections()
        
        # Pre-load everything for instant startup
        self.pre_load_everything()
        
        # Hide old parameter controls by default - using embedded widgets instead
        self.parameter_manager.hide_old_parameter_controls()
        
        self.logger.info("Professional V2 Main Window (Modular) initialized successfully!")
        
    def init_managers(self):
        """Initialize all manager modules."""
        self.logger.info("Initializing all manager modules...")
        
        # Initialize UI Components Manager
        self.ui_components = UIComponents(self)
        
        # Initialize Parameter Manager
        self.parameter_manager = ParameterManager(self)
        
        # Initialize Effect Manager
        self.effect_manager = EffectManager(self)
        
        # Initialize Preview Manager
        self.preview_manager = PreviewManager(self)
        
        # Initialize Webcam Manager
        self.webcam_manager = WebcamManager(self)
        
        # Initialize Style Manager
        self.style_manager = StyleManager(self)
        
        # Initialize Widget Manager
        self.widget_manager = WidgetManager(self)
        
        # Store manager references for easy access
        self.managers = {
            'ui_components': self.ui_components,
            'parameter_manager': self.parameter_manager,
            'effect_manager': self.effect_manager,
            'preview_manager': self.preview_manager,
            'webcam_manager': self.webcam_manager,
            'style_manager': self.style_manager,
            'widget_manager': self.widget_manager
        }
        
        self.logger.info("All manager modules initialized!")
    
    def _expose_ui_components(self):
        """Expose UI components from UIComponents manager for compatibility."""
        try:
            ui_components = self.ui_components.get_all_ui_components()
            for name, component in ui_components.items():
                setattr(self, name, component)
            
            # Ensure critical components are available
            if not hasattr(self, 'params_layout') and hasattr(self.ui_components, 'params_layout'):
                self.params_layout = self.ui_components.params_layout
            
            self.logger.info("UI components exposed for compatibility")
        except Exception as e:
            self.logger.error(f"Error exposing UI components: {e}")
        
    def init_ui(self):
        """Initialize the professional user interface using UI Components manager."""
        self.setWindowTitle("Dream.OS Stream Software (Open Source)")
        self.setGeometry(50, 50, 1800, 1100)
        
        # Create all UI components using UI Components manager
        self.ui_components.create_central_preview()
        self.ui_components.create_effects_dock()
        self.ui_components.create_controls_dock()
        self.ui_components.create_properties_dock()
        self.ui_components.create_timeline_dock()
        self.ui_components.create_menu_bar()
        self.ui_components.create_main_toolbar()
        self.ui_components.create_status_bar()
        
        # Create effect buttons using Effect Manager
        self.effect_manager.create_effect_buttons()
        
        # Initialize preview timer using Preview Manager
        self.preview_manager.pre_initialize_timer()
        
    def setup_connections(self):
        """Setup all signal connections."""
        self.logger.info("Setting up signal connections...")
        
        # Connect UI components
        if hasattr(self, 'start_stop_btn'):
            self.start_stop_btn.clicked.connect(self.on_start_stop_clicked)
            
        if hasattr(self, 'snapshot_btn'):
            self.snapshot_btn.clicked.connect(self.on_snapshot_clicked)
            
        if hasattr(self, 'reset_btn'):
            self.reset_btn.clicked.connect(self.on_reset_clicked)
            
        if hasattr(self, 'fullscreen_btn'):
            self.fullscreen_btn.clicked.connect(self.on_fullscreen_clicked)
            
        if hasattr(self, 'record_btn'):
            self.record_btn.clicked.connect(self.on_record_clicked)
            
        if hasattr(self, 'stream_btn'):
            self.stream_btn.clicked.connect(self.on_stream_clicked)
            
        # Connect camera controls
        if hasattr(self, 'brightness_slider'):
            self.brightness_slider.valueChanged.connect(self.on_camera_parameter_changed)
            
        if hasattr(self, 'contrast_slider'):
            self.contrast_slider.valueChanged.connect(self.on_camera_parameter_changed)
            
        if hasattr(self, 'saturation_slider'):
            self.saturation_slider.valueChanged.connect(self.on_camera_parameter_changed)
            
        # Connect performance controls
        if hasattr(self, 'quality_combo'):
            self.quality_combo.currentTextChanged.connect(self.on_performance_changed)
            
        if hasattr(self, 'fps_combo'):
            self.fps_combo.currentTextChanged.connect(self.on_performance_changed)
            
        if hasattr(self, 'resolution_slider'):
            self.resolution_slider.valueChanged.connect(self.on_performance_changed)
            
        # Connect preview controls
        if hasattr(self, 'size_combo'):
            self.size_combo.currentTextChanged.connect(self.preview_manager.on_preview_size_changed)
            
        if hasattr(self, 'zoom_combo'):
            self.zoom_combo.currentTextChanged.connect(self.preview_manager.on_zoom_changed)
            
        # Connect effect manager signals
        # Note: effect_applied is a signal defined in the EffectManager class
        # We'll handle effect application through direct method calls instead
        
        self.logger.info("Signal connections setup complete!")
        
    def pre_load_everything(self):
        """Pre-load all components for instant startup."""
        self.logger.info("Pre-loading all components for instant startup...")
        
        # Start preview immediately with minimal loading
        self.start_instant_preview_minimal()
        
        # Load remaining components in background
        self.load_remaining_components_async()
        
        self.logger.info("Minimal pre-loading complete - starting instant preview!")
    
    def start_instant_preview_minimal(self):
        """Start preview with minimal loading for fastest startup."""
        try:
            self.logger.info("Starting instant preview with minimal loading...")
            
            # Initialize webcam service only (no style loading yet)
            if hasattr(self, 'webcam_manager'):
                self.webcam_manager.init_webcam_service()
                
                # Start webcam processing immediately without style
                self.webcam_manager.start_processing_minimal()
                
                # Start preview immediately
                if hasattr(self, 'preview_manager'):
                    self.preview_manager.start_preview()
                
                # Update UI to show "Stop" state
                if hasattr(self, 'start_stop_btn'):
                    self.start_stop_btn.setText("⏹️ Stop Processing")
                    self.start_stop_btn.setStyleSheet("""
                        QPushButton {
                            background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                                stop:0 #aa0000, stop:1 #880000);
                            border: 1px solid #aa0000;
                            border-radius: 6px;
                            font-size: 12px;
                            font-weight: bold;
                        }
                        QPushButton:hover {
                            background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                                stop:0 #cc0000, stop:1 #aa0000);
                        }
                        QPushButton:pressed {
                            background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                                stop:0 #880000, stop:1 #660000);
                        }
                    """)
                
                # Set processing state
                self.is_processing = True
                
                self.logger.info("Instant preview started successfully!")
                self.update_status("Live preview active")
                
        except Exception as e:
            self.logger.error(f"Error starting instant preview: {e}")
    
    def load_remaining_components_async(self):
        """Load remaining components asynchronously in background."""
        try:
            # Use QTimer to load remaining components after UI is shown
            from PyQt5.QtCore import QTimer
            timer = QTimer()
            timer.singleShot(100, self._load_remaining_components)
        except Exception as e:
            self.logger.error(f"Error setting up async loading: {e}")
    
    def _load_remaining_components(self):
        """Load remaining components after UI is shown."""
        try:
            self.logger.info("Loading remaining components in background...")
            
            # Load styles in background (lazy loading)
            self.style_manager.pre_load_styles_lazy()
            
            # Pre-initialize timer
            self.preview_manager.pre_initialize_timer()
            
            self.logger.info("Background component loading complete!")
            
        except Exception as e:
            self.logger.error(f"Error loading remaining components: {e}")
    
    def start_instant_preview(self):
        """Start preview immediately for instant video streaming."""
        try:
            self.logger.info("Starting instant preview for immediate video streaming...")
            
            # Start webcam processing with default settings
            if hasattr(self, 'webcam_manager'):
                # Get a default style for immediate preview
                default_style = None
                if hasattr(self, 'style_manager'):
                    try:
                        # Try to get "Original" style first, then fallback to any available style
                        default_style = self.style_manager.get_style("Original")
                        if not default_style:
                            # Get first available style
                            categories = self.style_manager.get_categories()
                            if categories:
                                first_category = list(categories.keys())[0]
                                if categories[first_category]:
                                    first_style_name = categories[first_category][0]
                                    default_style = self.style_manager.get_style(first_style_name)
                    except Exception as e:
                        self.logger.warning(f"Could not get default style: {e}")
                
                # Start webcam with default style
                self.webcam_manager.start_processing()
                
                # Set current style for preview
                if default_style:
                    self.current_style = default_style
                    self.pending_params = {}
                
                # Start preview immediately
                if hasattr(self, 'preview_manager'):
                    self.preview_manager.start_preview()
                
                # Update UI to show "Stop" state
                if hasattr(self, 'start_stop_btn'):
                    self.start_stop_btn.setText("⏹️ Stop Processing")
                    self.start_stop_btn.setStyleSheet("""
                        QPushButton {
                            background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                                stop:0 #aa0000, stop:1 #880000);
                            border: 1px solid #aa0000;
                            border-radius: 6px;
                            font-size: 12px;
                            font-weight: bold;
                        }
                        QPushButton:hover {
                            background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                                stop:0 #cc0000, stop:1 #aa0000);
                        }
                        QPushButton:pressed {
                            background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                                stop:0 #880000, stop:1 #660000);
                        }
                    """)
                
                # Set processing state
                self.is_processing = True
                
                self.logger.info("Instant preview started successfully!")
                self.update_status("Live preview active")
                
        except Exception as e:
            self.logger.error(f"Error starting instant preview: {e}")
        
    def on_start_stop_clicked(self):
        """Handle start/stop button click."""
        try:
            self.orchestrate_processing_toggle()
        except Exception as e:
            self.logger.error(f"Error in start/stop processing: {e}")
            
    def on_snapshot_clicked(self):
        """Handle snapshot button click."""
        try:
            self.update_status("Snapshot captured")
            self.logger.info("Snapshot captured")
        except Exception as e:
            self.logger.error(f"Error capturing snapshot: {e}")
            
    def on_reset_clicked(self):
        """Handle reset button click."""
        try:
            # Reset all parameters
            self.parameter_manager.clear_embedded_parameter_widgets()
            self.current_style = None
            self.pending_params = {}
            
            # Update UI
            if hasattr(self, 'current_effect_label'):
                self.current_effect_label.setText("None")
                
            self.update_status("All effects reset")
            self.logger.info("All effects reset")
            
        except Exception as e:
            self.logger.error(f"Error resetting effects: {e}")
            
    def on_fullscreen_clicked(self):
        """Handle fullscreen button click."""
        try:
            if self.isFullScreen():
                self.showNormal()
            else:
                self.showFullScreen()
            self.logger.info("Fullscreen toggled")
        except Exception as e:
            self.logger.error(f"Error toggling fullscreen: {e}")
            
    def on_record_clicked(self):
        """Handle record button click."""
        try:
            self.update_status("Recording started")
            self.logger.info("Recording started")
        except Exception as e:
            self.logger.error(f"Error starting recording: {e}")
            
    def on_stream_clicked(self):
        """Handle stream button click."""
        try:
            self.update_status("Streaming started")
            self.logger.info("Streaming started")
        except Exception as e:
            self.logger.error(f"Error starting stream: {e}")
            
    def on_camera_parameter_changed(self):
        """Handle camera parameter changes."""
        try:
            # Update camera adjustment labels
            if hasattr(self, 'brightness_slider') and hasattr(self, 'brightness_label'):
                self.brightness_label.setText(f"Brightness: {self.brightness_slider.value()}")
                
            if hasattr(self, 'contrast_slider') and hasattr(self, 'contrast_label'):
                contrast_val = self.contrast_slider.value() / 100.0
                self.contrast_label.setText(f"Contrast: {contrast_val:.1f}")
                
            if hasattr(self, 'saturation_slider') and hasattr(self, 'saturation_label'):
                saturation_val = self.saturation_slider.value() / 100.0
                self.saturation_label.setText(f"Saturation: {saturation_val:.1f}")
                
        except Exception as e:
            self.logger.error(f"Error handling camera parameter change: {e}")
            
    def on_performance_changed(self):
        """Handle performance setting changes."""
        try:
            # Update performance labels
            if hasattr(self, 'resolution_slider') and hasattr(self, 'resolution_label'):
                resolution_val = self.resolution_slider.value()
                self.resolution_label.setText(f"Resolution: {resolution_val}%")
                
            # Update preview manager performance settings
            self.preview_manager.on_performance_changed()
            
        except Exception as e:
            self.logger.error(f"Error handling performance change: {e}")
            
    def on_effect_applied(self, effect_name):
        """Handle effect application."""
        try:
            self.effects_history.append(effect_name)
            self.update_status(f"Applied effect: {effect_name}")
            self.logger.info(f"Effect applied: {effect_name}")
        except Exception as e:
            self.logger.error(f"Error handling effect application: {e}")
            
    def get_manager(self, manager_name):
        """Get a specific manager instance."""
        return self.managers.get(manager_name)
        
    def get_all_managers(self):
        """Get all manager instances."""
        return self.managers.copy()
        
    def orchestrate_effect_application(self, effect_name):
        """Orchestrate the complete effect application process."""
        try:
            self.logger.info(f"Orchestrating effect application: {effect_name}")
            
            # 1. Apply effect through effect manager
            self.effect_manager.apply_effect(effect_name)
            
            # 2. Update preview if processing
            if self.is_processing:
                self.preview_manager.update_preview()
                
            # 3. Update status
            self.update_status(f"Effect applied: {effect_name}")
            
        except Exception as e:
            self.logger.error(f"Error orchestrating effect application: {e}")
            
    def orchestrate_parameter_change(self, parameter_name, value):
        """Orchestrate parameter change across all managers."""
        try:
            self.logger.info(f"Orchestrating parameter change: {parameter_name} = {value}")
            
            # 1. Update parameter manager
            self.parameter_manager.on_embedded_parameter_changed(parameter_name, value)
            
            # 2. Update preview if processing
            if self.is_processing:
                self.preview_manager.update_preview()
                
            # 3. Update status
            self.update_status(f"Parameter updated: {parameter_name}")
            
        except Exception as e:
            self.logger.error(f"Error orchestrating parameter change: {e}")
            
    def orchestrate_processing_toggle(self):
        """Orchestrate processing start/stop across all managers."""
        try:
            if not self.is_processing:
                # Start processing
                self.logger.info("Orchestrating processing start")
                self.is_processing = True
                self.webcam_manager.start_processing()
                self.preview_manager.start_preview()
                
                # Update UI to show "Stop" state
                if hasattr(self, 'start_stop_btn'):
                    self.start_stop_btn.setText("⏹️ Stop Processing")
                    self.start_stop_btn.setStyleSheet("""
                        QPushButton {
                            background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                                stop:0 #aa0000, stop:1 #880000);
                            border: 1px solid #aa0000;
                            border-radius: 6px;
                            font-size: 12px;
                            font-weight: bold;
                        }
                        QPushButton:hover {
                            background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                                stop:0 #cc0000, stop:1 #aa0000);
                        }
                        QPushButton:pressed {
                            background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                                stop:0 #880000, stop:1 #660000);
                        }
                    """)
                
                self.update_status("Processing started")
            else:
                # Stop processing
                self.logger.info("Orchestrating processing stop")
                self.is_processing = False
                self.webcam_manager.stop_processing()
                self.preview_manager.stop_preview()
                
                # Update UI to show "Start" state
                if hasattr(self, 'start_stop_btn'):
                    self.start_stop_btn.setText("▶️ Start Processing")
                    self.start_stop_btn.setStyleSheet("""
                        QPushButton {
                            background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                                stop:0 #00aa00, stop:1 #008800);
                            border: 1px solid #00aa00;
                            border-radius: 6px;
                            font-size: 12px;
                            font-weight: bold;
                        }
                        QPushButton:hover {
                            background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                                stop:0 #00cc00, stop:1 #00aa00);
                        }
                        QPushButton:pressed {
                            background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                                stop:0 #008800, stop:1 #006600);
                        }
                    """)
                
                self.update_status("Processing stopped")
                
        except Exception as e:
            self.logger.error(f"Error orchestrating processing toggle: {e}")
    
    def on_preview_size_changed(self):
        """Handle preview size changes."""
        try:
            self.logger.info("Preview size changed")
            # Update preview area if needed
            if hasattr(self, 'preview_label'):
                self.preview_manager.update_preview_size()
        except Exception as e:
            self.logger.error(f"Error handling preview size change: {e}")
    
    def on_variant_changed(self):
        """Handle effect variant changes."""
        try:
            if hasattr(self, 'effect_variant_combo'):
                variant = self.effect_variant_combo.currentText()
                self.logger.info(f"Effect variant changed to: {variant}")
                self.style_manager.set_current_variant(variant)
                self.update_status(f"Variant: {variant}")
        except Exception as e:
            self.logger.error(f"Error handling variant change: {e}")
            
    def update_status(self, message):
        """Update the status bar with a message."""
        try:
            if hasattr(self, 'status_label'):
                self.status_label.setText(message)
            self.logger.info(message)
        except Exception as e:
            self.logger.error(f"Error updating status: {e}")
            
    def closeEvent(self, event):
        """Handle application close event."""
        try:
            # Clean up all managers
            self.preview_manager.cleanup()
            self.webcam_manager.cleanup()
            self.widget_manager.cleanup()
            
            self.logger.info("Application closing - cleanup complete")
            event.accept()
            
        except Exception as e:
            self.logger.error(f"Error during cleanup: {e}")
            event.accept()


def main():
    """Main entry point for the modular V2 application."""
    app = QApplication(sys.argv)
    
    # Setup logging
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    
    # Create and show the main window
    window = ProfessionalV2MainWindow()
    window.show()
    
    # Start the application
    sys.exit(app.exec_())


if __name__ == "__main__":
    main() 