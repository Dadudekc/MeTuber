import os
from PyQt5.QtWidgets import QSplashScreen, QVBoxLayout, QLabel, QProgressBar, QWidget
from PyQt5.QtCore import Qt, QTimer, pyqtSignal
from PyQt5.QtGui import QPixmap, QFont, QPainter, QColor

class SplashScreen(QSplashScreen):
    """Professional splash screen for Dreamscape Stream Software."""
    
    finished = pyqtSignal()
    
    def __init__(self):
        # Create a text-based logo for Dreamscape
        pixmap = QPixmap(400, 300)
        pixmap.fill(Qt.black)
        
        # Create a painter to draw the logo
        painter = QPainter(pixmap)
        painter.setRenderHint(QPainter.Antialiasing)
        
        # Set up the font
        font = QFont("Segoe UI", 36, QFont.Bold)
        painter.setFont(font)
        
        # Draw the main text
        painter.setPen(QColor("#0096ff"))  # Dreamscape blue
        painter.drawText(pixmap.rect(), Qt.AlignCenter, "Dreamscape")
        
        # Draw subtitle - positioned higher up
        subtitle_font = QFont("Segoe UI", 16)
        painter.setFont(subtitle_font)
        painter.setPen(QColor("#cccccc"))  # Light gray
        
        # Calculate position to move subtitle up
        main_text_rect = painter.fontMetrics().boundingRect("Dreamscape")
        subtitle_rect = painter.fontMetrics().boundingRect("Stream Software")
        
        # Position subtitle closer to main text, above the loading area
        subtitle_y = (pixmap.height() // 2) + (main_text_rect.height() // 2) + 20
        painter.drawText(pixmap.width() // 2, subtitle_y, "Stream Software")
        
        painter.end()
        
        super().__init__(pixmap, Qt.WindowStaysOnTopHint)
        
        self.setWindowTitle("Dreamscape Stream Software")
        
        # Add loading text and progress bar
        self.progress = 0
        self.setup_ui()
        
        # Timer for progress animation
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_progress)
        
    def setup_ui(self):
        """Setup the splash screen UI elements."""
        # Create a transparent overlay for text
        self.setStyleSheet("""
            QSplashScreen {
                background-color: rgba(0, 0, 0, 200);
                color: white;
            }
        """)
        
        # Show initial message
        self.showMessage("Starting Dreamscape Stream Software...", 
                        Qt.AlignBottom | Qt.AlignCenter, Qt.white)
    
    def start_loading(self, tasks):
        """Start the loading animation with a list of tasks."""
        self.tasks = tasks
        self.current_task = 0
        self.progress = 0
        self.timer.start(50)  # Update every 50ms for smooth animation
        
    def update_progress(self):
        """Update the loading progress."""
        self.progress += 2
        
        if self.current_task < len(self.tasks):
            task_name = self.tasks[self.current_task]
            message = f"Loading {task_name}... {self.progress}%"
            self.showMessage(message, Qt.AlignBottom | Qt.AlignCenter, Qt.white)
            
            # Move to next task every 25%
            if self.progress >= 25 * (self.current_task + 1):
                self.current_task += 1
                
        if self.progress >= 100:
            self.showMessage("Ready! Opening application...", 
                           Qt.AlignBottom | Qt.AlignCenter, Qt.white)
            self.timer.stop()
            QTimer.singleShot(500, self.close_splash)
            
    def close_splash(self):
        """Close the splash screen and emit finished signal."""
        self.close()
        self.finished.emit()
        
    def update_message(self, message):
        """Update the splash screen message manually."""
        self.showMessage(message, Qt.AlignBottom | Qt.AlignCenter, Qt.white)
        
    def show_error(self, error_message):
        """Show an error message on the splash screen."""
        self.showMessage(f"Error: {error_message}", 
                        Qt.AlignBottom | Qt.AlignCenter, Qt.red) 