#!/usr/bin/env python3
"""
Preview Button Test

This test simulates exactly what happens when the preview button is pressed
in the main application to identify the issue.
"""

import sys
import os
import logging
import numpy as np
import cv2
from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel, QVBoxLayout, QWidget, QPushButton, QTextEdit
from PyQt5.QtCore import Qt, QTimer
from PyQt5.QtGui import QPixmap, QImage

# Add the src directory to the path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

class PreviewButtonTest(QMainWindow):
    """Test window to simulate preview button behavior."""
    
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Preview Button Test - Simulating Main App")
        self.setGeometry(100, 100, 1000, 700)
        
        # Create central widget
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        layout = QVBoxLayout(central_widget)
        
        # Create control buttons
        control_layout = QVBoxLayout()
        
        self.start_preview_btn = QPushButton("🚀 START PREVIEW (Simulates Preview Button)")
        self.start_preview_btn.setStyleSheet("""
            QPushButton {
                background-color: #00ff00;
                color: #000000;
                border: 3px solid #008000;
                border-radius: 10px;
                font-size: 16px;
                font-weight: bold;
                padding: 15px;
                margin: 5px;
            }
            QPushButton:hover {
                background-color: #80ff80;
            }
        """)
        self.start_preview_btn.clicked.connect(self.start_preview)
        control_layout.addWidget(self.start_preview_btn)
        
        self.stop_preview_btn = QPushButton("⏹️ STOP PREVIEW")
        self.stop_preview_btn.setStyleSheet("""
            QPushButton {
                background-color: #ff0000;
                color: #ffffff;
                border: 3px solid #800000;
                border-radius: 10px;
                font-size: 16px;
                font-weight: bold;
                padding: 15px;
                margin: 5px;
            }
            QPushButton:hover {
                background-color: #ff8080;
            }
        """)
        self.stop_preview_btn.clicked.connect(self.stop_preview)
        self.stop_preview_btn.setEnabled(False)
        control_layout.addWidget(self.stop_preview_btn)
        
        self.test_camera_btn = QPushButton("📷 Test Camera Access")
        self.test_camera_btn.clicked.connect(self.test_camera_access)
        control_layout.addWidget(self.test_camera_btn)
        
        layout.addLayout(control_layout)
        
        # Create preview label (same as main app)
        self.preview_label = QLabel("PREVIEW AREA - Click START PREVIEW to test")
        self.preview_label.setMinimumSize(800, 600)
        self.preview_label.setStyleSheet("""
            QLabel {
                background: #000000;
                color: #ffffff;
                border: 3px solid #ffffff;
                border-radius: 10px;
                font-size: 18px;
                font-weight: bold;
                padding: 20px;
            }
        """)
        layout.addWidget(self.preview_label)
        
        # Create log display
        self.log_display = QTextEdit()
        self.log_display.setMaximumHeight(150)
        self.log_display.setStyleSheet("""
            QTextEdit {
                background: #f0f0f0;
                color: #000000;
                border: 2px solid #cccccc;
                border-radius: 5px;
                font-family: monospace;
                font-size: 12px;
            }
        """)
        layout.addWidget(self.log_display)
        
        # Preview state
        self.preview_timer = None
        self.is_preview_active = False
        self.camera_cap = None
        
        self.log("🔧 Preview Button Test initialized")
        self.log("🎯 This simulates exactly what happens when you press the preview button")
        
    def log(self, message):
        """Add message to log display."""
        self.log_display.append(f"{message}")
        print(message)
        
    def start_preview(self):
        """Simulate pressing the preview button."""
        try:
            self.log("🚀 START PREVIEW BUTTON PRESSED!")
            self.log("=" * 50)
            
            # Step 1: Test camera access
            self.log("📷 Step 1: Testing camera access...")
            if not self.test_camera_access():
                self.log("❌ Camera access failed - cannot start preview")
                return
                
            # Step 2: Initialize preview timer
            self.log("⏰ Step 2: Initializing preview timer...")
            self.init_preview_timer()
            
            # Step 3: Start camera capture
            self.log("📹 Step 3: Starting camera capture...")
            self.start_camera_capture()
            
            # Step 4: Start preview updates
            self.log("🔄 Step 4: Starting preview updates...")
            self.start_preview_updates()
            
            # Update UI state
            self.start_preview_btn.setEnabled(False)
            self.stop_preview_btn.setEnabled(True)
            self.is_preview_active = True
            
            self.log("✅ Preview started successfully!")
            self.log("🎬 You should now see live camera feed in the preview area")
            
        except Exception as e:
            self.log(f"❌ Error starting preview: {e}")
            import traceback
            self.log(f"Traceback: {traceback.format_exc()}")
            
    def stop_preview(self):
        """Stop the preview."""
        try:
            self.log("⏹️ STOPPING PREVIEW...")
            
            # Stop timer
            if self.preview_timer:
                self.preview_timer.stop()
                self.preview_timer = None
                
            # Release camera
            if self.camera_cap:
                self.camera_cap.release()
                self.camera_cap = None
                
            # Update UI state
            self.start_preview_btn.setEnabled(True)
            self.stop_preview_btn.setEnabled(False)
            self.is_preview_active = False
            
            # Clear preview
            self.preview_label.setText("PREVIEW STOPPED - Click START PREVIEW to test again")
            self.preview_label.setStyleSheet("""
                QLabel {
                    background: #000000;
                    color: #ffffff;
                    border: 3px solid #ffffff;
                    border-radius: 10px;
                    font-size: 18px;
                    font-weight: bold;
                    padding: 20px;
                }
            """)
            
            self.log("✅ Preview stopped")
            
        except Exception as e:
            self.log(f"❌ Error stopping preview: {e}")
            
    def test_camera_access(self):
        """Test if camera can be accessed."""
        try:
            self.log("🔧 Testing camera access...")
            
            # Try to open camera
            cap = cv2.VideoCapture(0)
            if cap.isOpened():
                self.log("✅ Camera opened successfully")
                
                # Try to read a frame
                ret, frame = cap.read()
                if ret and frame is not None:
                    self.log(f"✅ Frame captured: {frame.shape}")
                    cap.release()
                    return True
                else:
                    self.log("❌ Failed to capture frame from camera")
                    cap.release()
                    return False
            else:
                self.log("❌ Failed to open camera")
                return False
                
        except Exception as e:
            self.log(f"❌ Camera test failed: {e}")
            return False
            
    def init_preview_timer(self):
        """Initialize the preview update timer."""
        try:
            self.preview_timer = QTimer()
            self.preview_timer.timeout.connect(self.update_preview)
            self.preview_timer.setInterval(100)  # 10 FPS
            self.log("✅ Preview timer initialized")
            
        except Exception as e:
            self.log(f"❌ Error initializing timer: {e}")
            
    def start_camera_capture(self):
        """Start camera capture."""
        try:
            self.camera_cap = cv2.VideoCapture(0)
            if self.camera_cap.isOpened():
                self.log("✅ Camera capture started")
            else:
                self.log("❌ Failed to start camera capture")
                
        except Exception as e:
            self.log(f"❌ Error starting camera capture: {e}")
            
    def start_preview_updates(self):
        """Start preview updates."""
        try:
            if self.preview_timer:
                self.preview_timer.start()
                self.log("✅ Preview timer started")
            else:
                self.log("❌ No preview timer available")
                
        except Exception as e:
            self.log(f"❌ Error starting preview updates: {e}")
            
    def update_preview(self):
        """Update the preview display."""
        try:
            if not self.camera_cap or not self.camera_cap.isOpened():
                self.log("⚠️ Camera not available for preview update")
                return
                
            # Capture frame
            ret, frame = self.camera_cap.read()
            if not ret or frame is None:
                self.log("⚠️ Failed to capture frame")
                return
                
            # Convert BGR to RGB
            rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            
            # Convert to QImage
            height, width, channel = rgb_frame.shape
            bytes_per_line = 3 * width
            q_image = QImage(rgb_frame.data, width, height, bytes_per_line, QImage.Format_RGB888)
            
            # Convert to QPixmap
            pixmap = QPixmap.fromImage(q_image)
            
            # Scale to fit label
            label_size = self.preview_label.size()
            scaled_pixmap = pixmap.scaled(label_size, Qt.KeepAspectRatio, Qt.SmoothTransformation)
            
            # Set on label
            self.preview_label.setPixmap(scaled_pixmap)
            
            # Force update
            self.preview_label.repaint()
            self.preview_label.update()
            
            # Log success (but not every frame to avoid spam)
            if hasattr(self, '_frame_count'):
                self._frame_count += 1
                if self._frame_count % 30 == 0:  # Every 30 frames (3 seconds at 10 FPS)
                    self.log(f"✅ Preview updated: Frame {self._frame_count}")
            else:
                self._frame_count = 1
                
        except Exception as e:
            self.log(f"❌ Error updating preview: {e}")

def main():
    """Run the preview button test."""
    app = QApplication(sys.argv)
    
    print("🧪 Testing Preview Button Behavior...")
    try:
        window = PreviewButtonTest()
        window.show()
        print("✅ Preview button test window created successfully")
        print("🎯 Click 'START PREVIEW' to simulate pressing the preview button")
        print("🔍 This will show exactly what happens in the main application")
        
        # Run the application
        sys.exit(app.exec_())
        
    except Exception as e:
        print(f"❌ Preview button test failed: {e}")
        import traceback
        print(f"Traceback: {traceback.format_exc()}")
        return 1

if __name__ == "__main__":
    main()
