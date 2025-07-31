#!/usr/bin/env python3
"""
Test Plugin System

Demonstrates the plugin system functionality with a sample cartoon effect.
"""

import sys
import os
import cv2
import numpy as np
from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QHBoxLayout, QWidget, QPushButton, QLabel, QComboBox
from PyQt5.QtCore import QTimer, Qt
from PyQt5.QtGui import QPixmap, QImage

# Add the project root to Python path
project_root = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, project_root)

try:
    from src.plugins import PluginManager
    print("✓ PluginManager imported successfully")
except ImportError as e:
    print(f"✗ Error importing PluginManager: {e}")
    sys.exit(1)

class PluginTestWindow(QMainWindow):
    """Test window for demonstrating the plugin system."""
    
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Plugin System Test")
        self.setGeometry(100, 100, 800, 600)
        
        # Initialize plugin manager
        print("Initializing plugin manager...")
        self.plugin_manager = PluginManager()
        self.plugin_manager.initialize()
        
        # Setup UI
        self.setup_ui()
        
        # Setup camera
        self.setup_camera()
        
        # Setup timer for frame updates
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_frame)
        self.timer.start(33)  # ~30 FPS
    
    def setup_ui(self):
        """Setup the user interface."""
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        layout = QVBoxLayout()
        
        # Effect selection
        effect_layout = QHBoxLayout()
        effect_layout.addWidget(QLabel("Select Effect:"))
        
        self.effect_combo = QComboBox()
        self.effect_combo.addItem("None")
        
        # Add available effects
        effects = self.plugin_manager.get_all_effects()
        print(f"Found {len(effects)} effects:")
        for effect in effects:
            print(f"  - {effect.name} ({effect.category})")
            self.effect_combo.addItem(effect.name)
        
        self.effect_combo.currentTextChanged.connect(self.on_effect_changed)
        effect_layout.addWidget(self.effect_combo)
        
        layout.addLayout(effect_layout)
        
        # Video display
        self.video_label = QLabel()
        self.video_label.setMinimumSize(640, 480)
        self.video_label.setStyleSheet("border: 2px solid gray;")
        layout.addWidget(self.video_label)
        
        # Effect controls (will be populated dynamically)
        self.controls_widget = QWidget()
        layout.addWidget(self.controls_widget)
        
        central_widget.setLayout(layout)
    
    def setup_camera(self):
        """Setup camera capture."""
        print("Setting up camera...")
        self.cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)
        if not self.cap.isOpened():
            print("Error: Could not open camera")
            self.cap = None
        else:
            self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
            self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
            print("✓ Camera setup complete")
    
    def update_frame(self):
        """Update the video frame."""
        if not self.cap:
            return
        
        ret, frame = self.cap.read()
        if not ret:
            return
        
        # Apply current effect
        if self.plugin_manager.get_current_effect():
            frame = self.plugin_manager.apply_effect(frame)
        
        # Convert to QPixmap and display
        self.display_frame(frame)
    
    def display_frame(self, frame):
        """Display a frame in the video label."""
        # Convert BGR to RGB
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        
        # Convert to QImage
        height, width, channel = rgb_frame.shape
        bytes_per_line = 3 * width
        q_image = QImage(rgb_frame.data, width, height, bytes_per_line, QImage.Format_RGB888)
        
        # Scale to fit label
        pixmap = QPixmap.fromImage(q_image)
        scaled_pixmap = pixmap.scaled(self.video_label.size(), Qt.KeepAspectRatio, Qt.SmoothTransformation)
        
        self.video_label.setPixmap(scaled_pixmap)
    
    def on_effect_changed(self, effect_name):
        """Handle effect selection change."""
        print(f"Effect changed to: {effect_name}")
        
        if effect_name == "None":
            self.plugin_manager.current_effect = None
            self.plugin_manager.current_effect_id = None
            self.update_controls()
            return
        
        # Find the effect by name
        effects = self.plugin_manager.get_all_effects()
        for effect in effects:
            if effect.name == effect_name:
                # Set as current effect
                effect_id = None
                for pid, plugin in self.plugin_manager.registry.plugins.items():
                    if plugin == effect:
                        effect_id = pid
                        break
                
                if effect_id:
                    self.plugin_manager.set_current_effect(effect_id)
                    self.update_controls()
                break
    
    def update_controls(self):
        """Update the effect controls."""
        # Clear existing controls
        for child in self.controls_widget.children():
            child.deleteLater()
        
        if not self.plugin_manager.get_current_effect():
            return
        
        # Create new controls
        layout = QVBoxLayout()
        
        # Get UI component for current effect
        effect_id = self.plugin_manager.get_current_effect_id()
        ui_component = self.plugin_manager.get_effect_ui(effect_id)
        
        if ui_component:
            # Create UI components
            ui_widget = ui_component.create_ui_components()
            layout.addWidget(ui_widget)
        
        self.controls_widget.setLayout(layout)
    
    def closeEvent(self, event):
        """Handle window close event."""
        if self.cap:
            self.cap.release()
        self.plugin_manager.cleanup()
        event.accept()

def main():
    """Main function."""
    print("Starting Plugin System Test...")
    
    app = QApplication(sys.argv)
    
    # Create and show test window
    window = PluginTestWindow()
    window.show()
    
    # Print plugin statistics
    stats = window.plugin_manager.get_statistics()
    print("\nPlugin System Statistics:")
    print(f"Total plugins: {stats['total_plugins']}")
    print(f"Enabled plugins: {stats['enabled_plugins']}")
    print(f"Categories: {stats['category_counts']}")
    
    print("\n✓ Plugin system test started successfully!")
    print("Select an effect from the dropdown to test it.")
    
    # Run the application
    sys.exit(app.exec_())

if __name__ == "__main__":
    main() 