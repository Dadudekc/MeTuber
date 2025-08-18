#!/usr/bin/env python3
"""
Display Pipeline Test

This test verifies the display pipeline works correctly.
"""

import sys
import numpy as np
import cv2
from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel, QVBoxLayout, QWidget, QPushButton
from PyQt5.QtCore import Qt, QTimer
from PyQt5.QtGui import QPixmap, QImage

class DisplayPipelineTest(QMainWindow):
    """Test window to verify display pipeline."""
    
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Display Pipeline Test")
        self.setGeometry(100, 100, 800, 600)
        
        # Create central widget
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        layout = QVBoxLayout(central_widget)
        
        # Create test button
        self.test_btn = QPushButton("Test Display Pipeline")
        self.test_btn.clicked.connect(self.test_display_pipeline)
        layout.addWidget(self.test_btn)
        
        # Create preview label (same as main app)
        self.preview_label = QLabel("PREVIEW AREA - Click Test Button")
        self.preview_label.setMinimumSize(640, 480)
        self.preview_label.setStyleSheet("""
            QLabel {
                background: #000000;
                color: #ffffff;
                border: 3px solid #00ff00;
                border-radius: 10px;
                font-size: 18px;
                font-weight: bold;
                padding: 20px;
            }
        """)
        layout.addWidget(self.preview_label)
        
        # Create status label
        self.status_label = QLabel("Status: Ready")
        self.status_label.setStyleSheet("color: #0000ff; font-weight: bold; font-size: 16px;")
        layout.addWidget(self.status_label)
        
        self.log("🔧 Display Pipeline Test initialized")
        
    def log(self, message):
        """Add message to status."""
        self.status_label.setText(message)
        print(message)
        
    def test_display_pipeline(self):
        """Test the complete display pipeline."""
        try:
            self.log("🧪 Testing Display Pipeline...")
            
            # Step 1: Create test frame
            self.log("📸 Step 1: Creating test frame...")
            frame = self.create_test_frame()
            if frame is None:
                self.log("❌ Failed to create test frame")
                return
            self.log(f"✅ Test frame created: {frame.shape}")
            
            # Step 2: Convert BGR to RGB
            self.log("🔄 Step 2: Converting BGR to RGB...")
            rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            self.log(f"✅ RGB conversion: {rgb_frame.shape}")
            
            # Step 3: Convert to QImage
            self.log("🖼️ Step 3: Converting to QImage...")
            height, width, channel = rgb_frame.shape
            bytes_per_line = 3 * width
            q_image = QImage(rgb_frame.data, width, height, bytes_per_line, QImage.Format_RGB888)
            self.log(f"✅ QImage created: {q_image.size()}")
            
            # Step 4: Convert to QPixmap
            self.log("🎨 Step 4: Converting to QPixmap...")
            pixmap = QPixmap.fromImage(q_image)
            self.log(f"✅ QPixmap created: {pixmap.size()}")
            
            # Step 5: Scale to fit label
            self.log("📏 Step 5: Scaling to fit label...")
            label_size = self.preview_label.size()
            self.log(f"🔍 Label size: {label_size}")
            
            if label_size.width() > 0 and label_size.height() > 0:
                scaled_pixmap = pixmap.scaled(label_size, Qt.KeepAspectRatio, Qt.SmoothTransformation)
                self.log(f"✅ Scaled pixmap: {scaled_pixmap.size()}")
                
                # Step 6: Set on label
                self.log("🎯 Step 6: Setting pixmap on label...")
                self.preview_label.setPixmap(scaled_pixmap)
                self.log("✅ Pixmap set on label")
                
                # Step 7: Force update
                self.log("🔄 Step 7: Forcing update...")
                self.preview_label.repaint()
                self.preview_label.update()
                self.log("✅ Update forced")
                
                # Step 8: Verify
                current_pixmap = self.preview_label.pixmap()
                if current_pixmap:
                    self.log(f"✅ Verification: Pixmap is set! Size: {current_pixmap.size()}")
                    self.log("🎉 Display pipeline test PASSED!")
                else:
                    self.log("❌ Verification: Pixmap is not set!")
            else:
                self.log("❌ Label size is zero!")
                
        except Exception as e:
            self.log(f"❌ Display pipeline test failed: {e}")
            import traceback
            print(f"Traceback: {traceback.format_exc()}")
            
    def create_test_frame(self):
        """Create a test frame."""
        try:
            # Create a colorful test frame
            height, width = 480, 640
            frame = np.zeros((height, width, 3), dtype=np.uint8)
            
            # Add colorful stripes
            stripe_height = height // 6
            colors = [
                [255, 0, 0],    # Red
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
            cv2.putText(frame, "DISPLAY PIPELINE TEST", (50, 240), 
                       cv2.FONT_HERSHEY_SIMPLEX, 1.5, (255, 255, 255), 3)
            cv2.putText(frame, "If you see this, the pipeline works!", (50, 300), 
                       cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 0), 2)
            
            return frame
            
        except Exception as e:
            self.log(f"❌ Error creating test frame: {e}")
            return None

def main():
    """Run the display pipeline test."""
    app = QApplication(sys.argv)
    
    print("🧪 Testing Display Pipeline...")
    try:
        window = DisplayPipelineTest()
        window.show()
        print("✅ Display pipeline test window created successfully")
        print("🔍 Click 'Test Display Pipeline' to test the display system")
        
        # Run the application
        sys.exit(app.exec_())
        
    except Exception as e:
        print(f"❌ Display pipeline test failed: {e}")
        import traceback
        print(f"Traceback: {traceback.format_exc()}")
        return 1

if __name__ == "__main__":
    main()
