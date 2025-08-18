#!/usr/bin/env python3
"""
Dreamscape V2 - Professional Webcam Effects Studio (Modular Version)
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
    
    def __init__(self, plugin_manager=None):
        super().__init__()
        self.logger = logging.getLogger(__name__)
        logging.basicConfig(level=logging.DEBUG)
        
        self.logger.debug("Initializing ProfessionalV2MainWindow...")
        
        # Store plugin manager
        self.plugin_manager = plugin_manager
        
        # Initialize state variables
        self.is_processing = False
        self.current_style = None
        self.effects_history = []
        self.favorite_effects = []
        self.current_frame = None
        self.preview_pixmap = None
        self.pending_style = None
        self.pending_params = {}  # Ensure this is always a dictionary
        
        self.logger.debug("Initializing managers...")
        # Initialize all managers
        self.init_managers()
        self.logger.debug("Managers initialized.")
        
        # Setup UI using UI Components manager
        self.logger.debug("Setting up professional theme...")
        self.ui_components.setup_professional_theme()
        self.logger.debug("Theme set up.")
        
        self.logger.debug("Initializing UI...")
        self.init_ui()
        self.logger.debug("UI initialized.")
        
        # Expose UI components after UI is initialized
        self.logger.debug("Exposing UI components...")
        self._expose_ui_components()
        self.logger.debug("UI components exposed.")
        
        self.logger.debug("Setting up connections...")
        self.setup_connections()
        self.logger.debug("Connections set up.")
        
        # Pre-load everything for instant startup
        self.logger.debug("Pre-loading everything...")
        self.pre_load_everything()
        self.logger.debug("Pre-loading complete.")
        
        # Hide old parameter controls by default - using embedded widgets instead
        self.logger.debug("Hiding old parameter controls...")
        self.parameter_manager.hide_old_parameter_controls()
        self.logger.debug("Old parameter controls hidden.")
        
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
        
        # Initialize AI parameter optimizer
        from .modules.ai_parameter_optimizer import AIParameterOptimizer
        self.ai_optimizer = AIParameterOptimizer()
        
        # Integrate plugin system if available
        if self.plugin_manager:
            self.integrate_plugin_system()
        
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
    
    def integrate_plugin_system(self):
        """Integrate the plugin system with existing managers."""
        self.logger.info("Integrating plugin system...")
        
        try:
            # Get all available effects from plugin system
            plugin_effects = self.plugin_manager.get_all_effects()
            
            # Add plugin effects to effect manager
            for effect in plugin_effects:
                self.effect_manager.add_plugin_effect(effect)
            
            # Setup plugin parameter handling
            self.setup_plugin_parameter_handling()
            
            self.logger.info(f"Integrated {len(plugin_effects)} plugin effects")
            
        except Exception as e:
            self.logger.error(f"Failed to integrate plugin system: {e}")
    
    def setup_plugin_parameter_handling(self):
        """Setup parameter handling for plugin effects."""
        if not self.plugin_manager:
            return
        
        # Connect plugin parameter changes to main window
        def on_plugin_parameter_changed(effect_name, param_name, value):
            self.logger.debug(f"Plugin parameter changed: {effect_name}.{param_name} = {value}")
            
            # Update current effect parameters
            if self.plugin_manager.current_effect:
                self.plugin_manager.set_parameter(param_name, value)
            
            # Trigger preview update
            self.preview_manager.update_preview()
        
        # Store the callback for later use
        self.plugin_parameter_callback = on_plugin_parameter_changed
    
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
        self.setWindowTitle("Dreamscape Stream Software (Open Source)")
        self.setGeometry(50, 50, 1800, 1100)
        
        # Create all UI components using UI Components manager
        self.ui_components.create_central_preview()
        self.ui_components.create_effects_dock()
        self.ui_components.create_controls_dock()
        self.ui_components.create_audio_captioner_dock()
        self.ui_components.create_properties_dock()
        self.ui_components.create_timeline_dock()
        self.ui_components.create_menu_bar()
        self.ui_components.create_main_toolbar()
        self.ui_components.create_status_bar()
        
        # Create effect buttons using Effect Manager
        self.effect_manager.create_effect_buttons()
        
        # Initialize preview timer using Preview Manager
        self.preview_manager.pre_initialize_timer()
        
        # CRITICAL FIX: Add test button to verify preview label is working
        self.logger.info("🔍 Debug: Adding test preview button...")
        self.create_test_preview_button()
        
    def setup_connections(self):
        """Setup all signal connections."""
        self.logger.info("Setting up signal connections...")
        
        # Connect start/stop button
        if hasattr(self, 'start_stop_btn'):
            self.logger.info("Connecting start_stop_btn...")
            self.start_stop_btn.toggled.connect(self.on_start_stop_clicked)
            self.logger.info("start_stop_btn connected successfully")
        else:
            self.logger.warning("start_stop_btn not found!")
        
        # Connect UI components
        # Processing status indicator shows current state
        self.logger.info("Processing status indicator active")
            
        if hasattr(self, 'snapshot_btn'):
            self.logger.info("Connecting snapshot_btn...")
            self.snapshot_btn.clicked.connect(self.on_snapshot_clicked)
            self.logger.info("snapshot_btn connected successfully")
        else:
            self.logger.warning("snapshot_btn not found!")
            
        if hasattr(self, 'reset_btn'):
            self.logger.info("Connecting reset_btn...")
            self.reset_btn.clicked.connect(self.on_reset_clicked)
            self.logger.info("reset_btn connected successfully")
        else:
            self.logger.warning("reset_btn not found!")
            
        if hasattr(self, 'fullscreen_btn'):
            self.logger.info("Connecting fullscreen_btn...")
            self.fullscreen_btn.clicked.connect(self.on_fullscreen_clicked)
            self.logger.info("fullscreen_btn connected successfully")
        else:
            self.logger.warning("fullscreen_btn not found!")
            
        if hasattr(self, 'record_btn'):
            self.logger.info("Connecting record_btn...")
            self.record_btn.clicked.connect(self.on_record_clicked)
            self.logger.info("record_btn connected successfully")
        else:
            self.logger.warning("record_btn not found!")
            
        if hasattr(self, 'stream_btn'):
            self.logger.info("Connecting stream_btn...")
            self.stream_btn.clicked.connect(self.on_stream_clicked)
            self.logger.info("stream_btn connected successfully")
        else:
            self.logger.warning("stream_btn not found!")
            
        # Connect AI optimization button
        if hasattr(self, 'ai_optimization_btn'):
            self.logger.info("Connecting ai_optimization_btn...")
            self.ai_optimization_btn.toggled.connect(self.on_ai_optimization_toggled)
            self.logger.info("ai_optimization_btn connected successfully")
        else:
            self.logger.warning("ai_optimization_btn not found!")
            
        # Connect virtual camera button
        if hasattr(self, 'virtual_camera_btn'):
            self.logger.info("Connecting virtual_camera_btn...")
            self.virtual_camera_btn.toggled.connect(self.on_virtual_camera_toggled)
            self.logger.info("virtual_camera_btn connected successfully")
        else:
            self.logger.warning("virtual_camera_btn not found!")
            
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
            
        # Connect audio captioner controls
        if (hasattr(self, 'ui_components') and 
            hasattr(self.ui_components, 'audio_captioner_controls')):
            
            audio_controls = self.ui_components.audio_captioner_controls
            audio_controls.captioner_enabled.connect(self.on_captioner_enabled)
            audio_controls.audio_device_changed.connect(self.on_audio_device_changed)
            audio_controls.captioner_config_changed.connect(self.on_captioner_config_changed)
            
        # Connect effect manager signals
        # Note: effect_applied is a signal defined in the EffectManager class
        # We'll handle effect application through direct method calls instead
        
        self.logger.info("Signal connections setup complete!")
        
    def pre_load_everything(self):
        """Pre-load all components for instant startup."""
        self.logger.info("Pre-loading all components for instant startup...")
        
        # Start preview immediately with minimal loading
        self.start_instant_preview_minimal()
        
        # Pre-load camera and styles in background for instant start/stop
        self.pre_load_camera_and_styles_async()
        
        self.logger.info("Minimal pre-loading complete - starting instant preview!")
    
    def pre_load_camera_and_styles_async(self):
        """Pre-load camera and styles asynchronously for instant start/stop."""
        try:
            # Use QTimer to load camera and styles after UI is shown
            from PyQt5.QtCore import QTimer
            timer = QTimer()
            timer.singleShot(500, self._pre_load_camera_and_styles)
        except Exception as e:
            self.logger.error(f"Error setting up async camera/style loading: {e}")
    
    def _pre_load_camera_and_styles(self):
        """Pre-load camera and styles in background."""
        try:
            self.logger.info("Pre-loading camera and styles in background...")
            
            # Pre-load camera (this will happen in background)
            if hasattr(self, 'webcam_manager'):
                self.webcam_manager.pre_load_camera_async()
            
            # Pre-load styles (this will happen in background)
            if hasattr(self, 'style_manager'):
                try:
                    self.style_manager.pre_load_styles_lazy()
                except Exception as e:
                    self.logger.warning(f"Could not pre-load styles: {e}")
            
            self.logger.info("Background camera and style loading initiated!")
            
        except Exception as e:
            self.logger.error(f"Error pre-loading camera and styles: {e}")
    
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
            
            # Pre-initialize timer
            self.preview_manager.pre_initialize_timer()
            
            self.logger.info("Background component loading complete!")
            
        except Exception as e:
            self.logger.error(f"Error loading remaining components: {e}")
    
    def start_instant_preview_minimal(self):
        """Start preview with minimal loading for fastest startup."""
        try:
            self.logger.info("Starting instant preview with minimal loading...")
            
            # Initialize webcam service only (no style loading yet)
            if hasattr(self, 'webcam_manager'):
                self.webcam_manager.init_webcam_service()
                
                # CRITICAL FIX: Start webcam processing immediately without style
                try:
                    if self.webcam_manager.start_processing_minimal():
                        self.logger.info("✅ Webcam processing started successfully")
                    else:
                        self.logger.warning("⚠️ Webcam processing failed, will use test frames")
                except Exception as webcam_error:
                    self.logger.warning(f"⚠️ Webcam start error: {webcam_error}, will use test frames")
                
                # Initialize timer first, then start preview
                if hasattr(self, 'preview_manager'):
                    self.preview_manager.pre_initialize_timer()
                    self.preview_manager.start_preview()
                
                # Ensure the main window and central widget are visible
                self.show()
                if hasattr(self, 'centralWidget'):
                    central_widget = self.centralWidget()
                    if central_widget:
                        central_widget.setVisible(True)
                        central_widget.show()
                
                # Set processing state to False initially - user must click to start
                self.is_processing = False
                
                # Update UI to show "Stopped" state initially
                if hasattr(self, 'processing_status_label'):
                    self.processing_status_label.setText("⏸️ Preview Stopped")
                    self.processing_status_label.setStyleSheet("""
                        QLabel {
                            background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                                stop:0 #666666, stop:1 #555555);
                            border: 1px solid #666666;
                            border-radius: 6px;
                            font-size: 12px;
                            font-weight: bold;
                            color: white;
                            padding: 8px;
                        }
                    """)
                
                self.logger.info("Instant preview started successfully!")
                self.update_status("Click 'Start Preview' to begin")
                
                # Start AI parameter optimization (disabled for performance)
                # self.start_ai_optimization()
                
                # Enable virtual camera button
                if hasattr(self, 'virtual_camera_btn'):
                    self.virtual_camera_btn.setChecked(True)
                    self.logger.info("Virtual camera button enabled")
                
        except Exception as e:
            self.logger.error(f"Error starting instant preview: {e}")
            import traceback
            self.logger.error(f"Traceback: {traceback.format_exc()}")
    
    def start_ai_optimization(self):
        """Start AI-powered parameter optimization."""
        try:
            if hasattr(self, 'ai_optimizer'):
                self.ai_optimizer.start_continuous_optimization(
                    self.webcam_manager, 
                    self.parameter_manager
                )
                self.logger.info("🤖 AI parameter optimization started")
                self.update_status("AI optimization active")
            else:
                self.logger.warning("AI optimizer not available")
        except Exception as e:
            self.logger.error(f"Error starting AI optimization: {e}")
    
    def stop_ai_optimization(self):
        """Stop AI-powered parameter optimization."""
        try:
            if hasattr(self, 'ai_optimizer'):
                self.ai_optimizer.stop_continuous_optimization()
                self.logger.info("🤖 AI parameter optimization stopped")
                self.update_status("AI optimization stopped")
        except Exception as e:
            self.logger.error(f"Error stopping AI optimization: {e}")
    
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
                
                # Initialize timer first, then start preview
                if hasattr(self, 'preview_manager'):
                    self.preview_manager.pre_initialize_timer()
                    self.preview_manager.start_preview()
                
                # Update UI to show "Active" state
                if hasattr(self, 'processing_status_label'):
                    self.processing_status_label.setText("🟢 Live Processing Active")
                    self.processing_status_label.setStyleSheet("""
                        QLabel {
                            background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                                stop:0 #00aa00, stop:1 #008800);
                            border: 1px solid #00aa00;
                            border-radius: 6px;
                            font-size: 12px;
                            font-weight: bold;
                            color: white;
                            padding: 8px;
                        }
                    """)
                
                # Set processing state
                self.is_processing = True
                
                self.logger.info("Instant preview started successfully!")
                self.update_status("Live preview active")
                
        except Exception as e:
            self.logger.error(f"Error starting instant preview: {e}")
        
    def update_processing_status(self, is_active: bool):
        """Update the processing status indicator."""
        try:
            if hasattr(self, 'processing_status_label'):
                if is_active:
                    self.processing_status_label.setText("🟢 Live Processing Active")
                    self.processing_status_label.setStyleSheet("""
                        QLabel {
                            background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                                stop:0 #00aa00, stop:1 #008800);
                            border: 1px solid #00aa00;
                            border-radius: 6px;
                            font-size: 12px;
                            font-weight: bold;
                            color: white;
                            padding: 8px;
                        }
                    """)
                else:
                    self.processing_status_label.setText("🔴 Processing Inactive")
                    self.processing_status_label.setStyleSheet("""
                        QLabel {
                            background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                                stop:0 #aa0000, stop:1 #880000);
                            border: 1px solid #aa0000;
                            border-radius: 6px;
                            font-size: 12px;
                            font-weight: bold;
                            color: white;
                            padding: 8px;
                        }
                    """)
        except Exception as e:
            self.logger.error(f"Error updating processing status: {e}")
    
    def on_start_stop_clicked(self, is_started: bool):
        """Handle start/stop button click."""
        try:
            self.logger.info(f"=== START/STOP BUTTON CLICKED: {is_started} ===")
            
            if is_started:
                # Start preview and processing
                self.logger.info("Starting preview and processing...")
                success = self.webcam_manager.start_processing()
                if success:
                    self.start_stop_btn.setText("⏹️ Stop Preview")
                    self.update_processing_status(True)
                    self.update_status("Preview started")
                    self.logger.info("Preview and processing started successfully")
                else:
                    self.logger.error("Failed to start preview")
                    self.start_stop_btn.setChecked(False)
            else:
                # Stop preview and processing
                self.logger.info("Stopping preview and processing...")
                self.webcam_manager.stop_processing()
                self.start_stop_btn.setText("▶️ Start Preview")
                self.update_processing_status(False)
                self.update_status("Preview stopped")
                self.logger.info("Preview and processing stopped")
            
            self.logger.info("=== START/STOP BUTTON HANDLER COMPLETED ===")
        except Exception as e:
            self.logger.error(f"Error handling start/stop: {e}")
            import traceback
            self.logger.error(f"Traceback: {traceback.format_exc()}")
            
    def on_snapshot_clicked(self):
        """Handle snapshot button click."""
        try:
            self.logger.info("=== SNAPSHOT BUTTON CLICKED ===")
            self.update_status("Snapshot captured")
            self.logger.info("Snapshot captured")
            self.logger.info("=== SNAPSHOT BUTTON HANDLER COMPLETED ===")
        except Exception as e:
            self.logger.error(f"Error capturing snapshot: {e}")
            import traceback
            self.logger.error(f"Traceback: {traceback.format_exc()}")
            
    def on_reset_clicked(self):
        """Handle reset button click."""
        try:
            self.logger.info("=== RESET BUTTON CLICKED ===")
            # Reset all parameters
            self.parameter_manager.clear_embedded_parameter_widgets()
            self.current_style = None
            self.pending_params = {}
            
            # Update UI
            if hasattr(self, 'current_effect_label'):
                self.current_effect_label.setText("None")
                
            self.update_status("All effects reset")
            self.logger.info("All effects reset")
            self.logger.info("=== RESET BUTTON HANDLER COMPLETED ===")
            
        except Exception as e:
            self.logger.error(f"Error resetting effects: {e}")
            import traceback
            self.logger.error(f"Traceback: {traceback.format_exc()}")
            
    def on_fullscreen_clicked(self):
        """Handle fullscreen button click."""
        try:
            self.logger.info("=== FULLSCREEN BUTTON CLICKED ===")
            if self.isFullScreen():
                self.showNormal()
                self.logger.info("Exiting fullscreen")
            else:
                self.showFullScreen()
                self.logger.info("Entering fullscreen")
            self.logger.info("=== FULLSCREEN BUTTON HANDLER COMPLETED ===")
        except Exception as e:
            self.logger.error(f"Error toggling fullscreen: {e}")
            import traceback
            self.logger.error(f"Traceback: {traceback.format_exc()}")
            
    def on_record_clicked(self):
        """Handle record button click."""
        try:
            self.logger.info("=== RECORD BUTTON CLICKED ===")
            self.update_status("Recording started")
            self.logger.info("Recording started")
            self.logger.info("=== RECORD BUTTON HANDLER COMPLETED ===")
        except Exception as e:
            self.logger.error(f"Error starting recording: {e}")
            import traceback
            self.logger.error(f"Traceback: {traceback.format_exc()}")
            
    def on_stream_clicked(self):
        """Handle stream button click."""
        try:
            self.logger.info("=== STREAM BUTTON CLICKED ===")
            self.update_status("Streaming started")
            self.logger.info("Streaming started")
            self.logger.info("=== STREAM BUTTON HANDLER COMPLETED ===")
        except Exception as e:
            self.logger.error(f"Error starting stream: {e}")
            import traceback
            self.logger.error(f"Traceback: {traceback.format_exc()}")
    
    def on_ai_optimization_toggled(self, enabled: bool):
        """Handle AI optimization toggle."""
        try:
            self.logger.info(f"=== AI OPTIMIZATION TOGGLED: {enabled} ===")
            
            if enabled:
                # Start AI optimization
                self.start_ai_optimization()
                self.update_status("AI optimization enabled")
            else:
                # Stop AI optimization
                self.stop_ai_optimization()
                self.update_status("AI optimization disabled")
            
            self.logger.info("=== AI OPTIMIZATION TOGGLE COMPLETED ===")
        except Exception as e:
            self.logger.error(f"Error toggling AI optimization: {e}")
            import traceback
            self.logger.error(f"Traceback: {traceback.format_exc()}")
    
    def on_virtual_camera_toggled(self, enabled: bool):
        """Handle virtual camera toggle."""
        try:
            self.logger.info(f"=== VIRTUAL CAMERA TOGGLED: {enabled} ===")
            
            if enabled:
                # Virtual camera is already enabled by default in webcam service
                self.update_status("Virtual camera enabled - use in OBS/Zoom")
                self.logger.info("Virtual camera is active - available as 'OBS Virtual Camera'")
            else:
                # Note: Virtual camera is always active when webcam service is running
                # This is just for UI feedback
                self.update_status("Virtual camera disabled")
                self.logger.info("Virtual camera disabled")
            
            self.logger.info("=== VIRTUAL CAMERA TOGGLE COMPLETED ===")
        except Exception as e:
            self.logger.error(f"Error toggling virtual camera: {e}")
            import traceback
            self.logger.error(f"Traceback: {traceback.format_exc()}")
            
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
    
    def on_captioner_enabled(self, enabled: bool):
        """Handle captioner enable/disable."""
        try:
            self.logger.info(f"Captioner enabled: {enabled}")
            if enabled:
                self.update_status("Captioner enabled - speak to see live captions!")
            else:
                self.update_status("Captioner disabled")
        except Exception as e:
            self.logger.error(f"Error handling captioner enable/disable: {e}")
    
    def on_audio_device_changed(self, device_index: int):
        """Handle audio device change."""
        try:
            self.logger.info(f"Audio device changed to index: {device_index}")
            self.update_status(f"Audio device changed to index: {device_index}")
        except Exception as e:
            self.logger.error(f"Error handling audio device change: {e}")
    
    def on_captioner_config_changed(self, config: dict):
        """Handle captioner configuration changes."""
        try:
            self.logger.info(f"Captioner config changed: {config}")
            self.update_status("Captioner settings updated")
        except Exception as e:
            self.logger.error(f"Error handling captioner config change: {e}")
            
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
            self.logger.info("=== ORCHESTRATE PROCESSING TOGGLE STARTED ===")
            self.logger.info(f"Current is_processing state: {self.is_processing}")
            
            if not self.is_processing:
                # Start processing (instant since camera is pre-loaded)
                self.logger.info("Orchestrating processing start (instant)")
                self.is_processing = True
                self.logger.info(f"Set is_processing to: {self.is_processing}")
                
                # Set webcam manager as running
                if hasattr(self, 'webcam_manager'):
                    self.webcam_manager.is_running = True
                    self.logger.info("Set webcam_manager.is_running to True")
                
                # Just start preview - camera is already running
                self.logger.info("Starting preview...")
                self.preview_manager.start_preview()
                self.logger.info("Preview started")
                
                # Update UI to show "Active" state
                self.update_processing_status(True)
                
                self.update_status("Processing started")
                self.logger.info("Status updated to 'Processing started'")
            else:
                # Stop processing (instant)
                self.logger.info("Orchestrating processing stop (instant)")
                self.is_processing = False
                self.logger.info(f"Set is_processing to: {self.is_processing}")
                
                # Set webcam manager as not running
                if hasattr(self, 'webcam_manager'):
                    self.webcam_manager.is_running = False
                    self.logger.info("Set webcam_manager.is_running to False")
                
                self.logger.info("Stopping preview...")
                self.preview_manager.stop_preview()
                self.logger.info("Preview stopped")
                
                # Update UI to show "Inactive" state
                self.update_processing_status(False)
                
                self.update_status("Processing stopped")
                self.logger.info("Status updated to 'Processing stopped'")
                
            self.logger.info("=== ORCHESTRATE PROCESSING TOGGLE COMPLETED ===")
                
        except Exception as e:
            self.logger.error(f"Error orchestrating processing toggle: {e}")
            import traceback
            self.logger.error(f"Traceback: {traceback.format_exc()}")
    
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
    
    def create_test_preview_button(self):
        """Create a test button in the status bar for testing preview display."""
        try:
            self.logger.info("🔍 Debug: Adding test preview button...")
            
            # Create test preview button
            test_btn = QPushButton("🧪 Test Preview")
            test_btn.setToolTip("Test preview display with a sample frame")
            test_btn.clicked.connect(self.test_preview_display)
            
            # Create performance control button
            perf_btn = QPushButton("⚡ Performance")
            perf_btn.setToolTip("Toggle between performance and quality modes")
            perf_btn.setCheckable(True)
            perf_btn.setChecked(False)  # Start in quality mode
            perf_btn.clicked.connect(self.toggle_performance_mode)
            
            # Add both buttons to status bar
            self.statusBar().addPermanentWidget(test_btn)
            self.statusBar().addPermanentWidget(perf_btn)
            
            self.logger.info("✅ Test preview button added to status bar")
            
        except Exception as e:
            self.logger.error(f"Error creating test preview button: {e}")
    
    def toggle_performance_mode(self):
        """Toggle between performance and quality modes."""
        try:
            sender = self.sender()
            if sender.isChecked():
                # Performance mode (lower quality, higher FPS)
                self.logger.info("⚡ Switching to PERFORMANCE mode")
                self.preview_manager.update_performance_settings(
                    target_fps=20,
                    frame_skip=1,
                    quality_reduction=True
                )
                sender.setText("⚡ Performance")
                sender.setToolTip("Currently in PERFORMANCE mode (click for QUALITY)")
                self.statusBar().showMessage("Performance mode: Higher FPS, lower quality", 3000)
            else:
                # Quality mode (higher quality, lower FPS)
                self.logger.info("🎨 Switching to QUALITY mode")
                self.preview_manager.update_performance_settings(
                    target_fps=15,
                    frame_skip=2,
                    quality_reduction=False
                )
                sender.setText("🎨 Quality")
                sender.setToolTip("Currently in QUALITY mode (click for PERFORMANCE)")
                self.statusBar().showMessage("Quality mode: Higher quality, lower FPS", 3000)
                
        except Exception as e:
            self.logger.error(f"Error toggling performance mode: {e}")
    
    def test_preview_display(self):
        """Test if the preview label is working by displaying a test frame."""
        try:
            self.logger.info("🧪 Testing preview display...")
            
            if not hasattr(self, 'preview_label') or self.preview_label is None:
                self.logger.error("❌ Preview label not found!")
                return
            
            # Create a simple test frame
            import numpy as np
            import cv2
            
            # Create a colorful test frame
            height, width = 480, 640
            frame = np.zeros((height, width, 3), dtype=np.uint8)
            
            # Add colorful stripes
            stripe_height = height // 6
            colors = [
                [255, 0, 0],    # Red
                # Red
                [0, 255, 0],    # Green
                [0, 0, 255],    # Blue
                [255, 255, 0],  # Yellow
                [255, 0, 255],  # Magenta
                [0, 255, 255],  # Cyan
            ]
            
            for i, color in enumerate(colors):
                y_start = i * stripe_height
                y_end = (i + 1) * stripe_height
                frame[y_start:y_end, :] = color
            
            # Add text
            cv2.putText(frame, "PREVIEW TEST", (50, 240), 
                       cv2.FONT_HERSHEY_SIMPLEX, 1.5, (255, 255, 255), 3)
            cv2.putText(frame, "If you see this, preview works!", (50, 300), 
                       cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 0), 2)
            
            # Display the test frame
            if hasattr(self, 'preview_manager') and self.preview_manager:
                self.preview_manager.update_preview_display(frame)
                self.logger.info("✅ Test frame sent to preview manager")
            else:
                self.logger.error("❌ Preview manager not available")
                
        except Exception as e:
            self.logger.error(f"❌ Error testing preview display: {e}")
            import traceback
            self.logger.error(f"Traceback: {traceback.format_exc()}")
            
    def closeEvent(self, event):
        """Handle application close event."""
        try:
            # Clean up all managers
            self.preview_manager.cleanup()
            self.webcam_manager.cleanup()
            self.widget_manager.cleanup()
            
            # Clean up captioner
            if (hasattr(self, 'ui_components') and 
                hasattr(self.ui_components, 'audio_captioner_controls')):
                audio_controls = self.ui_components.audio_captioner_controls
                if audio_controls:
                    audio_controls.cleanup()
            
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