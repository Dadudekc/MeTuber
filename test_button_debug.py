#!/usr/bin/env python3
"""
Simple test script to debug button functionality
"""

import sys
import os
from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QVBoxLayout, QWidget, QLabel
from PyQt5.QtCore import QTimer

# Add the project root to Python path
project_root = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, project_root)

class ButtonTestWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Button Debug Test")
        self.setGeometry(100, 100, 400, 300)
        
        # Create central widget
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        layout = QVBoxLayout(central_widget)
        
        # Create test label
        self.test_label = QLabel("Click buttons to test functionality")
        layout.addWidget(self.test_label)
        
        # Create test buttons
        self.start_button = QPushButton("Start Processing")
        self.start_button.clicked.connect(self.on_start_clicked)
        layout.addWidget(self.start_button)
        
        self.stop_button = QPushButton("Stop Processing")
        self.stop_button.clicked.connect(self.on_stop_clicked)
        layout.addWidget(self.stop_button)
        
        self.snapshot_button = QPushButton("Take Snapshot")
        self.snapshot_button.clicked.connect(self.on_snapshot_clicked)
        layout.addWidget(self.snapshot_button)
        
        # Test timer
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_test)
        self.timer.start(1000)  # Update every second
        
        self.counter = 0
        
    def on_start_clicked(self):
        self.test_label.setText("Start button clicked!")
        print("Start button clicked")
        
    def on_stop_clicked(self):
        self.test_label.setText("Stop button clicked!")
        print("Stop button clicked")
        
    def on_snapshot_clicked(self):
        self.test_label.setText("Snapshot button clicked!")
        print("Snapshot button clicked")
        
    def update_test(self):
        self.counter += 1
        if self.counter % 5 == 0:
            print(f"Test counter: {self.counter}")

def main():
    app = QApplication(sys.argv)
    window = ButtonTestWindow()
    window.show()
    return app.exec_()

if __name__ == "__main__":
    sys.exit(main()) 