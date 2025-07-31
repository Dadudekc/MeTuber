"""
UI Components Module for Dreamscape V2 Professional

Handles all UI creation, styling, and layout management.
Preserves exact visual appearance while modularizing the code.
"""

import logging
from PyQt5.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QFormLayout,
    QLabel, QPushButton, QSlider, QComboBox, QGroupBox, QDockWidget,
    QScrollArea, QFrame, QSplitter, QMenuBar, QToolBar, QStatusBar,
    QDoubleSpinBox, QSpinBox, QCheckBox, QGraphicsView, QGraphicsScene
)
from PyQt5.QtCore import Qt, pyqtSignal
from PyQt5.QtGui import QPixmap, QFont, QPalette, QColor, QIcon


class UIComponents:
    """Manages all UI components and styling for the main window."""
    
    def __init__(self, main_window):
        """Initialize UI components with reference to main window."""
        self.main_window = main_window
        self.logger = logging.getLogger(__name__)
        
        # UI Component references
        self.central_widget = None
        self.preview_label = None
        self.current_effect_label = None
        self.effect_variant_combo = None
        self.brightness_slider = None
        self.contrast_slider = None
        self.saturation_slider = None
        self.quality_combo = None
        self.fps_combo = None
        self.resolution_slider = None
        self.params_layout = None
        self.embedded_param_widgets = {}
        
        # Button components
        self.processing_status_label = None
        self.snapshot_btn = None
        self.reset_btn = None
        self.fullscreen_btn = None
        self.record_btn = None
        self.stream_btn = None
        
        # Combo box components
        self.size_combo = None
        self.zoom_combo = None
        
        # Layout components
        self.effects_layout = None
        self.timeline_layout = None
        
        # Dock components
        self.effects_dock = None
        
        # Status components
        self.status_label = None
        self.fps_label = None
        self.resolution_label = None
        
    def setup_professional_theme(self):
        """Setup the professional dark theme styling."""
        self.logger.info("Setting up professional dark theme")
        
        # Apply theme to the entire application
        from PyQt5.QtWidgets import QApplication
        from PyQt5.QtGui import QPalette, QColor
        app = QApplication.instance()
        
        # Create sophisticated dark palette
        dark_palette = QPalette()
        
        # Professional color scheme
        dark_palette.setColor(QPalette.Window, QColor(32, 32, 32))
        dark_palette.setColor(QPalette.WindowText, QColor(240, 240, 240))
        dark_palette.setColor(QPalette.Base, QColor(20, 20, 20))
        dark_palette.setColor(QPalette.AlternateBase, QColor(40, 40, 40))
        dark_palette.setColor(QPalette.ToolTipBase, QColor(60, 60, 60))
        dark_palette.setColor(QPalette.ToolTipText, QColor(240, 240, 240))
        dark_palette.setColor(QPalette.Text, QColor(240, 240, 240))
        dark_palette.setColor(QPalette.Button, QColor(45, 45, 45))
        dark_palette.setColor(QPalette.ButtonText, QColor(240, 240, 240))
        dark_palette.setColor(QPalette.BrightText, QColor(255, 100, 100))
        dark_palette.setColor(QPalette.Link, QColor(0, 150, 255))
        dark_palette.setColor(QPalette.Highlight, QColor(0, 150, 255))
        dark_palette.setColor(QPalette.HighlightedText, QColor(255, 255, 255))
        
        # Apply the palette
        app.setPalette(dark_palette)
        
        # Application-wide styling
        app.setStyleSheet("""
            QMainWindow {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
                    stop:0 #1a1a1a, stop:1 #2d2d2d);
                color: #ffffff;
                font-family: 'Segoe UI', Arial, sans-serif;
                font-size: 10pt;
            }
            
            QDockWidget {
                background: #2d2d2d;
                border: 1px solid #404040;
                titlebar-close-icon: url(close.png);
                titlebar-normal-icon: url(undock.png);
            }
            
            QDockWidget::title {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 #404040, stop:1 #2d2d2d);
                padding: 6px;
                border: 1px solid #404040;
                border-bottom: none;
                font-weight: bold;
                color: #ffffff;
            }
            
            QGroupBox {
                font-weight: bold;
                border: 2px solid #404040;
                border-radius: 5px;
                margin-top: 1ex;
                padding-top: 10px;
                color: #ffffff;
                background: #2d2d2d;
            }
            
            QGroupBox::title {
                subcontrol-origin: margin;
                left: 10px;
                padding: 0 5px 0 5px;
                color: #0096ff;
            }
            
            QPushButton {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 #404040, stop:1 #2d2d2d);
                border: 1px solid #404040;
                border-radius: 4px;
                padding: 8px 16px;
                color: #ffffff;
                font-weight: bold;
                min-width: 80px;
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
            
            QPushButton:disabled {
                background: #1a1a1a;
                color: #666666;
                border: 1px solid #333333;
            }
            
            QSlider::groove:horizontal {
                border: 1px solid #404040;
                height: 8px;
                background: #2d2d2d;
                border-radius: 4px;
            }
            
            QSlider::handle:horizontal {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 #0096ff, stop:1 #007acc);
                border: 1px solid #0096ff;
                width: 18px;
                margin: -2px 0;
                border-radius: 9px;
            }
            
            QSlider::handle:horizontal:hover {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 #00aaff, stop:1 #0096ff);
            }
            
            QComboBox {
                background: #2d2d2d;
                border: 1px solid #404040;
                border-radius: 4px;
                padding: 6px;
                color: #ffffff;
                min-width: 100px;
            }
            
            QComboBox:hover {
                border: 1px solid #0096ff;
            }
            
            QComboBox::drop-down {
                border: none;
                width: 20px;
            }
            
            QComboBox::down-arrow {
                image: url(down_arrow.png);
                width: 12px;
                height: 12px;
            }
            
            QComboBox QAbstractItemView {
                background: #2d2d2d;
                border: 1px solid #404040;
                selection-background-color: #0096ff;
                color: #ffffff;
            }
            
            QLabel {
                color: #ffffff;
                background: transparent;
            }
            
            QScrollArea {
                background: #2d2d2d;
                border: 1px solid #404040;
            }
            
            QScrollBar:vertical {
                background: #2d2d2d;
                width: 12px;
                border-radius: 6px;
            }
            
            QScrollBar::handle:vertical {
                background: #404040;
                border-radius: 6px;
                min-height: 20px;
            }
            
            QScrollBar::handle:vertical:hover {
                background: #505050;
            }
            
            QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {
                height: 0px;
            }
            
            QMenuBar {
                background: #2d2d2d;
                border-bottom: 1px solid #404040;
                color: #ffffff;
            }
            
            QMenuBar::item {
                background: transparent;
                padding: 8px 12px;
            }
            
            QMenuBar::item:selected {
                background: #404040;
            }
            
            QMenu {
                background: #2d2d2d;
                border: 1px solid #404040;
                color: #ffffff;
            }
            
            QMenu::item:selected {
                background: #0096ff;
            }
            
            QToolBar {
                background: #2d2d2d;
                border: none;
                spacing: 4px;
                padding: 4px;
            }
            
            QStatusBar {
                background: #2d2d2d;
                border-top: 1px solid #404040;
                color: #ffffff;
            }
            
            QCheckBox {
                color: #ffffff;
                spacing: 8px;
            }
            
            QCheckBox::indicator {
                width: 16px;
                height: 16px;
                border: 1px solid #404040;
                background: #2d2d2d;
                border-radius: 3px;
            }
            
            QCheckBox::indicator:checked {
                background: #0096ff;
                border: 1px solid #0096ff;
            }
            
            QSpinBox, QDoubleSpinBox {
                background: #2d2d2d;
                border: 1px solid #404040;
                border-radius: 4px;
                padding: 4px;
                color: #ffffff;
                min-width: 60px;
            }
            
            QSpinBox::up-button, QDoubleSpinBox::up-button,
            QSpinBox::down-button, QDoubleSpinBox::down-button {
                background: #404040;
                border: none;
                width: 16px;
                height: 12px;
            }
            
            QSpinBox::up-button:hover, QDoubleSpinBox::up-button:hover,
            QSpinBox::down-button:hover, QDoubleSpinBox::down-button:hover {
                background: #505050;
            }
        """)
        
    def create_central_preview(self):
        """Create the central preview area."""
        self.logger.info("Creating central preview area")
        
        # Create central widget
        self.central_widget = QWidget()
        self.main_window.setCentralWidget(self.central_widget)
        
        # Ensure central widget is visible
        self.central_widget.setVisible(True)
        self.central_widget.show()
        
        # Create layout and set it on the central_widget
        layout = QVBoxLayout()
        self.central_widget.setLayout(layout)
        
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(10)
        
        # Create preview label
        self.preview_label = QLabel("🎥 Live Preview")
        self.preview_label.setAlignment(Qt.AlignCenter)
        self.preview_label.setMinimumSize(640, 480)
        self.preview_label.setStyleSheet("""
            QLabel {
                background: #000000;
                border: 2px solid #404040;
                border-radius: 8px;
                color: #ffffff;
                font-size: 18px;
                font-weight: bold;
            }
        """)
        
        # Ensure the preview label is visible
        self.preview_label.setVisible(True)
        self.preview_label.show()
        
        layout.addWidget(self.preview_label)
        
        # Create preview controls
        controls_layout = QHBoxLayout()
        
        # Preview size control
        size_label = QLabel("Preview Size:")
        self.size_combo = QComboBox()
        self.size_combo.addItems(["480x360", "640x480", "800x600", "1024x768", "Full Screen"])
        self.size_combo.setCurrentText("480x360")
        
        # Zoom control
        zoom_label = QLabel("Zoom:")
        self.zoom_combo = QComboBox()
        self.zoom_combo.addItems(["Fit", "100%", "150%", "200%"])
        self.zoom_combo.setCurrentText("Fit")
        
        controls_layout.addWidget(size_label)
        controls_layout.addWidget(self.size_combo)
        controls_layout.addStretch()
        controls_layout.addWidget(zoom_label)
        controls_layout.addWidget(self.zoom_combo)
        
        layout.addLayout(controls_layout)
        
    def create_effects_dock(self):
        """Create the effects dock widget."""
        self.logger.info("Creating effects dock widget")
        
        effects_dock = QDockWidget("🎨 Popular Effects", self.main_window)
        effects_dock.setAllowedAreas(Qt.LeftDockWidgetArea | Qt.RightDockWidgetArea)
        effects_dock.setMinimumWidth(250)
        effects_dock.setMaximumWidth(350)
        
        # Create scrollable effects widget
        effects_widget = QWidget()
        effects_layout = QVBoxLayout(effects_widget)
        effects_layout.setSpacing(8)
        effects_layout.setContentsMargins(10, 10, 10, 10)
        
        # Create scroll area
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_area.setWidget(effects_widget)
        scroll_area.setVerticalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        scroll_area.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        
        effects_dock.setWidget(scroll_area)
        self.main_window.addDockWidget(Qt.LeftDockWidgetArea, effects_dock)
        
        # Store for later use
        self.effects_dock = effects_dock
        self.effects_layout = effects_layout
        
        # Store in main window for easy access
        self.main_window.effects_dock = effects_dock
        self.main_window.effects_layout = effects_layout
        
    def create_controls_dock(self):
        """Create the controls dock widget."""
        self.logger.info("Creating controls dock widget")
        
        controls_dock = QDockWidget("🎛️ Controls", self.main_window)
        controls_dock.setAllowedAreas(Qt.LeftDockWidgetArea | Qt.RightDockWidgetArea)
        controls_dock.setMinimumWidth(200)
        controls_dock.setMaximumWidth(300)
        
        controls_widget = QWidget()
        controls_layout = QVBoxLayout(controls_widget)
        controls_layout.setSpacing(10)
        controls_layout.setContentsMargins(10, 10, 10, 10)
        
        # Start/Stop Button
        start_group = QGroupBox("🎬 Preview Control")
        start_layout = QVBoxLayout(start_group)
        
        self.start_stop_btn = QPushButton("▶️ Start Preview")
        self.start_stop_btn.setCheckable(True)
        self.start_stop_btn.setMinimumHeight(45)
        self.start_stop_btn.setStyleSheet("""
            QPushButton {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 #27ae60, stop:1 #2ecc71);
                border: 1px solid #27ae60;
                border-radius: 8px;
                font-size: 13px;
                font-weight: bold;
                color: white;
            }
            QPushButton:hover {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 #2ecc71, stop:1 #27ae60);
            }
            QPushButton:checked {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 #e74c3c, stop:1 #c0392b);
                border: 1px solid #e74c3c;
            }
        """)
        
        start_info = QLabel("Click to start/stop camera preview\nand video processing")
        start_info.setAlignment(Qt.AlignCenter)
        start_info.setStyleSheet("""
            QLabel {
                color: #666666;
                font-size: 10px;
                padding: 4px;
            }
        """)
        
        start_layout.addWidget(self.start_stop_btn)
        start_layout.addWidget(start_info)
        
        # Processing Status Indicator
        status_group = QGroupBox("📊 Processing Status")
        status_layout = QVBoxLayout(status_group)
        
        self.processing_status_label = QLabel("⏸️ Preview Stopped")
        self.processing_status_label.setAlignment(Qt.AlignCenter)
        self.processing_status_label.setMinimumHeight(40)
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
        
        # Auto-processing info
        self.auto_processing_info = QLabel("Processing starts automatically\nwhen preview is active")
        self.auto_processing_info.setAlignment(Qt.AlignCenter)
        self.auto_processing_info.setStyleSheet("""
            QLabel {
                color: #666666;
                font-size: 10px;
                padding: 4px;
            }
        """)
        
        status_layout.addWidget(self.processing_status_label)
        status_layout.addWidget(self.auto_processing_info)
        
        # AI Optimization Control
        ai_group = QGroupBox("🤖 AI Optimization")
        ai_layout = QVBoxLayout(ai_group)
        
        self.ai_optimization_btn = QPushButton("🤖 Enable AI Optimization")
        self.ai_optimization_btn.setCheckable(True)
        self.ai_optimization_btn.setMinimumHeight(35)
        self.ai_optimization_btn.setStyleSheet("""
            QPushButton {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 #4a90e2, stop:1 #357abd);
                border: 1px solid #4a90e2;
                border-radius: 6px;
                font-size: 11px;
                font-weight: bold;
                color: white;
            }
            QPushButton:hover {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 #5ba0f2, stop:1 #4a90e2);
            }
            QPushButton:checked {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 #2ecc71, stop:1 #27ae60);
                border: 1px solid #2ecc71;
            }
        """)
        
        ai_info = QLabel("AI automatically selects\noptimal parameters")
        ai_info.setAlignment(Qt.AlignCenter)
        ai_info.setStyleSheet("""
            QLabel {
                color: #666666;
                font-size: 9px;
                padding: 2px;
            }
        """)
        
        ai_layout.addWidget(self.ai_optimization_btn)
        ai_layout.addWidget(ai_info)
        
        # Virtual Camera Control
        vcam_group = QGroupBox("📹 Virtual Camera")
        vcam_layout = QVBoxLayout(vcam_group)
        
        self.virtual_camera_btn = QPushButton("📹 Enable Dreamscape Virtual Camera")
        self.virtual_camera_btn.setCheckable(True)
        self.virtual_camera_btn.setMinimumHeight(35)
        self.virtual_camera_btn.setStyleSheet("""
            QPushButton {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 #e74c3c, stop:1 #c0392b);
                border: 1px solid #e74c3c;
                border-radius: 6px;
                font-size: 11px;
                font-weight: bold;
                color: white;
            }
            QPushButton:hover {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 #f75c4c, stop:1 #e74c3c);
            }
            QPushButton:checked {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 #27ae60, stop:1 #229954);
                border: 1px solid #27ae60;
            }
        """)
        
        vcam_info = QLabel("Use 'OBS Virtual Camera'\nin OBS, Zoom, or any streaming software")
        vcam_info.setAlignment(Qt.AlignCenter)
        vcam_info.setStyleSheet("""
            QLabel {
                color: #666666;
                font-size: 9px;
                padding: 2px;
            }
        """)
        
        vcam_layout.addWidget(self.virtual_camera_btn)
        vcam_layout.addWidget(vcam_info)
        
        # Add all groups to the controls layout
        controls_layout.addWidget(start_group)
        controls_layout.addWidget(status_group)
        controls_layout.addWidget(ai_group)
        controls_layout.addWidget(vcam_group)
        
        # Action buttons
        actions_group = QGroupBox("📸 Actions")
        actions_layout = QVBoxLayout(actions_group)
        
        self.snapshot_btn = QPushButton("📸 Snapshot")
        self.reset_btn = QPushButton("🔄 Reset")
        self.fullscreen_btn = QPushButton("🖥️ Fullscreen")
        self.record_btn = QPushButton("🔴 Record")
        self.stream_btn = QPushButton("📡 Stream")
        
        for btn in [self.snapshot_btn, self.reset_btn, self.fullscreen_btn, 
                   self.record_btn, self.stream_btn]:
            btn.setMinimumHeight(35)
            actions_layout.addWidget(btn)
            
        controls_layout.addWidget(actions_group)
        
        # Performance indicators
        perf_group = QGroupBox("⚡ Performance")
        perf_layout = QVBoxLayout(perf_group)
        
        self.cpu_label = QLabel("CPU: 0%")
        self.memory_label = QLabel("Memory: 0 MB")
        self.gpu_label = QLabel("GPU: 0%")
        
        for label in [self.cpu_label, self.memory_label, self.gpu_label]:
            label.setStyleSheet("color: #0096ff; font-weight: bold;")
            perf_layout.addWidget(label)
            
        controls_layout.addWidget(perf_group)
        controls_layout.addStretch()
        
        controls_dock.setWidget(controls_widget)
        self.main_window.addDockWidget(Qt.RightDockWidgetArea, controls_dock)
    
    def create_audio_captioner_dock(self):
        """Create the audio and captioner dock widget."""
        self.logger.info("Creating audio and captioner dock widget")
        
        # Import the audio captioner controls component
        from ..components.audio_captioner_controls import AudioCaptionerControls
        
        audio_captioner_dock = QDockWidget("🎤 Audio & Captions", self.main_window)
        audio_captioner_dock.setAllowedAreas(Qt.LeftDockWidgetArea | Qt.RightDockWidgetArea)
        audio_captioner_dock.setMinimumWidth(250)
        audio_captioner_dock.setMaximumWidth(350)
        
        # Create the audio captioner controls widget
        self.audio_captioner_controls = AudioCaptionerControls()
        
        audio_captioner_dock.setWidget(self.audio_captioner_controls)
        self.main_window.addDockWidget(Qt.RightDockWidgetArea, audio_captioner_dock)
        
        self.logger.info("Audio and captioner dock created successfully")
        
    def create_properties_dock(self):
        """Create the properties dock widget."""
        self.logger.info("Creating properties dock widget")
        
        properties_dock = QDockWidget("🎛️ Controls & Settings", self.main_window)
        properties_dock.setAllowedAreas(Qt.BottomDockWidgetArea | Qt.LeftDockWidgetArea | Qt.RightDockWidgetArea)
        properties_dock.setMinimumHeight(200)
        properties_dock.setMaximumHeight(400)
        
        properties_widget = QWidget()
        properties_layout = QHBoxLayout(properties_widget)
        
        # Column 1: Current Effect & Basic Controls
        left_column = QVBoxLayout()
        
        current_group = QGroupBox("🎨 Current Effect")
        current_layout = QFormLayout(current_group)
        
        self.current_effect_label = QLabel("None")
        self.current_effect_label.setStyleSheet("color: #0096ff; font-weight: bold;")
        current_layout.addRow("Effect:", self.current_effect_label)
        
        self.effect_variant_combo = QComboBox()
        self.effect_variant_combo.addItems(["Standard", "Enhanced", "Pro", "Custom"])
        current_layout.addRow("Variant:", self.effect_variant_combo)
        
        left_column.addWidget(current_group)
        
        # Camera Controls
        camera_group = QGroupBox("📹 Camera Controls")
        camera_layout = QFormLayout(camera_group)
        
        # Brightness
        self.brightness_slider = QSlider(Qt.Horizontal)
        self.brightness_slider.setRange(-100, 100)
        self.brightness_slider.setValue(0)
        self.brightness_label = QLabel("Brightness: 0")
        camera_layout.addRow(self.brightness_label, self.brightness_slider)
        
        # Contrast
        self.contrast_slider = QSlider(Qt.Horizontal)
        self.contrast_slider.setRange(50, 300)
        self.contrast_slider.setValue(100)
        self.contrast_label = QLabel("Contrast: 1.0")
        camera_layout.addRow(self.contrast_label, self.contrast_slider)
        
        # Saturation
        self.saturation_slider = QSlider(Qt.Horizontal)
        self.saturation_slider.setRange(0, 200)
        self.saturation_slider.setValue(100)
        self.saturation_label = QLabel("Saturation: 1.0")
        camera_layout.addRow(self.saturation_label, self.saturation_slider)
        
        left_column.addWidget(camera_group)
        
        # Column 2: Effect Parameters
        middle_column = QVBoxLayout()
        
        params_group = QGroupBox("🎛️ Effect Parameters")
        self.params_layout = QFormLayout(params_group)
        
        middle_column.addWidget(params_group)
        
        # Column 3: Performance & Output
        right_column = QVBoxLayout()
        
        # Performance Settings
        performance_group = QGroupBox("⚡ Performance")
        performance_layout = QFormLayout(performance_group)
        
        # Processing Quality
        self.quality_combo = QComboBox()
        self.quality_combo.addItems(["Fast", "Balanced", "High Quality"])
        self.quality_combo.setCurrentText("Balanced")
        performance_layout.addRow("Quality:", self.quality_combo)
        
        # Frame Rate Limit
        self.fps_combo = QComboBox()
        self.fps_combo.addItems(["15 FPS", "30 FPS", "60 FPS", "120 FPS"])
        self.fps_combo.setCurrentText("30 FPS")
        performance_layout.addRow("Frame Rate:", self.fps_combo)
        
        # Resolution Scale
        self.resolution_slider = QSlider(Qt.Horizontal)
        self.resolution_slider.setRange(25, 200)
        self.resolution_slider.setValue(100)
        self.resolution_label = QLabel("Resolution: 100%")
        performance_layout.addRow(self.resolution_label, self.resolution_slider)
        
        right_column.addWidget(performance_group)
        right_column.addStretch()
        
        # Add columns to main layout
        properties_layout.addLayout(left_column)
        properties_layout.addLayout(middle_column)
        properties_layout.addLayout(right_column)
        
        properties_dock.setWidget(properties_widget)
        self.main_window.addDockWidget(Qt.BottomDockWidgetArea, properties_dock)
        
    def create_timeline_dock(self):
        """Create the timeline dock widget."""
        self.logger.info("Creating timeline dock widget")
        
        timeline_dock = QDockWidget("📅 Effect Timeline", self.main_window)
        timeline_dock.setAllowedAreas(Qt.BottomDockWidgetArea)
        timeline_dock.setMinimumHeight(120)
        timeline_dock.setMaximumHeight(200)
        
        timeline_widget = QWidget()
        timeline_layout = QVBoxLayout(timeline_widget)
        
        # Timeline header
        header_layout = QHBoxLayout()
        header_layout.addWidget(QLabel("Applied Effects:"))
        header_layout.addStretch()
        
        # Timeline scroll area
        self.timeline_scroll = QScrollArea()
        self.timeline_scroll.setWidgetResizable(True)
        self.timeline_scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        self.timeline_scroll.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        
        self.timeline_widget = QWidget()
        self.timeline_layout = QHBoxLayout(self.timeline_widget)
        self.timeline_layout.setSpacing(10)
        self.timeline_layout.setContentsMargins(10, 5, 10, 5)
        
        self.timeline_scroll.setWidget(self.timeline_widget)
        
        timeline_layout.addLayout(header_layout)
        timeline_layout.addWidget(self.timeline_scroll)
        
        timeline_dock.setWidget(timeline_widget)
        self.main_window.addDockWidget(Qt.BottomDockWidgetArea, timeline_dock)
        
    def create_menu_bar(self):
        """Create the menu bar."""
        self.logger.info("Creating menu bar")
        
        menubar = self.main_window.menuBar()
        
        # File menu
        file_menu = menubar.addMenu("📁 File")
        
        new_action = file_menu.addAction("🆕 New Project")
        open_action = file_menu.addAction("📂 Open Project")
        save_action = file_menu.addAction("💾 Save Project")
        file_menu.addSeparator()
        export_action = file_menu.addAction("📤 Export Video")
        file_menu.addSeparator()
        exit_action = file_menu.addAction("🚪 Exit")
        
        # Edit menu
        edit_menu = menubar.addMenu("✏️ Edit")
        
        undo_action = edit_menu.addAction("↶ Undo")
        redo_action = edit_menu.addAction("↷ Redo")
        edit_menu.addSeparator()
        copy_action = edit_menu.addAction("📋 Copy")
        paste_action = edit_menu.addAction("📋 Paste")
        
        # View menu
        view_menu = menubar.addMenu("👁️ View")
        
        fullscreen_action = view_menu.addAction("🖥️ Fullscreen")
        view_menu.addSeparator()
        dock_menu = view_menu.addMenu("📋 Docks")
        dock_menu.addAction("🎨 Effects")
        dock_menu.addAction("🎛️ Controls")
        dock_menu.addAction("🎛️ Properties")
        dock_menu.addAction("📅 Timeline")
        
        # Tools menu
        tools_menu = menubar.addMenu("🔧 Tools")
        
        settings_action = tools_menu.addAction("⚙️ Settings")
        tools_menu.addSeparator()
        calibrate_action = tools_menu.addAction("🎯 Calibrate Camera")
        test_action = tools_menu.addAction("🧪 Test Effects")
        
        # Help menu
        help_menu = menubar.addMenu("❓ Help")
        
        about_action = help_menu.addAction("ℹ️ About")
        help_action = help_menu.addAction("📖 Documentation")
        help_menu.addSeparator()
        update_action = help_menu.addAction("🔄 Check for Updates")
        
    def create_main_toolbar(self):
        """Create the main toolbar."""
        self.logger.info("Creating main toolbar")
        
        toolbar = self.main_window.addToolBar("Main Toolbar")
        toolbar.setMovable(False)
        toolbar.setToolButtonStyle(Qt.ToolButtonTextUnderIcon)
        
        # Add toolbar actions
        toolbar.addAction("▶️ Start")
        toolbar.addAction("⏸️ Pause")
        toolbar.addAction("⏹️ Stop")
        toolbar.addSeparator()
        toolbar.addAction("📸 Snapshot")
        toolbar.addAction("🔴 Record")
        toolbar.addSeparator()
        toolbar.addAction("⚙️ Settings")
        
    def create_status_bar(self):
        """Create the status bar."""
        self.logger.info("Creating status bar")
        
        status_bar = self.main_window.statusBar()
        status_bar.setStyleSheet("color: #ffffff; background: #2d2d2d;")
        
        # Status labels
        self.status_label = QLabel("Ready")
        self.fps_label = QLabel("FPS: 0")
        self.resolution_label = QLabel("Resolution: 640x480")
        
        status_bar.addWidget(self.status_label)
        status_bar.addPermanentWidget(self.fps_label)
        status_bar.addPermanentWidget(self.resolution_label)
        
    def get_all_ui_components(self):
        """Return all UI components for external access."""
        return {
            'central_widget': self.central_widget,
            'preview_label': self.preview_label,
            'current_effect_label': self.current_effect_label,
            'effect_variant_combo': self.effect_variant_combo,
            'brightness_slider': self.brightness_slider,
            'contrast_slider': self.contrast_slider,
            'saturation_slider': self.saturation_slider,
            'quality_combo': self.quality_combo,
            'fps_combo': self.fps_combo,
            'resolution_slider': self.resolution_slider,
            'params_layout': self.params_layout,
            'embedded_param_widgets': self.embedded_param_widgets,
            'start_stop_btn': self.start_stop_btn,
            'processing_status_label': self.processing_status_label,
            'ai_optimization_btn': self.ai_optimization_btn,
            'virtual_camera_btn': self.virtual_camera_btn,
            'snapshot_btn': self.snapshot_btn,
            'reset_btn': self.reset_btn,
            'fullscreen_btn': self.fullscreen_btn,
            'record_btn': self.record_btn,
            'stream_btn': self.stream_btn,
            'size_combo': self.size_combo,
            'zoom_combo': self.zoom_combo,
            'effects_dock': self.effects_dock,
            'effects_layout': self.effects_layout,
            'timeline_layout': self.timeline_layout,
            'status_label': self.status_label,
            'fps_label': self.fps_label,
            'resolution_label': self.resolution_label
        } 