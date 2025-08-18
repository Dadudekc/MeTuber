#!/usr/bin/env python3
"""
Visual Display Test

This test creates a simple window with a bright, obvious preview to verify
what's actually being displayed.
"""

import sys
import numpy as np
import cv2
from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel, QVBoxLayout, QWidget, QPushButton
from PyQt5.QtCore import Qt, QTimer
from PyQt5.QtGui import QPixmap, QImage

class VisualDisplayTest(QMainWindow):
    """Test window to verify visual display."""
    
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Visual Display Test - BRIGHT PREVIEW")
        self.setGeometry(100, 100, 800, 600)
        
        # Create central widget
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        layout = QVBoxLayout(central_widget)
        
        # Create test button
        self.test_btn = QPushButton("Generate BRIGHT Test Frame")
        self.test_btn.clicked.connect(self.generate_bright_frame)
        layout.addWidget(self.test_btn)
        
        # Create preview label with obvious styling
        self.preview_label = QLabel("PREVIEW AREA - SHOULD BE BRIGHT")
        self.preview_label.setMinimumSize(640, 480)
        self.preview_label.setStyleSheet("""
            QLabel {
                background: #ff0000;
                color: #ffffff;
                border: 5px solid #00ff00;
                border-radius: 10px;
                font-size: 20px;
                font-weight: bold;
                padding: 20px;
            }
        """)
        layout.addWidget(self.preview_label)
        
        # Create status label
        self.status_label = QLabel("Status: Ready")
        self.status_label.setStyleSheet("color: #0000ff; font-weight: bold; font-size: 16px;")
        layout.addWidget(self.status_label)
        
        # Timer for continuous updates
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_frame)
        self.timer.start(100)  # 10 FPS
        
        self.frame_count = 0
        
    def generate_bright_frame(self):
        """Generate a very bright, obvious test frame."""
        try:
            # Create a bright, colorful frame
            height, width = 480, 640
            frame = np.ones((height, width, 3), dtype=np.uint8) * 255  # Pure white
            
            # Add bright colored stripes
            stripe_height = height // 8
            colors = [
                [255, 0, 0],    # Bright Red
                [0, 255, 0],    # Bright Green
                [0, 0, 255],    # Bright Blue
                [255, 255, 0],  # Bright Yellow
                [255, 0, 255],  # Bright Magenta
                [0, 255, 255],  # Bright Cyan
                [255, 128, 0],  # Bright Orange
                [128, 0, 255],  # Bright Purple
            ]
            
            for i, color in enumerate(colors):
                y_start = i * stripe_height
                y_end = (i + 1) * stripe_height
                frame[y_start:y_end, :] = color
            
            # Add bright text
            cv2.putText(frame, "BRIGHT TEST FRAME", (50, 240), 
                       cv2.FONT_HERSHEY_SIMPLEX, 2, (255, 255, 255), 4)
            cv2.putText(frame, f"Frame: {self.frame_count}", (50, 300), 
                       cv2.FONT_HERSHEY_SIMPLEX, 1.5, (0, 0, 0), 3)
            
            # Display the frame
            self.display_frame(frame)
            self.status_label.setText(f"Generated bright frame {self.frame_count}")
            self.frame_count += 1
            
        except Exception as e:
            self.status_label.setText(f"Error: {e}")
            
    def update_frame(self):
        """Update frame continuously."""
        try:
            # Create a simple animated frame
            height, width = 480, 640
            frame = np.zeros((height, width, 3), dtype=np.uint8)
            
            # Create moving bright circle
            time_offset = self.frame_count * 0.1
            center_x = int(width // 2 + 200 * np.sin(time_offset))
            center_y = int(height // 2 + 150 * np.cos(time_offset * 0.7))
            
            # Draw bright circle
            cv2.circle(frame, (center_x, center_y), 80, (255, 255, 255), -1)
            
            # Add bright text
            cv2.putText(frame, "MOVING BRIGHT CIRCLE", (50, 240), 
                       cv2.FONT_HERSHEY_SIMPLEX, 1.5, (255, 255, 255), 3)
            cv2.putText(frame, f"Frame: {self.frame_count}", (50, 300), 
                       cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
            
            # Display the frame
            self.display_frame(frame)
            self.frame_count += 1
            
        except Exception as e:
            self.status_label.setText(f"Update error: {e}")
            
    def display_frame(self, frame):
        """Display the frame on the preview label."""
        try:
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
            
        except Exception as e:
            self.status_label.setText(f"Display error: {e}")

def main():
    """Run the visual display test."""
    app = QApplication(sys.argv)
    
    print("🧪 Testing Visual Display...")
    try:
        window = VisualDisplayTest()
        window.show()
        print("✅ Visual display test window created successfully")
        print("🔍 Look for a bright, colorful preview with moving elements")
        print("🔍 If you see it, the display system is working")
        print("🔍 If you don't see it, there's a visual/display issue")
        
        # Run the application
        sys.exit(app.exec_())
        
    except Exception as e:
        print(f"❌ Visual display test failed: {e}")
        import traceback
        print(f"Traceback: {traceback.format_exc()}")
        return 1

if __name__ == "__main__":
    main()
