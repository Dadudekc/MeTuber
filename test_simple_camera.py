#!/usr/bin/env python3
"""
Simple Camera Test

This test isolates the camera issue step by step.
"""

import cv2
import time
import numpy as np
from PyQt5.QtWidgets import QApplication, QLabel, QVBoxLayout, QWidget, QMainWindow
from PyQt5.QtCore import QTimer
from PyQt5.QtGui import QPixmap, QImage
from PyQt5.Qt import Qt

class SimpleCameraTest(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Simple Camera Test")
        self.setGeometry(100, 100, 800, 600)
        
        # Create central widget
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        layout = QVBoxLayout(central_widget)
        
        # Create preview label
        self.preview_label = QLabel("Camera Preview - Starting...")
        self.preview_label.setMinimumSize(640, 480)
        self.preview_label.setStyleSheet("""
            QLabel {
                background: #000000;
                color: #ffffff;
                border: 3px solid #ffffff;
                font-size: 16px;
                padding: 20px;
            }
        """)
        layout.addWidget(self.preview_label)
        
        # Initialize camera
        self.camera = None
        self.timer = None
        
        # Start camera after a short delay
        QTimer.singleShot(1000, self.start_camera)
        
    def start_camera(self):
        """Start camera step by step."""
        try:
            print("🔧 Step 1: Opening camera...")
            self.preview_label.setText("Step 1: Opening camera...")
            
            # Open camera
            self.camera = cv2.VideoCapture(0)
            
            if not self.camera.isOpened():
                print("❌ Failed to open camera")
                self.preview_label.setText("❌ Failed to open camera")
                return
                
            print("✅ Camera opened successfully")
            self.preview_label.setText("Step 2: Testing frame capture...")
            
            # Test frame capture
            ret, frame = self.camera.read()
            if not ret or frame is None:
                print("❌ Failed to capture frame")
                self.preview_label.setText("❌ Failed to capture frame")
                return
                
            print(f"✅ Frame captured: {frame.shape}")
            self.preview_label.setText("Step 3: Starting preview timer...")
            
            # Start timer for continuous updates
            self.timer = QTimer()
            self.timer.timeout.connect(self.update_frame)
            self.timer.start(100)  # 10 FPS
            
            print("✅ Preview timer started")
            self.preview_label.setText("✅ Camera preview active!")
            
        except Exception as e:
            print(f"❌ Error starting camera: {e}")
            self.preview_label.setText(f"❌ Error: {e}")
            import traceback
            print(f"Traceback: {traceback.format_exc()}")
            
    def update_frame(self):
        """Update frame display."""
        try:
            if not self.camera or not self.camera.isOpened():
                return
                
            # Capture frame
            ret, frame = self.camera.read()
            if not ret or frame is None:
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
            
        except Exception as e:
            print(f"❌ Error updating frame: {e}")
            
    def closeEvent(self, event):
        """Clean up when window closes."""
        if self.camera:
            self.camera.release()
        if self.timer:
            self.timer.stop()
        event.accept()

def main():
    """Run the simple camera test."""
    app = QApplication([])
    
    print("🧪 Simple Camera Test Starting...")
    print("🔍 This will test camera access step by step")
    
    try:
        window = SimpleCameraTest()
        window.show()
        print("✅ Test window created")
        print("⏳ Camera will start automatically in 1 second...")
        
        app.exec_()
        
    except Exception as e:
        print(f"❌ Test failed: {e}")
        import traceback
        print(f"Traceback: {traceback.format_exc()}")

if __name__ == "__main__":
    main()
