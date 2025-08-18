#!/usr/bin/env python3
"""
Comprehensive Diagnostic Test for Preview System

This test will systematically check each component to identify where the issue is.
"""

import sys
import os
import logging
import numpy as np
import cv2
from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel, QVBoxLayout, QWidget, QPushButton, QTextEdit
from PyQt5.QtCore import Qt, QTimer
from PyQt5.QtGui import QPixmap, QImage

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

class DiagnosticTest(QMainWindow):
    """Test window to systematically diagnose preview issues."""
    
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Preview Diagnostic Test")
        self.setGeometry(100, 100, 800, 600)
        
        # Create central widget
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        layout = QVBoxLayout(central_widget)
        
        # Create test buttons
        self.test_frame_btn = QPushButton("Test 1: Generate Test Frame")
        self.test_frame_btn.clicked.connect(self.test_frame_generation)
        layout.addWidget(self.test_frame_btn)
        
        self.test_display_btn = QPushButton("Test 2: Test Display System")
        self.test_display_btn.clicked.connect(self.test_display_system)
        layout.addWidget(self.test_display_btn)
        
        self.test_camera_btn = QPushButton("Test 3: Test Camera Access")
        self.test_camera_btn.clicked.connect(self.test_camera_access)
        layout.addWidget(self.test_camera_btn)
        
        self.test_effects_btn = QPushButton("Test 4: Test Effects System")
        self.test_effects_btn.clicked.connect(self.test_effects_system)
        layout.addWidget(self.test_effects_btn)
        
        # Create preview label
        self.preview_label = QLabel("Preview Area")
        self.preview_label.setMinimumSize(640, 480)
        self.preview_label.setStyleSheet("""
            QLabel {
                background: #000000;
                color: #ffffff;
                border: 2px solid #ffffff;
                border-radius: 8px;
                font-size: 16px;
                padding: 20px;
            }
        """)
        layout.addWidget(self.preview_label)
        
        # Create log display
        self.log_display = QTextEdit()
        self.log_display.setMaximumHeight(150)
        layout.addWidget(self.log_display)
        
        self.log("🔧 Diagnostic test initialized")
        
    def log(self, message):
        """Add message to log display."""
        self.log_display.append(f"{message}")
        print(message)
        
    def test_frame_generation(self):
        """Test 1: Generate a test frame."""
        try:
            self.log("🧪 Test 1: Frame Generation")
            
            # Create test frame
            height, width = 480, 640
            frame = np.zeros((height, width, 3), dtype=np.uint8)
            
            # Add some content
            cv2.rectangle(frame, (100, 100), (540, 380), (0, 255, 0), 3)
            cv2.putText(frame, "Test Frame", (250, 240), 
                       cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)
            
            self.log(f"✅ Test frame created: {frame.shape}")
            
            # Store for other tests
            self.test_frame = frame
            
        except Exception as e:
            self.log(f"❌ Frame generation failed: {e}")
            
    def test_display_system(self):
        """Test 2: Test the display system."""
        try:
            self.log("🧪 Test 2: Display System")
            
            if not hasattr(self, 'test_frame'):
                self.log("❌ No test frame available. Run Test 1 first.")
                return
                
            # Convert BGR to RGB
            rgb_frame = cv2.cvtColor(self.test_frame, cv2.COLOR_BGR2RGB)
            self.log(f"✅ BGR to RGB conversion: {rgb_frame.shape}")
            
            # Convert to QImage
            height, width, channel = rgb_frame.shape
            bytes_per_line = 3 * width
            q_image = QImage(rgb_frame.data, width, height, bytes_per_line, QImage.Format_RGB888)
            self.log(f"✅ QImage created: {q_image.size()}")
            
            # Convert to QPixmap
            pixmap = QPixmap.fromImage(q_image)
            self.log(f"✅ QPixmap created: {pixmap.size()}")
            
            # Scale to fit label
            label_size = self.preview_label.size()
            scaled_pixmap = pixmap.scaled(label_size, Qt.KeepAspectRatio, Qt.SmoothTransformation)
            self.log(f"✅ Pixmap scaled: {scaled_pixmap.size()}")
            
            # Display on label
            self.preview_label.setPixmap(scaled_pixmap)
            self.log("✅ Pixmap set on label")
            
            # Force update
            self.preview_label.repaint()
            self.preview_label.update()
            self.log("✅ Display update forced")
            
        except Exception as e:
            self.log(f"❌ Display system test failed: {e}")
            import traceback
            self.log(f"Traceback: {traceback.format_exc()}")
            
    def test_camera_access(self):
        """Test 3: Test camera access."""
        try:
            self.log("🧪 Test 3: Camera Access")
            
            # Try to open camera
            cap = cv2.VideoCapture(0)
            if cap.isOpened():
                self.log("✅ Camera opened successfully")
                
                # Try to read a frame
                ret, frame = cap.read()
                if ret and frame is not None:
                    self.log(f"✅ Frame captured: {frame.shape}")
                    
                    # Display the frame
                    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                    height, width, channel = rgb_frame.shape
                    bytes_per_line = 3 * width
                    q_image = QImage(rgb_frame.data, width, height, bytes_per_line, QImage.Format_RGB888)
                    pixmap = QPixmap.fromImage(q_image)
                    
                    label_size = self.preview_label.size()
                    scaled_pixmap = pixmap.scaled(label_size, Qt.KeepAspectRatio, Qt.SmoothTransformation)
                    self.preview_label.setPixmap(scaled_pixmap)
                    self.preview_label.repaint()
                    self.preview_label.update()
                    
                    self.log("✅ Camera frame displayed")
                else:
                    self.log("❌ Failed to capture frame from camera")
                    
                cap.release()
                self.log("✅ Camera released")
            else:
                self.log("❌ Failed to open camera")
                
        except Exception as e:
            self.log(f"❌ Camera test failed: {e}")
            import traceback
            self.log(f"Traceback: {traceback.format_exc()}")
            
    def test_effects_system(self):
        """Test 4: Test effects system."""
        try:
            self.log("🧪 Test 4: Effects System")
            
            if not hasattr(self, 'test_frame'):
                self.log("❌ No test frame available. Run Test 1 first.")
                return
                
            # Test basic OpenCV effects
            self.log("Testing basic OpenCV effects...")
            
            # Blur effect
            blurred = cv2.GaussianBlur(self.test_frame, (15, 15), 0)
            self.log("✅ Gaussian blur applied")
            
            # Edge detection
            gray = cv2.cvtColor(self.test_frame, cv2.COLOR_BGR2GRAY)
            edges = cv2.Canny(gray, 100, 200)
            edges_colored = cv2.cvtColor(edges, cv2.COLOR_GRAY2BGR)
            self.log("✅ Edge detection applied")
            
            # Display edges
            rgb_frame = cv2.cvtColor(edges_colored, cv2.COLOR_BGR2RGB)
            height, width, channel = rgb_frame.shape
            bytes_per_line = 3 * width
            q_image = QImage(rgb_frame.data, width, height, bytes_per_line, QImage.Format_RGB888)
            pixmap = QPixmap.fromImage(q_image)
            
            label_size = self.preview_label.size()
            scaled_pixmap = pixmap.scaled(label_size, Qt.KeepAspectRatio, Qt.SmoothTransformation)
            self.preview_label.setPixmap(scaled_pixmap)
            self.preview_label.repaint()
            self.preview_label.update()
            
            self.log("✅ Effects test frame displayed")
            
        except Exception as e:
            self.log(f"❌ Effects test failed: {e}")
            import traceback
            self.log(f"Traceback: {traceback.format_exc()}")

def main():
    """Run the diagnostic test."""
    app = QApplication(sys.argv)
    
    # Test basic PyQt functionality
    print("🧪 Testing PyQt5 installation...")
    try:
        window = DiagnosticTest()
        window.show()
        print("✅ PyQt5 test window created successfully")
        
        # Run the application
        sys.exit(app.exec_())
        
    except Exception as e:
        print(f"❌ PyQt5 test failed: {e}")
        import traceback
        print(f"Traceback: {traceback.format_exc()}")
        return 1

if __name__ == "__main__":
    main()
