#!/usr/bin/env python3
"""
Comprehensive Test for Preview Display Pipeline

This test will identify exactly where the display is failing by testing
each step of the pipeline individually.
"""

import sys
import os
import logging
import numpy as np
import cv2
from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel, QVBoxLayout, QWidget, QPushButton
from PyQt5.QtCore import Qt, QTimer
from PyQt5.QtGui import QPixmap, QImage

# Add the src directory to the path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

class PreviewDisplayTest(QMainWindow):
    """Test window to debug preview display issues."""
    
    def __init__(self):
        super().__init__()
        self.logger = logging.getLogger(__name__)
        self.setWindowTitle("Preview Display Test - Debug Window")
        self.setGeometry(100, 100, 800, 600)
        
        # Create central widget
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        layout = QVBoxLayout(central_widget)
        
        # Create test preview label
        self.preview_label = QLabel("🎥 Test Preview Area")
        self.preview_label.setAlignment(Qt.AlignCenter)
        self.preview_label.setMinimumSize(640, 480)
        self.preview_label.setStyleSheet("""
            QLabel {
                background-color: #1a1a1a;
                border: 2px solid #404040;
                border-radius: 8px;
                color: #808080;
                font-size: 16px;
            }
        """)
        layout.addWidget(self.preview_label)
        
        # Create test buttons
        self.test_frame_button = QPushButton("Generate Test Frame")
        self.test_frame_button.clicked.connect(self.test_frame_generation)
        layout.addWidget(self.test_frame_button)
        
        self.display_test_button = QPushButton("Display Test Frame")
        self.display_test_button.clicked.connect(self.test_frame_display)
        layout.addWidget(self.display_test_button)
        
        self.camera_test_button = QPushButton("Test Camera Access")
        self.camera_test_button.clicked.connect(self.test_camera_access)
        layout.addWidget(self.camera_test_button)
        
        self.pipeline_test_button = QPushButton("Test Full Pipeline")
        self.pipeline_test_button.clicked.connect(self.test_full_pipeline)
        layout.addWidget(self.pipeline_test_button)
        
        # Status label
        self.status_label = QLabel("Status: Ready")
        self.status_label.setStyleSheet("color: #00ff00; font-weight: bold;")
        layout.addWidget(self.status_label)
        
        self.logger.info("✅ Test window created successfully")
        
    def update_status(self, message, color="#00ff00"):
        """Update status display."""
        self.status_label.setText(f"Status: {message}")
        self.status_label.setStyleSheet(f"color: {color}; font-weight: bold;")
        self.logger.info(f"Status: {message}")
        
    def test_frame_generation(self):
        """Test 1: Frame generation."""
        try:
            self.update_status("Testing frame generation...", "#ffff00")
            self.logger.info("🧪 Test 1: Frame Generation")
            
            # Generate test frame
            height, width = 480, 640
            frame = np.zeros((height, width, 3), dtype=np.uint8)
            
            # Create a simple pattern
            for y in range(height):
                for x in range(width):
                    r = int(128 + 127 * (x / width))
                    g = int(128 + 127 * (y / height))
                    b = int(128 + 127 * ((x + y) / (width + height)))
                    frame[y, x] = [r, g, b]
            
            # Add some text
            cv2.putText(frame, "Test Frame", (width//2 - 100, height//2), 
                       cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)
            
            self.logger.info(f"✅ Test frame generated: {frame.shape}, dtype: {frame.dtype}")
            self.logger.info(f"🔍 Frame data range: {frame.min()} to {frame.max()}")
            self.logger.info(f"🔍 Frame size in memory: {frame.nbytes} bytes")
            
            # Store frame for later tests
            self.test_frame = frame
            self.update_status("Frame generation successful!", "#00ff00")
            
        except Exception as e:
            self.logger.error(f"❌ Frame generation failed: {e}")
            self.update_status("Frame generation failed!", "#ff0000")
            import traceback
            self.logger.error(f"Traceback: {traceback.format_exc()}")
    
    def test_frame_display(self):
        """Test 2: Frame display on QLabel."""
        try:
            if not hasattr(self, 'test_frame'):
                self.update_status("Generate test frame first!", "#ff0000")
                return
                
            self.update_status("Testing frame display...", "#ffff00")
            self.logger.info("🧪 Test 2: Frame Display")
            
            # Convert BGR to RGB
            self.logger.info("🔍 Converting BGR to RGB...")
            rgb_frame = cv2.cvtColor(self.test_frame, cv2.COLOR_BGR2RGB)
            self.logger.info(f"✅ RGB conversion successful: {rgb_frame.shape}")
            
            # Get frame dimensions
            height, width, channel = rgb_frame.shape
            bytes_per_line = 3 * width
            self.logger.info(f"🔍 Dimensions: {width}x{height}x{channel}")
            self.logger.info(f"🔍 Bytes per line: {bytes_per_line}")
            
            # Convert to QImage
            self.logger.info("🔍 Creating QImage...")
            q_image = QImage(rgb_frame.data, width, height, bytes_per_line, QImage.Format_RGB888)
            self.logger.info(f"✅ QImage created: {q_image.size()}, format: {q_image.format()}")
            self.logger.info(f"🔍 QImage is null: {q_image.isNull()}")
            self.logger.info(f"🔍 QImage depth: {q_image.depth()}")
            
            # Convert to QPixmap
            self.logger.info("🔍 Creating QPixmap...")
            pixmap = QPixmap.fromImage(q_image)
            self.logger.info(f"✅ QPixmap created: {pixmap.size()}")
            self.logger.info(f"🔍 QPixmap is null: {pixmap.isNull()}")
            
            # Check label properties
            self.logger.info(f"🔍 Label size: {self.preview_label.size()}")
            self.logger.info(f"🔍 Label is visible: {self.preview_label.isVisible()}")
            self.logger.info(f"🔍 Label geometry: {self.preview_label.geometry()}")
            
            # Scale pixmap to fit label
            label_size = self.preview_label.size()
            if label_size.width() > 0 and label_size.height() > 0:
                self.logger.info("🔍 Scaling pixmap to fit label...")
                scaled_pixmap = pixmap.scaled(
                    label_size, 
                    Qt.KeepAspectRatio, 
                    Qt.SmoothTransformation
                )
                self.logger.info(f"✅ Scaled pixmap: {scaled_pixmap.size()}")
                
                # Set pixmap on label
                self.logger.info("🔍 Setting pixmap on label...")
                self.preview_label.setPixmap(scaled_pixmap)
                self.logger.info("✅ Pixmap set on label")
                
                # Force update
                self.logger.info("🔍 Forcing label update...")
                self.preview_label.repaint()
                self.preview_label.update()
                self.logger.info("✅ Label update forced")
                
                # Verify pixmap was set
                current_pixmap = self.preview_label.pixmap()
                if current_pixmap:
                    self.logger.info(f"✅ Verification: pixmap is set, size: {current_pixmap.size()}")
                    self.update_status("Frame display successful!", "#00ff00")
                else:
                    self.logger.error("❌ Verification failed: pixmap not set on label")
                    self.update_status("Frame display verification failed!", "#ff0000")
            else:
                self.logger.error(f"❌ Label size is invalid: {label_size}")
                self.update_status("Invalid label size!", "#ff0000")
                
        except Exception as e:
            self.logger.error(f"❌ Frame display failed: {e}")
            self.update_status("Frame display failed!", "#ff0000")
            import traceback
            self.logger.error(f"Traceback: {traceback.format_exc()}")
    
    def test_camera_access(self):
        """Test 3: Camera access."""
        try:
            self.update_status("Testing camera access...", "#ffff00")
            self.logger.info("🧪 Test 3: Camera Access")
            
            # Try to open camera
            self.logger.info("🔍 Attempting to open camera...")
            cap = cv2.VideoCapture(0)
            
            if cap.isOpened():
                self.logger.info("✅ Camera opened successfully")
                
                # Try to read a frame
                ret, frame = cap.read()
                if ret and frame is not None:
                    self.logger.info(f"✅ Frame read successfully: {frame.shape}")
                    self.logger.info(f"🔍 Frame data range: {frame.min()} to {frame.max()}")
                    
                    # Store camera frame
                    self.camera_frame = frame
                    self.update_status("Camera access successful!", "#00ff00")
                else:
                    self.logger.warning("⚠️ Camera opened but frame read failed")
                    self.update_status("Camera frame read failed!", "#ff8000")
            else:
                self.logger.warning("⚠️ Camera could not be opened")
                self.update_status("Camera not accessible!", "#ff8000")
            
            # Clean up
            cap.release()
            self.logger.info("✅ Camera released")
            
        except Exception as e:
            self.logger.error(f"❌ Camera test failed: {e}")
            self.update_status("Camera test failed!", "#ff0000")
            import traceback
            self.logger.error(f"Traceback: {traceback.format_exc()}")
    
    def test_full_pipeline(self):
        """Test 4: Full display pipeline with camera frame."""
        try:
            if not hasattr(self, 'camera_frame'):
                self.update_status("Test camera access first!", "#ff0000")
                return
                
            self.update_status("Testing full pipeline...", "#ffff00")
            self.logger.info("🧪 Test 4: Full Display Pipeline")
            
            # Use camera frame
            frame = self.camera_frame
            self.logger.info(f"🔍 Using camera frame: {frame.shape}")
            
            # Convert BGR to RGB
            rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            
            # Convert to QImage
            height, width, channel = rgb_frame.shape
            bytes_per_line = 3 * width
            q_image = QImage(rgb_frame.data, width, height, bytes_per_line, QImage.Format_RGB888)
            
            # Convert to QPixmap
            pixmap = QPixmap.fromImage(q_image)
            
            # Scale and display
            label_size = self.preview_label.size()
            if label_size.width() > 0 and label_size.height() > 0:
                scaled_pixmap = pixmap.scaled(
                    label_size, 
                    Qt.KeepAspectRatio, 
                    Qt.SmoothTransformation
                )
                
                # Set on label
                self.preview_label.setPixmap(scaled_pixmap)
                self.preview_label.repaint()
                self.preview_label.update()
                
                self.logger.info("✅ Full pipeline test completed successfully")
                self.update_status("Full pipeline test successful!", "#00ff00")
            else:
                self.logger.error("❌ Invalid label size for full pipeline test")
                self.update_status("Full pipeline test failed!", "#ff0000")
                
        except Exception as e:
            self.logger.error(f"❌ Full pipeline test failed: {e}")
            self.update_status("Full pipeline test failed!", "#ff0000")
            import traceback
            self.logger.error(f"Traceback: {traceback.format_exc()}")

def main():
    """Main test function."""
    app = QApplication(sys.argv)
    
    # Create test window
    test_window = PreviewDisplayTest()
    test_window.show()
    
    # Run the application
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()
