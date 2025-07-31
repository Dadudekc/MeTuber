"""
Audio and Captioner Controls Component

Provides UI controls for audio capture and speech-to-text captioner functionality.
"""

import logging
from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QFormLayout, QGroupBox,
    QPushButton, QComboBox, QSlider, QLabel, QCheckBox, QSpinBox,
    QDoubleSpinBox, QProgressBar, QFrame
)
from PyQt5.QtCore import Qt, pyqtSignal, QTimer
from PyQt5.QtGui import QFont, QPalette, QColor

# Try to import captioner components, handle missing dependencies gracefully
try:
    from src.captioner import CaptionerManager, CaptionerConfig
    CAPTIONER_AVAILABLE = True
except ImportError as e:
    print(f"Warning: Captioner dependencies not available: {e}")
    print("Audio and captioner features will be disabled.")
    CAPTIONER_AVAILABLE = False
    # Create dummy classes for compatibility
    class CaptionerConfig:
        def __init__(self):
            self.enabled = False
    class CaptionerManager:
        def __init__(self, config=None):
            pass


class AudioCaptionerControls(QWidget):
    """Audio and captioner control panel."""
    
    # Signals
    captioner_enabled = pyqtSignal(bool)
    audio_device_changed = pyqtSignal(int)
    captioner_config_changed = pyqtSignal(dict)
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.logger = logging.getLogger(__name__)
        
        # Captioner manager
        self.captioner_manager = None
        self.captioner_config = CaptionerConfig()
        
        # UI state
        self.is_captioner_active = False
        self.available_audio_devices = []
        self.available_engines = ["whisper", "google", "dummy"]
        
        # UI components
        self.captioner_enable_checkbox = None
        self.audio_device_combo = None
        self.engine_combo = None
        self.language_combo = None
        self.font_size_spin = None
        self.font_color_combo = None
        self.background_opacity_slider = None
        self.typing_speed_slider = None
        self.show_duration_slider = None
        self.audio_level_progress = None
        self.status_label = None
        
        # Timer for audio level updates
        self.audio_level_timer = QTimer()
        self.audio_level_timer.timeout.connect(self.update_audio_level)
        
        self.init_ui()
        self.setup_connections()
        
    def init_ui(self):
        """Initialize the user interface."""
        layout = QVBoxLayout(self)
        layout.setSpacing(10)
        layout.setContentsMargins(10, 10, 10, 10)
        
        # Audio Device Selection
        audio_group = QGroupBox("🎤 Audio Input")
        audio_layout = QFormLayout(audio_group)
        
        self.audio_device_combo = QComboBox()
        self.audio_device_combo.addItem("Default Microphone", -1)
        audio_layout.addRow("Device:", self.audio_device_combo)
        
        self.audio_level_progress = QProgressBar()
        self.audio_level_progress.setRange(0, 100)
        self.audio_level_progress.setValue(0)
        self.audio_level_progress.setStyleSheet("""
            QProgressBar {
                border: 1px solid #444;
                border-radius: 3px;
                text-align: center;
            }
            QProgressBar::chunk {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                    stop:0 #00ff00, stop:0.5 #ffff00, stop:1 #ff0000);
                border-radius: 2px;
            }
        """)
        audio_layout.addRow("Level:", self.audio_level_progress)
        
        layout.addWidget(audio_group)
        
        # Captioner Settings
        captioner_group = QGroupBox("📝 Captioner Settings")
        captioner_layout = QFormLayout(captioner_group)
        
        self.captioner_enable_checkbox = QCheckBox("Enable Live Captions")
        if not CAPTIONER_AVAILABLE:
            self.captioner_enable_checkbox.setEnabled(False)
            self.captioner_enable_checkbox.setToolTip("Captioner dependencies not available")
        self.captioner_enable_checkbox.setStyleSheet("""
            QCheckBox {
                color: #ffffff;
                font-weight: bold;
            }
            QCheckBox::indicator {
                width: 18px;
                height: 18px;
            }
            QCheckBox::indicator:unchecked {
                border: 2px solid #666;
                background: #333;
                border-radius: 3px;
            }
            QCheckBox::indicator:checked {
                border: 2px solid #00aa00;
                background: #00aa00;
                border-radius: 3px;
            }
        """)
        captioner_layout.addRow(self.captioner_enable_checkbox)
        
        self.engine_combo = QComboBox()
        self.engine_combo.addItems(self.available_engines)
        captioner_layout.addRow("Engine:", self.engine_combo)
        
        self.language_combo = QComboBox()
        self.language_combo.addItems(["en", "es", "fr", "de", "it", "pt", "ru", "ja", "ko", "zh"])
        captioner_layout.addRow("Language:", self.language_combo)
        
        layout.addWidget(captioner_group)
        
        # Text Styling
        styling_group = QGroupBox("🎨 Text Styling")
        styling_layout = QFormLayout(styling_group)
        
        self.font_size_spin = QSpinBox()
        self.font_size_spin.setRange(12, 72)
        self.font_size_spin.setValue(32)
        styling_layout.addRow("Font Size:", self.font_size_spin)
        
        self.font_color_combo = QComboBox()
        self.font_color_combo.addItems(["White", "Yellow", "Green", "Cyan", "Magenta"])
        styling_layout.addRow("Font Color:", self.font_color_combo)
        
        self.background_opacity_slider = QSlider(Qt.Horizontal)
        self.background_opacity_slider.setRange(0, 100)
        self.background_opacity_slider.setValue(70)
        styling_layout.addRow("Background Opacity:", self.background_opacity_slider)
        
        layout.addWidget(styling_group)
        
        # Animation Settings
        animation_group = QGroupBox("⚡ Animation")
        animation_layout = QFormLayout(animation_group)
        
        self.typing_speed_slider = QSlider(Qt.Horizontal)
        self.typing_speed_slider.setRange(1, 20)
        self.typing_speed_slider.setValue(5)
        animation_layout.addRow("Typing Speed:", self.typing_speed_slider)
        
        self.show_duration_slider = QSlider(Qt.Horizontal)
        self.show_duration_slider.setRange(1, 10)
        self.show_duration_slider.setValue(3)
        animation_layout.addRow("Show Duration (s):", self.show_duration_slider)
        
        layout.addWidget(animation_group)
        
        # Status
        status_group = QGroupBox("📊 Status")
        status_layout = QVBoxLayout(status_group)
        
        if CAPTIONER_AVAILABLE:
            self.status_label = QLabel("Captioner: Ready")
            self.status_label.setStyleSheet("color: #00aa00; font-weight: bold;")
        else:
            self.status_label = QLabel("Captioner: Dependencies Missing")
            self.status_label.setStyleSheet("color: #ff6600; font-weight: bold;")
        status_layout.addWidget(self.status_label)
        
        layout.addWidget(status_group)
        
        # Control buttons
        buttons_layout = QHBoxLayout()
        
        self.refresh_devices_btn = QPushButton("🔄 Refresh Devices")
        self.refresh_devices_btn.setMinimumHeight(30)
        buttons_layout.addWidget(self.refresh_devices_btn)
        
        self.test_captioner_btn = QPushButton("🎤 Test Captioner")
        self.test_captioner_btn.setMinimumHeight(30)
        buttons_layout.addWidget(self.test_captioner_btn)
        
        layout.addLayout(buttons_layout)
        layout.addStretch()
        
    def setup_connections(self):
        """Setup signal connections."""
        # Audio device selection
        self.audio_device_combo.currentIndexChanged.connect(self.on_audio_device_changed)
        
        # Captioner settings
        self.captioner_enable_checkbox.toggled.connect(self.on_captioner_enabled)
        self.engine_combo.currentTextChanged.connect(self.on_captioner_config_changed)
        self.language_combo.currentTextChanged.connect(self.on_captioner_config_changed)
        
        # Text styling
        self.font_size_spin.valueChanged.connect(self.on_captioner_config_changed)
        self.font_color_combo.currentTextChanged.connect(self.on_captioner_config_changed)
        self.background_opacity_slider.valueChanged.connect(self.on_captioner_config_changed)
        
        # Animation settings
        self.typing_speed_slider.valueChanged.connect(self.on_captioner_config_changed)
        self.show_duration_slider.valueChanged.connect(self.on_captioner_config_changed)
        
        # Control buttons
        self.refresh_devices_btn.clicked.connect(self.refresh_audio_devices)
        self.test_captioner_btn.clicked.connect(self.test_captioner)
        
    def initialize_captioner(self):
        """Initialize the captioner manager."""
        try:
            if not CAPTIONER_AVAILABLE:
                self.logger.warning("Captioner not available - dependencies missing")
                self.update_status("Captioner: Dependencies missing")
                return False
                
            if self.captioner_manager is None:
                self.captioner_manager = CaptionerManager(self.captioner_config)
                
                # Set up callbacks
                self.captioner_manager.set_text_callback(self.on_text_update)
                self.captioner_manager.set_error_callback(self.on_captioner_error)
                self.captioner_manager.set_status_callback(self.on_captioner_status)
                
                # Initialize
                if self.captioner_manager.initialize():
                    self.logger.info("Captioner initialized successfully")
                    self.update_status("Captioner: Initialized")
                    return True
                else:
                    self.logger.error("Failed to initialize captioner")
                    self.update_status("Captioner: Initialization failed")
                    return False
            return True
        except Exception as e:
            self.logger.error(f"Error initializing captioner: {e}")
            self.update_status(f"Captioner: Error - {str(e)}")
            return False
    
    def start_captioner(self):
        """Start the captioner."""
        if not self.initialize_captioner():
            return False
            
        try:
            if self.captioner_manager.start():
                self.is_captioner_active = True
                self.update_status("Captioner: Active")
                self.audio_level_timer.start(100)  # Update every 100ms
                self.logger.info("Captioner started successfully")
                return True
            else:
                self.logger.error("Failed to start captioner")
                self.update_status("Captioner: Start failed")
                return False
        except Exception as e:
            self.logger.error(f"Error starting captioner: {e}")
            self.update_status(f"Captioner: Error - {str(e)}")
            return False
    
    def stop_captioner(self):
        """Stop the captioner."""
        try:
            if self.captioner_manager:
                self.captioner_manager.stop()
                self.is_captioner_active = False
                self.audio_level_timer.stop()
                self.audio_level_progress.setValue(0)
                self.update_status("Captioner: Stopped")
                self.logger.info("Captioner stopped")
        except Exception as e:
            self.logger.error(f"Error stopping captioner: {e}")
    
    def on_captioner_enabled(self, enabled: bool):
        """Handle captioner enable/disable."""
        if enabled:
            if self.start_captioner():
                self.captioner_enabled.emit(True)
            else:
                self.captioner_enable_checkbox.setChecked(False)
        else:
            self.stop_captioner()
            self.captioner_enabled.emit(False)
    
    def on_audio_device_changed(self, index: int):
        """Handle audio device selection change."""
        device_data = self.audio_device_combo.itemData(index)
        if device_data is not None:
            self.audio_device_changed.emit(device_data)
            self.update_captioner_config()
    
    def on_captioner_config_changed(self):
        """Handle captioner configuration changes."""
        self.update_captioner_config()
    
    def update_captioner_config(self):
        """Update the captioner configuration."""
        try:
            # Update config from UI values
            self.captioner_config.enabled = self.captioner_enable_checkbox.isChecked()
            self.captioner_config.engine = self.engine_combo.currentText()
            self.captioner_config.language = self.language_combo.currentText()
            self.captioner_config.font_size = self.font_size_spin.value()
            
            # Font color mapping
            color_map = {
                "White": (255, 255, 255),
                "Yellow": (255, 255, 0),
                "Green": (0, 255, 0),
                "Cyan": (0, 255, 255),
                "Magenta": (255, 0, 255)
            }
            self.captioner_config.font_color = color_map.get(
                self.font_color_combo.currentText(), (255, 255, 255)
            )
            
            self.captioner_config.background_opacity = self.background_opacity_slider.value() / 100.0
            self.captioner_config.typing_speed = self.typing_speed_slider.value() / 100.0
            self.captioner_config.show_duration = self.show_duration_slider.value()
            
            # Update captioner if active
            if self.captioner_manager and self.is_captioner_active:
                self.captioner_manager.update_config(self.captioner_config)
            
            # Emit config change signal
            config_dict = {
                'enabled': self.captioner_config.enabled,
                'engine': self.captioner_config.engine,
                'language': self.captioner_config.language,
                'font_size': self.captioner_config.font_size,
                'font_color': self.captioner_config.font_color,
                'background_opacity': self.captioner_config.background_opacity,
                'typing_speed': self.captioner_config.typing_speed,
                'show_duration': self.captioner_config.show_duration
            }
            self.captioner_config_changed.emit(config_dict)
            
        except Exception as e:
            self.logger.error(f"Error updating captioner config: {e}")
    
    def refresh_audio_devices(self):
        """Refresh the list of available audio devices."""
        try:
            if not CAPTIONER_AVAILABLE:
                self.logger.warning("Captioner not available - cannot refresh audio devices")
                self.update_status("Captioner: Dependencies missing")
                return
                
            if self.captioner_manager and self.captioner_manager.audio_capture:
                devices = self.captioner_manager.get_available_devices()
                self.available_audio_devices = devices
                
                # Update combo box
                self.audio_device_combo.clear()
                self.audio_device_combo.addItem("Default Microphone", -1)
                
                for device in devices:
                    self.audio_device_combo.addItem(
                        f"{device['name']} ({device['channels']}ch)",
                        device['index']
                    )
                
                self.logger.info(f"Found {len(devices)} audio devices")
                self.update_status(f"Found {len(devices)} audio devices")
            else:
                self.logger.warning("Captioner not initialized, cannot refresh devices")
                self.update_status("Captioner not initialized")
        except Exception as e:
            self.logger.error(f"Error refreshing audio devices: {e}")
            self.update_status(f"Error refreshing devices: {str(e)}")
    
    def test_captioner(self):
        """Test the captioner functionality."""
        try:
            if not self.captioner_enable_checkbox.isChecked():
                self.captioner_enable_checkbox.setChecked(True)
            
            self.update_status("Captioner: Testing...")
            self.logger.info("Testing captioner functionality")
            
        except Exception as e:
            self.logger.error(f"Error testing captioner: {e}")
            self.update_status(f"Test failed: {str(e)}")
    
    def update_audio_level(self):
        """Update the audio level indicator."""
        try:
            if self.captioner_manager and self.is_captioner_active:
                # Get audio level from captioner (placeholder - would need implementation)
                level = 50  # Placeholder value
                self.audio_level_progress.setValue(level)
        except Exception as e:
            self.logger.error(f"Error updating audio level: {e}")
    
    def on_text_update(self, text: str):
        """Handle text updates from captioner."""
        self.logger.debug(f"Captioner text: {text}")
        # This would be connected to the main window for display
    
    def on_captioner_error(self, error: str):
        """Handle captioner errors."""
        self.logger.error(f"Captioner error: {error}")
        self.update_status(f"Captioner error: {error}")
    
    def on_captioner_status(self, status: str):
        """Handle captioner status updates."""
        self.logger.info(f"Captioner status: {status}")
        self.update_status(f"Captioner: {status}")
    
    def update_status(self, message: str):
        """Update the status label."""
        self.status_label.setText(message)
    
    def get_captioner_manager(self):
        """Get the captioner manager instance."""
        return self.captioner_manager
    
    def is_active(self):
        """Check if captioner is active."""
        return self.is_captioner_active
    
    def cleanup(self):
        """Clean up resources."""
        try:
            self.stop_captioner()
            if self.captioner_manager:
                self.captioner_manager.cleanup()
        except Exception as e:
            self.logger.error(f"Error cleaning up captioner: {e}") 