#!/usr/bin/env python3
"""
Dreamscape V2 - Working Version with Direct Camera Access
Based on the original backup that had working camera preview
"""

import sys
import logging
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QTabWidget,
    QLabel, QPushButton, QComboBox, QGroupBox, QFormLayout, QSlider, QMenuBar,
    QAction, QStatusBar, QFrame, QSplitter, QScrollArea, QGridLayout, QListWidget,
    QListWidgetItem, QDockWidget, QToolBar, QProgressBar, QTextEdit, QCheckBox,
    QSpinBox, QDoubleSpinBox, QButtonGroup, QRadioButton, QTableWidget, QTableWidgetItem,
    QHeaderView, QGraphicsView, QGraphicsScene, QGraphicsPixmapItem, QGraphicsProxyWidget,
    QSizePolicy
)
from PyQt5.QtCore import Qt, QTimer, pyqtSignal, QThread, QPropertyAnimation, QEasingCurve
from PyQt5.QtGui import QPixmap, QPalette, QColor, QFont, QIcon, QPainter, QBrush, QLinearGradient, QImage
import cv2
import numpy as np
from datetime import datetime

class ProfessionalV2MainWindow(QMainWindow):
    """Professional V2 main window with working camera preview."""
    
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
        self.is_processing = False
        self.current_style = None
        self.effects_history = []
        self.favorite_effects = []
        
        # Camera and preview
        self.direct_cap = None
        self.standby_cap = None
        self.current_frame = None
        self.preview_pixmap = None
        self.pending_style = None
        self.pending_params = {}
        
        self.setup_professional_theme()
        self.init_ui()
        self.setup_connections()
        self.setup_animations()
        
        # Pre-load everything for instant startup
        self.pre_load_camera()
        self.pre_load_styles()
        self.pre_initialize_timer()
        
        self.logger.info("Professional V2 Main Window initialized successfully!")
        
    def setup_professional_theme(self):
        """Apply professional theme."""
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
        
        QApplication.setPalette(dark_palette)
        
        # Professional stylesheet
        self.setStyleSheet("""
            QMainWindow {
                background-color: #202020;
                color: #f0f0f0;
            }
            QLabel {
                color: #f0f0f0;
                font-size: 12px;
            }
            QPushButton {
                background-color: #2d2d2d;
                border: 1px solid #404040;
                border-radius: 4px;
                padding: 8px 16px;
                color: #f0f0f0;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #404040;
                border-color: #606060;
            }
            QPushButton:pressed {
                background-color: #1a1a1a;
            }
            QComboBox {
                background-color: #2d2d2d;
                border: 1px solid #404040;
                border-radius: 4px;
                padding: 4px 8px;
                color: #f0f0f0;
            }
            QSlider::groove:horizontal {
                border: 1px solid #404040;
                height: 8px;
                background: #2d2d2d;
                border-radius: 4px;
            }
            QSlider::handle:horizontal {
                background: #0066cc;
                border: 1px solid #0066cc;
                width: 18px;
                margin: -2px 0;
                border-radius: 9px;
            }
        """)
        
    def init_ui(self):
        """Initialize the user interface."""
        self.setWindowTitle("Dreamscape V2 - Professional Webcam Effects Studio")
        self.setGeometry(100, 100, 1200, 800)
        
        # Create central widget
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        # Main layout
        main_layout = QHBoxLayout(central_widget)
        
        # Left panel for controls
        left_panel = QWidget()
        left_layout = QVBoxLayout(left_panel)
        
        # Create central preview
        self.create_central_preview()
        main_layout.addWidget(self.preview_widget, 2)
        
        # Create controls
        self.create_controls_panel(left_layout)
        main_layout.addWidget(left_panel, 1)
        
        # Create status bar
        self.create_status_bar()
        
    def create_central_preview(self):
        """Create the central preview area."""
        self.preview_widget = QWidget()
        preview_layout = QVBoxLayout(self.preview_widget)
        
        # Preview label
        self.video_label = QLabel("Click 'Start Processing' to begin")
        self.video_label.setAlignment(Qt.AlignCenter)
        self.video_label.setMinimumSize(640, 480)
        self.video_label.setStyleSheet("""
            QLabel {
                background-color: #1a1a1a;
                border: 2px solid #404040;
                border-radius: 8px;
                color: #808080;
                font-size: 16px;
            }
        """)
        preview_layout.addWidget(self.video_label)
        
        # Control buttons
        button_layout = QHBoxLayout()
        
        self.start_stop_btn = QPushButton("▶️ Start Processing")
        self.start_stop_btn.clicked.connect(self.on_start_stop_clicked)
        button_layout.addWidget(self.start_stop_btn)
        
        self.snapshot_btn = QPushButton("📸 Snapshot")
        self.snapshot_btn.clicked.connect(self.on_snapshot_clicked)
        button_layout.addWidget(self.snapshot_btn)
        
        self.reset_btn = QPushButton("🔄 Reset")
        self.reset_btn.clicked.connect(self.on_reset_clicked)
        button_layout.addWidget(self.reset_btn)
        
        preview_layout.addLayout(button_layout)
        
    def create_controls_panel(self, layout):
        """Create the controls panel."""
        # Effects list
        effects_group = QGroupBox("Effects")
        effects_layout = QVBoxLayout(effects_group)
        
        self.effects_list = QListWidget()
        self.effects_list.addItems([
            "🔍 Edge Detection",
            "🎨 Cartoon",
            "🌊 Watercolor",
            "⚡ Glitch",
            "🎭 Oil Painting",
            "✏️ Pencil Sketch"
        ])
        self.effects_list.itemClicked.connect(self.on_effect_selected)
        effects_layout.addWidget(self.effects_list)
        
        layout.addWidget(effects_group)
        
        # Current effect display
        self.current_effect_label = QLabel("Current Effect: None")
        layout.addWidget(self.current_effect_label)
        
        # Performance indicators
        perf_group = QGroupBox("Performance")
        perf_layout = QVBoxLayout(perf_group)
        
        self.fps_label = QLabel("FPS: 0")
        self.frame_count_label = QLabel("Frames: 0")
        
        perf_layout.addWidget(self.fps_label)
        perf_layout.addWidget(self.frame_count_label)
        
        layout.addWidget(perf_group)
        
    def create_status_bar(self):
        """Create the status bar."""
        self.status_bar = QStatusBar()
        self.setStatusBar(self.status_bar)
        self.status_bar.showMessage("Ready")
        
    def setup_connections(self):
        """Setup signal connections."""
        # Timer for preview updates
        self.preview_timer = QTimer()
        self.preview_timer.timeout.connect(self.update_preview)
        
    def setup_animations(self):
        """Setup UI animations."""
        pass  # Simplified for working version
        
    def pre_load_camera(self):
        """Pre-load camera for instant startup."""
        try:
            self.logger.info("Pre-loading camera...")
            self.standby_cap = cv2.VideoCapture(0)
            if self.standby_cap.isOpened():
                self.standby_cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
                self.standby_cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
                self.standby_cap.set(cv2.CAP_PROP_FPS, 30)
                self.logger.info("Camera pre-loaded successfully")
            else:
                self.logger.warning("Failed to pre-load camera")
        except Exception as e:
            self.logger.error(f"Error pre-loading camera: {e}")
            
    def pre_load_styles(self):
        """Pre-load styles."""
        self.logger.info("Pre-loading styles...")
        
    def pre_initialize_timer(self):
        """Pre-initialize timer."""
        self.preview_timer.start(500)  # Slow timer when stopped
        
    def on_start_stop_clicked(self):
        """Handle start/stop button click."""
        self.logger.info("=== START/STOP BUTTON CLICKED ===")
        
        try:
            if not self.is_processing:
                # START TIMER IMMEDIATELY - BLAZING FAST!
                self.video_label.clear()
                self.preview_timer.stop()
                self.preview_timer.start(33)  # ~30 FPS for smooth preview
                
                try:
                    # Use PRE-LOADED camera for INSTANT start!
                    if hasattr(self, 'standby_cap') and self.standby_cap and self.standby_cap.isOpened():
                        self.direct_cap = self.standby_cap
                        self.standby_cap = None  # Transfer ownership
                        self.logger.info("Using pre-loaded camera")
                    else:
                        # Fallback if pre-load failed
                        self.direct_cap = cv2.VideoCapture(0)
                        self.logger.info("Using fallback camera")
                    
                    # Update UI state instantly
                    self.start_stop_btn.setText("⏸️ Stop Processing")
                    self.is_processing = True
                    self.update_status("Processing started")
                    
                except Exception as start_error:
                    self.logger.error(f"❌ CRITICAL ERROR starting webcam: {start_error}")
                    import traceback
                    self.logger.error(f"Full traceback:\n{traceback.format_exc()}")
                    self.update_status(f"FAILED to start webcam: {start_error}")
                    
                    # Cleanup on error
                    self.is_processing = False
                    self.preview_timer.stop()
                    self.start_stop_btn.setText("▶️ Start Processing")
                    
            else:
                # STOP processing
                self.is_processing = False
                self.preview_timer.stop()
                self.preview_timer.start(500)  # Slow timer when stopped
                
                # Release camera
                if hasattr(self, 'direct_cap') and self.direct_cap:
                    self.direct_cap.release()
                    self.direct_cap = None
                
                # Update UI
                self.start_stop_btn.setText("▶️ Start Processing")
                self.video_label.clear()
                self.video_label.setText("Click 'Start Processing' to begin")
                self.update_status("Processing stopped")
            
        except Exception as e:
            self.logger.error(f"❌ CRITICAL ERROR in start/stop handler: {e}")
            import traceback
            self.logger.error(f"Full traceback:\n{traceback.format_exc()}")
            
            # Force reset on critical error
            self.is_processing = False
            self.preview_timer.stop()
            self.start_stop_btn.setText("▶️ Start Processing")
            
        self.logger.info("=== START/STOP BUTTON HANDLER COMPLETED ===")
            
    def on_snapshot_clicked(self):
        """Handle snapshot button click."""
        if self.current_frame is not None:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"snapshot_{timestamp}.jpg"
            cv2.imwrite(filename, self.current_frame)
            self.update_status(f"Snapshot saved: {filename}")
        else:
            self.update_status("No frame available for snapshot")
        
    def on_reset_clicked(self):
        """Handle reset button click."""
        self.current_effect_label.setText("Current Effect: None")
        self.effects_history.clear()
        self.pending_style = None
        self.pending_params = {}
        self.update_status("Effects reset")
        
    def on_effect_selected(self, item):
        """Handle effect selection."""
        effect_name = item.text()
        self.current_effect_label.setText(f"Current Effect: {effect_name}")
        self.effects_history.append(effect_name)
        self.update_status(f"Effect selected: {effect_name}")
        
    def update_preview(self):
        """Update the preview display."""
        if not self.is_processing or not self.direct_cap:
            return
            
        try:
            ret, frame = self.direct_cap.read()
            if ret and frame is not None:
                self.current_frame = frame.copy()
                
                # Convert frame to QPixmap
                height, width = frame.shape[:2]
                bytes_per_line = 3 * width
                q_image = QImage(
                    frame.data,
                    width,
                    height,
                    bytes_per_line,
                    QImage.Format_RGB888
                ).rgbSwapped()
                
                # Scale to fit label
                pixmap = QPixmap.fromImage(q_image)
                scaled_pixmap = pixmap.scaled(
                    self.video_label.size(),
                    Qt.KeepAspectRatio,
                    Qt.SmoothTransformation
                )
                
                self.video_label.setPixmap(scaled_pixmap)
                
                # Update performance indicators
                self.frame_count_label.setText(f"Frames: {len(self.effects_history)}")
                
            else:
                self.logger.warning("Failed to read frame from camera")
                
        except Exception as e:
            self.logger.error(f"Error updating preview: {e}")
            
    def update_status(self, message):
        """Update status bar message."""
        self.status_bar.showMessage(message)
        self.logger.info(message)
        
    def closeEvent(self, event):
        """Handle window close event."""
        try:
            # Stop processing
            if self.is_processing:
                self.is_processing = False
                self.preview_timer.stop()
                
            # Release camera
            if self.direct_cap:
                self.direct_cap.release()
            if self.standby_cap:
                self.standby_cap.release()
                
        except Exception as e:
            self.logger.error(f"Error during close: {e}")
            
        event.accept()

def main():
    """Main application entry point."""
    app = QApplication(sys.argv)
    
    # Setup logging
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    
    # Create and show main window
    window = ProfessionalV2MainWindow()
    window.show()
    
    # Start event loop
    return app.exec_()

if __name__ == "__main__":
    sys.exit(main()) 