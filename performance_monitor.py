#!/usr/bin/env python3
"""
Performance Monitor Overlay for Dreamscape V2
Shows real-time performance metrics for the optimized preview pipeline
"""

import time
import psutil
import threading
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QLabel, QPushButton
from PyQt5.QtCore import QTimer, Qt
from PyQt5.QtGui import QFont, QPalette, QColor

class PerformanceMonitor(QWidget):
    """Real-time performance monitoring overlay."""
    
    def __init__(self):
        super().__init__()
        self.setWindowTitle("🚀 Performance Monitor - Dreamscape V2")
        self.setWindowFlags(Qt.WindowStaysOnTopHint | Qt.FramelessWindowHint)
        self.setAttribute(Qt.WA_TranslucentBackground)
        
        # Setup UI
        self.setup_ui()
        
        # Performance tracking
        self.fps_history = []
        self.cpu_history = []
        self.memory_history = []
        self.frame_times = []
        
        # Start monitoring
        self.start_monitoring()
    
    def setup_ui(self):
        """Setup the monitoring UI."""
        layout = QVBoxLayout()
        
        # Title
        title = QLabel("🚀 Performance Monitor")
        title.setFont(QFont("Arial", 12, QFont.Bold))
        title.setStyleSheet("color: #00ff00; background: rgba(0,0,0,0.8); padding: 5px; border-radius: 5px;")
        layout.addWidget(title)
        
        # FPS Display
        self.fps_label = QLabel("FPS: --")
        self.fps_label.setFont(QFont("Consolas", 10))
        self.fps_label.setStyleSheet("color: #00ff00; background: rgba(0,0,0,0.7); padding: 3px;")
        layout.addWidget(self.fps_label)
        
        # CPU Display
        self.cpu_label = QLabel("CPU: --")
        self.cpu_label.setFont(QFont("Consolas", 10))
        self.cpu_label.setStyleSheet("color: #ffff00; background: rgba(0,0,0,0.7); padding: 3px;")
        layout.addWidget(self.cpu_label)
        
        # Memory Display
        self.memory_label = QLabel("Memory: --")
        self.memory_label.setFont(QFont("Consolas", 10))
        self.memory_label.setStyleSheet("color: #00ffff; background: rgba(0,0,0,0.7); padding: 3px;")
        layout.addWidget(self.memory_label)
        
        # Frame Time Display
        self.frame_time_label = QLabel("Frame Time: --")
        self.frame_time_label.setFont(QFont("Consolas", 10))
        self.frame_time_label.setStyleSheet("color: #ff00ff; background: rgba(0,0,0,0.7); padding: 3px;")
        layout.addWidget(self.frame_time_label)
        
        # Performance Mode Display
        self.mode_label = QLabel("Mode: Quality")
        self.mode_label.setFont(QFont("Consolas", 10))
        self.mode_label.setStyleSheet("color: #ffffff; background: rgba(0,0,0,0.7); padding: 3px;")
        layout.addWidget(self.mode_label)
        
        # Close button
        close_btn = QPushButton("❌ Close")
        close_btn.clicked.connect(self.close)
        close_btn.setStyleSheet("""
            QPushButton {
                background: #ff0000;
                color: white;
                border: none;
                padding: 5px;
                border-radius: 3px;
            }
            QPushButton:hover {
                background: #cc0000;
            }
        """)
        layout.addWidget(close_btn)
        
        self.setLayout(layout)
        
        # Make draggable
        self.old_pos = None
        self.setMouseTracking(True)
    
    def mousePressEvent(self, event):
        """Handle mouse press for dragging."""
        if event.button() == Qt.LeftButton:
            self.old_pos = event.globalPos()
    
    def mouseMoveEvent(self, event):
        """Handle mouse move for dragging."""
        if self.old_pos:
            delta = event.globalPos() - self.old_pos
            self.move(self.pos() + delta)
            self.old_pos = event.globalPos()
    
    def mouseReleaseEvent(self, event):
        """Handle mouse release."""
        self.old_pos = None
    
    def start_monitoring(self):
        """Start the performance monitoring timer."""
        self.monitor_timer = QTimer()
        self.monitor_timer.timeout.connect(self.update_metrics)
        self.monitor_timer.start(100)  # Update every 100ms
    
    def update_metrics(self):
        """Update performance metrics."""
        try:
            # CPU Usage
            cpu_percent = psutil.cpu_percent(interval=0.0)
            self.cpu_label.setText(f"CPU: {cpu_percent:.1f}%")
            
            # Memory Usage
            memory = psutil.virtual_memory()
            memory_mb = memory.used // (1024 * 1024)
            self.memory_label.setText(f"Memory: {memory_mb} MB")
            
            # Performance mode detection (simplified)
            if cpu_percent > 80:
                self.mode_label.setText("Mode: Performance")
                self.mode_label.setStyleSheet("color: #ff8800; background: rgba(0,0,0,0.7); padding: 3px;")
            elif cpu_percent > 50:
                self.mode_label.setText("Mode: Balanced")
                self.mode_label.setStyleSheet("color: #ffff00; background: rgba(0,0,0,0.7); padding: 3px;")
            else:
                self.mode_label.setText("Mode: Quality")
                self.mode_label.setStyleSheet("color: #00ff00; background: rgba(0,0,0,0.7); padding: 3px;")
            
            # Store history for trends
            self.cpu_history.append(cpu_percent)
            self.memory_history.append(memory_mb)
            
            # Keep only last 100 samples
            if len(self.cpu_history) > 100:
                self.cpu_history.pop(0)
                self.memory_history.pop(0)
            
        except Exception as e:
            print(f"Error updating metrics: {e}")
    
    def update_fps(self, fps):
        """Update FPS display."""
        self.fps_label.setText(f"FPS: {fps:.1f}")
        
        # Color code FPS
        if fps >= 25:
            color = "#00ff00"  # Green
        elif fps >= 15:
            color = "#ffff00"  # Yellow
        else:
            color = "#ff0000"  # Red
        
        self.fps_label.setStyleSheet(f"color: {color}; background: rgba(0,0,0,0.7); padding: 3px;")
        
        # Store FPS history
        self.fps_history.append(fps)
        if len(self.fps_history) > 100:
            self.fps_history.pop(0)
    
    def update_frame_time(self, frame_time_ms):
        """Update frame time display."""
        self.frame_time_label.setText(f"Frame Time: {frame_time_ms:.1f}ms")
        
        # Color code frame time
        if frame_time_ms <= 33:
            color = "#00ff00"  # Green (30+ FPS)
        elif frame_time_ms <= 66:
            color = "#ffff00"  # Yellow (15+ FPS)
        else:
            color = "#ff0000"  # Red (<15 FPS)
        
        self.frame_time_label.setStyleSheet(f"color: {color}; background: rgba(0,0,0,0.7); padding: 3px;")
        
        # Store frame time history
        self.frame_times.append(frame_time_ms)
        if len(self.frame_times) > 100:
            self.frame_times.pop(0)
    
    def get_performance_summary(self):
        """Get a summary of performance metrics."""
        if not self.fps_history:
            return "No performance data available"
        
        avg_fps = sum(self.fps_history) / len(self.fps_history)
        avg_cpu = sum(self.cpu_history) / len(self.cpu_history) if self.cpu_history else 0
        avg_memory = sum(self.memory_history) / len(self.memory_history) if self.memory_history else 0
        
        return f"""
Performance Summary:
- Average FPS: {avg_fps:.1f}
- Average CPU: {avg_cpu:.1f}%
- Average Memory: {avg_memory:.0f} MB
- Current Mode: {self.mode_label.text()}
        """

def main():
    """Main function to run the performance monitor."""
    app = QApplication([])
    
    monitor = PerformanceMonitor()
    monitor.show()
    
    print("🚀 Performance Monitor Started!")
    print("Drag the overlay to position it on your screen")
    print("Monitor will show real-time performance metrics")
    
    app.exec_()

if __name__ == "__main__":
    main()
